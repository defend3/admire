from __future__ import annotations

import asyncio
from datetime import datetime, timedelta
from typing import Optional, Union

import discord
from loguru import logger as log
from melaniebot.core import bank, commands

from .abc import RoleToolsMixin


def _(x):
    return x


class RoleToolsEvents(RoleToolsMixin):
    """This class contains all the event listeners as well as the core logic for
    handling adding/removing roles with our settings.
    """

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent) -> None:
        await self._ready.wait()
        guild = self.bot.get_guild(payload.guild_id)
        if not guild:
            return
        if await self.bot.cog_disabled_in_guild(self, guild):
            return
        if guild.id not in self.settings:
            return
        if getattr(payload.emoji, "id", None):
            key = f"{payload.channel_id}-{payload.message_id}-{payload.emoji.id}"
        else:
            emoji = str(payload.emoji).strip("\N{VARIATION SELECTOR-16}")
            key = f"{payload.channel_id}-{payload.message_id}-{emoji}"
        guild_settings = self.settings[guild.id]["reaction_roles"]
        if key in guild_settings:
            # add roles

            role = guild.get_role(guild_settings[key])
            if not await self.config.role(role).selfassignable():
                return
            member = guild.get_member(payload.user_id)
            if not role or not member:
                return
            if member.bot:
                return
            if await self.check_guild_verification(member, guild):
                log.debug("Ignoring user due to verification check.")
                return
            if getattr(member, "pending", False):
                return
            log.debug(f"Adding role to {member.name} in {member.guild}")
            await self.give_roles(member, [role], "Reaction Role")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent) -> None:
        await self._ready.wait()
        guild = self.bot.get_guild(payload.guild_id)
        if not guild:
            return
        if await self.bot.cog_disabled_in_guild(self, guild):
            return
        if guild.id not in self.settings:
            return
        if getattr(payload.emoji, "id", None):
            key = f"{payload.channel_id}-{payload.message_id}-{payload.emoji.id}"
        else:
            emoji = str(payload.emoji).strip("\N{VARIATION SELECTOR-16}")
            key = f"{payload.channel_id}-{payload.message_id}-{emoji}"
        guild_settings = self.settings[guild.id]["reaction_roles"]
        if key in guild_settings:
            # add roles
            role = guild.get_role(guild_settings[key])
            if not await self.config.role(role).selfremovable():
                return

            member = guild.get_member(payload.user_id)
            if not role or not member:
                return
            if member.bot:
                return
            log.debug(f"Removing role from {member.name} in {member.guild}")
            await self.remove_roles(member, [role], "Reaction Role")

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member) -> None:
        await self._ready.wait()
        if await self.bot.cog_disabled_in_guild(self, member.guild):
            return
        await self._sticky_leave(member)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        await self._ready.wait()
        if await self.bot.cog_disabled_in_guild(self, member.guild):
            return
        await self._sticky_join(member)
        if getattr(member, "pending", False):
            return
        await self._auto_give(member)

    async def check_guild_verification(self, member: discord.Member, guild: discord.Guild) -> Union[bool, int]:
        if member.roles:
            return False
        allowed_discord = datetime.utcnow() - member.created_at
        # since discords check for verification level 2 is actually discord age not join age
        allowed_server = (datetime.utcnow() - member.joined_at) if member.joined_at else timedelta(minutes=10)
        if guild.verification_level.value >= 2 and allowed_discord <= timedelta(minutes=5):
            log.debug(f"Waiting 5 minutes for {member.name} in {guild}")
            return 300 - int(allowed_discord.total_seconds())
        elif guild.verification_level.value >= 3 and allowed_server <= timedelta(minutes=10):
            log.debug(f"Waiting 10 minutes for {member.name} in {guild}")
            return 600 - int(allowed_server.total_seconds())
        return False

    async def wait_for_verification(self, member: discord.Member, guild: discord.Guild) -> None:
        wait = await self.check_guild_verification(member, guild)
        if wait:
            log.debug(f"Waiting {wait} seconds before allowing the user to have a role")
            await asyncio.sleep(int(wait))

    async def check_atomicity(self, guild: discord.Guild) -> bool:
        """Determine the type of atomicity to use when applying/removing roles.

        This takes into account the global cog setting for atomic role assignment.
        Essentially letting me still have my fewer API calls while allowing
        regular users to use the old method.

        Server settings will override the global setting and prefer using atomic
        role assignment in general. This is only used for things like
        reaction roles, and other automatic methods. Commands like
        `;giverole` will pass the atomic bool kwarg specifically to avoid
        rate limiting the bot when assinging a massive number of roles to users.
        That in turn is not atomic potentially causing issues but should proceed a lot
        faster than if the atomic setting was `False`.

        Parameters
        ----------
            guild: discord.Guild
                The guild which the role atomicity is required

        Returns
        -------
            bool
                Whether or not to atomically assign roles.
                `True` will assign each role independant of the state
                of the bots cache.
                `False` will assign the roles as a group.

        """
        global_atomic = await self.config.atomic()
        server_atomic = await self.config.guild(guild).atomic()
        return global_atomic if server_atomic is None else server_atomic

    async def give_roles(
        self,
        member: discord.Member,
        roles: list[discord.Role],
        reason: Optional[str] = None,
        *,
        check_required: bool = True,
        check_exclusive: bool = True,
        check_inclusive: bool = True,
        check_cost: bool = True,
        atomic: Optional[bool] = None,
    ) -> None:
        """Handles all the logic for applying roles to a user.

        Parameters
        ----------
            member: discord.Member
                The member who should receive roles
            roles: list[discord.Role]
                The potentially new roles the user should receive.
            reason: Optional[str]
                The optional reason for adding the roles.

        Keyword Arguments
        -----------------
            check_required: bool
                Whether we actually want to check required roles when giving the roles.
                Defaults to True.
            check_exclusive: bool
                Wheter we actually want to check exclusivity when giving the roles.
                Defaults to True.
            check_inclusive: bool
                Wheter we actually want to check inclusivity when giving the roles.
                Defaults to True.
            check_cost: bool
                Wheter we actually want to check the cost for the role when giving the roles.
                Defaults to True.
            atomic: bool
                Whether to apply each role individually to prevent race conditions
                when assigning bulk roles together at once.
                Default for guilds is False to reduce API calls and the giverole/removerole commands
                will force use of this to reduce API calls on potentially
                large numbers of members getting roles

        """
        if not member.guild.get_member(member.id):
            return
        guild = member.guild
        if not guild.me.guild_permissions.manage_roles:
            return
        if atomic is None:
            atomic = await self.check_atomicity(guild)
        to_add = set() if atomic else set(member.roles)
        log.debug("Atomic role assignment %s", atomic)

        for role in roles:
            if role is None or role >= guild.me.top_role:
                continue
            if role in to_add and not atomic:
                continue
            if (required := await self.config.role(role).required()) and check_required:
                has_required = True
                for role_id in required:
                    r = guild.get_role(role_id)
                    if r is None:
                        async with self.config.role(role).required() as required_roles:
                            required_roles.remove(role_id)
                        continue
                    if r not in member.roles:
                        has_required = False
                if not has_required:
                    continue
            if (cost := await self.config.role(role).cost()) and check_cost:
                if await bank.can_spend(member, cost):
                    try:
                        await bank.withdraw_credits(member, cost)
                    except Exception:
                        log.info(f"Could not assign {role} to {member} as they don't have enough credits.")
                        continue
                else:
                    log.info(f"Could not assign {role} to {member} as they don't have enough credits.")
                    continue
            if (inclusive := await self.config.role(role).inclusive_with()) and check_inclusive:
                inclusive_roles = []
                for role_id in inclusive:
                    log.debug(role_id)
                    r = guild.get_role(role_id)
                    if r is None:
                        async with self.config.role(role).inclusive_with() as inclusive_with:
                            inclusive_with.remove(role_id)
                        continue
                    if r and await self.config.role(r).selfassignable():
                        to_add.add(r)
                        inclusive_roles.append(r)
                if atomic:
                    await member.add_roles(*inclusive_roles, reason="Inclusive Roles")
            if (exclusive := await self.config.role(role).exclusive_to()) and check_exclusive:
                skip_role_assign = False
                exclusive_roles = []
                for role_id in exclusive:
                    r = guild.get_role(role_id)
                    if r is None:
                        # cleanup roles that are missing automatically
                        # we should never :tm: end up in a situation where
                        # roles are not chunked properly
                        async with self.config.role(role).exclusive_to() as exclusive_to:
                            exclusive_to.remove(role_id)
                            continue
                    if r in member.roles:
                        if await self.config.role(r).selfremovable():
                            if atomic:
                                exclusive_roles.append(r)
                            else:
                                to_add.remove(r)
                        else:
                            # we want to only remove the role (and assign the new one)
                            # if the current role is self-removable
                            # If the role is not self-removable we don't want
                            # to apply the initial role to begin with
                            skip_role_assign = True
                if skip_role_assign:
                    # we want to skip assigning the role which means the continue
                    # needs to be here
                    # I don't think we should be removing roles at all if this
                    # is the case but if required this can be adjusted in the future
                    continue
                if atomic:
                    await member.remove_roles(*exclusive_roles, reason="Exclusive Roles")
            to_add.add(role)
        if atomic:
            await member.add_roles(*list(to_add), reason=reason)
        else:
            await member.edit(roles=list(to_add), reason=reason)

    async def remove_roles(
        self,
        member: discord.Member,
        roles: list[discord.Role],
        reason: Optional[str] = None,
        *,
        check_inclusive: bool = True,
        atomic: Optional[bool] = None,
    ) -> None:
        """Handles all the logic for removing roles from a user.

        Parameters
        ----------
            member: discord.Member
                The member who should receive roles
            roles: list[discord.Role]
                The potentially new roles the user should receive.
            reason: Optional[str]
                The optional reason for adding the roles.

        Keyword Arguments
        -----------------
            check_inclusive: bool
                Wheter we actually want to check inclusivity when giving the roles.
                Defaults to True.
            atomic: bool
                Whether to apply each role individually to prevent race conditions
                when assigning bulk roles together at once.
                Default for guilds is False to reduce API calls and the giverole/removerole commands
                will force use of this to reduce API calls on potentially
                large numbers of members getting roles

        """
        if not member.guild.get_member(member.id):
            return
        guild = member.guild
        if not guild.me.guild_permissions.manage_roles:
            return
        if atomic is None:
            atomic = await self.check_atomicity(guild)
        to_rem = set() if atomic else set(member.roles)
        for role in roles:
            if role is None or role.position >= guild.me.top_role.position:
                continue
            if role not in to_rem and not atomic:
                continue
            if (inclusive := await self.config.role(role).inclusive_with()) and check_inclusive:
                for role_id in inclusive:
                    r = guild.get_role(role_id)
                    if not r:
                        continue
                    if await self.config.role(r).selfremovable():
                        if atomic:
                            to_rem.add(r)
                        else:
                            to_rem.remove(r)
            if atomic:
                to_rem.add(role)
            else:
                to_rem.remove(role)
        log.debug(f"{to_rem}")
        if atomic:
            await member.remove_roles(*list(to_rem), reason=reason)
        else:
            await member.edit(roles=list(to_rem), reason=reason)

    async def _auto_give(self, member: discord.Member) -> None:
        guild = member.guild
        if guild.id not in self.settings:
            return
        await self.wait_for_verification(member, guild)
        roles_ids = self.settings[guild.id]["auto_roles"]
        roles = [guild.get_role(role) for role in roles_ids]
        await self.give_roles(member, roles, "Automatic Roles")

    async def _sticky_leave(self, member: discord.Member) -> None:
        guild = member.guild
        if await self.bot.cog_disabled_in_guild(self, guild):
            return
        async with self.config.member(member).sticky_roles() as sticky_roles:
            for role in member.roles:
                if not await self.config.role(role).sticky():
                    continue
                if role.id not in sticky_roles:
                    sticky_roles.append(role.id)

    async def _sticky_join(self, member: discord.Member) -> None:
        guild = member.guild
        if await self.bot.cog_disabled_in_guild(self, guild):
            return
        if not guild.me.guild_permissions.manage_roles:
            return
        to_reapply = await self.config.member(member).sticky_roles()
        if not to_reapply:
            return
        await self.config.member(member).sticky_roles.clear()

        to_add = []

        for role_id in to_reapply:
            role = guild.get_role(role_id)
            if role and role < guild.me.top_role:
                to_add.append(role)

        if to_add:
            # use this to prevent issues with inclusive/exclusive roles
            # That may have previously been assigned manually
            await member.add_roles(*to_add, reason="Sticky Roles")

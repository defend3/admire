from __future__ import annotations

import contextlib
from typing import Optional, Union

import discord
from loguru import logger as log
from melaniebot.core import commands
from melaniebot.core.commands import Context
from melaniebot.core.utils.chat_formatting import humanize_list, pagify
from melaniebot.core.utils.menus import start_adding_reactions
from melaniebot.core.utils.predicates import ReactionPredicate

from .abc import RoleToolsMixin, roletools
from .converter import RoleEmojiConverter, RoleHierarchyConverter
from .menus import BaseMenu, ReactRolePages


def _(x):
    return x


class RoleToolsReactions(RoleToolsMixin):
    """This class contains commands related to reaction roles."""

    @roletools.command()
    @commands.admin_or_permissions(manage_roles=True)
    async def cleanup(self, ctx: Context) -> None:
        """Cleanup old/missing reaction roles and settings.

        Note: This will also clear out reaction roles if the bot is just
        missing permissions to see the reactions.

        """
        guild = ctx.guild
        async with ctx.typing(), self.config.guild(ctx.guild).reaction_roles() as cur_settings:
            to_remove = []
            for key, role_id in cur_settings.items():
                chan_id, message_id, emoji = key.split("-")
                channel = guild.get_channel(int(chan_id))
                if not channel:
                    to_remove.append((key, role_id))
                    continue
                my_perms = channel.permissions_for(guild.me)
                if not my_perms.read_messages and not my_perms.read_message_history:
                    to_remove.append((key, role_id))
                    continue
                try:
                    await channel.fetch_message(int(message_id))
                except Exception:
                    to_remove.append((key, role_id))
                    continue
                role = guild.get_role(int(role_id))
                if not role:
                    to_remove.append((key, role_id))
            for key, role_id in to_remove:
                del cur_settings[key]
                with contextlib.suppress(KeyError):
                    del self.settings[guild.id]["reaction_roles"][key]

                async with self.config.role_from_id(role_id).reactions() as reactions:
                    reactions.remove(key)
        await ctx.send("I am finished deleting old settings.")

    @roletools.command(hidden=True)
    @commands.is_owner()
    @commands.cooldown(1, 86400, commands.BucketType.default)
    async def ownercleanup(self, ctx: Context) -> None:
        """Cleanup old/missing reaction roles and settings on the bot.

        Note: This will also clear out reaction roles if the bot is just
        missing permissions to see the reactions.

        """
        async with ctx.typing():
            for guild_id in self.settings:
                guild = self.bot.get_guild(guild_id)
                if not guild:
                    continue
                async with self.config.guild(ctx.guild).reaction_roles() as cur_settings:
                    to_remove = []
                    for key, role_id in cur_settings.items():
                        chan_id, message_id, emoji = key.split("-")
                        channel = guild.get_channel(int(chan_id))
                        if not channel:
                            to_remove.append((key, role_id))
                            continue
                        my_perms = channel.permissions_for(guild.me)
                        if not my_perms.read_messages and not my_perms.read_message_history:
                            to_remove.append((key, role_id))
                            continue
                        try:
                            message = await channel.fetch_message(int(message_id))
                        except Exception:
                            to_remove.append((key, role_id))
                            continue
                        if not message:
                            to_remove.append((key, role_id))
                            continue
                        role = guild.get_role(int(role_id))
                        if not role:
                            to_remove.append((key, role_id))
                    for key, role_id in to_remove:
                        del cur_settings[key]
                        with contextlib.suppress(KeyError):
                            del self.settings[guild.id]["reaction_roles"][key]

                        async with self.config.role_from_id(role_id).reactions() as reactions:
                            reactions.remove(key)
        await ctx.send("I am finished deleting old settings.")

    @roletools.command(aliases=["reactionroles", "reactrole"])
    @commands.admin_or_permissions(manage_roles=True)
    async def reactroles(self, ctx: Context) -> None:
        """View current bound roles in the server."""
        if ctx.guild.id not in self.settings:
            await ctx.send("There are no bound roles in this server.")
            return
        async with ctx.typing():
            msg = f"Reaction Roles in {ctx.guild.name}\n"
            for key, role_id in self.settings[ctx.guild.id]["reaction_roles"].items():
                channel_id, msg_id, emoji = key.split("-")
                if emoji.isdigit():
                    emoji = self.bot.get_emoji(int(emoji))
                if not emoji:
                    emoji = "Emoji from another server"
                role = ctx.guild.get_role(role_id)
                if channel := ctx.guild.get_channel(int(channel_id)):
                    # This can be potentially a very expensive operation
                    # so instead we fake the message link unless the channel is missing
                    # this way they can check themselves without rate limitng
                    # the bot trying to fetch something constantly that is broken.
                    message = f"https://discord.com/channels/{ctx.guild.id}/{channel_id}/{msg_id}"
                else:
                    message = None
                msg += f"{emoji} - {role.mention if role else ('None')} [Reaction Message]({message or ('None')})\n"

            pages = list(pagify(msg))
        await BaseMenu(source=ReactRolePages(pages=pages), delete_message_after=False, clear_reactions_after=True, timeout=60, cog=self, page_start=0).start(
            ctx=ctx,
        )

    @roletools.command(aliases=["clearreacts"])
    @commands.admin_or_permissions(manage_roles=True)
    async def clearreact(self, ctx: Context, message: discord.Message, *emojis: Optional[Union[discord.Emoji, str]]) -> None:
        """Clear the reactions for reaction roles. This will remove all reactions
        and then re-apply the bots reaction for you.

        `<message>` The message you want to clear reactions on.
        `[emojis...]` Optional emojis you want to specifically remove.
        If no emojis are provided this will clear all the reaction role
        emojis the bot has for the message provided.

        Note: This will only clear reactions which have a corresponding
        reaction role on it.

        """
        if not message.channel.permissions_for(ctx.me).manage_messages:
            await ctx.send("I require manage messages in order to clear other people's reactions.")
            return
        if emojis:
            for emoji in emojis:
                final_key = str(getattr(emoji, "id", emoji)).strip("\N{VARIATION SELECTOR-16}")
                key = f"{message.channel.id}-{message.id}-{final_key}"
                if key in self.settings[ctx.guild.id]["reaction_roles"]:
                    __, __, emoji = key.split("-")
                    if emoji.isdigit():
                        emoji = self.bot.get_emoji(int(emoji))
                    with contextlib.suppress(discord.Forbidden):
                        await message.clear_reaction(emoji)

                    await message.add_reaction(emoji)
        else:
            try:
                await message.clear_reactions()
            except discord.HTTPException:
                await ctx.send("There was an error clearing reactions on that message.")
                return
            for key in self.settings[ctx.guild.id]["reaction_roles"]:
                if f"{message.channel.id}-{message.id}" in key:
                    __, __, emoji = key.split("-")
                    if emoji.isdigit():
                        emoji = self.bot.get_emoji(int(emoji))
                    if emoji is None:
                        continue
                    with contextlib.suppress(discord.HTTPException):
                        await message.add_reaction(emoji)

        await ctx.send("Finished clearing reactions on that message.")

    @roletools.command(aliases=["reacts"])
    @commands.admin_or_permissions(manage_roles=True)
    async def react(self, ctx: Context, message: discord.Message, emoji: Union[discord.Emoji, str], *, role: RoleHierarchyConverter) -> None:
        """Create a reaction role.

        `<message>` can be the channel_id-message_id pair from copying
        message ID while holding SHIFT or a message link `<emoji>` The
        emoji you want people to react with to get the role. `<role>`
        The role you want people to receive for reacting.

        """
        if not message.guild or message.guild.id != ctx.guild.id:
            await ctx.send("You cannot add a Reaction Role to a message not in this guild.")
            return
        async with self.config.guild(ctx.guild).reaction_roles() as cur_setting:
            use_emoji = str(emoji.id) if isinstance(emoji, discord.Emoji) else str(emoji).strip("️")
            key = f"{message.channel.id}-{message.id}-{use_emoji}"
            send_to_react = False
            try:
                await message.add_reaction(str(emoji).strip("\N{VARIATION SELECTOR-16}"))
            except discord.HTTPException:
                send_to_react = True
            if ctx.guild.id not in self.settings:
                self.settings[ctx.guild.id] = await self.config.guild(ctx.guild).all()
            self.settings[ctx.guild.id]["reaction_roles"][key] = role.id
            cur_setting[key] = role.id
        async with self.config.role(role).reactions() as reactions:
            reactions.append(key)
        await ctx.send(f"Created the reaction role {role.name} to {emoji} on {message.jump_url}")
        if send_to_react:
            await ctx.send("I couldn't add the emoji to the message. Please make sure to add the emoji to the message for this to work.")
        if not await self.config.role(role).selfassignable():
            msg_str = f"{role.name} is not self assignable. Would you liked to make it self assignable and self removeable?"
            msg = await ctx.send(msg_str)
            start_adding_reactions(msg, ReactionPredicate.YES_OR_NO_EMOJIS)
            pred = ReactionPredicate.yes_or_no(msg, ctx.author)
            try:
                await ctx.bot.wait_for("reaction_add", check=pred, timeout=60)
            except TimeoutError:
                await ctx.send(f"Okay I won't automatically make {role.name} self assignable.")
                return
            if pred.result:
                await self.config.role(role).selfassignable.set(True)
                await self.config.role(role).selfremovable.set(True)
                await ctx.send(f"{role.name} has been made self assignable and self removeable.")

    @roletools.command(aliases=["remreacts"])
    @commands.admin_or_permissions(manage_roles=True)
    async def remreact(self, ctx: Context, message: discord.Message, *, role_or_emoji: Union[RoleHierarchyConverter, discord.Emoji, str]) -> None:
        """Remove a reaction role.

        `<message>` can be the channel_id-message_id pair
        from copying message ID while holding SHIFT or a message link
        `<emoji>` The emoji you want people to react with to get the role.
        `<role>` The role you want people to receive for reacting.

        Note: This will not remove the emoji reactions on the message.

        """
        if not message.guild or message.guild.id != ctx.guild.id:
            await ctx.send("You cannot remove a Reaction Role from a message not in this guild.")
            return
        if ctx.guild.id not in self.settings:
            await ctx.send("There are no roletools settings on this server.")
            return
        if not self.settings[ctx.guild.id]["reaction_roles"]:
            await ctx.send("There are no reaction roles setup for this guild.")
            return
        found = False
        if isinstance(role_or_emoji, discord.Role):
            for keys, role_ids in self.settings[ctx.guild.id]["reaction_roles"].items():
                if role_or_emoji.id == role_ids and f"{message.channel.id}-{message.id}" in keys:
                    key = keys
                    found = True
                    role_id = role_ids
        else:
            final_key = str(getattr(role_or_emoji, "id", role_or_emoji)).strip("\N{VARIATION SELECTOR-16}")
            key = f"{message.channel.id}-{message.id}-{final_key}"
            if key in self.settings[ctx.guild.id]["reaction_roles"]:
                found = True
                role_id = self.settings[ctx.guild.id]["reaction_roles"][key]
        if found:
            channel, message_id, emoji = key.split("-")
            if emoji.isdigit():
                emoji = self.bot.get_emoji(int(emoji))
            async with self.config.guild(ctx.guild).reaction_roles() as cur_setting:
                role = ctx.guild.get_role(cur_setting[key])
                with contextlib.suppress(KeyError):
                    del self.settings[ctx.guild.id]["reaction_roles"][key]

                del cur_setting[key]
                async with self.config.role_from_id(role_id).reactions() as reactions:
                    reactions.remove(key)
            with contextlib.suppress(Exception):
                await message.clear_reaction(emoji)

            await ctx.send(f"Removed role reaction on {role} to {emoji} on {message.jump_url}")
        else:
            await ctx.send("I could not find a reaction role on that message or for that role/emoji combination.")

    @roletools.command(aliases=["bulksreacts"])
    @commands.admin_or_permissions(manage_roles=True)
    async def bulkreact(self, ctx: Context, message: discord.Message, *role_emoji: RoleEmojiConverter) -> None:
        """Create multiple roles reactions for a single message.

        `<message>` can be the channel_id-message_id pair
        from copying message ID while holding SHIFT or a message link
        `[role_emoji...]` Must be a role-emoji pair separated by either `;`, `,`, `|`, or `-`.

        Note: Any spaces will be considered a new set of role-emoji pairs, if you
        want to specify a role with a space in it without pinging it enclose
        the full role-emoji pair in quotes.

        e.g. `;roletools bulkreact 461417772115558410-821105109097644052 @member-:smile:`
        `;roletools bulkreact 461417772115558410-821105109097644052 "Super Member-:frown:"`

        """
        if not message.guild or message.guild.id != ctx.guild.id:
            return await ctx.send("You cannot add a Reaction Role to a message not in this guild.")
        added = []
        not_added = []
        send_to_react = False
        async with self.config.guild(ctx.guild).reaction_roles() as cur_setting:
            for role, emoji in role_emoji:
                log.debug(type(emoji))
                use_emoji = str(emoji.id) if isinstance(emoji, discord.PartialEmoji) else str(emoji).strip("️")
                key = f"{message.channel.id}-{message.id}-{use_emoji}"
                if key not in cur_setting:
                    try:
                        await message.add_reaction(str(emoji).strip().strip("\N{VARIATION SELECTOR-16}"))
                    except discord.HTTPException:
                        send_to_react = True
                        log.exception("could not add reaction to message")
                    if ctx.guild.id not in self.settings:
                        self.settings[ctx.guild.id] = await self.config.guild(ctx.guild).all()
                    self.settings[ctx.guild.id]["reaction_roles"][key] = role.id
                    cur_setting[key] = role.id
                    added.append((key, role))
                    async with self.config.role(role).reactions() as reactions:
                        reactions.append(key)

                else:
                    not_added.append((key, role))
        ask_to_modify = False
        if added:
            msg = "__The following Reaction Roles were created__\n"

            if any(m is False for m in [await self.config.role(r).selfassignable() for x, r in added]):
                ask_to_modify = True
            for item, role in added:
                channel, message_id, emoji = item.split("-")
                if emoji.isdigit():
                    emoji = self.bot.get_emoji(int(emoji))
                msg += f"{role.name} - {emoji} on {message.jump_url}\n"
            for page in pagify(msg):
                await ctx.send(page)
            if send_to_react:
                await ctx.send("I couldn't add an emoji to the message. Please make sure to add the missing emojis to the message for this to work.")
        if not_added:
            msg = "__The following Reaction Roles could not be created__\n"
            for item, role in not_added:
                channel, message_id, emoji = item.split("-")
                if emoji.isdigit():
                    emoji = self.bot.get_emoji(int(emoji))
                msg += f"{role.name} - {emoji} on {message.jump_url}\n"
            await ctx.send(msg)

        if ask_to_modify:
            msg_str = "Some roles are not self assignable. Would you liked to make them self assignable and self removeable?"
            msg = await ctx.send(msg_str)
            start_adding_reactions(msg, ReactionPredicate.YES_OR_NO_EMOJIS)
            pred = ReactionPredicate.yes_or_no(msg, ctx.author)
            try:
                await ctx.bot.wait_for("reaction_add", check=pred, timeout=60)
            except TimeoutError:
                await ctx.send(f"Okay I won't automatically make {role.name} self assignable.")
                return
            if pred.result:
                for key, role in added:
                    await self.config.role(role).selfassignable.set(True)
                    await self.config.role(role).selfremovable.set(True)
                await ctx.send(f"{humanize_list([r for x, r in added])} have been made self assignable and self removeable.")

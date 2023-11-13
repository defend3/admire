from __future__ import annotations

import argparse

import discord
import regex as re
from dateutil import parser
from discord.ext.commands.converter import MemberConverter, RoleConverter
from loguru import logger as log
from melaniebot.core.commands import BadArgument, Context, Converter
from melaniebot.core.commands.converter import TimedeltaConverter

from .api import UnavailableMember


def _(x):
    return x


# credit to mikeshardmind (Sinbad) for parse_time
# https://github.com/mikeshardmind/SinbadCogs/blob/v3/scheduler/time_utils.py
def parse_time(datetimestring: str):
    return parser.parse(datetimestring, ignoretz=True)


# credit to mikeshardmind (Sinbad) once again for all the argument parsing stuff
# this was mostly inspired from his rolemanagement cog
# https://github.com/mikeshardmind/SinbadCogs/blob/v3/rolemanagement/converters.py
class NoExitParser(argparse.ArgumentParser):
    def error(self, message):
        raise BadArgument(message)


class AdvancedMemberSelect:
    """Select a lot of members at once with multiple UNIX-like arguments.

    Actions
    -------
    --take-action --take-actions
    --send-dm
    --send-modlog
    --confirm
    --reason <text>
    --time --length <duration>

    Member search
    -------------
    --select [member, ...]
    --hackban-select [member, ...]
    --exclude [member, ...]
    --everyone
    --name <regex>
    --nickname <regex>
    --display-name <regex>
    --status --activity <regex>
    --only-humans
    --only-bots
    --joined-before <time>
    --joined-after <time>
    --last-njoins <int>
    --first-njoins <int>

    Permission search
    -----------------
    --has-perm <permissions>
    --has-any-perm [permission, ...]
    --has-all-perms [permission, ...]
    --has-none-perms [permission, ...]
    --has-perm-int <int>

    Role search
    -----------
    --has-role <role>
    --has-any-role [role, ...]
    --has-all-roles [role, ...]
    --has-none-roles [role, ...]
    --has-no-roles
    --has-exactly-nroles <int>
    --has-more-than-nroles <int>
    --has-less-than-nroles <int>
    --above <role>
    --below <role>

    """

    def parse_arguments(self, arguments: str):
        parser = NoExitParser(description="Mass member selection in a server.", add_help=False)

        parser.add_argument("--take-action", "--take-actions", dest="take_action", action="store_true")
        parser.add_argument("--send-dm", dest="send_dm", action="store_true")
        parser.add_argument("--send-modlog", dest="send_modlog", action="store_true")
        parser.add_argument("--confirm", dest="confirm", action="store_true")
        parser.add_argument("--reason", dest="reason", nargs="*")
        parser.add_argument("--length", "--time", dest="time", nargs="*")

        parser.add_argument("--everyone", dest="everyone", action="store_true")
        parser.add_argument("--select", dest="select", nargs="+")
        parser.add_argument("--hackban-select", dest="hackban_select", nargs="+")
        parser.add_argument("--exclude", dest="exclude", nargs="+")
        parser.add_argument("--name", dest="name")
        parser.add_argument("--nickname", dest="nickname")
        parser.add_argument("--display-name", dest="display_name")
        parser.add_argument("--status", "--activity", dest="activity")
        parser.add_argument("--only-humans", dest="only_humans", action="store_true")
        parser.add_argument("--only-bots", dest="only_bots", action="store_true")
        parser.add_argument("--joined-before", dest="joined_before", nargs="*")
        parser.add_argument("--joined-after", dest="joined_after", nargs="*")
        parser.add_argument("--last-njoins", dest="last_njoins", type=int)
        parser.add_argument("--first-njoins", dest="first_njoins", type=int)

        parser.add_argument("--has-perm", dest="has_perm")
        parser.add_argument("--has-any-perm", dest="has_any_perm", nargs="+")
        parser.add_argument("--has-all-perms", dest="has_all_perms", nargs="+")
        parser.add_argument("--has-none-perms", dest="has_none_perms", nargs="+")
        parser.add_argument("--has-perm-int", dest="has_perm_int", type=int)

        parser.add_argument("--has-role", dest="has_role")
        parser.add_argument("--has-any-role", dest="has_any_role", nargs="+")
        parser.add_argument("--has-all-roles", dest="has_all_roles", nargs="+")
        parser.add_argument("--has-none-roles", dest="has_none_roles", nargs="+")
        parser.add_argument("--has-no-roles", dest="has_no_roles", action="store_true")
        parser.add_argument("--has-exactly-nroles", dest="has_exactly_nroles", nargs=1, type=int)
        parser.add_argument("--has-more-than-nroles", dest="has_more_than_nroles", nargs=1, type=int)
        parser.add_argument("--has-less-than-nroles", dest="has_less_than_nroles", nargs=1, type=int)
        parser.add_argument("--above", dest="above")
        parser.add_argument("--below", dest="below")

        return parser.parse_args(arguments)

    async def process_arguments(self, args: argparse.Namespace):
        guild = self.ctx.guild
        members = []
        unavailable_members = []

        if not args.take_action and not args.send_dm and not args.send_modlog:
            msg = "I'm not doing anything! Please provide at least one of these arguments: `--take-action`, `--send-dm`, `--send-modlog`."
            raise BadArgument(msg)
        if args.only_bots and args.only_humans:
            msg = "Can't combine `--only-humans` with `--only-bots`."
            raise BadArgument(msg)

        if args.everyone:
            return (guild.members, [])
        members = guild.members
        if args.name:
            members = self._name_regex(members, args.name, "name")
        if args.nickname:
            members = self._name_regex(members, args.nickname, "nickname")
        if args.display_name:
            members = self._name_regex(members, args.display_name, "display_name")
        if args.activity:
            members = self._status_regex(members, args.activity)
        if args.only_humans:
            members = [x for x in members if not x.bot]
        if args.only_bots:
            members = [x for x in members if x.bot]
        if args.joined_before:
            members = self._join(members, " ".join(args.joined_before), "before")
        if args.joined_after:
            members = self._join(members, " ".join(args.joined_after), "after")
        if args.last_njoins:
            members = self._last_njoins(members, args.last_njoins)
        if args.first_njoins:
            members = self._first_njoins(members, args.first_njoins)

        if args.has_perm:
            members = self._perms(members, [args.has_perm], "perm")
        if args.has_any_perm:
            members = self._perms(members, args.has_any_perm, "any-perm")
        if args.has_all_perms:
            members = self._perms(members, args.has_all_perms, "all-perms")
        if args.has_none_perms:
            members = self._perms(members, args.has_none_perms, "none-perms")
        if args.has_perm_int:
            members = self._perm_int(members, args.has_perm_int)

        if args.has_role:
            members = await self._role(members, [args.has_role], "has-role")
        if args.has_any_role:
            members = await self._role(members, args.has_any_role, "has-any-role")
        if args.has_all_roles:
            members = await self._role(members, args.has_all_roles, "has-all-roles")
        if args.has_none_roles:
            members = await self._role(members, args.has_none_roles, "has-none-roles")
        if args.has_no_roles:
            members = await self._role(members, None, "has-no-roles")
        if args.has_exactly_nroles:
            members = self._nroles(members, args.has_exactly_nroles[0], "exactly")
        if args.has_more_than_nroles:
            members = self._nroles(members, args.has_more_than_nroles[0], "more")
        if args.has_less_than_nroles:
            members = self._nroles(members, args.has_less_than_nroles[0], "less")
        if args.above:
            members = await self._role(members, [args.above], "above")
        if args.below:
            members = await self._role(members, [args.below], "below")

        if args.exclude:
            members = await self._selection(members, args.exclude, "exclude")
        if args.select:
            if members == guild.members:
                members = []
            members = await self._selection(members, args.select, "select")
        if args.hackban_select:
            if members == guild.members:
                members = []
            unavailable_members = await self._unavailable_selection(args.hackban_select)

        if members or unavailable_members:
            return (members, unavailable_members)
        else:
            raise BadArgument("The search could't find any member.")

    def _name_regex(self, members: list, pattern: str, attribute: str):
        pattern = re.compile(pattern)

        def member_filter(member: discord.Member):
            return bool(pattern.search(getattr(member, attribute)))

        return list(filter(member_filter, members))

    def _status_regex(self, members: list, pattern: str):
        pattern = re.compile(pattern)

        def member_filter(member: discord.Member):
            # credit to mikeshardmind for this part of code
            # https://github.com/mikeshardmind/SinbadCogs/blob/4d265a9819fd25be44bc7422e6e60c44624624da/statuswarn/statuswarn.py#L27
            maybe_custom = next((a for a in member.activities if a.type == 4), None)
            return bool(pattern.search(maybe_custom.state or "")) if maybe_custom else False

        return list(filter(member_filter, members))

    def _join(self, members: list, date: str, when: str):
        try:
            date = parse_time(date)
        except Exception:
            msg = f"Can't convert `{date}` from `--joined-{when}` into a valid date object. Here are some examples of the date format you must follow:\n- `February 14 at 6pm`\n- `28 May 2018`\n- `jan 4 16:09`"
            raise BadArgument(msg)

        def member_filter(member: discord.Member):
            if when == "before" and member.joined_at < date:
                return True
            return bool(when == "after" and member.joined_at > date)

        return list(filter(member_filter, members))

    def _last_njoins(self, members: list, number: int):
        try:
            last_member = sorted(members, key=lambda x: x.joined_at, reverse=True)[number]
        except IndexError:
            last_member = sorted(members, key=lambda x: x.joined_at, reverse=True)[len(members) - 1]

        def member_filter(member: discord.Member):
            return member.joined_at > last_member.joined_at

        return list(filter(member_filter, members))

    def _first_njoins(self, members: list, number: int):
        try:
            last_member = sorted(members, key=lambda x: x.joined_at)[number]
        except IndexError:
            last_member = sorted(members, key=lambda x: x.joined_at)[len(members) - 1]

        def member_filter(member: discord.Member):
            return member.joined_at < last_member.joined_at

        return list(filter(member_filter, members))

    def _perms(self, members: list, permissions: list, requires: str):
        allowed_permissions = dir(discord.Permissions)
        for permission in permissions:
            if permission not in allowed_permissions:
                msg = (
                    f"Can't convert `{permission}` from `--has-{requires}` into a valid permission object. Please provide something like this: `send_messages`"
                )
                raise BadArgument(msg)

        def member_filter(member: discord.Member) -> bool:
            if requires == "all-perms":
                if set(permissions).issubset([x[0] for x in member.guild_permissions if x[1]]):
                    return True
            elif requires == "any-perm":
                if {x[0] for x in member.guild_permissions if x[1]}.intersection(permissions):
                    return True
            elif requires == "none-perms":
                if not {x[0] for x in member.guild_permissions if x[1]}.intersection(permissions):
                    return True
            elif requires == "perm" and getattr(member.guild_permissions, permissions[0]):
                return True
            return False

        return list(filter(member_filter, members))

    def _perm_int(self, members: list, permissions: int):
        def member_filter(member: discord.Member):
            return member.guild_permissions.value == permissions

        return list(filter(member_filter, members))

    async def _role(self, members: list, _roles: list, requires: str):
        if _roles:
            roles = []
            for role in _roles:
                try:
                    roles.append(await RoleConverter().convert(self.ctx, role))
                except (discord.errors.NotFound, discord.ext.commands.errors.BadArgument):
                    msg = f"Can't convert `{role}` from `--{requires}` into a valid role object. Please provide the exact role name (in quotes if it has spaces) or an ID."
                    raise BadArgument(msg)

        def member_filter(member: discord.Member) -> bool:
            if requires == "has-role" and roles[0] in member.roles:
                return True
            elif requires == "has-any-roles" and set(member.roles).intersection(roles):
                return True
            elif requires == "has-all-roles" and set(roles).issubset(member.roles):
                return True
            elif requires == "has-none-roles" and not set(member.roles).intersection(roles):
                return True
            elif requires == "has-no-roles" and len(member.roles) == 1:
                return True
            elif requires == "above" and member.top_role.position > roles[0].position:
                return True
            elif requires == "below" and member.top_role.position < roles[0].position:
                return True
            return False

        return list(filter(member_filter, members))

    def _nroles(self, members: list, number: int, condition: str):
        number += 1  # do not count @everyone role

        def member_filter(member: discord.Member) -> bool:
            if condition == "exactly" and len(member.roles) == number:
                return True
            elif condition == "more" and len(member.roles) > number:
                return True
            elif condition == "less" and len(member.roles) < number:
                return True
            return False

        return list(filter(member_filter, members))

    async def _selection(self, members: list, _selection: list, requires: str):
        selection = []
        for member in _selection:
            try:
                selection.append(await MemberConverter().convert(self.ctx, member))
            except discord.errors.NotFound as e:
                msg = f"Can't convert `{member}` from `--{requires}` into a valid member object. Please provide the exact member's name (in quotes if it has spaces), mention him, or provide its ID."
                raise BadArgument(msg) from e

        if requires != "select":
            return list(set(members) - set(selection))

        members.extend(selection)
        return members

    async def _unavailable_selection(self, _selection):
        # don't question my function names
        selection = []
        for member in _selection:
            try:
                selection.append(await UnavailableMember.convert(self.ctx, member))
            except BadArgument as e:
                msg = f"Can't convert `{member}` from `--hackban-select` into a valid user object. __You can only provide a user ID.__"
                raise BadArgument(msg) from e

        return selection

    async def convert(self, ctx, arguments):
        self.ctx = ctx
        async with ctx.typing():
            args = self.parse_arguments(arguments)
            self.reason = " ".join(args.reason or "")
            if args.time:
                try:
                    self.time = await TimedeltaConverter().convert(ctx, " ".join(args.time))
                except BadArgument as e:
                    msg = f"Can't convert `{' '.join(args.time)}` from `--time`/`--length` into a valid time object.\nExamples of the format: `20m`, `2h30m`, `7d`, `1d6h30m45s`"
                    raise BadArgument(msg) from e
            else:
                self.time = None
            self.take_action = args.take_action
            self.send_dm = args.send_dm
            self.send_modlog = args.send_modlog
            self.confirm = args.confirm
            (self.members, self.unavailable_members) = await self.process_arguments(args)
            return self


class ValidRegex(Converter):
    """This will check to see if the provided regex pattern is valid.

    Guidance code on how to do this from:

     This function (and a lot of code related to regex) is made by
    TrustyJAID
    https://github.com/TrustyJAID/Trusty-cogs/blob/master/retrigger/converters.py#L240

    """

    async def convert(self, ctx: Context, argument: str) -> str:
        try:
            result = re.compile(argument)
        except Exception as e:
            log.exception("Retrigger conversion error")
            err_msg = f"`{argument}` is not a valid regex pattern. {e}"
            raise BadArgument(err_msg) from e
        return result

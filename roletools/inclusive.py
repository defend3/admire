from __future__ import annotations

from melaniebot.core import commands
from melaniebot.core.commands import Context
from melaniebot.core.utils.chat_formatting import humanize_list

from .abc import RoleToolsMixin, roletools
from .converter import RoleHierarchyConverter


def _(x):
    return x


class RoleToolsInclusive(RoleToolsMixin):
    """This class handles setting inclusive roles."""

    @roletools.group(name="include", aliases=["inclusive"])
    async def inclusive(self, ctx: Context) -> None:
        """Set role inclusion."""

    @inclusive.command(name="add")
    @commands.admin_or_permissions(manage_roles=True)
    async def inclusive_add(self, ctx: Context, role: RoleHierarchyConverter, *include: RoleHierarchyConverter) -> None:
        """Add role inclusion (This will add roles if the designated role is
        acquired if the designated role is removed the included roles will also
        be removed if the included roles are set to selfremovable).

        `<role>` This is the role a user may acquire you want to set exclusions for.
        `<include>` The role(s) you wish to have added when a user gains the `<role>`

        Note: This will only work for reaction roles and automatic roles from this cog.

        """
        cur_setting = await self.config.role(role).inclusive_with()
        exclusive = await self.config.role(role).exclusive_to()
        for included_role in include:
            if included_role.id in exclusive:
                await ctx.send("You cannot include a role that is already considered exclusive.")
                return
            if included_role.id not in cur_setting:
                cur_setting.append(included_role.id)
        await self.config.role(role).inclusive_with.set(cur_setting)
        roles = [ctx.guild.get_role(i) for i in cur_setting]
        role_names = humanize_list([i.mention for i in roles if i])
        await ctx.send(f"The {role.mention} role will now add the following roles if it is acquired through roletools.\n{role_names}.")

    @inclusive.command(name="mutual")
    @commands.admin_or_permissions(manage_roles=True)
    async def mutual_inclusive_add(self, ctx: Context, *roles: RoleHierarchyConverter) -> None:
        """Allow setting roles mutually inclusive to eachother.

        This is equivalent to individually setting each roles inclusive
        roles to another set of roles.

        `[role...]` The roles you want to set as mutually inclusive.

        """
        if len(roles) <= 1:
            await ctx.send_help()
            return
        for role in roles:
            exclusive = await self.config.role(role).exclusive_to()
            async with self.config.role(role).inclusive_with() as inclusive_roles:
                for add_role in roles:
                    if add_role.id == role.id:
                        continue
                    if add_role.id in exclusive:
                        await ctx.send("You cannot exclude a role that is already considered exclusive.")
                        return
                    if add_role.id not in inclusive_roles:
                        inclusive_roles.append(add_role.id)
        await ctx.send(f"The following roles are now mutually inclusive to eachother:\n{humanize_list([r.mention for r in roles])}")

    @inclusive.command(name="remove")
    @commands.admin_or_permissions(manage_roles=True)
    async def inclusive_remove(self, ctx: Context, role: RoleHierarchyConverter, *include: RoleHierarchyConverter) -> None:
        """Remove role inclusion.

        `<role>` This is the role a user may acquire you want to set
        exclusions for. `<include>` The role(s) currently inclusive you
        no longer wish to have included

        """
        cur_setting = await self.config.role(role).inclusive_with()
        for included_role in include:
            if included_role.id in cur_setting:
                cur_setting.remove(included_role.id)
        await self.config.role(role).inclusive_with.set(cur_setting)
        if roles := [ctx.guild.get_role(i) for i in cur_setting]:
            role_names = humanize_list([i.mention for i in roles if i])
            await ctx.send(f"The {role.mention} role will now add the following roles if it is acquired through roletools.\n{role_names}.")
        else:
            await ctx.send(f"The {role.mention} role will no longer have included roles.")

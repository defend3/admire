from __future__ import annotations

from customhelp.abc import ThemesMeta  # type: ignore
from customhelp.core.base_help import (
    EMPTY_STRING,
    Category,
    Context,
    EmbedField,
    HelpSettings,
    cast,
    commands,
    get_aliases,
    get_cooldowns,
    get_perms,
    pagify,
)
from melanie import make_e


class DankHelp(ThemesMeta):
    """Inspired from Dankmemer's help menu."""

    async def format_bot_help(self, ctx: Context, help_settings: HelpSettings, get_pages: bool = False):
        embed = make_e(
            "Melanie has over 500 commands!\n\nTo view all commands, visit https://melaniebot.net/commands",
            tip="get detailed command help with ;help <command>",
            status="info",
        )

        return await ctx.send(embed=embed)

    async def format_category_help(self, ctx: Context, obj: Category, help_settings: HelpSettings, get_pages: bool = False, **kwargs):
        coms = await self.get_category_help_mapping(ctx, obj, help_settings=help_settings, **kwargs)
        if not coms:
            return

        if await ctx.embed_requested():
            emb = await self.embed_template(help_settings, ctx)
            emb["embed"]["title"] = (str(obj.reaction) if obj.reaction else "") + " " + obj.name.capitalize()
            if description := obj.long_desc:
                emb["embed"]["description"] = f"{description[:250]}"

            all_cog_text = [", ".join(f"`{name}`" for name, command in sorted(data.items())) for cog_name, data in coms]

            all_cog_text = ", ".join(all_cog_text)
            for page in pagify(all_cog_text, page_length=1000, delims=[","], shorten_by=0):
                field = EmbedField(EMPTY_STRING, page[1:] if page.startswith(",") else page, False)
                emb["fields"].append(field)

            pages = await self.make_embeds(ctx, emb, help_settings=help_settings)
            if get_pages:
                return pages
            else:
                await self.send_pages(ctx, pages, embed=True, help_settings=help_settings)
        else:
            await ctx.send("You need to enable embeds to use the help menu")

    async def format_command_help(self, ctx: Context, obj: commands.Command, help_settings: HelpSettings) -> None:
        send = help_settings.verify_exists
        if not send:
            async for __ in self.help_filter_func(ctx, (obj,), bypass_hidden=True, help_settings=help_settings):
                send = True

        if not send:
            return

        command = obj
        signature = f"`{ctx.clean_prefix}{command.qualified_name} {command.signature}`"
        subcommands = None

        if hasattr(command, "all_commands"):
            grp = cast(commands.Group, command)
            subcommands = await self.get_group_help_mapping(ctx, grp, help_settings=help_settings)

        if await ctx.embed_requested():
            emb = await self.embed_template(help_settings, ctx)
            if description := command.description:
                emb["embed"]["title"] = f"{description[:250]}"

            command_help = command.format_help_for_context(ctx)
            if command_help:
                splitted = command_help.split("\n\n")
                name = splitted[0]
                value = "\n\n".join(splitted[1:])
                emb["fields"].append(EmbedField("Description:", name[:250], False))
            else:
                value = ""
            emb["fields"].append(EmbedField("Usage:", signature, False))

            if aliases := get_aliases(command, ctx.invoked_with):
                emb["fields"].append(EmbedField("Aliases", ", ".join(aliases), False))

            if final_perms := get_perms(command):
                emb["fields"].append(EmbedField("Permissions", final_perms, False))

            if cooldowns := get_cooldowns(command):
                emb["fields"].append(EmbedField("Cooldowns:", "\n".join(cooldowns), False))

            if value:
                emb["fields"].append(EmbedField("Full description:", value[:1024], False))

            if subcommands:

                def shorten_line(a_line: str) -> str:
                    return a_line if len(a_line) < 70 else f"{a_line[:67]}.."

                subtext = "\n" + "\n".join(
                    shorten_line(f"`{name:<15}:`{command.format_shortdoc_for_context(ctx)}") for name, command in sorted(subcommands.items())
                )
                for i, page in enumerate(pagify(subtext, page_length=500, shorten_by=0)):
                    title = "**__Subcommands:__**" if i == 0 else EMPTY_STRING
                    field = EmbedField(title, page, False)
                    emb["fields"].append(field)

            pages = await self.make_embeds(ctx, emb, help_settings=help_settings)
            await self.send_pages(ctx, pages, embed=True, help_settings=help_settings)
        else:
            await ctx.send("You need to enable embeds to use the help menu")

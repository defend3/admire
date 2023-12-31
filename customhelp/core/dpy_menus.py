from __future__ import annotations

import contextlib
from typing import Any, Union

import discord
from melaniebot.vendored.discord.ext import menus

# None of the below classes are done by me, it's mostly copy paste/ edited from a piece of code
# from trusty which got circulated around to me from !nowo. All credits go to him.
# Annd phen did some epico button magic.
# Not using an AsyncIterator cause even the core help loads all the commands at once.


class ListPages(menus.ListPageSource):
    def __init__(self, pages: list[Union[discord.Embed, str]]) -> None:
        super().__init__(pages, per_page=1)

    def is_paginating(self) -> bool:
        return True

    async def format_page(self, menu: menus.MenuPages, page: Union[discord.Embed, str]):
        return page


class BaseMenu(menus.MenuPages, inherit_buttons=False):
    def __init__(
        self,
        source: menus.PageSource,
        # cog: commands.Cog,
        clear_reactions_after: bool = True,
        delete_message_after: bool = False,
        timeout: int = 60,
        message: discord.Message = None,
        page_start: int = 0,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            source,
            clear_reactions_after=clear_reactions_after,
            delete_message_after=delete_message_after,
            timeout=timeout,
            message=message,
            **kwargs,
        )
        self.page_start = page_start

    async def show_page(self, page_number, payload=None) -> None:
        # added unused payload arg since ButtonMenu requires the button to be passed
        # when showing a page with InteractionButton.update
        await super().show_page(page_number)

    async def change_source(self, source, payload) -> None:
        await super().change_source(source)

    def add_button(self, button, *, react: bool = False, interaction=None):
        return super().add_button(button, react=react)

    async def show_checked_page(self, page_number: int, payload=None) -> None:
        max_pages = self._source.get_max_pages()
        with contextlib.suppress(IndexError):
            if max_pages is None or page_number < max_pages and page_number >= 0:
                # If it doesn't give maximum pages, it cannot be checked
                await self.show_page(page_number, payload)
            elif page_number >= max_pages:
                await self.show_page(0, payload)
            else:
                await self.show_page(max_pages - 1, payload)

    def reaction_check(self, payload) -> bool:
        """Just extends the default reaction_check to use owner_ids."""
        if payload.message_id != self.message.id:
            return False
        if payload.user_id not in (*self.bot.owner_ids, self._author_id):
            return False
        return payload.emoji in self.buttons


class ReplyMenus(BaseMenu, inherit_buttons=False):
    async def send_initial_message(self, ctx, channel):
        page = await self._source.get_page(0)
        kwargs = await self._get_kwargs_from_page(page)
        kwargs["reference"] = ctx.message.to_reference(fail_if_not_exists=False)  # sends message silently when message is deleted
        return await ctx.send(**kwargs)

    async def _get_kwargs_from_page(self, page):
        # Do this if you dont want to ping the user
        kwargs = {"allowed_mentions": discord.AllowedMentions(replied_user=False)}
        value = await discord.utils.maybe_coroutine(self._source.format_page, self, page)
        if isinstance(value, dict):
            kwargs |= value
        elif isinstance(value, str):
            kwargs["content"] = value
        elif isinstance(value, discord.Embed):
            kwargs["embed"] = value
        return kwargs


def get_button_menu(use_replies: bool) -> None:
    return

    # class HelpButtonMenu(BaseButtonMenu, BaseMenu, inherit_buttons=False):
    #     async def send_initial_message(self, ctx, channel: discord.TextChannel):

    #     async def show_page(self, page_number, button):

    #     async def change_source(self, source, button):


NoReplyMenus = BaseMenu

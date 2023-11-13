from __future__ import annotations

import unicodedata
from typing import Union

import discord
from melaniebot.core.utils import chat_formatting as chat

from .common_variables import ACTIVITY_TYPES, APP_ICON_URL, NON_ESCAPABLE_CHARACTERS
from .utils import _, bool_emojify, find_app_by_name, get_twemoji


async def emoji_embed(ctx, emoji: Union[discord.Emoji, discord.PartialEmoji]) -> discord.Embed:
    """Make embed with info about emoji."""
    em = discord.Embed(
        title=isinstance(emoji, str)
        and "\n".join(unicodedata.name(c, "[Unable to resolve unicode name]") for c in emoji)
        or chat.escape(emoji.name, formatting=True),
        color=await ctx.embed_color(),
    )

    if isinstance(emoji, str):
        em.add_field(name="Unicode character", value="\n".join(f"\\{c}" if c not in NON_ESCAPABLE_CHARACTERS else c for c in emoji))
        em.add_field(name="Unicode category", value="\n".join(unicodedata.category(c) for c in emoji))
        em.set_image(url=await get_twemoji(emoji))
    if not isinstance(emoji, str):
        em.add_field(name="ID", value=emoji.id)
        em.add_field(name="Animated", value=bool_emojify(emoji.animated))
        em.set_image(url=emoji.url)
    if isinstance(emoji, discord.Emoji):
        em.add_field(name="Exists since", value=emoji.created_at.strftime(ctx.cog.TIME_FORMAT))
        em.add_field(name=_('":" required'), value=bool_emojify(emoji.require_colons))
        em.add_field(name="Managed", value=bool_emojify(emoji.managed))
        em.add_field(name="Server", value=emoji.guild)
        em.add_field(name="Available", value=bool_emojify(emoji.available))
        em.add_field(name="Usable by bot", value=bool_emojify(emoji.is_usable()))
        if emoji.roles:
            em.add_field(name="Roles", value=chat.escape("\n".join(x.name for x in emoji.roles), formatting=True), inline=False)
    elif isinstance(emoji, discord.PartialEmoji):
        em.add_field(name="Exists since", value=emoji.created_at.strftime(ctx.cog.TIME_FORMAT))
        em.add_field(name="Custom emoji", value=bool_emojify(emoji.is_custom_emoji()))
        # em.add_field(
    return em


async def activity_embed(ctx, activity: discord.Activity) -> discord.Embed:
    # sourcery no-metrics
    """Make embed with info about activity."""
    # design is not my best side
    if isinstance(activity, discord.CustomActivity):
        em = discord.Embed(title=activity.name, color=await ctx.embed_color())
        if activity.emoji:
            if activity.emoji.is_unicode_emoji():
                emoji_pic = await get_twemoji(activity.emoji.name)
            else:
                emoji_pic = activity.emoji.url
            if activity.name:
                em.set_thumbnail(url=emoji_pic)
            else:
                em.set_image(url=emoji_pic)
        em.set_footer(text="custom status")
    elif isinstance(activity, discord.Game):
        em = discord.Embed(title=f"Playing {activity.name}", timestamp=activity.start or discord.Embed.Empty, color=await ctx.embed_color())
        # noinspection PyUnresolvedReferences
        apps = await ctx.cog.bot.http.request(discord.http.Route("GET", "/applications/detectable"))
        app = await find_app_by_name(apps, activity.name)
        if app:
            em.set_thumbnail(url=APP_ICON_URL.format(app_id=app.get("id", ""), icon_hash=app.get("icon", "")))
        if activity.end:
            em.add_field(name="This game will end at", value=activity.end.strftime(ctx.cog.TIME_FORMAT))
        if activity.start:
            em.set_footer(text="Playing since")
    elif isinstance(activity, discord.Activity):
        party_size = activity.party.get("size")
        party_size = f" ({party_size[0]}/{party_size[1]})" if party_size else ""
        em = discord.Embed(
            title=f"{_(ACTIVITY_TYPES.get(activity.type, activity.type))} {activity.name}",
            description=f"{activity.details and activity.details or ''}\n{activity.state and activity.state or ''}{party_size}",
            color=await ctx.embed_color(),
        )
        # noinspection PyUnresolvedReferences
        apps = await ctx.cog.bot.http.request(discord.http.Route("GET", "/applications/detectable"))
        app = await find_app_by_name(apps, activity.name)
        if app:
            em.set_thumbnail(url=APP_ICON_URL.format(app_id=app.get("id", activity.application_id or ""), icon_hash=app.get("icon", "")))
        if activity.small_image_text:
            em.add_field(name="Small image text", value=activity.small_image_text, inline=False)
        if activity.application_id:
            em.add_field(name="Application ID", value=activity.application_id)
        if activity.start:
            em.add_field(name="Started at", value=activity.start.strftime(ctx.cog.TIME_FORMAT))
        if activity.end:
            em.add_field(name="Will end at", value=activity.end.strftime(ctx.cog.TIME_FORMAT))
        if activity.large_image_text:
            em.add_field(name="Large image text", value=activity.large_image_text, inline=False)
        if activity.small_image_url:
            em.set_thumbnail(url=activity.small_image_url)
        if activity.large_image_url:
            em.set_image(url=activity.large_image_url)
    elif isinstance(activity, discord.Streaming):
        em = discord.Embed(title=activity.name, description=f"Streaming on {activity.platform}", url=activity.url)
        if activity.game:
            em.add_field(name="Game", value=activity.game)
    elif isinstance(activity, discord.Spotify):
        em = discord.Embed(
            title=activity.title,
            description=f'by {", ".join(activity.artists)}\non {activity.album}',
            color=activity.color,
            timestamp=activity.created_at,
            url=f"https://open.spotify.com/track/{activity.track_id}",
        )
        em.add_field(name="Started at", value=activity.start.strftime(ctx.cog.TIME_FORMAT))
        em.add_field(name="Duration", value=str(activity.duration)[:-3])  # 0:03:33.877[000]  # 0:03:33.877[000]
        em.add_field(name="Will end at", value=activity.end.strftime(ctx.cog.TIME_FORMAT))
        em.set_image(url=activity.album_cover_url)
        em.set_footer(text="Listening since")
    else:
        em = discord.Embed(title=f"Unsupported activity type: {type(activity)}")
    return em

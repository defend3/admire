from __future__ import annotations

import datetime
from collections.abc import Sized

import discord
import regex as re
import ujson
from melaniebot.core.bot import Melanie as Bot
from melaniebot.core.utils.menus import DEFAULT_CONTROLS, commands, menu

SEARCH_ANIME_MANGA_QUERY = """
query ($id: Int, $page: Int, $search: String, $type: MediaType) {
    Page (page: $page, perPage: 10) {
        media (id: $id, search: $search, type: $type) {
            id
            idMal
            description(asHtml: false)
            title {
                english
                romaji
            }
            coverImage {
            		medium
            }
            bannerImage
            averageScore
            meanScore
            status
            episodes
            chapters
            externalLinks {
                url
                site
            }
            nextAiringEpisode {
                timeUntilAiring
            }
        }
    }
}
"""

SEARCH_CHARACTER_QUERY = """
query ($id: Int, $page: Int, $search: String) {
  Page(page: $page, perPage: 10) {
    characters(id: $id, search: $search) {
      id
      description (asHtml: true),
      name {
        first
        last
        native
      }
      image {
        large
      }
      media {
        nodes {
          id
          type
          title {
            romaji
            english
            native
            userPreferred
          }
        }
      }
    }
  }
}
"""

SEARCH_USER_QUERY = """
query ($id: Int, $page: Int, $search: String) {
    Page (page: $page, perPage: 10) {
        users (id: $id, search: $search) {
            id
            name
            siteUrl
            avatar {
                    large
            }
            about (asHtml: true),
            stats {
                watchedTime
                chaptersRead
            }
            favourites {
            manga {
              nodes {
                id
                title {
                  romaji
                  english
                  native
                  userPreferred
                }
              }
            }
            characters {
              nodes {
                id
                name {
                  first
                  last
                  native
                }
              }
            }
            anime {
              nodes {
                id
                title {
                  romaji
                  english
                  native
                  userPreferred
                }
              }
            }
            }
        }
    }
}
"""

BaseCog = getattr(commands, "Cog", object)


class AniSearch(BaseCog):
    """Search for anime, manga, characters and users using Anilist."""

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.url = "https://graphql.anilist.co"

    def format_name(self, first_name, last_name) -> str:  # Combines first_name and last_name and/or shows either of the two
        if first_name and last_name:
            return f"{first_name} {last_name}"
        elif first_name:
            return first_name
        elif last_name:
            return last_name
        else:
            return "No name"

    def clean_html(self, description):  # Removes html tags
        return self._extracted_from_clean_spoilers_2(description, "<.*?>")

    def clean_spoilers(self, description):  # Removes spoilers using the html tag given by AniList
        return self._extracted_from_clean_spoilers_2(description, "/<span[^>]*>.*</span>/g")

    # TODO Rename this here and in `clean_html` and `clean_spoilers`
    def _extracted_from_clean_spoilers_2(self, description, arg1) -> str:
        if not description:
            return ""
        cleanr = re.compile(arg1)
        return re.sub(cleanr, "", description)

    def description_parser(self, description: str) -> str:  # Limits text to 400characters and 5 lines and adds "..." at the end
        description = self.clean_spoilers(description)
        description = self.clean_html(description)
        description = "\n".join(description.split("\n")[:5])
        return f"{description[:400]}..." if len(description) > 400 else description

    def list_maximum(self, items: Sized):  # Limits to 5 strings than adds "+X more"
        if len(items) > 5:
            return items[:5] + [f"+ {str(len(items) - 5)} more"]
        else:
            return items

    async def _request(self, query, variables=None):
        if variables is None:
            variables = {}

        request_json = {"query": query, "variables": variables}

        headers = {"content-type": "application/json"}

        async with self.bot.aio.post(self.url, data=ujson.dumps(request_json), headers=headers) as response:
            return await response.json()

    async def _search_anime_manga(self, ctx, cmd, entered_title):
        variables = {"search": entered_title, "page": 1, "type": cmd}

        data = (await self._request(SEARCH_ANIME_MANGA_QUERY, variables))["data"]["Page"]["media"]

        if data is None or len(data) <= 0:
            return None

        # a list of embeds
        embeds = []

        # Outputs MediaStatuses to strings
        MediaStatusToString = {
            # Has completed and is no longer being released
            "FINISHED": "Finished",
            # Currently releasing
            "RELEASING": "Releasing",
            # To be released at a later date
            "NOT_YET_RELEASED": "Not yet released",
            # Ended before the work could be finished
            "CANCELLED": "Cancelled",
        }

        for anime_manga in data:
            # Sets up various variables for Embed
            link = f"https://anilist.co/{cmd.lower()}/{anime_manga['id']}"
            description = anime_manga["description"]
            title = anime_manga["title"]["english"] or anime_manga["title"]["romaji"]
            if anime_manga.get("nextAiringEpisode"):
                seconds = anime_manga["nextAiringEpisode"]["timeUntilAiring"]
                time_left = str(datetime.timedelta(seconds=seconds))
            else:
                time_left = "Never"

            external_links = ""
            for i in range(len(anime_manga["externalLinks"])):
                ext_link = anime_manga["externalLinks"][i]
                external_links += f"[{ext_link['site']}]({ext_link['url']}), "
                if i + 1 == len(anime_manga["externalLinks"]):
                    external_links = external_links[:-2]

            embed = discord.Embed(title=title)
            embed.url = link
            embed.color = 3447003
            embed.description = self.description_parser(description)
            embed.set_thumbnail(url=anime_manga["coverImage"]["medium"])
            embed.add_field(name="Score", value=anime_manga.get("averageScore", "N/A"))
            if cmd == "ANIME":
                embed.add_field(name="Episodes", value=anime_manga.get("episodes", "N/A"))
                embed.set_footer(text=f'Status : {MediaStatusToString[anime_manga["status"]]}, Next episode : {time_left}, Powered by Anilist')

            else:
                embed.add_field(name="Chapters", value=anime_manga.get("chapters", "N/A"))
                embed.set_footer(text="Status : " + MediaStatusToString.get(anime_manga.get("status"), "N/A") + ", Powered by Anilist")
            if external_links:
                embed.add_field(name="Streaming and/or Info sites", value=external_links)
            if anime_manga["bannerImage"]:
                embed.set_image(url=anime_manga["bannerImage"])
            embed.add_field(
                name="You can find out more",
                value=f"[Anilist]({link}), [MAL](https://myanimelist.net/{cmd.lower()}/{anime_manga['idMal']}), Kitsu (Soon™)",
            )
            embeds.append(embed)

        return (embeds, data)

    async def _search_character(self, ctx, entered_title):
        variables = {"search": entered_title, "page": 1}

        data = (await self._request(SEARCH_CHARACTER_QUERY, variables))["data"]["Page"]["characters"]

        if data is None or len(data) <= 0:
            return None

        # a list of embeds
        embeds = []

        for character in data:
            # Sets up various variables for Embed
            link = f"https://anilist.co/character/{character['id']}"
            character_anime = [
                f'[{anime["title"]["userPreferred"]}]({"https://anilist.co/anime/" + str(anime["id"])})'
                for anime in character["media"]["nodes"]
                if anime["type"] == "ANIME"
            ]
            character_manga = [
                f'[{manga["title"]["userPreferred"]}]({"https://anilist.co/manga/" + str(manga["id"])})'
                for manga in character["media"]["nodes"]
                if manga["type"] == "MANGA"
            ]
            embed = discord.Embed(title=self.format_name(character["name"]["first"], character["name"]["last"]))
            embed.url = link
            embed.color = 3447003
            embed.description = self.description_parser(character["description"])
            embed.set_thumbnail(url=character["image"]["large"])
            if character_anime:
                embed.add_field(name="Anime", value="\n".join(self.list_maximum(character_anime)))
            if character_manga:
                embed.add_field(name="Manga", value="\n".join(self.list_maximum(character_manga)))
            embed.set_footer(text="Powered by Anilist")
            embeds.append(embed)

        return (embeds, data)

    async def _search_user(self, ctx, entered_title):
        variables = {"search": entered_title, "page": 1}

        data = (await self._request(SEARCH_USER_QUERY, variables))["data"]["Page"]["users"]

        if data is None or len(data) <= 0:
            return None

        # a list of embeds
        embeds = []

        for user in data:
            # Sets up various variables for Embed
            link = f"https://anilist.co/user/{user['id']}"
            title = f"[{user['name']}]({link})"
            title = user["name"]

            embed = discord.Embed(title=title)
            embed.url = link
            embed.color = 3447003
            embed.description = self.description_parser(user["about"])
            embed.set_thumbnail(url=user["avatar"]["large"])
            embed.add_field(name="Watched time", value=datetime.timedelta(minutes=int(user["stats"]["watchedTime"])))
            embed.add_field(name="Chapters read", value=user["stats"].get("chaptersRead", "N/A"))
            for category in ("anime", "manga", "characters"):
                fav = []
                for node in user["favourites"][category]["nodes"]:
                    url_path = category
                    if url_path == "characters":
                        name = node["name"]
                        title = self.format_name(name["first"], name["last"])
                        url_path = "character"  # without the s
                    else:
                        title = node["title"]["userPreferred"]

                    fav.append(f'[{title}](https://anilist.co/{url_path}/{node["id"]})')

                if fav:
                    embed.add_field(name=f"Favorite {category}", value="\n".join(self.list_maximum(fav)))
            embed.set_footer(text="Powered by Anilist")
            embeds.append(embed)

        return (embeds, data)

    @commands.command()
    async def anime(self, ctx, *, entered_title) -> None:
        """Searches for anime using Anilist."""
        try:
            cmd = "ANIME"
            (embeds, data) = await self._search_anime_manga(ctx, cmd, entered_title)

            if embeds is not None:
                await menu(ctx, pages=embeds, controls=DEFAULT_CONTROLS, message=None, page=0, timeout=30)
            else:
                await ctx.send("No anime was found or there was an error in the process")

        except TypeError:
            await ctx.send("No anime was found or there was an error in the process")

    @commands.command()
    async def manga(self, ctx, *, entered_title) -> None:
        """Searches for manga using Anilist."""
        try:
            cmd = "MANGA"
            (embeds, data) = await self._search_anime_manga(ctx, cmd, entered_title)

            if embeds is not None:
                await menu(ctx, pages=embeds, controls=DEFAULT_CONTROLS, message=None, page=0, timeout=30)
            else:
                await ctx.send("No mangas were found or there was an error in the process")

        except TypeError:
            await ctx.send("No mangas were found or there was an error in the process")

    @commands.command()
    async def character(self, ctx, *, entered_title) -> None:
        """Searches for characters using Anilist."""
        try:
            (embeds, data) = await self._search_character(ctx, entered_title)

            if embeds is not None:
                await menu(ctx, pages=embeds, controls=DEFAULT_CONTROLS, message=None, page=0, timeout=30)
            else:
                await ctx.send("No characters were found or there was an error in the process")

        except TypeError:
            await ctx.send("No characters were found or there was an error in the process")

    @commands.command()
    async def user(self, ctx, *, entered_title) -> None:
        """Searches users using Anilist."""
        try:
            (embeds, data) = await self._search_user(ctx, entered_title)

            if embeds is not None:
                await menu(ctx, pages=embeds, controls=DEFAULT_CONTROLS, message=None, page=0, timeout=30)
            else:
                await ctx.send("No users were found or there was an error in the process")

        except TypeError:
            await ctx.send("No users were found or there was an error in the process")

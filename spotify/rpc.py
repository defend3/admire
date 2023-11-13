from __future__ import annotations

from typing import Union

from loguru import logger as log
from melaniebot.core.bot import Melanie
from melaniebot.core.commands import commands

from dashboard.rpc.utils import rpccheck


class DashboardRPC_Spotify:
    def __init__(self, cog: commands.Cog) -> None:
        self.bot: Melanie = cog.bot
        self.cog: commands.Cog = cog

        self.bot.register_rpc_handler(self.authenticate_user)

    def unload(self) -> None:
        self.bot.unregister_rpc_handler(self.authenticate_user)

    @rpccheck()
    async def authenticate_user(self, user: int, code: str, state: str) -> Union[dict[str, int], dict[str, Union[int, str]]]:
        if not self.bot.get_cog("Spotify"):
            return {"status": 0, "message": "Spotify cog is not loaded."}

        user = int(user)  # Blame socket communication for this

        userobj = self.bot.get_user(user)
        if not userobj:
            return {"status": 0, "message": "Unknown user."}
        if not self.cog._credentials:
            return {"status": 0, "message": "Bot owner has not set credentials."}
        log.debug(user)
        try:
            auth = self.cog.temp_cache[userobj.id]
        except KeyError:
            return {"status": 0, "message": "You must authenticate using a link given by bot. If this fails try posting the full URL inside discord."}

        user_token = await auth.request_token(code=code, state=state)
        await self.cog.save_token(userobj, user_token)

        del self.cog.temp_cache[userobj.id]
        self.cog.dashboard_authed.append(userobj.id)

        return {"status": 1}

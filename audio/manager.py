from __future__ import annotations

import asyncio  # disables for # https://github.com/PyCQA/pylint/issues/1469
import asyncio.subprocess
import contextlib
import itertools
import pathlib
import platform
import shutil
import time
from re import Pattern
from typing import ClassVar, Final, Optional

import regex as re
from melaniebot.core import data_manager

from .utils import task_callback

with contextlib.suppress(Exception):

    def _(x):
        return x

    from melanie import log

    JAR_VERSION: Final[str] = "3.4.0"
    JAR_BUILD: Final[int] = 1275
    LAVALINK_DOWNLOAD_URL: Final[str] = f"https://github.com/Cog-Creators/Lavalink-Jars/releases/download/{JAR_VERSION}_{JAR_BUILD}/Lavalink.jar"
    LAVALINK_DOWNLOAD_DIR: Final[pathlib.Path] = data_manager.cog_data_path(raw_name="Audio")
    LAVALINK_JAR_FILE: Final[pathlib.Path] = LAVALINK_DOWNLOAD_DIR / "Lavalink.jar"
    BUNDLED_APP_YML: Final[pathlib.Path] = pathlib.Path(__file__).parent / "data" / "application.yml"
    LAVALINK_APP_YML: Final[pathlib.Path] = LAVALINK_DOWNLOAD_DIR / "application.yml"
    _RE_READY_LINE: Final[Pattern] = re.compile(rb"Started Launcher in \S+ seconds")
    _FAILED_TO_START: Final[Pattern] = re.compile(rb"Web server failed to start\. (.*)")
    _RE_BUILD_LINE: Final[Pattern] = re.compile(rb"Build:\s+(?P<build>\d+)")
_RE_JAVA_VERSION_LINE_PRE223: Final[Pattern] = re.compile(r'version "1\.(?P<major>[0-8])\.(?P<minor>0)(?:_(?:\d+))?(?:-.*)?"')

_RE_JAVA_VERSION_LINE_223: Final[Pattern] = re.compile(r'version "(?P<major>\d+)(?:\.(?P<minor>\d+))?(?:\.\d+)*(\-[a-zA-Z0-9]+)?"')

LAVALINK_BRANCH_LINE: Final[Pattern] = re.compile(rb"Branch\s+(?P<branch>[\w\-\d_.]+)")
LAVALINK_JAVA_LINE: Final[Pattern] = re.compile(rb"JVM:\s+(?P<jvm>\d+[.\d+]*)")
LAVALINK_LAVAPLAYER_LINE: Final[Pattern] = re.compile(rb"Lavaplayer\s+(?P<lavaplayer>\d+[.\d+]*)")
LAVALINK_BUILD_TIME_LINE: Final[Pattern] = re.compile(rb"Build time:\s+(?P<build_time>\d+[.\d+]*)")


class ServerManager:
    _java_available: ClassVar[Optional[bool]] = None
    _java_version: ClassVar[Optional[tuple[int, int]]] = None
    _up_to_date: ClassVar[Optional[bool]] = None
    _blacklisted_archs: list[str] = []

    _lavaplayer: ClassVar[Optional[str]] = None
    _lavalink_build: ClassVar[Optional[int]] = None
    _jvm: ClassVar[Optional[str]] = None
    _lavalink_branch: ClassVar[Optional[str]] = None
    _buildtime: ClassVar[Optional[str]] = None
    _java_exc: ClassVar[str] = "java"

    def __init__(self) -> None:
        self.ready: asyncio.Event = asyncio.Event()

        self._proc: Optional[asyncio.subprocess.Process] = None  # pylint:disable=no-member
        self._monitor_task: Optional[asyncio.Task] = None
        self._shutdown: bool = False

    @property
    def path(self) -> Optional[str]:
        return self._java_exc

    @property
    def jvm(self) -> Optional[str]:
        return self._jvm

    @property
    def lavaplayer(self) -> Optional[str]:
        return self._lavaplayer

    @property
    def ll_build(self) -> Optional[int]:
        return self._lavalink_build

    @property
    def ll_branch(self) -> Optional[str]:
        return self._lavalink_branch

    @property
    def build_time(self) -> Optional[str]:
        return self._buildtime

    async def start(self, java_path: str) -> None:
        arch_name = platform.machine()
        self._java_exc = java_path
        if arch_name in self._blacklisted_archs:
            msg = "You are attempting to run Lavalink audio on an unsupported machine architecture."
            raise asyncio.CancelledError(msg)

        if self._proc is not None:
            if self._proc.returncode is None:
                msg = "Internal Lavalink server is already running"
                raise RuntimeError(msg)
            elif self._shutdown:
                msg = "Server manager has already been used - create another one"
                raise RuntimeError(msg)

        await self.maybe_download_jar()

        # Copy the application.yml across.
        # For people to customise their Lavalink server configuration they need to run it
        # externally
        shutil.copyfile(BUNDLED_APP_YML, LAVALINK_APP_YML)

        args = await self._get_jar_args()
        self._proc = await asyncio.subprocess.create_subprocess_exec(
            *args,
            cwd=str(LAVALINK_DOWNLOAD_DIR),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )  # pylint:disable=no-member

        log.info("Internal Lavalink server started. PID: {}", self._proc.pid)

        try:
            await asyncio.wait_for(self._wait_for_launcher(), timeout=120)
        except TimeoutError:
            log.warning("Timeout occurred whilst waiting for internal Lavalink server to be ready")

        self._monitor_task = asyncio.create_task(self._monitor())
        self._monitor_task.add_done_callback(task_callback)

    async def _get_jar_args(self) -> list[str]:
        (java_available, java_version) = await self._has_java()

        if not java_available:
            msg = "You must install Java 11 for Lavalink to run."
            raise RuntimeError(msg)

        return [self._java_exc, "-Djdk.tls.client.protocols=TLSv1.2", "-jar", str(LAVALINK_JAR_FILE)]

    async def _has_java(self) -> tuple[bool, Optional[tuple[int, int]]]:
        if self._java_available is not None:
            # Return cached value if we've checked this before
            return self._java_available, self._java_version
        java_exec = shutil.which(self._java_exc)
        java_available = java_exec is not None
        if not java_available:
            self.java_available = False
            self.java_version = None
        else:
            self._java_version = version = await self._get_java_version()
            self._java_available = (11, 0) <= version < (12, 0)
            self._java_exc = java_exec
        return self._java_available, self._java_version

    async def _get_java_version(self) -> tuple[int, int]:
        """This assumes we've already checked that java exists."""
        _proc: asyncio.subprocess.Process = await asyncio.create_subprocess_exec(
            self._java_exc,
            "-version",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )  # pylint:disable=no-member
        # java -version outputs to stderr
        _, err = await _proc.communicate()

        version_info: str = err.decode("utf-8")
        lines = version_info.splitlines()
        for line in lines:
            match = _RE_JAVA_VERSION_LINE_PRE223.search(line)
            if match is None:
                match = _RE_JAVA_VERSION_LINE_223.search(line)
            if match is None:
                continue
            major = int(match["major"])
            minor = 0
            if minor_str := match["minor"]:
                minor = int(minor_str)

            return major, minor

        msg = f"The output of `{self._java_exc} -version` was unexpected."
        raise RuntimeError(msg)

    async def _wait_for_launcher(self) -> None:
        log.debug("Waiting for Lavalink server to be ready")
        lastmessage = 0
        for i in itertools.cycle(range(50)):
            line = await self._proc.stdout.readline()
            if _RE_READY_LINE.search(line):
                self.ready.set()
                log.info("Internal Lavalink server is ready to receive requests.")
                break
            if _FAILED_TO_START.search(line):
                msg = f"Lavalink failed to start: {line.decode().strip()}"
                raise RuntimeError(msg)
            if self._proc.returncode is not None and lastmessage + 2 < time.time():
                # Avoid Console spam only print once every 2 seconds
                lastmessage = time.time()
                log.critical("Internal lavalink server exited early")
            if i == 49:
                # Sleep after 50 lines to prevent busylooping
                await asyncio.sleep(0.1)

    async def _monitor(self) -> None:
        while self._proc.returncode is None:
            await asyncio.sleep(0.5)

        # This task hasn't been cancelled - Lavalink was shut down by something else
        log.info("Internal Lavalink jar shutdown unexpectedly")
        if not self._has_java_error():
            log.info("Restarting internal Lavalink server")
            await self.start(self._java_exc)
        else:
            log.critical("Your Java is borked. Please find the hs_err_pid{}.log file in the Audio data folder and report this issue.", self._proc.pid)

    def _has_java_error(self) -> bool:
        poss_error_file = LAVALINK_DOWNLOAD_DIR / f"hs_err_pid{self._proc.pid}.log"
        return poss_error_file.exists()

    async def shutdown(self) -> None:
        if self._shutdown is True or self._proc is None:
            # For convenience, calling this method more than once or calling it before starting it
            # does nothing.
            return
        log.info("Shutting down internal Lavalink server")
        if self._monitor_task is not None:
            self._monitor_task.cancel()
        self._proc.terminate()
        await self._proc.wait()
        self._shutdown = True

    async def _download_jar(self) -> None:
        return
        # async with self.bot.get(LAVALINK_DOWNLOAD_URL) as response:
        #     if response.status == 404:
        #         # A 404 means our LAVALINK_DOWNLOAD_URL is invalid, so likely the jar version
        #         # hasn't been published yet
        #         raise LavalinkDownloadFailed(
        #         # Other bad responses should be raised but we should retry just incase
        #     with rich.progress.Progress(
        #     ) as progress:
        #             while chunk:

    async def _is_up_to_date(self):
        if self._up_to_date is True:
            # Return cached value if we've checked this before
            return True
        args = await self._get_jar_args()
        args.append("--version")
        _proc = await asyncio.subprocess.create_subprocess_exec(
            *args,
            cwd=str(LAVALINK_DOWNLOAD_DIR),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )  # pylint:disable=no-member
        stdout = (await _proc.communicate())[0]
        if (build := _RE_BUILD_LINE.search(stdout)) is None:
            # Output is unexpected, suspect corrupted jarfile
            return False
        if (branch := LAVALINK_BRANCH_LINE.search(stdout)) is None:
            # Output is unexpected, suspect corrupted jarfile
            return False
        if (java := LAVALINK_JAVA_LINE.search(stdout)) is None:
            # Output is unexpected, suspect corrupted jarfile
            return False
        if (lavaplayer := LAVALINK_LAVAPLAYER_LINE.search(stdout)) is None:
            # Output is unexpected, suspect corrupted jarfile
            return False
        if (buildtime := LAVALINK_BUILD_TIME_LINE.search(stdout)) is None:
            # Output is unexpected, suspect corrupted jarfile
            return False

        build = int(build["build"])
        date = buildtime["build_time"].decode()
        date = date.replace(".", "/")
        self._lavalink_build = build
        self._lavalink_branch = branch["branch"].decode()
        self._jvm = java["jvm"].decode()
        self._lavaplayer = lavaplayer["lavaplayer"].decode()
        self._buildtime = date
        self._up_to_date = build >= JAR_BUILD
        return self._up_to_date

    async def maybe_download_jar(self) -> None:
        if not (LAVALINK_JAR_FILE.exists() and await self._is_up_to_date()):
            await self._download_jar()

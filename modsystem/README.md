# WarnSystem

This is the WarnSystem cog for Melanie, rewrite of the V2 cog, BetterMod. It is an alternative to the core moderation system of Melanie, similar to Dyno. You can warn members up to 5 levels:

1. simple warning
2. mute (can be a temporary mute)
3. kick
4. softban (ban then unban, which can cleanup the messages of an user up to a week)
5. ban (can be a temporary ban, or even a hack ban, which allows you to ban on an user not on the server)

When you warn a member, **he receives a DM** with the reason of his warn. It's also logged on your defined modlog. You can keep track of a members' warnings with an interactive menu, and even edit or delete his old warnings.

There is a detailed documentation, covering all commands in details, please read this if you want to know how commands works in details: https://laggron.red/warnsystem.html

The cog is highly customizable and frequently updated. It's also built with an API, allowing you to use WarnSystem without a context on Discord, perfect for your pre-made eval commands or any scheduler. You can get more details about this on the [API reference](https://laggron.red/warnsystem-api.html).

## Installation and quick start

`;` is your prefix.

1.  Install the repo if it's not already done.

    ```
    ;repo add Laggrons-Dumb-Cogs https://github.com/retke/Laggrons-Dumb-Cogs v3
    ```

2.  If you have the core Warnings cog loaded, unload it, or the command names will conflict.

    ```
    ;unload warnings
    ```

3.  Install and load WarnSystem

    ```py
    ;cog install Laggrons-Dumb-Cogs warnsystem
    # Type "I agree" if requested
    # wait for your bot to install the cog
    ;load warnsystem
    ```

    WarnSystem is now installed!

4.  On your server, set your modlog channel

    ```
    ;warnset channel #channel-name
    ```

    _Note: If you already set a modlog channel with the modlogs cog, it will be used if you skip this part._

5.  Setup a mute role. **This might take a long time, depending on the number of text channels on your server.**

    ```
    ;warnset mute
    ```

    The mutes are done with a role. Feel free to edit its permissions, but make sure it stays under the bot's top role!

6.  (Optional) Import your data from BetterMod.

    **You must have the latest version of BetterMod before using this command. Using an outdated body will break the data of the cog!**

    1.  Grab your server ID. To get this, you can either:

        - Use the `;serverinfo` command in the General cog.
        - Enable the developer mode (User settings > Appearance), right click on your server, then click "Copy ID"

    2.  Go to your V2 bot's directory, and navigate to `data/bettermod/history/` and find the file which name is your server ID, and copy its full path.

    3.  Type this command: `;warnset convert <path_to_file>`
        You will then be guided through the final steps.

All done! You can now start to warn members with the `;warn` command.
See the full list of possible settings with `;help warnset`.

## Discord server

If you need support, have bugs to report or suggestions to bring, please join my Discord server and tell me, `El Laggron#0260`, about it!

[![Discord server](https://discordapp.com/api/guilds/363008468602454017/embed.png?style=banner3)](https://discord.gg/AVzjfpR)

## Extensions

As said before, it's possible to develop extensions to WarnSystem. Currently, there aren't any, but some are planned, such as an automod.

## [Laggron's Dumb Cogs](https://github.com/retke/Laggrons-Dumb-Cogs)

![Artwork](https://github.com/retke/Laggrons-Dumb-Cogs/blob/master/.github/RESSOURCES/BANNERS/Base_banner.png)

This cog is part of the Laggron's Dumb Cogs repository, where utility cogs for managing your server are made!
If you like this cog, you should check the other cogs from [the repository](https://github.com/retke/Laggrons-Dumb-Cogs)!

You can also support me on [Patreon](https://patreon.com/retke) or [Github Sponsors](https://github.com/sponsors/retke/card) and get exclusive rewards!

## Contribute

If you're reading this from Github and want to contribute or just understand the source code, I'm gonna stop you right there. Indeed, the cog is a bit complex so let me explain a bit how each file work before source diving.

- `__init__.py` The first file invoked when loading the cog. Nothing really useful here, only the check for the Warnings cog. _Added in 1.3:_ Data conversion stuff is located here.
- `abc.py` Just stuff for the inheritance of some classes.
- `api.py` The most important functions are there, such as warning a member, getting the warns, generating embeds... Those functions don't need a context to be invoked.
- `automod.py` Automod setup commands are here (`;automod` group command). The actual automod functions are located at the end of `api.py`.
- `converters.py` The argument parser for the `;masswarn` command. Informations are just extracted from text and they're given back to the command (works like a discord.py converter).
- `errors.py` The custom errors raised by `api.py` are in this file. There are only empty classes inherited from `Exception`.
- `settings.py` The cog file was getting really long, so I made a `SettingsMixin` class with the `;warnset` group command. The cog's class inherits from this one.
- `warnsystem.py` The file of the cog. All commands are stored there, except the `;warnset` group command.

If you're looking to edit something for a warn command, you may get lost. The command itself is 10 lines long. It calls `WarnSystem.call_warn` to prevent repeating what has to be done for all 5 warnings, but this function calls another one, `API.warn`, which is located in `api.py`, where most of the stuff is done.

So if you want to edit the interface of the commands, look in `warnsystem.py`. For internals, look in `api.py` instead. Any function called with `self.api` inside the WarnSystem class is located under the `API` class.

With that said, source diving should be easier.

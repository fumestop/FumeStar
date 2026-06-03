from __future__ import annotations

from typing import TYPE_CHECKING, Optional

import discord
from discord import app_commands
from discord.ext import commands

if TYPE_CHECKING:
    from bot import FumeStar

from utils.db import (
    is_blacklisted_user,
    add_blacklisted_user,
    is_blacklisted_guild,
    add_blacklisted_guild,
    remove_blacklisted_user,
    remove_blacklisted_guild,
)
from utils.config import Config


@app_commands.guilds(Config.COMMUNITY_GUILD_ID)
class Blacklist(
    commands.GroupCog,
    group_name="blacklist",
    group_description="Blacklist commands.",
):
    def __init__(self, bot: FumeStar):
        self.bot: FumeStar = bot

    @app_commands.command(name="add")
    async def _blacklist_add(
        self,
        ctx: discord.Interaction,
        user_id: Optional[str] = None,
        guild_id: Optional[str] = None,
    ):
        """Add a user or guild to the blacklist.

        Parameters
        ----------
        user_id : Optional[str]
            The user ID to add to the blacklist.
        guild_id : Optional[str]
            The guild ID to add to the blacklist.

        """
        # noinspection PyUnresolvedReferences
        await ctx.response.defer(thinking=True)

        if self.bot.owner != ctx.user:
            return await ctx.edit_original_response(
                content="Sorry, this is an owner only command!"
            )

        if user_id:
            if not user_id.isdigit():
                return await ctx.edit_original_response(
                    content="Invalid user ID provided."
                )

            else:
                user_id = int(user_id)

            if await is_blacklisted_user(self.bot.pool, user_id):
                return await ctx.edit_original_response(
                    content="User already blacklisted."
                )

            await add_blacklisted_user(self.bot.pool, user_id)

            return await ctx.edit_original_response(
                content="User added to the blacklist."
            )

        elif guild_id:
            if not guild_id.isdigit():
                return await ctx.edit_original_response(
                    content="Invalid guild ID provided."
                )

            guild_id = int(guild_id)

            if await is_blacklisted_guild(self.bot.pool, guild_id):
                return await ctx.edit_original_response(
                    content="Guild already blacklisted."
                )

            await add_blacklisted_guild(self.bot.pool, guild_id)

            return await ctx.edit_original_response(
                content="Guild added to the blacklist."
            )

        else:
            return await ctx.edit_original_response(
                content="No user or guild ID provided."
            )

    @app_commands.command(name="remove")
    @app_commands.rename(guild_id="server_id")
    async def _blacklist_remove(
        self,
        ctx: discord.Interaction,
        user_id: Optional[str] = None,
        guild_id: Optional[str] = None,
    ):
        """Remove a user or guild from the blacklist.

        Parameters
        ----------
        user_id : Optional[str]
            The user ID to remove from the blacklist.
        guild_id : Optional[str]
            The guild ID to remove from the blacklist.

        """
        # noinspection PyUnresolvedReferences
        await ctx.response.defer(thinking=True)

        if self.bot.owner != ctx.user:
            return await ctx.edit_original_response(
                content="Sorry, this is an owner only command!"
            )

        if user_id:
            if not user_id.isdigit():
                return await ctx.edit_original_response(
                    content="Invalid user ID provided."
                )

            else:
                user_id = int(user_id)

            if not await is_blacklisted_user(self.bot.pool, user_id):
                return await ctx.edit_original_response(
                    content="User not blacklisted."
                )

            await remove_blacklisted_user(self.bot.pool, user_id)

            return await ctx.edit_original_response(
                content="User removed from the blacklist."
            )

        if guild_id:
            if not guild_id.isdigit():
                return await ctx.edit_original_response(
                    content="Invalid guild ID provided."
                )

            guild_id = int(guild_id)

            if not await is_blacklisted_guild(self.bot.pool, guild_id):
                return await ctx.edit_original_response(
                    content="Guild not blacklisted."
                )

            await remove_blacklisted_guild(self.bot.pool, guild_id)

            return await ctx.edit_original_response(
                content="Server removed from the blacklist."
            )

        return await ctx.edit_original_response(
            content="No user or server ID provided."
        )


async def setup(bot: FumeStar):
    await bot.add_cog(Blacklist(bot))

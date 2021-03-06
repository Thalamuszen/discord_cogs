from redbot.core import checks, Config
from redbot.core.i18n import Translator, cog_i18n
import discord
from redbot.core import commands
from redbot.core.utils import mod
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS
import asyncio
import datetime
from .wraith import Wraith
from redbot import version_info, VersionInfo

class Apex(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.api = Wraith(bot)


    @checks.mod()
    @commands.command()
    async def setapexkey(self, ctx, *, apikey):
        """Set your Apex API key for that cog to work.
        Note that it is safer to use this command in DM."""
        if version_info >= VersionInfo.from_str("3.2.0"):
            key = await ctx.bot.set_shared_api_tokens("apex", api_key=apikey)
        else:
            await self.bot.db.api_tokens.set_raw("apex", value={'api_key': apikey})
        await ctx.send("Done")

    @commands.command()
    async def apex(self, ctx, *, username):
        res = await self.api.get_infos(username)
        ls = []
        try:
            for i in res:
                emb = discord.Embed(title=i['legend'])
                emb.set_thumbnail(url=i['icon_url'])
                for j in i['stats']:
                    emb.add_field(name=j['name'], value=j['value'], inline=False)
                ls.append(emb)
            await menu(ctx, ls, DEFAULT_CONTROLS)
        except:
            await ctx.send("Unknown player")
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions, CommandNotFound, BucketType, cooldown, CommandOnCooldown
from discord import Webhook, RequestsWebhookAdapter
from time import gmtime, strftime
from discord.utils import get
import youtube_dl
import logging
import random
import praw
import time
import json
import sys
import os

with open("config.json", "r") as file:
    config = json.load(file)

Creator = config['discord']['creator']
Co_Creator = config['discord']['co-creator']
EmbedColor = 0x4d004d

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        time = strftime("%H:%M:%S")
        print(f"[{time}] The {ctx.command.name} command was executed.")
        await ctx.send("Engineer Cat and the discord server will be shut down due to it being merged with another bot to make a better bot `Vikashi`. You can join the discord server here : https://discord.gg/8xyCDs5")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        print("[-]", error)
        if isinstance(error, CommandNotFound):
            await ctx.send("That command does not exist. Please do +help to get a list of all commands.")
        elif isinstance(error, CommandOnCooldown):
            await ctx.send(f"That command is on cooldown. Try again in {error.retry_after:,.2f} seconds.")
        elif isinstance(error, MissingPermissions):
            Denied = discord.Embed(title="Permission denied", description="You do not have the required permissions to run that command.", color=EmbedColor)
            await ctx.send(embed=Denied)

    @commands.Cog.listener()
    async def on_ready(self):
        print("[+] The bot is in " + str(len(self.bot.guilds)) + " servers!")
        print(f"[+] Logged in as {self.bot.user.name} - {self.bot.user.id}.")
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(name="discord.gg/wVaV5KT | +help"))

def setup(bot):
    bot.add_cog(Events(bot))

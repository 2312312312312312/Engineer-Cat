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

with open("configuration.json", "r") as file:
    configuration = json.load(file)

def Save():
    with open('configuration.json', 'w') as f:
        json.dump(configuration, f)

Creator = config['discord']['creator']
Co_Creator = config['discord']['co-creator']
EmbedColor = 0x4d004d

class Configuration(commands.Cog):
    def __init__(self, bot,):
        self.bot = bot
    
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def modlog(self, ctx, mlog: discord.TextChannel):
        try:
            configuration[str(ctx.guild.id)]["modlog"] = mlog.id
            await ctx.send("Configured modlog.")
            Save()
        except KeyError:
            configuration[str(ctx.guild.id)] = {"welcomer" : None, "autorole" : None, "modlog" : None}
            configuration[str(ctx.guild.id)]["modlog"] = mlog.id
            await ctx.send("Configured modlog.")
            Save()

    @commands.command()
    async def welcomer(self, ctx, channel: discord.TextChannel):
        try:
            configuration[str(ctx.guild.id)]["welcomer"] = channel.id
            await ctx.send("Configured the welcomer.")
            Save()
        except KeyError:
            configuration[str(ctx.guild.id)] = {"welcomer" : None, "autorole" : None, "modlog" : None}
            configuration[str(ctx.guild.id)]["welcomer"] = channel.id
            await ctx.send("Configured the welcomer.")
            Save()

    @commands.command()
    async def autorole(self, ctx, role: discord.Role):
        try:
            configuration[str(ctx.guild.id)]["welcomer"] = role.id
            await ctx.send("Configured autorole.")
            Save()
        except KeyError:
            configuration[str(ctx.guild.id)] = {"welcomer" : None, "autorole" : None, "modlog" : None}
            configuration[str(ctx.guild.id)]["autorole"] = role.id
            await ctx.send("Configured autorole.")
            Save()

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def disableModlog(self, ctx):
        try:
            configuration[str(ctx.guild.id)]["modlog"] = None
            await ctx.send("Disabled modlog.")
            Save()
        except KeyError:
            configuration[str(ctx.guild.id)] = {"welcomer" : None, "autorole" : None, "modlog" : None}
            configuration[str(ctx.guild.id)]["modlog"] = None
            await ctx.send("Disabled modlog.")
            Save()

    @commands.command()
    async def disableWelcomer(self, ctx):
        try:
            configuration[str(ctx.guild.id)]["welcomer"] = None
            await ctx.send("Disabled the welcomer.")
            Save()
        except KeyError:
            configuration[str(ctx.guild.id)] = {"welcomer" : None, "autorole" : None, "modlog" : None}
            configuration[str(ctx.guild.id)]["welcomer"] = None
            await ctx.send("Disabled the welcomer.")
            Save()

    @commands.command()
    async def disableAutorole(self, ctx):
        try:
            configuration[str(ctx.guild.id)]["welcomer"] = None
            await ctx.send("Disabled autorole.")
            Save()
        except KeyError:
            configuration[str(ctx.guild.id)] = {"welcomer" : None, "autorole" : None, "modlog" : None}
            configuration[str(ctx.guild.id)]["autorole"] = None
            await ctx.send("Disabled autorole.")
            Save()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if str(member.guild.id) in configuration:
            if not configuration[str(member.guild.id)]["welcomer"] == None:
                if not configuration[str(member.guild.id)]["autorole"] == None:
                    role = discord.utils.get(member.guild.roles, id=configuration[str(member.guild.id)]["autorole"])
                    await member.add_roles(role)
                    channel = self.bot.get_channel(configuration[str(member.guild.id)]["welcomer"])
                    Welcome = discord.Embed(title=f"Welcome", description=f"Welcome to the server {member.mention}!", color=EmbedColor)
                    Welcome.set_footer(text="Welcome!", icon_url="https://i.pinimg.com/originals/71/8b/3e/718b3eaa50e02f74dcc75e064f18face.gif")
                    await channel.send(f"{member.mention}", embed=Welcome)
                else:
                    channel = self.bot.get_channel(configuration[str(member.guild.id)]["welcomer"])
                    Welcome = discord.Embed(title=f"Welcome", description=f"Welcome to the server {member.mention}!", color=EmbedColor)
                    Welcome.set_footer(text="Welcome!", icon_url="https://i.pinimg.com/originals/71/8b/3e/718b3eaa50e02f74dcc75e064f18face.gif")
                    await channel.send(f"{member.mention}", embed=Welcome)

def setup(bot):
    bot.add_cog(Configuration(bot))
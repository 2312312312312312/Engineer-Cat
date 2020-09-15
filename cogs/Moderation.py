import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions, CommandNotFound, BucketType, cooldown, CommandOnCooldown
from discord import Webhook, RequestsWebhookAdapter
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

Creator = config['discord']['creator']
Co_Creator = config['discord']['co-creator']
EmbedColor = 0x4d004d

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, *, reason=None):
        await user.ban(reason=reason)
        print(f'[+] {user} was banned.')
        await ctx.send(f'{user} was banned.')
        ModLog = discord.Embed(title="Logged new activity!", description=f"{ctx.message.author.mention} banned {user.mention}.", color=EmbedColor)
        ModLog.set_footer(text="New activity!", icon_url="https://fc04.deviantart.net/fs71/f/2013/038/c/c/gold_ingot_by_barakaldo-d5u6i97.gif")
        channel = self.bot.get_channel(configuration[str(ctx.guild.id)]["modlog"])
        await channel.send(embed=ModLog)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            print(f"[+] {user} has been unbanned successfully.")
            await ctx.send(f"{user} has been unbanned sucessfully.")
            ModLog = discord.Embed(title="Logged new activity!", description=f"{ctx.message.author.mention} unbanned {user.mention}.", color=EmbedColor)
            ModLog.set_footer(text="New activity!", icon_url="https://fc04.deviantart.net/fs71/f/2013/038/c/c/gold_ingot_by_barakaldo-d5u6i97.gif")
            channel = self.bot.get_channel(configuration[str(ctx.guild.id)]["modlog"])
            await channel.send(embed=ModLog)
            return

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *, reason=None):
        await user.kick(reason=reason)
        print(f'[+] {user} was kicked.')
        await ctx.send(f'{user} was kicked.')
        ModLog = discord.Embed(title="Logged new activity!", description=f"{ctx.message.author.mention} kicked {user.mention}.", color=EmbedColor)
        ModLog.set_footer(text="New activity!", icon_url="https://fc04.deviantart.net/fs71/f/2013/038/c/c/gold_ingot_by_barakaldo-d5u6i97.gif")
        channel = self.bot.get_channel(configuration[str(ctx.guild.id)]["modlog"])
        await channel.send(embed=ModLog)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, user: discord.Member, *, reason=None):
        role = discord.utils.get(ctx.guild.roles, name="Muted")

        if role is None:
            await ctx.send("There is no Muted role in this server.")

        await user.add_roles(role)
        await ctx.send(f"Muted {user.mention}.")
        ModLog = discord.Embed(title="Logged new activity!", description=f"{ctx.message.author.mention} muted {user.mention}.", color=EmbedColor)
        ModLog.set_footer(text="New activity!", icon_url="https://fc04.deviantart.net/fs71/f/2013/038/c/c/gold_ingot_by_barakaldo-d5u6i97.gif")
        channel = self.bot.get_channel(configuration[str(ctx.guild.id)]["modlog"])
        await channel.send(embed=ModLog)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, user: discord.Member, *, reason=None):
        role = discord.utils.get(ctx.guild.roles, name="Muted")

        if role is None:
            await ctx.send("There is no Muted role in this server.")

        await user.remove_roles(role)
        await ctx.send(f"Unmuted {user.mention}.")
        ModLog = discord.Embed(title="Logged new activity!", description=f"{ctx.message.author.mention} unmuted {user.mention}.", color=EmbedColor)
        ModLog.set_footer(text="New activity!", icon_url="https://fc04.deviantart.net/fs71/f/2013/038/c/c/gold_ingot_by_barakaldo-d5u6i97.gif")
        channel = self.bot.get_channel(configuration[str(ctx.guild.id)]["modlog"])
        await channel.send(embed=ModLog)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, limit: int = 100):
        await ctx.message.delete()
        messages = await ctx.channel.purge(limit=limit)
        ModLog = discord.Embed(title="Logged new activity!", description=f"{ctx.message.author.mention} purged {limit} messages.", color=EmbedColor)
        ModLog.set_footer(text="New activity!", icon_url="https://fc04.deviantart.net/fs71/f/2013/038/c/c/gold_ingot_by_barakaldo-d5u6i97.gif")
        channel = self.bot.get_channel(configuration[str(ctx.guild.id)]["modlog"])
        await channel.send(embed=ModLog)

def setup(bot):
    bot.add_cog(Moderation(bot))

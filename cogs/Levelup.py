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

with open("users.json", "r") as file:
    users = json.load(file)

def SaveLevel():
    with open('users.json', 'w') as file:
        json.dump(users, file)

Creator = config['discord']['creator']
Co_Creator = config['discord']['co-creator']
EmbedColor = 0x4d004d

class Levelup(commands.Cog):
    def __init__(self, bot,):
        self.bot = bot

    @commands.command()
    async def rank(self, ctx):
        if str(ctx.message.author.id) in users[str(ctx.guild.id)]:
            xp = users[str(ctx.message.guild.id)][str(ctx.message.author.id)]["xp"]
            level = users[str(ctx.message.guild.id)][str(ctx.message.author.id)]["level"]
            balance = discord.Embed(title=f"{ctx.message.author}'s rank", description=f"**Level : `{level}`**\n**XP: `{xp}`**", color=EmbedColor)
            await ctx.send(embed=balance)
        else:
            await ctx.send("You don't have any XP. Please try again.")

    @commands.Cog.listener()
    async def on_message(self, message):
        async def add_experience(users, user, exp, server):
            users[str(message.guild.id)][str(user.id)]["xp"] += exp

        async def level_up(users, user, server):
            xp = users[str(message.guild.id)][str(user.id)]["xp"]
            level = users[str(message.guild.id)][str(user.id)]["level"]

            if xp > 1000:
                levelUp = level + 1
                users[str(message.guild.id)][str(message.author.id)] = {"level" : levelUp, "xp" : 0}
                SaveLevel()
                channel = self.bot.get_channel(message.channel.id)
                await channel.send(f":tada: Congrats {user.mention}, you leveled up to level **{level + 1}**!")

        if message.author.bot:
            return
        else:
            if not str(message.guild.id) in users:
                users[str(message.guild.id)] = {}

            if not str(message.author.id) in users[str(message.guild.id)]:
                users[str(message.guild.id)][str(message.author.id)] = {"level" : 0, "xp" : 0}

            randomEXP = random.randint(1, 10)
            await add_experience(users, message.author, randomEXP, message.guild)
            await level_up(users, message.author, message.guild)

        SaveLevel()

def setup(bot):
    bot.add_cog(Levelup(bot))
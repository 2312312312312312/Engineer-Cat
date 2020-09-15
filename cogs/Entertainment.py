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

Creator = config['discord']['creator']
Co_Creator = config['discord']['co-creator']
EmbedColor = 0x4d004d
bot = commands.Bot(command_prefix=config['discord']['prefix'], case_insensitive=True, help_command=None)
print("[+] Setting up reddit application.")
reddit = praw.Reddit(client_id=config['reddit']['client_id'], client_secret=config['reddit']['client_secret'], user_agent=config['reddit']['user_agent'])
print("[+] Successfully setup the reddit application.")

class Entertainment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def meme(self, ctx):
        memes_submissions = reddit.subreddit(config['subreddits']['memes']).hot()
        post_to_pick = random.randint(1, 60)
        for i in range(0, post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)

        Meme = discord.Embed(title="Heres a meme.", color=EmbedColor)
        Meme.set_image(url=submission.url)

        await ctx.send(embed=Meme)
        
    @commands.command()
    async def cursedminecraft(self, ctx):
        cursedminecraft_submissions = reddit.subreddit(config['subreddits']['cursedminecraft']).hot()
        post_to_pick = random.randint(1, 60)
        for i in range(0, post_to_pick):
            submission = next(x for x in cursedminecraft_submissions if not x.stickied)

        cursedminecraft = discord.Embed(title="Heres a very cursed minecraft picture.", color=EmbedColor)
        cursedminecraft.set_image(url=submission.url)

        await ctx.send(embed=cursedminecraft)

    @commands.command()
    async def discordmeme(self, ctx):
        discordmemes_submissions = reddit.subreddit(config['subreddits']['discordmemes']).hot()
        post_to_pick = random.randint(1, 60)
        for i in range(0, post_to_pick):
            submission = next(x for x in discordmemes_submissions if not x.stickied)

        DiscordMeme = discord.Embed(title="Heres a discord meme.", color=EmbedColor)
        DiscordMeme.set_image(url=submission.url)

        await ctx.send(embed=DiscordMeme)

    @commands.command()
    async def dog(self, ctx):
        dog_submissions = reddit.subreddit(config['subreddits']['dogs']).hot()
        post_to_pick = random.randint(1, 60)
        for i in range(0, post_to_pick):
            submission = next(x for x in dog_submissions if not x.stickied)

        Dog = discord.Embed(title="Heres a picture of a dog.", color=EmbedColor)
        Dog.set_image(url=submission.url)

        await ctx.send(embed=Dog)

    @commands.command()
    async def cat(self, ctx):
        cat_submissions = reddit.subreddit(config['subreddits']['cats']).hot()
        post_to_pick = random.randint(1, 60)
        for i in range(0, post_to_pick):
            submission = next(x for x in cat_submissions if not x.stickied)

        Cat = discord.Embed(title="Heres a picture of a cat.", color=EmbedColor)
        Cat.set_image(url=submission.url)

        await ctx.send(embed=Cat)

    @commands.command()
    async def avatar(self, ctx, user: discord.Member):
        Avatar = discord.Embed(title=f"{user.name}'s avatar.\n", color=EmbedColor)
        Avatar.set_image(url=user.avatar_url)
        await ctx.send(embed=Avatar)

    @commands.command()
    async def ping(self, ctx):
        print(f"[+] The bot's ping is {self.bot.latency * 1000}ms.")
        await ctx.send(f"Pong! {self.bot.latency * 1000}ms.")

    @commands.command()
    async def pong(self, ctx):
        print(f"[+] The bot's ping is {self.bot.latency * 1000}ms.")
        await ctx.send(f"Ping! {self.bot.latency * 1000}ms.")

def setup(bot):
    bot.add_cog(Entertainment(bot))
import discord
import ip2geotools
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions, CommandNotFound, BucketType, cooldown, CommandOnCooldown
from ip2geotools.databases.noncommercial import DbIpCity
from discord import Webhook, RequestsWebhookAdapter
from discord.utils import get
import youtube_dl
import logging
import random
import string
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
webhook = Webhook.partial(config['webhooks']['bugReportWebhook']['webhook_id'], config['webhooks']['bugReportWebhook']['webhook_token'],\
 adapter=RequestsWebhookAdapter())

class MainCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        try:
            user = ctx.message.author
            DM = await user.create_dm()
            embed = discord.Embed(title="Commands", description="Heres a list of commands.", color=EmbedColor)
            embed.add_field(name="📋 | Uncategorized", value="Help | +help | Shows a list of all commands.\nBugReport | +bugreport <bug report here> | Reports a bug.\nInfo | +info | Shows some information about the bot and the bot creator.")
            embed.add_field(name="🛠 | Moderation", value="Ban | +ban @user | Bans the specified user.\nUnban | +unban example#0000 | Unbans the specified user.\nKick | +kick @user | Kicks the specified user.\nMute | +mute @user | Mutes the specified user.\nUnmute | +unmute @user | Unmutes the specified user.\nPurge | +purge <number> | Purges the specified amount of messages in a text channel.", inline=False)
            embed.add_field(name="🔧 | Configuration", value="Welcomer | +welcomer #channel | Sets a channel to welcome new users.\nAutorole | +autorole @role | Automatically gives a role to a new member.\nModlog | +modlog #channel | Sets a channel to log all moderation activites.\nDisableWelcomer | +disableWelcomer | Disables the welcomer.\nDisableAutorole | +disableAutorole | Disables the autorole.\nDisableModlog | +disableModlog | Disables the modlog.", inline=False)
            embed.add_field(name="💎 | Economy", value="Register | +register | Registers your account so you can use the economy commands.\nBalance | +balance | Shows your balance.\nWork | +work | You work and then get paid.\nJobs | +jobs | Shows a list of jobs.\nGetJob | +getjob <jobname> | Gives you a job.\nGive | +give <amount> @user | Gives the specified amount of money to the specified user.\nRob | +rob @user | Steals a random amount of coins from a user.", inline=False)
            embed.add_field(name="🎶 | Music", value="Play | +play <song name> | Plays a song.\nJoin | +join | Joins the voice channel.\nLeave | +leave | Leaves the bot from the voice channel.\nVolume | +volume <number> | Changes the song volume.\nPause | +pause | Pauses the song.\nResume | +resume | Resumes the song.\nStop | +stop | Stops the song.\nSkip | +skip | Skips the song.\nLoop | +loop | Makes the song go in a loop.\nNow | +now | Shows the current song playing.\nQueue | +queue | Shows the song queue.\nRemove | +remove | Removes a song from the queue at a given index.\nShuffle | +shuffle | Shuffles the queue.", inline=False)
            embed.add_field(name="🍿 | Entertainment", value="Meme | +meme | Shows a meme.\nCursedMinecraft | +cursedminecraft | Shows a very cursed minecraft picture.\nDiscordMeme | +discordmeme | Shows a discord meme.\nDogs | +dog | Shows a picture of a dog.\nCats | +cat | Shows a picture of a cat.\nAvatar | +avatar @user | Shows the specified user's avatar.\nPing | +ping | Shows the bot's ping.\nPong | +pong | Shows the bot's ping.\nRank | +rank | Shows your level and XP in a server.", inline=False)
            embed.set_footer(text="Bot created by Infinityy#2250", icon_url="https://media-minecraftforum.cursecdn.com/avatars/93/716/635357200697011243.gif")
            await DM.send(embed=embed)
        except Exception as e:
            await ctx.send("I couldn't DM you.")
            print(e)

    @commands.command()
    @cooldown(1, 60, BucketType.user)
    async def bugreport(self, ctx, *args):
        Bug = ' '.join(args)
        BugReport = discord.Embed(title=f"New bug report from the user {ctx.message.author} - {ctx.message.author.id}!", description=Bug, color=EmbedColor)
        webhook.send(embed=BugReport)
        await ctx.send("Thanks for submitting a bug report!")

    @commands.command()
    async def info(self, ctx):
        Info = discord.Embed(title="Information", description=f"EngineerCat is a bot made by Infinityy, its in {len(self.bot.guilds)} servers, it has moderation commands and a modlog, it also has a level up system, its own economy, it can play music and it can show memes, cursed minecraft pictures, discord memes, dogs and cats and much more! If you want a full list of the commands just type +help.", color=EmbedColor)
        Info.add_field(name="Credits", value="Infinityy : Bot Creator\nNot_H3 : Bot Contributor", inline=False)
        Info.add_field(name="Donate", value="You can donate to this bitcoin wallet to support EngineerCat : bc1qn0z2y77zwqzt3xdmm532728hvm4eg09cyxw7ee", inline=False)
        Info.add_field(name="Links", value="[Infinityy's Github](https://github.com/NotInfinity)\n[Infinityy's Soundcloud](https://soundcloud.com/notinfinityy)\n[Offical discord server](https://discord.gg/wVaV5KT)\n[Bot invite](https://discordapp.com/api/oauth2/authorize?client_id=723530583115956366&permissions=8&scope=bot)\n[Source code](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline=False)
        Info.set_footer(text="Bot created by Infinityy#2250", icon_url="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/d44e8e4c-db34-4361-8508-e7288d4cc10f/d5du037-03efa70a-b8b4-45b7-be7f-68719da19a32.gif?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwic3ViIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsImF1ZCI6WyJ1cm46c2VydmljZTpmaWxlLmRvd25sb2FkIl0sIm9iaiI6W1t7InBhdGgiOiIvZi9kNDRlOGU0Yy1kYjM0LTQzNjEtODUwOC1lNzI4OGQ0Y2MxMGYvZDVkdTAzNy0wM2VmYTcwYS1iOGI0LTQ1YjctYmU3Zi02ODcxOWRhMTlhMzIuZ2lmIn1dXX0.Joj4Y-QXjk27WJ4GT_eXjQ1UOTkuxEWKGzvsNlsd_vY")
        await ctx.send(embed=Info)

def setup(bot):
    bot.add_cog(MainCommands(bot))
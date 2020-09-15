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

with open('economy.json') as file:
    amounts = json.load(file)

with open('jobs.json') as file:
    job = json.load(file)

def saveData():
    with open('economy.json', 'w') as file:
        json.dump(amounts, file)

    with open('jobs.json', 'w') as file:
        json.dump(job, file)

def Backup():
    with open('backup.json', 'w') as file:
        json.dump(amounts, file)

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def jobs(self, ctx):
        joblist = discord.Embed(title="Jobs", description="1. Plumber\n2. Cashier\n3. Fisher\n4. Janitor\n5. Youtuber", color=EmbedColor)
        await ctx.send(embed=joblist)

    @commands.command()
    async def getjob(self, ctx, jobname):
        try:
            id = str(ctx.message.author.id)
            if id in amounts:
                if jobname == "plumber":
                    job[id] = "Plumber"
                    await ctx.send("You are a plumber now.")
                elif jobname == "cashier":
                    job[id] = "Cashier"
                    await ctx.send("You are a cashier now.")
                elif jobname == "fisher":
                    job[id] = "Fisher"
                    await ctx.send("You are a fisher now.")
                elif jobname == "janitor":
                    job[id] = "Janitor"
                    await ctx.send("You are a janitor now.")
                elif jobname == "youtuber":
                    job[id] = "Youtuber"
                    await ctx.send("You are a youtuber now.")
                else:
                    await ctx.send("Thats not a job. Remember its case sensitive.")
            else:
                await ctx.send("You do not have an account")
            saveData()
        except Exception as e:
            print(e)

    @commands.command(pass_context=True)
    async def balance(self, ctx):
        id = str(ctx.message.author.id)
        if id in amounts:
            if id in job:
                balance = discord.Embed(title=f"{ctx.message.author}'s balance", description=f"**Wallet : `{amounts[id]}`**\n**Job : `{job[id]}`**", color=EmbedColor)
                await ctx.send(embed=balance)
            elif id not in job:
                job[id] = "None"
                balance = discord.Embed(title=f"{ctx.message.author}'s balance", description=f"**Wallet : `{amounts[id]}`**\n**Job : `{job[id]}`**", color=EmbedColor)
                await ctx.send(embed=balance)

            saveData()
        else:
            await ctx.send("You do not have an account")

    @commands.command(pass_context=True)
    async def register(self, ctx):
        id = str(ctx.message.author.id)
        if id not in amounts:
            amounts[id] = 100
            await ctx.send("You are now registered.")
            saveData()
            Backup()
            print(f"[+] Registered {ctx.message.author} - {ctx.message.author.id}")
        else:
            print("[+] The register command was executed but the user was already registed.")
            await ctx.send("You already have an account.")

    @commands.command(pass_context=True)
    async def give(self, ctx, amount: int, other: discord.Member):
        primary_id = str(ctx.message.author.id)
        other_id = str(other.id)
        if primary_id not in amounts:
            await ctx.send("You do not have an account.")
        elif other_id not in amounts:
            await ctx.send("The other party does not have an account.")
        elif amounts[primary_id] < amount:
            await ctx.send("You cannot afford this transaction.")
        else:
            amounts[primary_id] -= amount
            amounts[other_id] += amount
            await ctx.send("Transaction complete.")
        saveData()
        Backup()

    @commands.command(pass_context=True)
    @cooldown(1, 10, BucketType.user)
    async def work(self, ctx):            
        id = str(ctx.message.author.id)
        if id in amounts:
            if id in job:
                if job[id] == "Plumber":
                    randomCoins = random.randint(200, 10000)
                    amounts[id] += randomCoins
                    await ctx.send("You unclogged a toilet and you got " + str(randomCoins) + " coins!")
                    saveData()
                    Backup()
                elif job[id] == "Cashier":
                    randomCoins = random.randint(200, 10000)
                    amounts[id] += randomCoins
                    await ctx.send("You got paid " + str(randomCoins) + " coins!")
                    saveData()
                    Backup()
                elif job[id] == "Fisher":
                    randomCoins = random.randint(200, 10000)
                    amounts[id] += randomCoins
                    await ctx.send("You caught a fish and you got " + str(randomCoins) + " coins!")
                    saveData()
                    Backup()
                elif job[id] == "Janitor":
                    randomCoins = random.randint(200, 10000)
                    amounts[id] += randomCoins
                    await ctx.send("You sweeped the floors and you got " + str(randomCoins) + " coins!")
                    saveData()
                    Backup()
                elif job[id] == "Youtuber":
                    randomCoins = random.randint(200, 10000)
                    amounts[id] += randomCoins
                    await ctx.send("You uploaded a youtube video and you got " + str(randomCoins) + " coins!")
                    saveData()
                    Backup()
                elif job[id] == "None":
                    await ctx.send("You don't have a job. Do +jobs to get a list of jobs. And +getjob to get one of the jobs.")
            elif id not in job:
                job[id] = "None"
                await ctx.send("You don't have a job. Do +jobs to get a list of jobs. And +getjob to get one of the jobs.")
        else:
            await ctx.send("You do not have a account.")

    @commands.command(pass_context=True)
    @cooldown(1, 10, BucketType.user)
    async def rob(self, ctx, other: discord.Member):
        primary_id = str(ctx.message.author.id)
        other_id = str(other.id)
        if primary_id not in amounts:
            await ctx.send("You do not have an account.")
        elif other_id not in amounts:
            await ctx.send("The other party does not have an account.")
        else:
            stealAmount = random.randint(20, 500)
            Caught = random.randint(1, 2)
            if Caught == 1:
                print("[+] User was caught stealing.")
                amounts[primary_id] -= 250
                amounts[other_id] += 250
                await ctx.send(f"You were caught stealing now you paid {other.mention} 250 coins.")
            elif Caught == 2:
                amounts[primary_id] += stealAmount
                amounts[other_id] -= stealAmount
                await ctx.send(f"You stole {stealAmount} coins from {other.mention}.")
        saveData()
        Backup()

    @commands.command()
    async def save(self, ctx):
        saveData()
        Backup()

def setup(bot):
    bot.add_cog(Economy(bot))
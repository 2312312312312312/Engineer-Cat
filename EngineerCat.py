# Libraries
import discord
from discord.ext import commands
import json
import sys
import os

# Welcome message
class Welcome:
    os.system("clear")
    print("  ______             _                         _____      _   ")
    print(" |  ____|           (_)                       / ____|    | |  ")
    print(" | |__   _ __   __ _ _ _ __   ___  ___ _ __  | |     __ _| |_ ")
    print(" |  __| | '_ \ / _` | | '_ \ / _ \/ _ \ '__| | |    / _` | __|")
    print(" | |____| | | | (_| | | | | |  __/  __/ |    | |___| (_| | |_ ")
    print(" |______|_| |_|\__, |_|_| |_|\___|\___|_|     \_____\__,_|\__|")
    print("                __/ |                                         ")
    print("               |___/                                          ")
    print("")
    print("=====================================================")
    print("")
    print("[+] The discord.py version is " + str(discord.__version__) + ".") 

# Configuration
sys.stdout.write("\x1b]2;Engineer Cat\x07")
with open("config.json", "r") as file:
    config = json.load(file)

bot = commands.Bot(command_prefix=config['discord']['prefix'], case_insensitive=True, help_command=None)

# Bot Loader
Welcome()
bot.load_extension('cogs.Uncategorized')
print("[+] Loaded the Main Commands.")
bot.load_extension('cogs.Moderation')
print("[+] Loaded the Moderation commands.")
bot.load_extension('cogs.Economy')
print("[+] Loaded the Economy commands.")
bot.load_extension('cogs.Music')
print("[+] Loaded the Music commands.")
bot.load_extension('cogs.Entertainment')
print("[+] Loaded the Entertainment commands.")
bot.load_extension('cogs.Levelup')
print("[+] Loaded the level up system.")
bot.load_extension('cogs.Configuration')
print("[+] Loaded the guild configs.")
bot.load_extension('cogs.Events')
print("[+] Loaded the Events.")
bot.run(config['discord']['token'])
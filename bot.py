from discord.ext import commands
import discord
import os
from dotenv import load_dotenv
from commands.meal_commands import setup_meal_commands
from commands.search_commands import setup_search_commands

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

setup_meal_commands(bot)
setup_search_commands(bot)

bot.run(DISCORD_TOKEN)
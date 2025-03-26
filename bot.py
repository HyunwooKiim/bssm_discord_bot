from discord.ext import commands
import discord
import os
from dotenv import load_dotenv
from commands.meal_commands import setup_meal_commands
from commands.allergy_commands import setup_allergy_commands
from commands.hidden_commands import hidden_commands

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

setup_meal_commands(bot)
setup_allergy_commands(bot)
hidden_commands(bot)

bot.run(DISCORD_TOKEN)
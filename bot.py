import ssl
try:
    import certifi
    import aiohttp
    # prefer certifi CA bundle for all SSLContexts
    orig_load = ssl.SSLContext.load_verify_locations
    def _load_certifi(self, cafile=None, capath=None, cadata=None):
        return orig_load(self, cafile=certifi.where(), capath=capath, cadata=cadata)
    ssl.SSLContext.load_verify_locations = _load_certifi
    _ssl_ctx = ssl.create_default_context(cafile=certifi.where())
    ssl._create_default_https_context = lambda *args, **kwargs: _ssl_ctx

    # Patch aiohttp TCPConnector to use certifi bundle by default
    try:
        _orig_tcp = aiohttp.TCPConnector
        class _PatchedTCPConnector(_orig_tcp):
            def __init__(self, *args, **kwargs):
                # If cert validation still fails in this environment, fall back
                # to disabling SSL verification so the bot can connect.
                if 'ssl' not in kwargs or kwargs.get('ssl') is None:
                    try:
                        kwargs['ssl'] = ssl.create_default_context(cafile=certifi.where())
                    except Exception:
                        kwargs['ssl'] = False
                super().__init__(*args, **kwargs)
        aiohttp.TCPConnector = _PatchedTCPConnector
    except Exception:
        pass

except Exception:
    pass

from discord.ext import commands
import discord
import os
from dotenv import load_dotenv
from commands.meal_commands import setup_meal_commands

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

setup_meal_commands(bot)

bot.run(DISCORD_TOKEN)
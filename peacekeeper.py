import discord
from discord.ext import commands
from collections import defaultdict, deque
import random
import asyncio
import time
import aiohttp
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env
load_dotenv()

# CONFIG FROM ENV
MONITORED_USERS = set(map(int, os.getenv("MONITORED_USERS", "").split(",")))
MESSAGE_LIMIT = int(os.getenv("MESSAGE_LIMIT", 5))
TIME_WINDOW = int(os.getenv("TIME_WINDOW", 10))
SPAM_AMOUNT = int(os.getenv("SPAM_AMOUNT", 5))
MINIMUM_MESSAGE_PER_USER = int(os.getenv("MINIMUM_MESSAGE_PER_USER", 1))
MONITORED_CHANNEL_ID = int(os.getenv("MONITORED_CHANNEL_ID"))
TENOR_API_KEY = os.getenv("TENOR_API_KEY")
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

shared_message_log = deque(maxlen=MESSAGE_LIMIT)

user_last_messages = defaultdict(list)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id != MONITORED_CHANNEL_ID:
        return  # Only monitor the specified channel

    if message.author.id in MONITORED_USERS:
        now = time.time()
        user_log = user_message_log[message.author.id]
        user_log.append(now)

        total_messages = sum(len(user_message_log[uid]) for uid in MONITORED_USERS)
        if (
            total_messages >= MESSAGE_LIMIT
            and all(len(user_message_log[uid]) >= MINIMUM_MESSAGE_PER_USER for uid in MONITORED_USERS)
        ):
            await message.channel.send("Peacekeeper activated 🕊️")
            await spam_channel_with_tenor_gifs(message.channel)
            for uid in MONITORED_USERS:
                user_message_log[uid].clear()

    await bot.process_commands(message)


async def spam_channel_with_tenor_gifs(channel):
    async with aiohttp.ClientSession() as session:
        for _ in range(SPAM_AMOUNT):
            gif_url = await get_tenor_gif(session, "cute animals")
            if gif_url:
                await channel.send(gif_url)
            await asyncio.sleep(1)

async def get_tenor_gif(session, search_term):
    try:
        url = "https://tenor.googleapis.com/v2/search"
        params = {
            "q": search_term,
            "key": TENOR_API_KEY,
            "limit": 10,
            "media_filter": "minimal",
        }

        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                results = data.get("results", [])
                if results:
                    gif = random.choice(results)
                    return gif["media_formats"]["gif"]["url"]
    except Exception as e:
        print(f"Failed to fetch from Tenor: {e}")
    return None

# Start bot
bot.run(DISCORD_BOT_TOKEN)
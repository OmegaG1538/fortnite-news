import discord
import requests
import asyncio

import os

TOKEN = os.environ["TOKEN"]

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

last_news = None
CHANNEL_NAME = "fortnite-news"

def get_news():
    try:
        r = requests.get("https://fortniteapi.io/v2/news", headers={"Authorization": "demo"}).json()
        return r["news"]["motds"][0]["title"]
    except:
        return None

async def loop_news():
    await client.wait_until_ready()
    global last_news

    while True:
        news = get_news()
        if news and news != last_news:
            for guild in client.guilds:
                for channel in guild.text_channels:
                    if channel.name == CHANNEL_NAME:
                        await channel.send(f"🔥 Fortnite Update:\n{news}")
                        last_news = news
        await asyncio.sleep(300)

@client.event
async def on_ready():
    print("Bot is online")

client.loop.create_task(loop_news())
client.run(TOKEN)

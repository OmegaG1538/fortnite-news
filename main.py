import os
import discord
import requests
import asyncio
from flask import Flask
from threading import Thread

# ===== Flask server to keep Railway alive =====
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

t = Thread(target=run)
t.start()
# ========================================================

# ===== Discord Bot Setup =====
TOKEN = os.environ["TOKEN"]  # your token from Railway variables
intents = discord.Intents.default()
intents.message_content = True  # required for reading messages (optional)

client = discord.Client(intents=intents)

# ===== Channel to post updates =====
# Replace with your channel ID (right-click channel → Copy ID)
CHANNEL_ID = 123456789012345678

# ===== Keep track of last news =====
last_news = None

# ===== Get Fortnite news safely =====
def get_news():
    try:
        r = requests.get(
            "https://fortniteapi.io/v2/news",
            headers={"Authorization": "demo"},  # replace with your Fortnite API key if you have one
            timeout=10
        )
        r.raise_for_status()
        data = r.json()
        return data["news"]["motds"][0]["title"]
    except Exception as e:
        print("Error fetching news:", e)
        return None

# ===== Loop to post news every 5 minutes =====
async def loop_news():
    await client.wait_until_ready()
    global last_news

    while True:
        news = get_news()
        if news and news != last_news:
            channel = client.get_channel(CHANNEL_ID)
            if channel:
                try:
                    await channel.send(f"🔥 Fortnite Update:\n{news}")
                    last_news = news
                except Exception as e:
                    print("Error sending message:", e)
        await asyncio.sleep(300)  # 5 minutes

# ===== Bot Ready Event =====
@client.event
async def on_ready():
    print(f"Bot online as {client.user}")
    # Optional: Send test message when bot starts
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        try:
            await channel.send("✅ Fortnite News Bot is online!")
        except:
            pass

# ===== Start the news loop =====
client.loop.create_task(loop_news())
client.run(TOKEN)

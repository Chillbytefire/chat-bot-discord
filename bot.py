import os
import discord
import logging
import random
from flask import Flask
from threading import Thread


TOKEN = os.environ["DISCORD_TOKEN"]

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive"

def run():
    app.run(host="0.0.0.0", port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.event
async def on_message(message):

    if message.author.bot:
        return

    words = message.content.lower().split()

    if not words:
        return
    
    if "67" in words:
        await message.reply("kys")
        return

    is_mention = bot.user in message.mentions
    is_chat = words and words[0] == "chat"

    if not is_mention and not is_chat:
        return

    query = message.content.lower()

    query = query.replace(f"<@{bot.user.id}>", "")
    query = query.replace(f"<@!{bot.user.id}>", "")

    if query.startswith("chat "):
        query = query[5:]

    query = query.strip()

    if query.startswith("is this real"):
        
        responses = [
            "Real.",
            "Not real."
        ]

        await message.reply(random.choice(responses))
        return
    
    if query.startswith("rate"):
        await message.reply(f"{random.randint(0,10)}/10")
        return

    if query.startswith("who will win"):
        matchup = query[len("who will win "):]
    
        choices = [c.strip() for c in matchup.split(" or ") if c.strip()]

        if len(choices) < 2:
            await message.reply("nigga learn how to use de fukin bot")
            return

        await message.reply(random.choice(choices))
        return
    
    if query.startswith("am i cooked"):
        responses = [
            "absolutely cooked",
            "medium rare",
            "slightly toasted",
            "nah bro",
            "rip bro",
            "ggs",
            "hell naw",
            "yo future more cooked than yo present, and thats sayin something"
        ]

        await message.reply(random.choice(responses))
        return

    await message.reply("you called?")

keep_alive()
bot.run(TOKEN, reconnect=True)

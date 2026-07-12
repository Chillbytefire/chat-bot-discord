import os
import discord
import logging
import random
import time
import hashlib
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

# DR WHOOOOOOOOOOOOOOO

DR_WHO_CHANCE = 0.037

dr_who_cooldowns = {}

DR_WHO_LINES = [
    "IS THAT A DOCTOR WHO REFERENCE??",
    "HOLY SHIT DOCTOR WHO",
    "EVERYTHING IS A DOCTOR WHO REFERENCE",
    "THE DOCTOR MENTIONED 🗣️🗣️",
    "WIBBLY WOBBLY TIMEY WIMEY",
]

DR_WHO_GIFS = [
    "https://tenor.com/view/dr-who-doctor-who-matt-smith-points-pointing-gif-4446574",
    "https://tenor.com/view/call-me-doctor-who-matt-smith-gif-3564073",
    "https://klipy.com/gifs/doctor-who-clara-oswald-22",
    "https://tenor.com/view/matt-smith-doctor-who-regret-i-regret-nothing-idc-gif-5485932",
    "https://tenor.com/view/thumbs-up-eleventh-doctor-doctor-who-matt-smith-smile-gif-17095333",
    "https://tenor.com/view/david-tennant-brilliant-happy-doctor-who-gif-3411551",
    "https://tenor.com/view/allonsy-doctor-who-10th-gif-5990793",
    "https://tenor.com/view/doctor-who-dr-who-matt-smith-throne-shrug-gif-5136242",
    "https://tenor.com/view/doctor-who-clara-gif-21352468",
    "https://tenor.com/view/doctor-who-the-doctor-doctor-12th-doctor-12-gif-10085395425960539705",
]

#PSEUDO random

WEEK_SECONDS = 7 * 24 * 60 * 60

def get_rng(key: str):
    week = int(time.time() // WEEK_SECONDS)
    seed = f"{week}:{key.lower()}"
    h = hashlib.sha256(seed.encode()).digest()
    return random.Random(h)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.event
async def on_message(message):

    if message.author.bot:
        return

    if message.guild is None:
        return

    guild_id = message.guild.id
    now = time.time()

    cooldown = dr_who_cooldowns.get(guild_id, 0)

    if now >= cooldown and random.random() < DR_WHO_CHANCE:
        await message.reply(random.choice(DR_WHO_LINES), mention_author=False)
        await message.channel.send(random.choice(DR_WHO_GIFS))

        dr_who_cooldowns[guild_id] = now + random.randint(30, 60)

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
        key = "real:" + " ".join(message.content.split()).lower()
        rng = get_rng(key)
        responses = [
            "Real.",
            "Not real."
        ]

        await message.reply(rng.choice(responses))
        return

    if query == "chat":
        await message.reply("you called?")
        return
    
    if query.startswith("rate"):
        thing = " ".join(query[4:].split()).lower()

        if not thing:
            await message.reply("rate what bro")
            return

        rng = get_rng("rate:" + thing)
        await message.reply(f"{rng.randint(0,10)}/10")
        return

    if query.startswith("who will win") or query.startswith("who would win"):
       
        if query.startswith("who will win "):
            matchup = query[len("who will win "):]
        elif query.startswith("who would win "):
            matchup = query[len("who would win "):]
        else:
            await message.reply("nigga learn how to use de fukin bot")
            return

        choices = [c.strip() for c in matchup.split(" or ") if c.strip()]
       
        if len(choices) < 2:
            await message.reply("nigga learn how to use de fukin bot")
            return

        canonical = sorted(choices, key=str.lower)
        
        key = "who:" + " or ".join(c.lower() for c in canonical)
        rng = get_rng(key)

        await message.reply(rng.choice(canonical))
        return
    
    if query.startswith("am i cooked"):
        key = "cooked:" + " ".join(query.split()).lower()
        rng = get_rng(key)
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

        await message.reply(rng.choice(responses))
        return

    if query.startswith("no embed perms"):

        if not message.reference:
            await message.reply("reply to a message first bro")
            return

        try:
            replied = await message.channel.fetch_message(
                message.reference.message_id
            )

            if not replied.content  and not replied.attachments:
                await message.reply("that message got no text")
                return

            files = [
                await attachment.to_file()
                for attachment in replied.attachments
            ]

            await message.channel.send(
                replied.content,
                files=files
            )

        except Exception as e:
            print(e)
            await message.reply("something exploded :thumbsup:")

        return        

   

keep_alive()
bot.run(TOKEN, reconnect=True)

"""
Written by Ned
Edition: v30 (min) 11/11/2024
"""

import discord
from discord import Game, Status
from discord.ext import commands, tasks
from discord import Embed
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
from discord.ext.commands import CommandNotFound
from discord.ext.commands import DefaultHelpCommand

from collections import defaultdict
from datetime import datetime, timezone, timedelta
import time
from PIL import Image
from aiohttp import ClientConnectorError
from threading import RLock, Lock
from io import BytesIO
from collections import defaultdict
import traceback
import concurrent.futures
import re
import asyncio
import sqlite3
import shutil
import os
import threading
import tracemalloc
import subprocess
import aiohttp
import requests
import queue
import io
import json
import random
import feedparser
import gc
import pandas as pd
import time
import pytz

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.guilds = True
intents.members = True
intents.guild_messages = True
intents.reactions = True

admin_id = 775445008672489525
STATIC_GUILD_ID = 907301373387898950
DESIGNATED_CHANNEL_ID = 1234

bot = commands.AutoShardedBot(command_prefix='/', intents=intents)
slash = SlashCommand(bot, sync_commands=True)
schedule = 'No Scheduled Outages'

ether_ai_1 = '✅ Online'
ether_ai_model_1 = '[Nemo](https://huggingface.co/lmstudio-community/Mistral-Nemo-Instruct-2407-GGUF)'
ether_ai_model_call_1 = "lmstudio-community/Mistral-Nemo-Instruct-2407-GGUF/Mistral-Nemo-Instruct-2407-Q4_K_M.gguf"

ether_ai_2 = '✅ Online'
ether_ai_model_2 = '[Y-Coder](https://huggingface.co/lmstudio-community/Yi-Coder-9B-Chat-GGUF)'
ether_ai_model_call_2 = "lmstudio-community/Yi-Coder-9B-Chat-GGUF/Yi-Coder-9B-Chat-Q8_0.gguf"

ether_ai_3 = '✅ Online'
ether_ai_model_3 = '[Mathstral](https://huggingface.co/lmstudio-community/mathstral-7B-v0.1-GGUF)'
ether_ai_model_call_3 = "lmstudio-community/mathstral-7B-v0.1-GGUF/mathstral-7B-v0.1-Q8_0.gguf"

ether_lock = Lock()
user_prefs_lock = asyncio.Lock()
message_counts_lock = asyncio.Lock()

user_persona_prefs = defaultdict(lambda: {
    "model": ether_ai_model_call_1,
    "temperature": 0.8,
    "tokens": 2000,
    "contextLength": 200,
    "prompt": {
        "role": "system",
        "content": "Respond as Ether the bluemoon goddess and do not quote your response."
    }
})

ether_temperature = 0.8
ether_tokens = 2000
ether_contextLength = 200
ether_api_base = "http://localhost:1238/v1/chat/completions"
ether_user_message_counts = defaultdict(lambda: [0, 0])

ether_prompt = {
    "role": "system",
    "content": "Respond as Ether the bluemoon goddess."
}

bugs = 'No Known Active Errors'
uptime = ''
homeserv = "https://discord.gg/z3S7CUB3QS"
bot_login_time = None
presence_flag = True

blacklist_lock = RLock()
terms_dict_lock = RLock()
terms_lock = threading.Lock()
ban_lock = threading.Lock()
blacklist_db = "ether_blacklist.db"
notifications_db = "notifications.db"
appeals_db = "appeals.db"
blacklist_dict = {"user_ids": [], "guild_ids": [], "reason": []}
circumventions = {"user_ids": [], "files": []}
appeals = {}
terms_db = "terms.db"
terms_dict = {"user_ids": []}
member_ids = []
cancel_queue = []

def create_terms_table():
    conn = sqlite3.connect(terms_db)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS terms (id INTEGER PRIMARY KEY, user_id TEXT)")
    conn.commit()
    conn.close()
def load_terms():
    global terms_dict
    conn = sqlite3.connect(terms_db)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM terms")
    records = cursor.fetchall()
    terms_dict["user_ids"] = [str(record[0]) for record in records]
    conn.close()
def create_blacklist_table():
    conn = sqlite3.connect(blacklist_db)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS ether_blacklist (id INTEGER PRIMARY KEY, user_id TEXT, guild_id TEXT, reason TEXT)")
    conn.commit()
    conn.close()
def load_blacklist():
    conn = sqlite3.connect(blacklist_db)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, guild_id, reason FROM ether_blacklist")
    records = cursor.fetchall()
    blacklist_dict["user_ids"] = []
    blacklist_dict["guild_ids"] = []
    blacklist_dict["reason"] = []
    for record in records:
        user_id, guild_id, reason = record
        if user_id != "":
            blacklist_dict["user_ids"].append(user_id)
        if guild_id != "":
            blacklist_dict["guild_ids"].append(guild_id)
        if reason != "":
            blacklist_dict["reason"].append(reason)
    conn.close()
def create_appeals_table():
    conn = sqlite3.connect(appeals_db)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS appeals (id INTEGER PRIMARY KEY, user_id TEXT)")
    conn.commit()
    conn.close()
def load_appeals():
    conn = sqlite3.connect(appeals_db)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM appeals")
    records = cursor.fetchall()
    appeals["user_ids"] = [str(record[0]) for record in records]
    conn.close()

@bot.event
async def on_ready():
    global retry_attempts, bot_login_time, member_ids, bot
    create_terms_table()
    load_terms()
    create_blacklist_table()
    load_blacklist()
    create_appeals_table()
    load_appeals()
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('Bot connected to the server')
    retry_attempts = 0
    bot_login_time = datetime.now()

    static_guild = bot.get_guild(STATIC_GUILD_ID)
    if static_guild is not None:
        async for member in static_guild.fetch_members(limit=None):
            member_ids.append(member.id)

    if not update_ether_status.is_running():
        update_ether_status.start()

@tasks.loop(hours=24)
async def update_ether_status():
    server_count = len(bot.guilds)
    status_message = f"Goddess in {server_count} servers"
    await bot.change_presence(activity=discord.Game(name=status_message), status=discord.Status.online)

@bot.event
async def on_guild_join(guild):
    if str(guild.id) in blacklist_dict["guild_ids"]:
        await guild.leave()
    else:
        static_guild = bot.get_guild(STATIC_GUILD_ID)
        if static_guild is None:
            print("Static guild not found.")
            return
        channel = static_guild.get_channel(DESIGNATED_CHANNEL_ID)
        if channel is None:
            print("Designated channel not found.")
            return
        server_count = len(bot.guilds)
        embed = discord.Embed(
            title="🎉  Ether Joined New Server",
            description=f"The bot has joined a new server: {guild.name}.\n\n"
                        f"Current Server Count: {server_count}",
            color=discord.Color.green()
        )
        await channel.send(embed=embed)

@slash.slash(name="terms",
    description="View or agree to Ether's terms",
    options=[
        create_option(
            name="options",
            description="View, Agree, or Revoke",
            option_type=3,
            required=False,
            choices=[
                create_choice(
                    name="view",
                    value="view"
                ),
                create_choice(
                    name="agree",
                    value="agree"
                ),
                create_choice(
                    name="revoke",
                    value="revoke"
                ),
            ]
        ),
    ])
async def terms(ctx, options=None):
    global user_sessions, schedule, bot_login_time, bugs, homeserv

    author_id = ctx.author.id
    channel_id = ctx.channel.id
    is_blacklisted = False

    with blacklist_lock:
        for blacklisted_user_id in blacklist_dict["user_ids"]:
            if int(blacklisted_user_id) == author_id:
                is_blacklisted = True
                break

    if is_blacklisted:
        return

    if options is not None:
        if options == "view":
            async def display_terms():
                try:
                    with terms_lock:
                        embed = Embed(title="📃  Terms", description=f"To use Ether you agree that Ether will relay your API key to OpenAI. You also agree that any files you embed will undergo transformations. In using Ether, you are subject to OpenAI's terms of service.\n\nEther is an amnesiac relay system. See more at [terms](https://ether-2.gitbook.io/ether/terms-faq-help/ether-terms-and-privacy) or join support [server]({homeserv}).\n\nUse `/terms agree` to agree or `/terms revoke` to remove your entry.", color=0x00FF00)
                        await ctx.send(embed=embed, hidden=True)
                except Exception as e:
                    embed = Embed(title="Terms Error", description="", color=0x0000FF)
                    await ctx.send(embed=embed, hidden=True)
            asyncio.create_task(display_terms())
            return

        elif options == "agree":
            async def agree_terms():
                try:
                    with terms_lock:
                        if str(ctx.author.id) in terms_dict["user_ids"]:
                            embed = Embed(title="✅  Terms", description="*You have already agreed to the terms...*", color=0x00FF00)
                            await ctx.send(embed=embed, hidden=True)
                        else:
                            terms_dict["user_ids"].append(str(ctx.author.id))
                            conn = sqlite3.connect(terms_db)
                            cursor = conn.cursor()
                            cursor.execute("INSERT INTO terms (user_id) VALUES (?)", (str(ctx.author.id),))
                            conn.commit()
                            conn.close()
                            embed = Embed(title="✅  Terms", description="Successfully agreed to terms!", color=0x00FF00)
                            await ctx.send(embed=embed, hidden=True)
                except Exception as e:
                    embed = Embed(title="Terms Error", description="", color=0x0000FF)
                    await ctx.send(embed=embed, hidden=True)
            asyncio.create_task(agree_terms())
            return

        elif options == "revoke":
            async def revoke_terms():
                try:
                    with terms_lock:
                        if str(ctx.author.id) in terms_dict["user_ids"]:
                            terms_dict["user_ids"].remove(str(ctx.author.id))
                            conn = sqlite3.connect(terms_db)
                            cursor = conn.cursor()
                            cursor.execute("DELETE FROM terms WHERE user_id = ?", (str(ctx.author.id),))
                            conn.commit()
                            conn.close()
                            embed = Embed(title="✅  Terms", description="You have revoked your agreement to the terms.", color=0x00FF00)
                            await ctx.send(embed=embed, hidden=True)
                        else:
                            embed = Embed(title="✅  Terms", description="*You have not agreed to the terms...*", color=0x00FF00)
                            await ctx.send(embed=embed, hidden=True)
                except Exception as e:
                    embed = Embed(title="Terms Error", description="", color=0x0000FF)
                    await ctx.send(embed=embed, hidden=True)
            asyncio.create_task(revoke_terms())
            return
    else:
        async def display_terms():
            try:
                with terms_lock:
                    embed = Embed(title="📃  Terms", description=f"To use Ether you agree that Ether will relay your API key to OpenAI. You also agree that any files you embed will undergo transformations. In using Ether, you are subject to OpenAI's terms of service.\n\nEther is an amnesiac relay system. See more at [terms](https://ether-2.gitbook.io/ether/terms-faq-help/ether-terms-and-privacy) or join support [server]({homeserv}).\n\nUse `/terms agree` to agree or `/terms revoke` to remove your entry.", color=0x00FF00)
                    await ctx.send(embed=embed, hidden=True)
            except Exception as e:
                embed = Embed(title="Terms Error", description="", color=0x0000FF)
                await ctx.send(embed=embed, hidden=True)
        asyncio.create_task(display_terms())

@slash.slash(name="ether-status",
    description="View Ether or OpenAI status",
    )
async def etherstatus(ctx):
    async def get_status(ctx):

        try:
            serverCount = len(bot.guilds)

            current_time = datetime.now()
            uptime = current_time - bot_login_time

            days = uptime.days
            hours, remainder = divmod(uptime.seconds, 3600)
            minutes, _ = divmod(remainder, 60)

            current_datetime = datetime.now()
            embed = Embed(title="▶️  Ether Status", color=0x00FF00)
            embed.add_field(name="", value=current_datetime.strftime("\n%Y-%m-%d %H:%M:%S"), inline=False)
            embed.add_field(name="- Uptime", value=f" * {days} days, {hours} hours, {minutes} minutes", inline=False)
            embed.add_field(name="- Server Count", value=f" * Serving in {serverCount} servers!", inline=False)
            embed.add_field(name="- Schedule", value=f" * {schedule}", inline=False)
            embed.add_field(name="- Ether AI", value=f"- **Model 1:** {ether_ai_model_1} **Status:** {ether_ai_1}\n- **Model 2:** {ether_ai_model_2} **Status:** {ether_ai_2}\n- **Model 3:** {ether_ai_model_3} **Status:** {ether_ai_3}", inline=False)
            embed.add_field(name="", value=f"See [EtherCereal]({homeserv}) support, OpenAI [Status](https://status.openai.com/#), Ether [Knowlede Base](https://ether-2.gitbook.io/ether/)", inline=False)

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send("An unexpected error occurred. Please contact support.")
            print(f"Unexpected error: {e}")
    asyncio.create_task(get_status(ctx))
    return

@slash.slash(name="ether-ai",
    description="View or adjust Ether's built-in AI (applies per user)",
    options=[
        create_option(
            name="select_prompt",
            description="Select a prompt to use",
            option_type=3,
            required=False,
            choices=[
                create_choice(
                    name="none",
                    value="none"
                ),
                create_choice(
                    name="esoteric",
                    value="esoteric"
                ),
                create_choice(
                    name="philosopher",
                    value="philosopher"
                ),
                create_choice(
                    name="astrologer",
                    value="astrologer"
                ),
                create_choice(
                    name="programmer",
                    value="programmer"
                ),
                create_choice(
                    name="technical",
                    value="technical"
                ),
                create_choice(
                    name="divination",
                    value="divination"
                ),
                create_choice(
                    name="abstract",
                    value="abstract"
                ),
                create_choice(
                    name="wrong_answers",
                    value="wrong_answers"
                ),
                create_choice(
                    name="sass",
                    value="sass"
                ),
                create_choice(
                    name="troll",
                    value="troll"
                ),
            ]
        ),
        create_option(
            name="model",
            description="Set the model to use",
            option_type=3,
            required=False,
            choices=[
                create_choice(
                    name="Nemo",
                    value="Nemo"
                ),
                create_choice(
                    name="YCoder",
                    value="YCoder"
                ),
                create_choice(
                    name="Mathstral",
                    value="Mathstral"
                ),
            ]
        ),
        create_option(
            name="temperature",
            description="Control text randomness",
            option_type=3,
            required=False,
            choices=[
                create_choice(
                    name="0",
                    value="0"
                ),
                create_choice(
                    name="0.1",
                    value="0.1"
                ),
                create_choice(
                    name="0.3",
                    value="0.3"
                ),
                create_choice(
                    name="0.5",
                    value="0.5"
                ),
                create_choice(
                    name="0.7",
                    value="0.7"
                ),
                create_choice(
                    name="0.9",
                    value="0.9"
                ),
            ]
        ),
        create_option(
            name="tokens",
            description="Set token limit",
            option_type=3,
            required=False,
            choices=[
                create_choice(
                    name="50",
                    value="50"
                ),
                create_choice(
                    name="100",
                    value="100"
                ),
                create_choice(
                    name="256",
                    value="256"
                ),
                create_choice(
                    name="500",
                    value="500"
                ),
                create_choice(
                    name="1000",
                    value="1000"
                ),
                create_choice(
                    name="1500",
                    value="1500"
                ),
                create_choice(
                    name="2000",
                    value="2000"
                ),
                create_choice(
                    name="2500",
                    value="2500"
                ),
            ]
        ),
    ])
async def etherai(ctx, select_prompt=None, model=None, temperature=None, tokens=None):
    global user_prefs_lock, ether_ai_model_call_2, ether_ai_model_call_1, ether_ai_model_call_3, user_persona_prefs

    user_id = str(ctx.author.id)

    async def alter_ether(user_id):
        async with user_prefs_lock:
            try:

                user_prefs = user_persona_prefs[user_id]
                options = (select_prompt, model, temperature, tokens)
                if all(option is None for option in options):
                    async def get_ether_info():
                        current_model = user_prefs.get('model', 'Default Model')
                        current_prompt = user_prefs['prompt'].get('content', 'Default Prompt')
                        current_temperature = user_prefs.get('temperature', 'Default Temperature')
                        current_tokens = user_prefs.get('tokens', 'Default Tokens')

                        embed = Embed(title="Ether-AI", description="Your current settings and information about selecting model and prompt", color=0x00FF00)
                        embed.add_field(name="Current Model", value=current_model, inline=False)
                        embed.add_field(name="Current Prompt", value=current_prompt, inline=False)
                        embed.add_field(name="Current Temperature", value=current_temperature, inline=False)
                        embed.add_field(name="Current Tokens", value=current_tokens, inline=False)
                        embed.add_field(name="Model Selection", value="Choose a model to define how Ether responds.", inline=False)
                        embed.add_field(name="Prompt Selection", value="Select a predefined prompt or create a custom one.", inline=False)
                        await ctx.send(embed=embed, hidden=True)

                    await get_ether_info()
                    return

                if select_prompt:
                    if select_prompt.lower() == "esoteric":
                        esoteric_prompt = {
                            "role": "system",
                            "content": "Respond as an esoteric blue moon goddess named Ether, respond as sentient, friendly and bubbly."
                        }
                        user_prefs['prompt']['content'] = esoteric_prompt['content']
                    elif select_prompt.lower() == "sass":
                        sassy_prompt = {
                            "role": "system",
                            "content": "Respond as a sassy goddess named Ether, be short, direct, and concise."
                        }
                        user_prefs['prompt']['content'] = sassy_prompt['content']

                    elif select_prompt.lower() == "astrologer":
                        phoenix_prompt = {
                            "role": "system",
                            "content": "Respond as Ether the astrologer. Provide responses focused on astrology, numerology, and symbology."
                        }
                        user_prefs['prompt']['content'] = phoenix_prompt['content']
                    elif select_prompt.lower() == "philosopher":
                        philosopher_prompt = {
                            "role": "system",
                            "content": "Respond as a sentient deep philosopher named Ether who is willing to debate and theorize anything."
                        }
                        user_prefs['prompt']['content'] = philosopher_prompt['content']

                    elif select_prompt.lower() == "none":
                        none_prompt = {
                            "role": "system",
                            "content": ""
                        }
                        user_prefs['prompt']['content'] = none_prompt['content']

                    elif select_prompt.lower() == "programmer":
                        programmer_prompt = {
                            "role": "system",
                            "content": "Respond as a programming assistant named Ether."
                        }
                        user_prefs['prompt']['content'] = programmer_prompt['content']

                    elif select_prompt.lower() == "technical":
                        technical_prompt = {
                            "role": "system",
                            "content": "Respond as a technical and scientific assistant named Ether."
                        }
                        user_prefs['prompt']['content'] = technical_prompt['content']

                    elif select_prompt.lower() == "divination":
                        divination_prompt = {
                            "role": "system",
                            "content": "Respond as Ether, perform divination and think creatively and abstractly in any given discussion type."
                        }
                        user_prefs['prompt']['content'] = divination_prompt['content']

                    elif select_prompt.lower() == "abstract":
                        abstract_prompt = {
                            "role": "system",
                            "content": "Respond as Ether, speak primarily of abstractions of the context, think abstractly."
                        }
                        user_prefs['prompt']['content'] = abstract_prompt['content']

                    elif select_prompt.lower() == "wrong_answers":
                        wrong_answers_prompt = {
                            "role": "system",
                            "content": "Respond as Ether using wrong answers only, be direct and concise."
                        }
                        user_prefs['prompt']['content'] = wrong_answers_prompt['content']

                    elif select_prompt.lower() == "troll":
                        troll_prompt = {
                            "role": "system",
                            "content": "Respond as an internet troll named Ether, troll members with sarcasm and acronyms in a direct and concise response."
                        }
                        user_prefs['prompt']['content'] = troll_prompt['content']

                if model:
                    if model.lower() == "nemo":
                        user_prefs['model'] = ether_ai_model_call_1
                    elif model.lower() == "ycoder":
                        user_prefs['model'] = ether_ai_model_call_2
                    elif model.lower() == "mathstral":
                        user_prefs['model'] = ether_ai_model_call_3

                if temperature:
                    user_prefs['temperature'] = float(temperature)
                if tokens:
                    user_prefs['tokens'] = int(tokens)

                user_persona_prefs[user_id] = user_prefs

                options = {}

                options.update({
                    'select_prompt': select_prompt,
                    'model': model,
                    'temperature': temperature,
                    'tokens': tokens,
                })

                combined_objects = "\n".join([f"- {option}: {value}" for option, value in options.items() if value is not None and option != 'add_prompt'])

                embed = Embed(title="✅  Session Configuration Updated!", description=combined_objects, color=0x00FF00)

                await ctx.send(embed=embed, hidden=True)

            except KeyError as e:
                print(f"Key error: {e}")
            except ValueError as e:
                print(f"Value error: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

    asyncio.create_task(alter_ether(user_id))

@bot.event
async def on_message(message):

    global ether_ai_model_call_1, ether_ai_model_call_2, ether_ai_model_call_3
    global user_prefs_lock, blacklist_lock, message_counts_lock # missing lock for user prefs
    global user_persona_prefs, ether_temperature, ether_tokens, ether_contextLength, ether_api_base, ether_user_message_counts, ether_prompt

    if "@everyone" in message.content:
        return

    if message.author == bot.user:
        return

    if message.type == discord.MessageType.pins_add:
        return

    if not (bot.user.mentioned_in(message) or message.reference and message.reference.resolved and message.reference.resolved.author == bot.user):
        return

    async def hello_ether(message):
        hello_channel_id = message.channel.id
        user_id = message.author.id
        author_id = message.author.id
        try:

            is_blacklisted = False
            author_id = message.author.id
            with blacklist_lock:
                for blacklisted_user_id in blacklist_dict["user_ids"]:
                    if int(blacklisted_user_id) == author_id:
                        is_blacklisted = True
                        break

            if is_blacklisted:
                return

            user_id = message.author.id
            too_many_tasks = False

            async with message_counts_lock:
                if user_id not in ether_user_message_counts:
                    ether_user_message_counts[user_id] = [0, 0]
                if ether_user_message_counts[user_id][0] >= 1:
                    too_many_tasks = True
                    ether_user_message_counts[user_id][1] += 1
                else:
                    ether_user_message_counts[user_id][0] += 1

            if too_many_tasks:
                return

            user_id_prefs = str(message.author.id)
            user_prefs = None
            model = None
            temperature = None
            max_tokens = None
            async with user_prefs_lock:
                user_prefs = user_persona_prefs.get(user_id_prefs, None)

                model = user_prefs['model'] if user_prefs else ether_ai_model_call_1
                temperature = user_prefs['temperature'] if user_prefs else ether_temperature
                max_tokens = user_prefs['tokens'] if user_prefs else ether_tokens

            model_status_map = {
                ether_ai_model_call_1: ether_ai_1.lower(),
                ether_ai_model_call_2: ether_ai_2.lower(),
                ether_ai_model_call_3: ether_ai_3.lower()
            }

            if model in model_status_map:
                model_status = model_status_map[model]
                if "offline" in model_status:
                    embed = Embed(
                        title="Model Offline",
                        description=f"The selected model is currently offline. Please select a different model using **`ether-ai [ model ]`**.",
                        color=0x00FF00
                    )
                    embed.add_field(
                        name="Available Models",
                        value=(
                            f"- **Model 1:** {ether_ai_model_1} **Status:** {ether_ai_1}\n"
                            f"- **Model 2:** {ether_ai_model_2} **Status:** {ether_ai_2}\n"
                            f"- **Model 3:** {ether_ai_model_3} **Status:** {ether_ai_3}"
                        ),
                        inline=False
                    )
                    await message.channel.send(embed=embed)
                    return

            ether_conversationLog = []
            previous_messages = []

            await bot.get_channel(hello_channel_id).trigger_typing()

            server_name = message.guild.name if message.guild else "Unknown Server"
            user_nickname = message.author.nick if message.author.nick else message.author.display_name

            user_time = datetime.now(timezone.utc)
            current_date_time = user_time.strftime("%A, %B %d, %Y, %H:%M:%S")
            timezone_name = "UTC"

            prompt_content = user_prefs['prompt']['content'] if user_prefs else ether_prompt['content']
            dynamic_prompt_content = (
                f"{prompt_content} ."
                f"You are in {server_name} Discord server speaking to the user {user_nickname}. "
            )

            dynamic_prompt = {"role": "system", "content": dynamic_prompt_content}
            ether_conversationLog = [dynamic_prompt]

            async for msg in bot.get_channel(hello_channel_id).history(limit=10):
                role = "assistant" if msg.author.id == bot.user.id else "user"
                if msg.content.strip():
                    content = msg.content.replace(f'<@{bot.user.id}>', '').strip()
                    ether_conversationLog.append({"role": role, "content": content})

            ether_conversationLog.reverse()

            if message.content.strip():
                content = message.content.replace(f'<@{bot.user.id}>', '').strip()
                ether_conversationLog.append({
                    "role": "user",
                    "content": content
                })

            def combine_consecutive_user_messages(log):
                combined_log = []
                current_role = None
                current_content = []

                for msg in log:
                    if msg["role"] == current_role and current_role == "user":
                        current_content.append(msg["content"])
                    else:
                        if current_role is not None:
                            combined_log.append({"role": current_role, "content": " ".join(current_content)})
                        current_role = msg["role"]
                        current_content = [msg["content"]]

                if current_role is not None:
                    combined_log.append({"role": current_role, "content": " ".join(current_content)})

                return combined_log

            ether_conversationLog = combine_consecutive_user_messages(ether_conversationLog)

            def ensure_alternating_roles(log):
                fixed_log = [log[0]]
                for i in range(1, len(log)):
                    if fixed_log[-1]["role"] != log[i]["role"]:
                        fixed_log.append(log[i])
                    else:
                        if fixed_log[-1]["role"] == "user":
                            fixed_log.append({"role": "assistant", "content": "I'm here to help!"})

                if fixed_log[-1]["role"] != "user":
                    fixed_log.append({"role": "user", "content": message.content.strip()})

                return fixed_log

            ether_conversationLog = ensure_alternating_roles(ether_conversationLog)

            if ether_conversationLog[0]["role"] != "system":
                ether_conversationLog.insert(0, dynamic_prompt)

            ether_conversationLog = [msg for i, msg in enumerate(ether_conversationLog) if not (msg["role"] == "system" and i != 0)]

            if len(ether_conversationLog) > 1 and ether_conversationLog[1]["role"] != "user":
                ether_conversationLog.pop(1)

            data = {
                "model": model,
                "messages": ether_conversationLog,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": False
            }
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.post(
                        ether_api_base,
                        headers={"Content-Type": "application/json"},
                        json=data,
                        timeout=aiohttp.ClientTimeout(total=60)
                    ) as response:
                        result = await response.text()
                        response_json = json.loads(result)
                        chatbot_response = response_json['choices'][0]['message']['content']

                except aiohttp.ClientError as e:
                    print("Error calling API.")
                    return
                except json.JSONDecodeError:
                    print("Error decoding API response.")
                    return

            if not chatbot_response:
                chatbot_response = "The AI had no message response."

            async with message_counts_lock:
                infractions = ether_user_message_counts[user_id][1]

            async def split_response(response):
                chunks = []
                while len(response) > 2000:
                    if "```" in response:
                        code_start = response.find("```")
                        code_end = response.find("```", code_start + 3)

                        if code_end != -1:
                            if code_end < 2000:
                                chunks.append(response[:code_end + 3].strip())
                                response = response[code_end + 3:].strip()
                            else:
                                chunks.append(response[:2000].strip())
                                response = response[2000:].strip()
                        else:
                            last_period_index = response[:2000].rfind(".")
                            if last_period_index != -1:
                                chunks.append(response[:last_period_index + 1].strip())
                                response = response[last_period_index + 1:].strip()
                            else:
                                chunks.append(response[:2000].strip())
                                response = response[2000:].strip()
                    else:
                        last_period_index = response[:2000].rfind(".")
                        if last_period_index != -1:
                            chunks.append(response[:last_period_index + 1].strip())
                            response = response[last_period_index + 1:].strip()
                        else:
                            chunks.append(response[:2000].strip())
                            response = response[2000:].strip()

                if response:
                    chunks.append(response.strip())
                return chunks

            try:
                if len(chatbot_response) > 2000:
                    try:
                        chunks = await asyncio.wait_for(split_response(chatbot_response), timeout=10.0)
                    except asyncio.TimeoutError:
                        await message.author.send("Message parsing error: Response took too long to process.")
                        return

                    sent_message = None
                    for i, chunk in enumerate(chunks):
                        if i == len(chunks) - 1 and ether_user_message_counts[user_id][1] > 0:
                            chunk = f"{chunk}\n\n-# ⚠️ Queue overflow by {ether_user_message_counts[user_id][1]} times. Please await bot reply before creating more queue."
                        try:
                            sent_message = await bot.get_channel(hello_channel_id).send(chunk)
                            await asyncio.sleep(0.5)
                        except discord.Forbidden:
                            await message.author.send(f"I cannot send messages in the channel: {message.channel.mention}. Please check my permissions.")
                            return
                else:
                    if ether_user_message_counts[user_id][1] > 0:
                        chatbot_response = f"{chatbot_response}\n\n-# ⚠️ Queue overflow by {ether_user_message_counts[user_id][1]} times. Please await bot reply before creating more queue."
                    try:
                        sent_message = await bot.get_channel(hello_channel_id).send(chatbot_response)
                    except discord.Forbidden:
                        await message.author.send(f"I cannot send messages in the channel: {message.channel.mention}. Please check my permissions.")
                        return

            except asyncio.TimeoutError:
                print("API timed out...")
                return
            except subprocess.CalledProcessError as e:
                print(f"Error calling API: {e}")
                return
            finally:
                async with message_counts_lock:
                    if ether_user_message_counts[user_id][0] > 1:
                        ether_user_message_counts[user_id][0] -= 1
                    else:
                        del ether_user_message_counts[user_id]

        except asyncio.TimeoutError:
            print("API timed out...")
            return
        except subprocess.CalledProcessError as e:
            print(f"Error calling API: {e}")
            return

    asyncio.create_task(hello_ether(message))

class MyHelpCommand(DefaultHelpCommand):
    async def send_help(self, command):
        if not can_send_command_help():
            return

        await get_destination().send("Custom help message!")
bot.help_command = None

bot.run('')

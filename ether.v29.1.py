"""
┏┓ ┓         ┏┓┓ ┏┓
┣ ╋┣┓┏┓┏┓  ┓┏┏┛┃ ┗┫
┗┛┗┛┗┗ ┛   ┗┛┗━┻•┗┛

Written by Ned
Edition: dev v9, 4.18.2024          
"""

# discord libraries [>
import discord 
from discord import Game, Status
from discord.ext import commands, tasks
from discord import Embed
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
from discord.ext.commands import CommandNotFound
from discord.ext.commands import DefaultHelpCommand
# <]

# openai & langchain libraries [>
import openai
from gpt_index import SimpleDirectoryReader, GPTSimpleVectorIndex, LLMPredictor, PromptHelper
from langchain.chat_models import ChatOpenAI
# <]

from collections import defaultdict
from docx import Document
from bs4 import BeautifulSoup
from datetime import datetime
from PIL import Image
from aiohttp import ClientConnectorError
from threading import RLock
import ebooklib
from ebooklib import epub
from io import BytesIO
import sqlparse
import traceback
import pyshark
import concurrent.futures
import datetime
import re
import asyncio
import sqlite3
import shutil
import os
import fitz
import threading
import tracemalloc
import subprocess
import aiohttp
import aiofiles
import requests
import queue
import io
import magic
import codecs
import json
import random
import feedparser
import gc
import pandas as pd
# <]

# discord intents [>
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.guilds = True
intents.members = True
intents.guild_messages = True
intents.reactions = True
# <]

# global ID's [>
admin_id = 1234
STATIC_GUILD_ID = 1234
DESIGNATED_CHANNEL_ID = 1234
ROLE_ID_SESSIONS = 1234
ROLE_ID_SESSIONS_EXTENDING = 1234
ROLE_ID_DATA = 1234 
ROLE_ID_LIMITED = 1234 
ROLE_ID_DEV = 1234 
ROLE_IDS = [1234, 1234] 
admin_channels = (1234, 1234, 1234) 
# <]

# ether & beep boop stuff [>
bot = commands.Bot(command_prefix='/', intents=intents)
slash = SlashCommand(bot, sync_commands=True) 
schedule = 'No Scheduled Outages'
bugs = 'No Known Active Errors' 
uptime = '' 
homeserv = "" 
bot_login_time = None
presence_flag = True
# <]

# dictionaries and databases [>
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
cancel_queue = {}
# <]

# global session management [>
shared_sessions = {}
user_sessions = {} 
active_sessions = {}
shared_sessions_lock = RLock() 
user_sessions_lock = asyncio.Lock() 
user_sessions_fetch_lock = RLock() 
active_sessions_lock = asyncio.Lock()
active_sessions_fetch_lock = RLock()
sessions_exit_lock = RLock() 
# <]

# semaphore for indexing process [>
semaphore_limit = 5
semaphore = threading.BoundedSemaphore(15)
queue_lock = asyncio.Lock()
semaphore_lock = threading.Lock()
rate_limit_semaphore = asyncio.Semaphore(semaphore_limit)
# <]

# tracemalloc depreciated purpose [>
tracemalloc.start()
# <]

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
# <<<]

# beep boop hello [--->>
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
    bot_login_time = datetime.datetime.now()

    static_guild = bot.get_guild(STATIC_GUILD_ID)
    if static_guild is not None:
        async for member in static_guild.fetch_members(limit=None):
            member_ids.append(member.id)

    check_role_and_cancel_queue.start() 
    update_ether_status.start()  
    
    task_admin = asyncio.create_task(ether_admin())


# <<---]

@tasks.loop(hours=24)
async def update_ether_status():
    server_count = len(bot.guilds)
    await bot.change_presence(activity=Game(name=f"OpenAI in {server_count} servers"), status=Status.online)

# Task to manage cases where users who purchased extended use have expired or cancelled
@tasks.loop(hours=6)
async def check_role_and_cancel_queue():
    global active_sessions, user_sessions, member_ids, cancel_queue
    static_guild = bot.get_guild(STATIC_GUILD_ID)
    current_time = datetime.datetime.now()

    for member_id in member_ids:
        if any(session.author_id == member_id for session in active_sessions.values()):
            with user_sessions_fetch_lock:
                session_list = [session for key, sessions in user_sessions.items() for session in sessions if key.startswith(f"{member_id}-")]
                session_count = len(session_list)

                if session_count > 3:
                    role = await check_member_role(member_id, static_guild)

                    if role == "sessions" or role == "data":
                        continue
                    else:
                        if member_id in cancel_queue:
                            entry = cancel_queue[member_id]
                            timestamp = entry['timestamp']
                            message_sent = entry['message_sent']

                            if (current_time - timestamp).total_seconds() >= 24 * 60 * 60:
                                member = static_guild.get_member(member_id)
                                if member is not None and await check_member_role(member_id, static_guild) != "sessions":
                                    for session in session_list:
                                        asyncio.create_task(session.exit_session_instance())

                                    del cancel_queue[member_id]
                                continue
                        else:
                            cancel_queue[member_id] = {
                                'timestamp': current_time,
                                'message_sent': False
                            }

                            member = static_guild.get_member(member_id)
                            if member is not None:
                                dm_channel = await member.create_dm()
                                embed = Embed(title="Subscription Ended...", description="Your subscription with Ether has expired. Please renew your subscription within 24 hours at Ether's home server or your active sessions will be closed.", color=0x0000FF)
                                await dm_channel.send(embed=embed)

# Partner event with role and subscription, loads additional members into bot memory
# join events [--->
@bot.event
async def on_member_join(member):
    global member_ids
    static_guild = bot.get_guild(STATIC_GUILD_ID)
    if static_guild is None:
        print("Static guild not found.")
        return
    member_ids = [member.id for member in static_guild.members]
    member_ids.append(member.id)

# For public bot post a fun anouncement of guild joins
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
# <---]

# Admin stuff - ban, unban, leave
async def ether_admin():
    global schedule, bugs, admin_channels, blacklist_dict, homeserv, admin_id

    def check_admin_author_id(message):
        return message.author.id == admin_id

    def check_command_keyword(message):
        return re.sub(r'<@1130638110196256828>', '', message.content).strip().startswith(('banuser', 'banguild', 'unban', 'list', 'setstatus', 'logout', 'leave', 'setpfp'))

    while True:

        message = await bot.wait_for('message', check=lambda message: message.author.id == admin_id)
        
        if check_admin_author_id(message) and check_command_keyword(message):
            command, *args = message.content.split()[1:]

            if command == "banuser":
                if len(args) < 2:
                    await message.channel.send("Invalid number of arguments provided.")
                    continue

                user_id = args[0]
                reason = " ".join(args[1:])
                with blacklist_lock:
                    if str(user_id) not in blacklist_dict["user_ids"]:
                        blacklist_dict["user_ids"].append(str(user_id))
                        blacklist_dict["reason"].append(reason)
                        conn = sqlite3.connect(blacklist_db)
                        cursor = conn.cursor()
                        cursor.execute("INSERT INTO ether_blacklist (user_id, guild_id, reason) VALUES (?, '', ?)", (user_id, reason))
                        conn.commit()
                        conn.close()
                        await message.channel.send(f"User ID {user_id} has been added to the blacklist with the reason: {reason}")
                    else:
                        await message.channel.send("User ID is already blacklisted.")

            elif command == "list":
                with blacklist_lock:
                    if blacklist_dict["user_ids"]:
                        for user_id, reason in zip(blacklist_dict["user_ids"], blacklist_dict["reason"]):
                            await message.channel.send(f"User ID: {user_id}, Reason: {reason}")
                    else:
                        await message.channel.send("No user IDs in the blacklist.")

                    if blacklist_dict["guild_ids"]:
                        for guild_id, reason in zip(blacklist_dict["guild_ids"], blacklist_dict["reason"]):
                            await message.channel.send(f"Guild ID: {guild_id}, Reason: {reason}")
                    else:
                        await message.channel.send("No guild IDs in the blacklist.")
                    
            elif command == "setstatus":
                if len(args) < 2:
                    await message.channel.send("Invalid number of arguments provided.")
                    continue

                action = args[0]
                message_text = " ".join(args[1:])

                if action == 'schedule':
                    schedule = message_text
                    await message.channel.send(f"Schedule has been updated to: {message_text}")

                elif action == 'support':
                    homeserv = message_text
                    await message.channel.send(f"Support link has been updated to: {message_text}")

                else:
                    await message.channel.send("Invalid action provided.")

            elif command == "banguild":
                if len(args) < 2:
                    await message.channel.send("Invalid number of arguments provided.")
                    continue

                guild_id = args[0]
                reason = " ".join(args[1:])

                with blacklist_lock:
                    if str(guild_id) not in blacklist_dict["guild_ids"]:
                        blacklist_dict["guild_ids"].append(str(guild_id))
                        blacklist_dict["reason"].append(reason)
                        conn = sqlite3.connect(blacklist_db)
                        cursor = conn.cursor()
                        cursor.execute("INSERT INTO ether_blacklist (user_id, guild_id, reason) VALUES ('', ?, ?)", (guild_id, reason))
                        conn.commit()
                        conn.close()
                        await message.channel.send(f"Guild ID {guild_id} has been added to the blacklist with the reason: {reason}")
                    else:
                        await message.channel.send("Guild ID is already blacklisted.")

            elif command == "unban":
                if len(args) < 1:
                    await message.channel.send("Invalid number of arguments provided.")
                    continue

                target_id = args[0]
                with blacklist_lock:
                    if str(target_id) in blacklist_dict["user_ids"]:
                        blacklist_dict["user_ids"].remove(str(target_id))
                        conn = sqlite3.connect(blacklist_db)
                        cursor = conn.cursor()
                        cursor.execute("DELETE FROM ether_blacklist WHERE user_id = ?", (target_id,))
                        conn.commit()
                        conn.close()
                        await message.channel.send(f"User ID {target_id} has been removed from the blacklist.")
                    elif str(target_id) in blacklist_dict["guild_ids"]:
                        blacklist_dict["guild_ids"].remove(str(target_id))
                        conn = sqlite3.connect(blacklist_db)
                        cursor = conn.cursor()
                        cursor.execute("DELETE FROM ether_blacklist WHERE guild_id = ?", (target_id,))
                        conn.commit()
                        conn.close()
                        await message.channel.send(f"Guild ID {target_id} has been removed from the blacklist.")
                    else:
                        await message.channel.send("ID is not currently blacklisted.")

            elif command == "logout":
                await message.channel.send("Bye then I guess....")
                                    
                await bot.close()

            elif command == "leave":
                if len(args) < 1:
                    await message.channel.send("Invalid number of arguments provided.")
                    continue

                guild_id = args[0]

                try:
                    guild = bot.get_guild(int(guild_id))
                    if guild is not None:
                        await guild.leave()
                        await message.channel.send(f"Left server: {guild.name}")
                    else:
                        await message.channel.send("Server not found.")
                except Exception as e:
                    await message.channel.send(f"An error occurred while leaving the server: {e}")

# <---]

# function for EtherCereal role checks [--->
async def check_member_role(member_id, static_guild):
    global terms_dict
    with terms_dict_lock:
        member = static_guild.get_member(member_id)
        if member is None:
            if str(member_id) in terms_dict["user_ids"]:
                return "limited"  
            else:
                return "not_member"
        if any(role.id == ROLE_ID_DATA for role in member.roles):
            return "data"
        if any(role.id == ROLE_ID_SESSIONS for role in member.roles):
            return "sessions"
        if any(role.id == ROLE_ID_LIMITED for role in member.roles):
            return "limited"
        if any(role.id == ROLE_ID_DEV for role in member.roles):
            return "unlimited"
# <---]

# <<--- manager for base level session management --->>
@slash.slash(name="manager", 
    description="Start, stop, view, and manage sessions",
    options=[
        create_option(
            name="session_management",
            description="Start, stop, view, and manage sessions",
            option_type=3,
            required=False,
            choices=[
                create_choice(
                    name="start",
                    value="start" 
                ),
                create_choice(
                    name="view_sessions",
                    value="sessions" 
                ),
                create_choice(
                    name="session_config",
                    value="stats2" 
                ),
                create_choice(
                    name="save_session",
                    value="save_session" 
                ),
                create_choice(
                    name="load_session",
                    value="load_session" 
                ),
                create_choice(
                    name="load_session_defaults",
                    value="load_session_defaults" 
                ),
                create_choice(
                    name="exit",
                    value="exit" 
                ),
                create_choice(
                    name="exit_all",
                    value="exit_all" 
                ),
            ]
        ),
        create_option(
            name="session_name",
            description="Give this session a unique name",
            option_type=3,
            required=False
        ),
        create_option(
            name="extend_session",
            description="Extend one of your current sessions",
            option_type=3,
            required=False,
            choices=[
                create_choice(
                    name="1",
                    value="1"
                ),
                create_choice(
                    name="2",
                    value="2"
                ),
                create_choice(
                    name="3",
                    value="3"
                ),
                create_choice(
                    name="4",
                    value="4"
                ),
                create_choice(
                    name="5",
                    value="5"
                ),
                create_choice(
                    name="6",
                    value="6"
                ),
                create_choice(
                    name="7",
                    value="7"
                ),
                create_choice(
                    name="8",
                    value="8"
                ),
                create_choice(
                    name="9",
                    value="9"
                ),
                create_choice(
                    name="10",
                    value="10"
                ),
                create_choice(
                    name="11",
                    value="11"
                ),
                create_choice(
                    name="12",
                    value="12"
                ),
                create_choice(
                    name="13",
                    value="13"
                ),
                create_choice(
                    name="14",
                    value="14"
                ),
                create_choice(
                    name="15",
                    value="15"
                ),
                create_choice(
                    name="16",
                    value="16"
                ),
                create_choice(
                    name="17",
                    value="17"
                ),
                create_choice(
                    name="18",
                    value="18"
                ),
                create_choice(
                    name="19",
                    value="19"
                ),
                create_choice(
                    name="20",
                    value="20"
                ),
            ]
        ),
        create_option(
            name="exit_session_number",
            description="Exit a specific session using its number",
            option_type=3,
            required=False,
            choices=[
                create_choice(
                    name="1",
                    value="1"
                ),
                create_choice(
                    name="2",
                    value="2"
                ),
                create_choice(
                    name="3",
                    value="3"
                ),
                create_choice(
                    name="4",
                    value="4"
                ),
                create_choice(
                    name="5",
                    value="5"
                ),
                create_choice(
                    name="6",
                    value="6"
                ),
                create_choice(
                    name="7",
                    value="7"
                ),
                create_choice(
                    name="8",
                    value="8"
                ),
                create_choice(
                    name="9",
                    value="9"
                ),
                create_choice(
                    name="10",
                    value="10"
                ),
                create_choice(
                    name="11",
                    value="11"
                ),
                create_choice(
                    name="12",
                    value="12"
                ),
                create_choice(
                    name="13",
                    value="13"
                ),
                create_choice(
                    name="14",
                    value="14"
                ),
                create_choice(
                    name="15",
                    value="15"
                ),
                create_choice(
                    name="16",
                    value="16"
                ),
                create_choice(
                    name="17",
                    value="17"
                ),
                create_choice(
                    name="18",
                    value="18"
                ),
                create_choice(
                    name="19",
                    value="19"
                ),
                create_choice(
                    name="20",
                    value="20"
                ),
            ]
        ),
        create_option(
            name="utilities",
            description="Enable dummy predictor requests and jump listeners",
            option_type=3,
            required=False,
            choices=[
                create_choice(
                    name="keep_alive",
                    value="keep_alive" 
                ),
                create_choice(
                    name="jump_listener",
                    value="jump_listener" 
                ),
            ]
        ),
    ])
async def manager(ctx, session_management=None, session_name=None, extend_session=None, save_load=None, utilities=None, exit_session_number=None, exit=None):
    global user_sessions, schedule, bot_login_time, bugs, homeserv

    author_id = ctx.author.id
    if ctx.channel:
        channel_id = ctx.channel.id
    else:
        dm_channel = await ctx.author.create_dm()
        channel_id = dm_channel.id
    
    channel = ctx.channel
    
    static_guild = bot.get_guild(STATIC_GUILD_ID)

    member_id = ctx.author.id
    role_status = await check_member_role(member_id, static_guild)

    options = (session_management, session_name, extend_session, save_load, utilities, exit_session_number, exit)
    if all(option is None for option in options):
        async def get_help_task(ctx):
            try:
                session_list = None
                with user_sessions_fetch_lock:
                    session_list = [key for key in user_sessions.keys() if key.startswith(f"{author_id}-")]

                if len(session_list) > 0:
                    with user_sessions_fetch_lock:
                        session_info = ""
                        session_numbers = [int(session.split('-')[1]) for session in session_list]
                        for session_number, session_key in enumerate(session_list, start=1):
                            session = user_sessions[session_key][0]  
                            session_channels = []
                            for channel_id in session.server_share:
                                channel = bot.get_channel(channel_id)
                                if channel:
                                    session_channels.append(channel.mention)
                            session_channels_str = ", ".join(session_channels)
                            session_info += f"#️⃣  **{session_numbers[session_number-1]} - {session.unique_name}:** {session.ctx.channel.mention if hasattr(session.ctx.channel, 'name') else session.ctx.channel.recipient.name + 'DM Channel'}\n🔗  Extensions: {session_channels_str}\n\n"

                    chunks = [session_info[i:i+4000] for i in range(0, len(session_info), 4000)]

                    embed = Embed(title="❓  Manager Help", color=0x00FF00)
                    embed.add_field(name="", value="**__session_management__**\n- `start`\ninitialize a session\n- `view_sessions`\nview all sessions\n- `session_config`\nconfigure session\n- `save_session`\nsave config to file\n- `load_session`\nload config from file\n- `exit`\nexit a session\n- `exit_all`\nexit all sessions", inline=False)
                    embed.add_field(name="", value="**__session_name__**\n- `name a session`", inline=False)
                    embed.add_field(name="", value="**__extend_session__**\n- `extend a session into other channels`\nrequires the session number", inline=False)
                    embed.add_field(name="", value="**__utilities__**\n- `jump_listener`\nrestart session listener\n- `keep_alive`\ndummy service for predictor", inline=False)
                    embed.add_field(name="", value="**__session_name__**\n- `name a session`", inline=False)

                    for chunk in chunks:
                        embed.add_field(name="🗃️  Your Active Sessions", value=chunk, inline=False)
                        await ctx.send(embed=embed, hidden=True)
                        embed.remove_field(-1)  
                else:
                    session_info = "No active sessions"
                    embed = Embed(title="❓  Manager Help", color=0x00FF00)
                    embed.add_field(name="", value="**__session_management__**\n- `start`\ninitialize a session\n- `view_sessions`\nview all sessions\n- `session_config`\nconfigure session\n- `save_session`\nsave config to file\n- `load_session`\nload config from file\n- `exit`\nexit a session\n- `exit_all`\nexit all sessions", inline=False)
                    embed.add_field(name="", value="**__session_name__**\n- `name a session`", inline=False)
                    embed.add_field(name="", value="**__extend_session__**\n- `extend a session into other channels`\nrequires the session number", inline=False)
                    embed.add_field(name="", value="**__utilities__**\n- `jump_listener`\nrestart session listener\n- `keep_alive`\ndummy service for predictor", inline=False)
                    embed.add_field(name="", value="**__session_name__**\n- `name a session`", inline=False)
                    embed.add_field(name="🗃️  Your Active Sessions", value=session_info, inline=False)
                    await ctx.send(embed=embed, hidden=True)

            except Exception as e:
                embed = Embed(title="Manager Help Error", description="", color=0x0000FF)
                await ctx.send(embed=embed, hidden=True)
        asyncio.create_task(get_help_task(ctx))
        return
    
    if session_management == "sessions":
        session_list = None
        with user_sessions_fetch_lock:
            session_list = [key for key in user_sessions.keys() if key.startswith(f"{author_id}-")]

        if len(session_list) > 0:
            async def display_sessions():
                try:
                    with user_sessions_fetch_lock:
                        session_info = ""
                        session_numbers = [int(session.split('-')[1]) for session in session_list]
                        for session_number, session_key in enumerate(session_list, start=1):
                            session = user_sessions[session_key][0]  
                            session_channels = []
                            for channel_id in session.server_share:
                                channel = bot.get_channel(channel_id)
                                if channel:
                                    session_channels.append(channel.mention)
                            session_channels_str = ", ".join(session_channels)
                            session_info += f"#️⃣  **{session_numbers[session_number-1]} - {session.unique_name}:** {session.ctx.channel.mention if hasattr(session.ctx.channel, 'name') else session.ctx.channel.recipient.name + 'DM Channel'}\n🔗  Extensions: {session_channels_str}\n\n"

                    chunks = [session_info[i:i+4000] for i in range(0, len(session_info), 4000)]

                    for chunk in chunks:
                        embed = Embed(title="🗃️  Your Active Sessions", description=chunk, color=0x0000FF)
                        await ctx.send(embed=embed, hidden=True)
                except Exception as e:
                    print(e)
            asyncio.create_task(display_sessions())
            return
        
        else:
            embed = Embed(title="No Active Sessions", description="You don't have any active sessions.", color=0x0000FF)
            await ctx.send(embed=embed, hidden=True)
            return

    elif session_management == "exit_all":
        async def exit_all_sessions():
            try:
                with user_sessions_fetch_lock:
                    
                    session_list = [session for key, sessions in user_sessions.items() if key.startswith(f"{author_id}-") for session in sessions]

                    for session in session_list:
                        asyncio.create_task(session.exit_session_instance())

                    gc.collect()
                    embed = Embed(title="❎  All Sessions Closed!", description="", color=0x00FF00)
                    embed.add_field(name="", value=f"", inline=False)
                    await ctx.send(embed=embed, hidden=True)
                    
            except Exception as e:
                    print(e)
        asyncio.create_task(exit_all_sessions())
        return
    
    elif exit_session_number is not None:
        async def exit_session_by_number():
            try:
                session_number = int(exit_session_number)  
                with user_sessions_fetch_lock:
                    session_list = [session for key, sessions in user_sessions.items() if key.startswith(f"{author_id}-") for session in sessions]
                    for session in session_list:
                        if session_number == session.session_number:  
                            asyncio.create_task(session.exit_session_instance())
                            break  
                    embed = Embed(title=f"❎  Exited Session {session_number}", description=f"", color=0x00FF00)
                    await ctx.send(embed=embed, hidden=True)
            except Exception as e:
                print(f"Error exiting session: {e}")
        asyncio.create_task(exit_session_by_number())

    with active_sessions_fetch_lock:
        if any(session.channel_id == channel.id and session.author_id == author_id for session in active_sessions.values()):
            with user_sessions_fetch_lock:
                session_list = [session for key, sessions in user_sessions.items() for session in sessions if key.startswith(f"{author_id}-")]
                if session_list:
                    session = next((session for session in session_list if session.channel_id == channel.id), None)
                    if session is not None:
                        if session_name is not None:
                            async def set_name():
                                try:                 
                                    session.unique_name = session_name
                                    embed = Embed(title="❎  Session Name Updated!", description=f"Name: {session_name}", color=0x00FF00)
                                    embed.add_field(name="", value=f"", inline=False)
                                    await ctx.send(embed=embed, hidden=True)
                                except Exception as e:
                                    print(e)
                            asyncio.create_task(set_name())
                            return
              
                        if session_management is not None:
                            if session_management == "exit":
                                async def perform_exit():
                                    try:
                                        session_to_exit = next((session for session in session_list if session.channel_id == ctx.channel.id), None)
                                        if session_to_exit is not None:
                                            asyncio.create_task(session_to_exit.exit_session_instance())
                                            embed = Embed(title="❎  Session Closed!", description="", color=0x00FF00)
                                            embed.add_field(name="", value=f"", inline=False)
                                            await ctx.send(embed=embed, hidden=True)
                                        else:
                                            embed = Embed(title="⚠️  Error", description="You are not in a session channel. See /ether [manager] [sessions]", color=0xFF0000)
                                            await ctx.send(embed=embed, hidden=True)
                                    except Exception as e:
                                        print(f"Error exiting: {e}")

                                asyncio.create_task(perform_exit())
                                return
                            
                            if session_management == "save_session":
                                async def save_config():
                                    try:

                                        session_variables = {
                                            "tokens": session.tokens,
                                            "context": session.context,
                                            "model": session.model,
                                            "size": session.size,
                                            "number": session.number,
                                            "nicknames": session.nicknames,
                                            "role": session.role,
                                            "frequency": session.frequency,
                                            "presence": session.presence,
                                            "top_p": session.top_p,
                                            "unique_name": session.unique_name,
                                            "temperature": session.temperature,
                                            "image_model": session.image_model,
                                            "toggle_prompt": session.revised_prompt,
                                            "image_style": session.style,
                                            "no_mention": session.no_mention,
                                            "segmented_context": session.segmented_context,
                                            "stacked_context": session.stacked_context,
                                            "combined_context": session.combined_context,
                                            # new ----->>
                                            "session_channels": session.server_share,
                                            "api_base": session.api_base,
                                            "api_engine": session.api_engine,
                                        }

                                        session_json = json.dumps(session_variables)

                                        with open("session_config.json", "w") as file:
                                            file.write(session_json)

                                        channel_link = f'#{ctx.channel.mention}'
                                        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                        content = f"Configuration from {channel_link} ({timestamp})"

                                        await ctx.author.send(content=content, file=discord.File("session_config.json"))

                                        embed = Embed(title="🎛️  Session config sent to dm", description="", color=0x0000FF)
                                        await ctx.send(embed=embed, hidden=True)

                                    except Exception as e:
                                        embed = Embed(title="Config Save Error", description="", color=0x0000FF)
                                        await ctx.send(embed=embed, hidden=True)

                                asyncio.create_task(save_config())
                                return
                            
                            if session_management == "load_session":
                                async def load_config():
                                    try:
                                        embed = Embed(title="🎛️  Check direct messages to load config", description="", color=0x0000FF)
                                        await ctx.send(embed=embed, hidden=True)

                                        dm_channel = await ctx.author.create_dm()

                                        embed = Embed(title="🔼  Upload Configuration File", color=0x00FF00)
                                        embed.add_field(name="", value="Send your configuration json file as an attachment", inline=False)
                                        message = await dm_channel.send(embed=embed)

                                        def check(message):
                                            return message.author == ctx.author and message.attachments

                                        message = await bot.wait_for('message', check=check, timeout=60)
                                        uploaded_file = message.attachments[0]

                                        if uploaded_file.filename.endswith(".json"):
                                            file_content = await uploaded_file.read()

                                            session_variables = json.loads(file_content)

                                            session.tokens = int(session_variables.get("tokens"))
                                            session.context = int(session_variables.get("context"))
                                            session.model = session_variables.get("model")
                                            session.size = session_variables.get("size")
                                            session.number = int(session_variables.get("number"))
                                            session.style = str(session_variables.get("image_style"))
                                            session.no_mention = session_variables.get("no_mention")
                                            session.segmented_context = session_variables.get("segmented_context")
                                            session.stacked_context = session_variables.get("stacked_context")
                                            session.combined_context = session_variables.get("combined_context")

                                            session_channels = session_variables.get("session_channels", [])

                                            with shared_sessions_lock:
                                                for channel_id in session_channels:
                                                    if channel_id in shared_sessions:
                                                        continue
                                                    if channel_id not in shared_sessions:
                                                        if session.user_share or session.role_share:
                                                            shared_sessions[channel_id] = ctx.author.id
                                                            session.server_share.append(channel_id)
                                                        else:
                                                            session.server_share.append(channel_id)
                                                    elif session.user_share or session.role_share:
                                                        continue
                                                    else:
                                                        if channel_id not in session.server_share:
                                                            session.server_share.append(channel_id)
                                        
                                            session.nicknames = session_variables.get("nicknames")

                                            role_dict = session_variables.get("role", {"user_id": [], "user_role": [], "prompt": []})

                                            session.role = role_dict

                                            session.role = role_dict
                                            session.frequency = float(session_variables.get("frequency", 0))
                                            session.presence = float(session_variables.get("presence", 0))
                                            session.top_p = float(session_variables.get("top_p", 0))
                                            session.unique_name = session_variables.get("unique_name")
                                            session.temperature = float(session_variables.get("temperature"))
                                            session.image_model = session_variables.get("image_model")
                                            session.revised_prompt = session_variables.get("revised_prompt")

                                            embed = Embed(title="✅  Done!", description=(f"Your configuration has been uploaded into your session.\n#{ctx.channel.name} {ctx.channel.mention}"), color=0xFFA500)
                                            await dm_channel.send(embed=embed)
                                            return
                                        else:
                                            embed = Embed(title="❌  Error\n\n", description=("The file must be a .json file in the format you would receive it from Ether."), color=0xFFA500)
                                            await dm_channel.send(embed=embed)
                                            return
                                    except asyncio.TimeoutError:
                                        embed.description = "Operation Timed Out: No file uploaded."
                                        await message.edit(embed=embed)

                                asyncio.create_task(load_config())
                                return

                            if session_management == "load_session_defaults":
                                async def set_defaults():
                                    session.model = "gpt-3.5-turbo"
                                    session.assistant = None
                                    session.image_model = "dalle3"
                                    session.prompt = ''
                                    session.temperature = 0.3
                                    session.tokens = 2000
                                    session.number = 1
                                    session.size = '1024x1024'
                                    session.style = "vivid"
                                    session.frequency = 0
                                    session.presence = 0
                                    session.top_p = 0
                                    session.top_k = 0
                                    session.repeat_penalty = 0
                                    session.revised_prompt = False 
                                    session.unique_name = "Chat"
                                    session.nicknames = False
                                    session.no_mention = False
                                    session.eco = True
                                    session.context = 4
                                    session.advanced_mode = False
                                    session.segmented_context = "False"
                                    session.stacked_context = "False"
                                    session.combined_context = "True"
                                    session.api_engine = "openai"
                                    session.api_base = session.api_base_default
                                    session.associations_share = []
                                    session.associations = {}
                                    session.custom_model_name = "local-model"
                                    session.role_share = {}
                                    session.user_share = {} 
                                    session.selected_role = "user"
                                    with shared_sessions_lock:
                                        for channel_id in session.server_share:
                                            shared_sessions.pop(channel_id, None)
                                    session.server_share = []
                                    session.server_all_share = {}
                                    session.role = {"user_id": [], "user_role": [], "prompt": []}
                                    session.role["user_id"].append(ctx.author.id)
                                    session.role["user_role"].append(session.selected_role)
                                    session.role["prompt"].append('')
                                    session.index = None 
                                    session.prompt_helper = None 
                                    session.llm_predictor = None

                                    try:
                                        role_index = session.role["user_id"].index(author_id)
                                        prompt_value = session.role["prompt"][role_index]
                                        if len(prompt_value) > 100:
                                            prompt_value = prompt_value[:100] + "..."
                                        role_list = session.role.get("user_role", [])
                                        role_value = role_list[role_index] if role_index < len(role_list) else None
                                        tokens_value = session.tokens
                                        context_value = session.context
                                        nicknames_value = session.nicknames
                                        temperature_value = session.temperature
                                        session_number_value = session.session_number
                                        session_nomention_value = session.no_mention
                                        session_style_value = session.style
                                        model_value = session.model
                                        size_value = session.size
                                        number_value = session.number
                                        name_value = session.unique_name
                                        server_share_value = session.server_share
                                        presence_value = session.presence
                                        frequency_value = session.frequency
                                        top_p_value = session.top_p
                                        embed_value = session.learning_session
                                        image_model_value = session.image_model
                                        session_toggle_prompt = session.revised_prompt

                                        if session.stacked_context == "True":
                                            session_context_type = "stacked"
                                        elif session.segmented_context == "True":
                                            session_context_type = "segmented"
                                        elif session.combined_context == "True":
                                            session_context_type = "combined"

                                        server_share_channels = []
                                        for channel_id in server_share_value:
                                            channel = discord.utils.get(ctx.guild.channels, id=channel_id)
                                            if channel:
                                                channel_link = f"[{channel.name}](https://discord.com/channels/{ctx.guild.id}/{channel.id})"
                                                server_share_channels.append(channel_link)

                                        embed = Embed(title="⚙️  Session Stats", description="", color=0x0000FF)
                                        embed.add_field(name=f"ℹ️  **| Session** {session_number_value} **Name:** {name_value}\n\n", value=f"", inline=False)
                                        embed.add_field(name="🎛️ **| OpenAI Config**", value=f"- **Tokens:** {tokens_value}\n- **Temperature:** {temperature_value}\n- **Model:** {model_value}\n- **Role:** {role_value}\n- **Presence:** {presence_value}\n- **Frequency:** {frequency_value}\n- **Top_P:** {top_p_value}", inline=True)
                                        embed.add_field(name="🎨 **| DALLE Config**", value=f"- **Model:** {image_model_value}\n- **Style:** {session_style_value}\n- **Number:** {number_value}\n- **Size:** {size_value}\n- Toggles: {session_toggle_prompt}*Note: number, size, and variations are None in Dalle 3 currently*", inline=True)
                                        embed.add_field(name="💬 **| Chat Config**", value=f"- **No Mention:** {session_nomention_value}\n- **Context Amount:** {context_value}\n- **Context Type:** {session_context_type}\n- **Nicknames:** {nicknames_value}\n- **Embeddings:** {embed_value}", inline=True)
                                        extensions_value = "\n".join([f"{channel}" for channel in server_share_channels])
                                        embed.add_field(name="🔗 **| Extensions**", value=extensions_value, inline=True)
                                        embed.add_field(name="🗒️ **| Prompt:**", value=f"{prompt_value}", inline=True)
                                        embed.set_footer(text="Use /ether [manager] [prompt-view] to view full prompt or /ether [manager] [sessions] to see all sessions & extensions. Use /ether [manager] [session-save] OR [session-load] to save or load a session configuration.")
                                        await ctx.send(embed=embed, hidden=True)
                                        
                                    except Exception as e:
                                        print(f"Error displaying stats card: {e}")
                                   
                                asyncio.create_task(set_defaults())
                                return

                            options = (session_management, session_name, save_load, utilities, exit)
                            if session_management == "stats2" or all(option is None for option in options):
                                async def get_stats_task(ctx, session):
                                    try:
                                        role_index = session.role["user_id"].index(ctx.author.id)
                                        prompt_value = session.role["prompt"][role_index]
                                        if len(prompt_value) > 100:
                                            prompt_value = prompt_value[:100] + "..."
                                        role_list = session.role.get("user_role", [])
                                        role_value = role_list[role_index] if role_index < len(role_list) else None
                                        tokens_value = session.tokens
                                        context_value = session.context
                                        nicknames_value = session.nicknames
                                        temperature_value = session.temperature
                                        session_number_value = session.session_number
                                        session_nomention_value = session.no_mention
                                        session_style_value = session.style
                                        model_value = session.model
                                        size_value = session.size
                                        number_value = session.number
                                        name_value = session.unique_name
                                        server_share_value = session.server_share
                                        presence_value = session.presence
                                        frequency_value = session.frequency
                                        top_p_value = session.top_p
                                        embed_value = session.learning_session
                                        image_model_value = session.image_model
                                        session_toggle_prompt = session.revised_prompt
                                        api_engine = session.api_engine
                                        api_base = session.api_base
                                        top_k_value = session.top_k
                                        repeat_penalty_value = session.repeat_penalty

                                        if session.stacked_context == "True":
                                            session_context_type = "stacked"
                                        elif session.segmented_context == "True":
                                            session_context_type = "segmented"
                                        elif session.combined_context == "True":
                                            session_context_type = "combined"

                                        server_share_channels = []
                                        for channel_id in server_share_value:
                                            channel = discord.utils.get(ctx.guild.channels, id=channel_id)
                                            if channel:
                                                channel_link = f"[{channel.name}](https://discord.com/channels/{ctx.guild.id}/{channel.id})"
                                                server_share_channels.append(channel_link)

                                        association_names = []
                                        for member in session.associations_share:
                                            if isinstance(member, str):
                                                association_names.append(member)  
                                            elif hasattr(member, 'nick'):
                                                association_names.append(member.nick)
                                            else:
                                                association_names.append(member.name if hasattr(member, 'name') else "Unknown")  
                                        associations_name_value = ', '.join(association_names)

                                        user_ids = session.role["user_id"]
                                        user_roles = session.role["user_role"]
                                        prompts = session.role["prompt"]

                                        member_info = []

                                        for user_id, role, prompt in zip(user_ids, user_roles, prompts):
                                            member = ctx.guild.get_member(user_id)
                                            mention = member.mention if member else "Unknown Member"
                                            if len(prompt) > 25:
                                                prompt = prompt[:22] + "..."
                                            member_info.append(f"{mention} - Role: {role}, Prompt: {prompt}")

                                        member_info_value = "\n".join(member_info)

                                        embed = Embed(title="⚙️  Session Stats", description="", color=0x0000FF)
                                        embed.add_field(name=f"ℹ️  **| Session** {session_number_value} **Name:** {name_value}\n\n", value=f"", inline=False)
                                        embed.add_field(name="🎛️ **| OpenAI Config**", value=f"- **API:** {api_engine}\n- **Endpoint:** {api_base}\n- **Tokens:** {tokens_value}\n- **Temperature:** {temperature_value}\n- **Model:** {model_value}\n- **Role:** {role_value}\n- **Presence:** {presence_value}\n- **Frequency:** {frequency_value}\n- **Top_P:** {top_p_value}\n- **Top_K:** {top_k_value}\n- **Repeat Penalty:** {repeat_penalty_value}", inline=True)
                                        embed.add_field(name="🎨 **| DALLE Config**", value=f"- **Model:** {image_model_value}\n- **Style:** {session_style_value}\n- **Number:** {number_value}\n- **Size:** {size_value}\n- Toggles: {session_toggle_prompt}*Note: number, size, and variations are None in Dalle 3 currently*", inline=True)
                                        embed.add_field(name="💬 **| Chat Config**", value=f"- **No Mention:** {session_nomention_value}\n- **Context Amount:** {context_value}\n- **Context Type:** {session_context_type}\n- **Nicknames:** {nicknames_value}\n- **Embeddings:** {embed_value}", inline=True)
                                        extensions_value = "\n".join([f"{channel}" for channel in server_share_channels])
                                        embed.add_field(name="🔗 **| Extensions**", value=extensions_value, inline=True)
                                        embed.add_field(name="🔗 **| Association Shares**", value=associations_name_value, inline=True)
                                        embed.add_field(name="🗒️ **| Prompts & Roles:**", value=member_info_value, inline=False)

                                        embed.set_footer(text="Use /ether [manager] [prompt-view] to view full prompt or /ether [manager] [sessions] to see all sessions & extensions. Use /ether [manager] [session-save] OR [session-load] to save or load a session configuration.")
                                        await ctx.send(embed=embed, hidden=True)
                                        
                                    except Exception as e:
                                        print(f"Error displaying stats card: {e}")
                                asyncio.create_task(get_stats_task(ctx, session))
                                return
                         
                        if utilities is not None:

                            if utilities == "keep-alive":
                                async def keep_alive():
                                    try:
                                        if session.learning_session == True:
                                            if session.send_dummy_requests == False:
                                                asyncio.create_task(session.start_sending_dummy_requests())
                                                embed = Embed(title="🎛️  Keep Alive Enabled", description="Disable keep-alive using the same method as enabling", color=0x0000FF)
                                                await ctx.send(embed=embed, hidden=True)
                                            else:
                                                asyncio.create_task(session.stop_sending_dummy_requests()) 
                                                embed = Embed(title="🎛️  Keep Alive Disabled", description="Enable keep-alive using the same method as disabling", color=0x0000FF)
                                                await ctx.send(embed=embed, hidden=True)
                                        else:
                                            embed = Embed(title="⚠️  Error", description="This session does not have an active embedding", color=0xFF0000)
                                            await ctx.send(embed=embed, hidden=True)
                                    except Exception as e:
                                        print(f"Error exiting: {e}")
                                asyncio.create_task(keep_alive())
                                return
                            
                            if utilities == "jump-listener":
                                async def jump_listener():
                                    try:
                                        asyncio.create_task(session.start_listener())
                                        embed = Embed(title="🎛️  Jump!", description="Session listener jump-started", color=0x0000FF)
                                        await ctx.send(embed=embed, hidden=True)
                                    except Exception as e:
                                        print(f"Error exiting: {e}")
                                asyncio.create_task(jump_listener())
                                return
                       
                        return  
        # This code checks keys by author and extended channels to remove extensions as override new session
        # This works by allowing user to create session, overriding their own extension
        # Extended channels are added to global shares as shared sessions
        # Attempting to generate a session in channel where another user has an extended session should result in fail from current shared channel
        else:
            if any(session.author_id == author_id for session in active_sessions.values()):
                if extend_session is not None:
                    with user_sessions_fetch_lock:
                        selected_session = None
                        for session in active_sessions.values():
                            if session.author_id == author_id and session.session_number == int(extend_session):
                                selected_session = session
                                break

                        if selected_session is not None:
                            async def extend_session():
                                role_limits = {
                                    "limited": 20,
                                    "sessions": 20,
                                    "data": 20,
                                    "unlimited": 20,
                                }
                                if selected_session.extendable == "True":
                                    role_limit = role_limits.get(selected_session.role_status)
                                    if role_limit is not None:
                                        if len(selected_session.server_share) < role_limit:
                                            if ctx.channel.id in selected_session.server_share:
                                                selected_session.server_share.remove(ctx.channel.id)
                                                with shared_sessions_lock:
                                                    del shared_sessions[ctx.channel.id]
                                                for session in active_sessions.values():
                                                    if session != selected_session and ctx.channel.id in session.server_share:
                                                        session.server_share.remove(ctx.channel.id)
                                                session_channels = []
                                                for channel_id in selected_session.server_share:
                                                    channel = bot.get_channel(channel_id)
                                                    if channel:
                                                        session_channels.append(channel.mention)
                                                session_channels_str = ", ".join(session_channels)
                                                embed = Embed(title="📱  Extension Removed", description=f"{selected_session.unique_name} {selected_session.ctx.channel.mention if hasattr(selected_session.ctx.channel, 'name') else selected_session.ctx.channel.recipient.name + 'DM Channel'}\nExtensions: {session_channels_str}\n\n", color=0x0000FF)
                                                await ctx.send(embed=embed, hidden=True)
                                                return
                                            else:
                                                for session in active_sessions.values():
                                                    if ctx.channel.id in session.server_share:
                                                        session.server_share.remove(ctx.channel.id)
                                                selected_session.server_share.append(ctx.channel.id)
                                                with shared_sessions_lock:
                                                    shared_sessions[ctx.channel.id] = ctx.author.id
                                                session_channels = []
                                                for channel_id in selected_session.server_share:
                                                    channel = bot.get_channel(channel_id)
                                                    if channel:
                                                        session_channels.append(channel.mention)
                                                session_channels_str = ", ".join(session_channels)
                                                embed = Embed(title="📱  Extension Added", description=f"{selected_session.unique_name} {selected_session.ctx.channel.mention if hasattr(selected_session.ctx.channel, 'name') else selected_session.ctx.channel.recipient.name + 'DM Channel'}\nExtensions: {session_channels_str}\n\n", color=0x0000FF)
                                                await ctx.send(embed=embed, hidden=True)
                                                return
                                        else:
                                            if ctx.channel.id in selected_session.server_share:
                                                selected_session.server_share.remove(ctx.channel.id)
                                                with shared_sessions_lock:
                                                    del shared_sessions[ctx.channel.id]
                                                for session in active_sessions.values():
                                                    if session != selected_session and ctx.channel.id in session.server_share:
                                                        session.server_share.remove(ctx.channel.id)
                                                session_channels = []
                                                for channel_id in selected_session.server_share:
                                                    channel = bot.get_channel(channel_id)
                                                    if channel:
                                                        session_channels.append(channel.mention)
                                                session_channels_str = ", ".join(session_channels)
                                                embed = Embed(title="📱  Extension Removed", description=f"{selected_session.unique_name} {selected_session.ctx.channel.mention if hasattr(selected_session.ctx.channel, 'name') else selected_session.ctx.channel.recipient.name + 'DM Channel'}\nExtensions: {session_channels_str}\n\n", color=0x0000FF)
                                                await ctx.send(embed=embed, hidden=True)
                                                return
                                            else:
                                                embed = Embed(title="❌", description="Maximum Extensions Reached...", color=0x0000FF)
                                                await ctx.send(embed=embed, hidden=True)
                                                return
                                    else:
                                        print("Error in assigning Role variable")
                                else:
                                    embed = Embed(title="❌", description="The selected session is not extendable...", color=0x0000FF)
                                    await ctx.send(embed=embed, hidden=True)
                                    return

                            asyncio.create_task(extend_session())
                            return
                        else:
                            embed = Embed(title="❌", description="No session with this number...", color=0x0000FF)
                            await ctx.send(embed=embed, hidden=True)
                            return

    if session_management == "start":
        session_counts = None
        num_sessions = None
        with user_sessions_fetch_lock:
            session_counts = [key for key in user_sessions if key.startswith(f"{author_id}-")]
            num_sessions = len(session_counts)
        
        if role_status in ('limited', 'unlimited', 'data', 'sessions'):
            if role_status == 'limited':
                max_sessions_per_user = 20
            elif role_status == 'unlimited':
                max_sessions_per_user = 20
            elif role_status == 'data':
                max_sessions_per_user = 20
            elif role_status == 'sessions':
                max_sessions_per_user = 20
            
            if num_sessions >= max_sessions_per_user:
                embed = Embed(title="", description="Maximum Number of Sessions In Use\nTo see active sessions and their channels use /manager [session_configuration] [view_sessions]", color=0xFFA500)
                await ctx.send(embed=embed, hidden=True)
                return
            
        elif role_status == 'not_member':
            await join(ctx)
            return
        
        if ctx.guild is None:
            embed = Embed(title="⌛  Initializing...", color=0x00FF00)
            await ctx.send(embed=embed, hidden=True)

        user_id = str(ctx.author.id)
        def generate_session_key(user_id, session_number, channel_id, default):
            session_key = f"{user_id}-{session_number}-{channel_id}-{default}"
            return session_key

        session_numbers = [int(session.split('-')[1]) for session in session_counts]

        session_numbers.sort()

        session_number = 1

        for num in session_numbers:
            if session_number != num:
                break
            session_number += 1

        default = False
        session_key = generate_session_key(user_id, session_number, channel_id, default)
        session = UserSession(ctx, session_number, roleStatus=role_status)

        if session_key in user_sessions:
            user_sessions[session_key].append(session)
        else:
            user_sessions[session_key] = [session]
        active_sessions[session_key] = session

        await session.chat(session_number, default)

# <<--- association management --->>
@slash.slash(name="association-options", 
    description="Add, view, download, upload, or set association options",
    options=[
        create_option( 
            name="manage_associations",
            description="Download, upload, view, clear",
            option_type=3,
            required=False,
            choices=[
                create_choice(
                    name="download",
                    value="download" 
                ),
                create_choice(
                    name="upload",
                    value="upload" 
                ),
                create_choice(
                    name="view",
                    value="view" 
                ),
                create_choice(
                    name="clear",
                    value="clear" 
                ),
            ]
        ),
        create_option(
            name="add_association",
            description="Add associations to session instance",
            option_type=3,
            required=False
        ),
        create_option(
            name="share_associations",
            description="Give a user the ability to create associations",
            option_type=3,
            required=False,
        ),
    ])
async def association(ctx, manage_associations=None, add_association=None, share_associations=None):
    global user_sessions, schedule, bot_login_time, bugs, homeserv

    author_id = ctx.author.id
    channel = ctx.channel
    
    with active_sessions_fetch_lock:
        if any(session.channel_id == channel.id and session.author_id == author_id for session in active_sessions.values()):
            with user_sessions_fetch_lock:
                session_list = [session for key, sessions in user_sessions.items() for session in sessions if key.startswith(f"{author_id}-")]
                if session_list:
                    session = next((session for session in session_list if session.channel_id == channel.id), None)
                    if session is not None:

                        options = (manage_associations, add_association, share_associations)
                        if all(option is None for option in options):
                            embed = Embed(title="Um, this is awkward....", description="Nothing to do", color=0x0000FF)
                            await ctx.send(embed=embed, hidden=True)
                            return

                        if add_association is not None:
                            async def set_association():
                                try:
                                    if '><' in add_association:
                                        old_trigger, new_trigger = add_association.split('><')
                                        old_trigger = old_trigger.strip().lower()
                                        new_trigger = new_trigger.strip().lower()

                                        if old_trigger in session.associations:
                                            associations = session.associations[old_trigger]
                                            del session.associations[old_trigger]
                                            session.associations[new_trigger] = associations
                                            embed = Embed(title="✔️  Association updated!", description=f"{old_trigger} changed to {new_trigger}", color=0x0000FF)
                                            await ctx.send(embed=embed, hidden=True)
                                            return

                                        else:
                                            embed = Embed(title="🗙  That keyword is not in assocations...", description="", color=0x0000FF)
                                            await ctx.send(embed=embed, hidden=True)
                                            return
                                    else:
                                        keyword, association = add_association.split('>>')
                                        keyword = keyword.strip().lower()
                                        association = association.strip()

                                        if keyword in session.associations:
                                            if association == "":
                                                del session.associations[keyword]
                                                embed = Embed(title="✔️  Assocation cleared!", description="", color=0x0000FF)
                                                await ctx.send(embed=embed, hidden=True)
                                                return
                                            else:
                                                associations_to_add = association.split(',')
                                                for item in associations_to_add:
                                                    session.associations[keyword].append(item.strip())
                                                embed = Embed(title="✔️ Association added!", description=f"{keyword} = {association}", color=0x0000FF)
                                                await ctx.send(embed=embed, hidden=True)
                                                return
                                        else:
                                            if association != "":
                                                session.associations[keyword] = [item.strip() for item in association.split(',')]
                                                embed = Embed(title="✔️  Association added!", description=f"{keyword} = {association}", color=0x0000FF)
                                                await ctx.send(embed=embed, hidden=True)
                                                return
                                except Exception as e:
                                    print(f"Error processing association: {e}")
                            asyncio.create_task(set_association())
                            return
                        
                        if share_associations is not None:
                            async def add_shares():
                                try:
                                    if share_associations in session.associations_share:
                                        session.associations_share.remove(share_associations)
                                        embed = Embed(title="✔️  User Removed!", description=f"{share_associations}", color=0x0000FF)
                                        await ctx.send(embed=embed, hidden=True)
                                    else:
                                        session.associations_share.append(share_associations)
                                        embed = Embed(title="✔️  User Added!", description=f"{share_associations}", color=0x0000FF)
                                        await ctx.send(embed=embed, hidden=True)
                                except Exception as e:
                                    print(f"An error occurred: {e}")
                            asyncio.create_task(add_shares())
                            return

                        if manage_associations is not None:
                            if manage_associations == "download":
                                async def download_associations():
                                    try:
                                        embed = Embed(title="", description="Associations sent in direct message!", color=0x0000FF)
                                        await ctx.send(embed=embed, hidden=True)
                                        await session.download_associations()
                                    except Exception as e:
                                        print(f"An error occurred: {e}")
                                asyncio.create_task(download_associations())
                                return
                            
                            elif manage_associations == "upload":
                                async def apply_associations():
                                    try:
                                        embed = Embed(title="", description="Direct message sent!", color=0x0000FF)
                                        await ctx.send(embed=embed, hidden=True)
                                        await session.upload_associations()
                                    except Exception as e:
                                        print(f"An error occurred: {e}")
                                asyncio.create_task(apply_associations())
                                return
                        
                            elif manage_associations == "view":
                                async def view_associations():
                                    try:
                                        trigger_keywords = list(session.associations.keys())
                                        trigger_keywords_string = ", ".join(trigger_keywords)

                                        if trigger_keywords_string:
                                            paragraphs = [trigger_keywords_string[i:i+4000] for i in range(0, len(trigger_keywords_string), 1500)]

                                            for i, paragraph in enumerate(paragraphs):
                                                embed = discord.Embed(title="Current Associations", description=paragraph, color=discord.Color.blue())
                                                if i == 0:
                                                    await ctx.send(embed=embed, hidden=True)
                                                else:
                                                    await ctx.send(embed=embed, hidden=True)
                                                    await asyncio.sleep(1)
                                        else:
                                            embed = discord.Embed(title="", description="No associations found...", color=discord.Color.blue())
                                            await ctx.send(embed=embed, hidden=True)
                                    except Exception as e:
                                        print(f"An error occurred: {e}")
                                asyncio.create_task(view_associations())

                            elif manage_associations == "clear":
                                async def associations_clear():
                                    try:
                                        session.associations = {}
                                        embed = Embed(title="", description="Associations Cleared!", color=0x0000FF)
                                        await ctx.send(embed=embed, hidden=True)
                                    except Exception as e:
                                        print(f"An error occurred: {e}")
                                asyncio.create_task(associations_clear())
                                return

        else:
            embed = Embed(title="Um, this is awkward....", description="*No session matching this channel, check your sessions with `/manager [ session_management ] [ sessions ]`", color=0x0000FF)
            await ctx.send(embed=embed, hidden=True)

# <<--- OpenAI API configurations --->>
@slash.slash(name="openai-options", 
    description="Set OpenAI configurations for chat, image, and visual",
    options=[
        create_option(
            name="add_prompt",
            description="Add a prompt to be used in text chat",
            option_type=3,
            required=False
        ),
        create_option(
            name="manage_prompt",
            description="View or clear the current prompt",
            option_type=3,
            required=False,
            choices=[
                create_choice(
                    name="view",
                    value="view"
                ),
                create_choice(
                    name="clear",
                    value="clear"
                ),
            ]
        ),
        create_option(
            name="user_prompt",
            description="Give a prompt to a specific member",
            option_type=3,
            required=False,
        ),
        create_option(
            name="user_role",
            description="Give an AI role to a member",
            option_type=3,
            required=False,
        ),
        create_option(
            name="model",
            description="Set the text model to use",
            option_type=3,
            required=False,
            choices=[
                create_choice(
                    name="custom",
                    value="custom"
                ),
                create_choice(
                    name="gpt 3.5",
                    value="gpt-3.5-turbo"
                ),
                create_choice(
                    name="gpt 4",
                    value="gpt-4"
                ),
                create_choice(
                    name="gpt-4-1106-preview",
                    value="gpt-4-1106-preview"
                ),
                create_choice(
                    name="gpt-4-0613",
                    value="gpt-4-0613"
                ),
                create_choice(
                    name="gpt-4-0314",
                    value="gpt-4-0314"
                ),
                create_choice(
                    name="gpt-3.5-turbo-16k-0613",
                    value="gpt-3.5-turbo-16k-0613"
                ),
                create_choice(
                    name="gpt-3.5-turbo-16k",
                    value="gpt-3.5-turbo-16k"
                ),
                create_choice(
                    name="gpt-3.5-turbo-1106",
                    value="gpt-3.5-turbo-1106"
                ),
                create_choice(
                    name="gpt-3.5-turbo-0613",
                    value="gpt-3.5-turbo-0613"
                ),
                create_choice(
                    name="gpt-3.5-turbo-0301",
                    value="gpt-3.5-turbo-0301"
                ),
            ]
        ),
        create_option(
            name="api_base",
            description="Add endpoint for custom model, use 'default' for OpenAI",
            option_type=3,
            required=False
        ),
        create_option(
            name="assistant",
            description="Set an assistant to use",
            option_type=3,
            required=False,
            choices=[
                create_choice(
                    name="interpreter",
                    value="code_interpreter"
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
                create_choice(
                    name="1.2",
                    value="1.2"
                ),
                create_choice(
                    name="1.4",
                    value="1.4"
                ),
                create_choice(
                    name="1.6",
                    value="1.6"
                ),
                create_choice(
                    name="1.8",
                    value="1.8"
                ),
                create_choice(
                    name="2",
                    value="2"
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
                create_choice(
                    name="3000",
                    value="3000"
                ),
                create_choice(
                    name="3500",
                    value="3500"
                ),
                create_choice(
                    name="4000",
                    value="4000"
                ),
            ]
        ),
        create_option(
            name="role",
            description="Set OpenAI role",
            option_type=3,
            required=False,
            choices=[
                create_choice(
                    name="user",
                    value="user"
                ),
                create_choice(
                    name="system",
                    value="system"
                ),
            ]
        ),
        create_option(
            name="frequency",
            description="Set the frequency penalty",
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
                create_choice(
                    name="1.2",
                    value="1.2"
                ),
                create_choice(
                    name="1.4",
                    value="1.4"
                ),
                create_choice(
                    name="1.6",
                    value="1.6"
                ),
                create_choice(
                    name="1.8",
                    value="1.8"
                ),
                create_choice(
                    name="2",
                    value="2"
                ),
            ]
        ),
        create_option(
            name="presence",
            description="Set the presence penalty",
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
                create_choice(
                    name="1.2",
                    value="1.2"
                ),
                create_choice(
                    name="1.4",
                    value="1.4"
                ),
                create_choice(
                    name="1.6",
                    value="1.6"
                ),
                create_choice(
                    name="1.8",
                    value="1.8"
                ),
                create_choice(
                    name="2",
                    value="2"
                ),
            ]
        ),
        create_option(
            name="top_p",
            description="Set the probability cutoff",
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
                create_choice(
                    name="1",
                    value="1"
                ),
            ]
        ),
        create_option(
            name="top_k",
            description="Use in custom models",
            option_type=3,
            required=False
        ),
        create_option(
            name="repeat_penalty",
            description="Use in custom models",
            option_type=3,
            required=False
        ),
        create_option(
            name="custom_model_name",
            description="Set custom model name, default 'local-model'",
            option_type=3,
            required=False
        ),
        create_option(
            name="image_model",
            description="Set image model to use",
            option_type=3,
            required=False,
            choices=[
                create_choice(
                    name="dalle2",
                    value="dalle2"
                ),
                create_choice(
                    name="dalle3",
                    value="dalle3"
                ),
            ]
        ),
        create_option(
            name="style",
            description="Set style for DALL E 3 only",
            option_type=3,
            required=False,
            choices=[
                create_choice(
                    name="vivid",
                    value="vivid"
                ),
                create_choice(
                    name="natural",
                    value="natural"
                ),
            ]
        ),
        create_option(
            name="size",
            description="Set image size for DALLE to generate",
            option_type=3,
            required=False,
            choices=[
                create_choice(
                    name="256x256",
                    value="256x256"
                ),
                create_choice(
                    name="512x512",
                    value="512x512"
                ),
                create_choice(
                    name="1024x1024",
                    value="1024x1024"
                ),
                create_choice(
                    name="1024x1792",
                    value="1024x1792"
                ),
                create_choice(
                    name="1792x1024",
                    value="1792x1024"
                ),
            ]
        ),
        create_option(
            name="number",
            description="Set number of images to return",
            option_type=3,
            required=False,
            choices=[
                create_choice(
                    name="1",
                    value="1"
                ),
                create_choice(
                    name="2",
                    value="2"
                ),
                create_choice(
                    name="3",
                    value="3"
                ),
                create_choice(
                    name="4",
                    value="4"
                ),
                create_choice(
                    name="5",
                    value="5"
                ),
                create_choice(
                    name="6",
                    value="6"
                ),
                create_choice(
                    name="7",
                    value="7"
                ),
                create_choice(
                    name="8",
                    value="8"
                ),
                create_choice(
                    name="9",
                    value="9"
                ),
                create_choice(
                    name="10",
                    value="10"
                ),
                create_choice(
                    name="11",
                    value="11"
                ),
                create_choice(
                    name="12",
                    value="12"
                ),
                create_choice(
                    name="13",
                    value="13"
                ),
                create_choice(
                    name="14",
                    value="14"
                ),
                create_choice(
                    name="15",
                    value="15"
                ),
                create_choice(
                    name="16",
                    value="16"
                ),
                create_choice(
                    name="17",
                    value="17"
                ),
                create_choice(
                    name="18",
                    value="18"
                ),
                create_choice(
                    name="19",
                    value="19"
                ),
                create_choice(
                    name="20",
                    value="20"
                ),
            ]
        ),
        create_option(
            name="revised_prompt",
            description="Returns DALLE3 revised prompt with images",
            option_type=3,
            required=False,
            choices=[
                create_choice(
                    name="enable",
                    value="True"
                ),
                create_choice(
                    name="disable",
                    value="False"
                ),
            ]
        ),
    ])
async def openai_config(ctx, add_prompt=None, manage_prompt=None, user_prompt=None, user_role=None, model=None, custom_model_name=None, top_k=None, repeat_penalty=None, api_base=None, assistant=None, temperature=None, tokens=None, role=None, frequency=None, presence=None, top_p=None, image_model=None, style=None, size=None, number=None, revised_prompt=None):
    global user_sessions, schedule, bot_login_time, bugs, homeserv

    author_id = ctx.author.id    
    channel = ctx.channel

    with active_sessions_fetch_lock:
        if any(session.channel_id == channel.id and session.author_id == author_id for session in active_sessions.values()):
            with user_sessions_fetch_lock:
                session_list = [session for key, sessions in user_sessions.items() for session in sessions if key.startswith(f"{author_id}-")]
                if session_list:
                    session = next((session for session in session_list if session.channel_id == channel.id), None)
                    if session is not None:

                        options = (add_prompt, manage_prompt, user_prompt, user_role, model, assistant, temperature, tokens, role, frequency, presence, top_p, top_k, repeat_penalty, custom_model_name, api_base, image_model, style, size, number, revised_prompt)
                        if all(option is None for option in options):
                            async def get_stats_task(ctx, session):
                                try:
                                    role_index = session.role["user_id"].index(author_id)
                                    prompt_value = session.role["prompt"][role_index]
                                    if len(prompt_value) > 100:
                                        prompt_value = prompt_value[:100] + "..."
                                    role_list = session.role.get("user_role", [])
                                    role_value = role_list[role_index] if role_index < len(role_list) else None
                                    tokens_value = session.tokens
                                    temperature_value = session.temperature
                                    session_number_value = session.session_number
                                    session_style_value = session.style
                                    model_value = session.model
                                    size_value = session.size
                                    number_value = session.number
                                    name_value = session.unique_name
                                    presence_value = session.presence
                                    frequency_value = session.frequency
                                    top_p_value = session.top_p
                                    top_k_value = session.top_k 
                                    repeat_penalty_value = session.repeat_penalty 
                                    model_value = session.model
                                    api_base_value = session.api_base 
                                    custom_model_name_value = session.custom_model_name 
                                    image_model_value = session.image_model
                                    session_toggle_prompt = session.revised_prompt

                                    embed = Embed(title="⚙️  Session Stats", description="", color=0x0000FF)
                                    embed.add_field(name=f"ℹ️  **| Session** {session_number_value} **Name:** {name_value}\n\n", value=f"", inline=False)
                                    embed.add_field(name="🎛️ **| OpenAI Config**", value=f"- **Model:** {model_value}\n- **API Base:** {api_base_value}\n- **Model Name:** {custom_model_name_value}\n- **Tokens:** {tokens_value}\n- **Temperature:** {temperature_value}\n- **Role:** {role_value}\n- **Presence:** {presence_value}\n- **Frequency:** {frequency_value}\n- **Top_P:** {top_p_value}\n- **Top_K:** {top_k_value}\n- **Repeat Penalty:** {repeat_penalty_value}", inline=True)
                                    embed.add_field(name="🎨 **| DALLE Config**", value=f"- **Model:** {image_model_value}\n- **Style:** {session_style_value}\n- **Number:** {number_value}\n- **Size:** {size_value}\n- Toggles: {session_toggle_prompt}*Note: number, size, and variations are None in Dalle 3 currently*", inline=True)
                                    embed.add_field(name="🗒️ **| Prompt:**", value=f"{prompt_value}", inline=True)
                                    embed.set_footer(text="Use /ether [manager] [prompt-view] to view full prompt or /ether [manager] [sessions] to see all sessions & extensions. Use /ether [manager] [session-save] OR [session-load] to save or load a session configuration.")
                                    await ctx.send(embed=embed, hidden=True)
                                    
                                except Exception as e:
                                    print(f"Error displaying stats card: {e}")
                            asyncio.create_task(get_stats_task(ctx, session))
                            return

                        if add_prompt is not None and (user_prompt is None and user_role is None):
                            async def add_session_prompt():
                                try:
                                    if author_id in session.role["user_id"]:
                                        index = session.role["user_id"].index(author_id)
                                        session.role["prompt"][index] = add_prompt  
                                except Exception as e:
                                    embed = Embed(title="Prompt Error", description="", color=0x0000FF)
                                    await ctx.send(embed=embed, hidden=True)
                                    print(e)

                            asyncio.create_task(add_session_prompt())

                        if user_prompt is not None or user_role is not None:
                            if user_role is None and user_prompt is None:
                                embed = Embed(title="Error", description="You must include a role or prompt to give to the user", color=0x0000FF)
                                await ctx.send(embed=embed, hidden=True)
                                return
                            
                            async def generate_new_role_entry(role, add_prompt):
                                try:
                                    user_id = user_prompt if user_prompt else user_role  
                                    user_id = re.search(r'\d+', user_id).group()  
                                    user_id = int(user_id)  
                                    if user_id not in session.role["user_id"]:
                                        session.role["user_id"].append(user_id)
                                        if role is None:
                                            role = 'user'
                                        session.role["user_role"].append(role)
                                        if add_prompt is None:
                                            add_prompt = ''
                                        session.role["prompt"].append(add_prompt)
                                    else:
                                        index = session.role["user_id"].index(user_id)
                                        if role is not None:
                                            session.role["user_role"][index] = role
                                        if add_prompt is not None:
                                            session.role["prompt"][index] = add_prompt
                                except Exception as e:
                                    embed = Embed(title="Role entry error", description="", color=0x0000FF)
                                    await ctx.send(embed=embed, hidden=True)

                            asyncio.create_task(generate_new_role_entry(role, add_prompt))
                            
                        if manage_prompt is not None:
                            async def manage_session_prompt():
                                try:
                                    role_index = session.role["user_id"].index(author_id)
                                    prompt_text = session.role["prompt"][role_index]
                                
                                    if manage_prompt == "view":
                                        if len(prompt_text) > 1500:
                                            chunks = []
                                            while len(prompt_text) > 1500:
                                                last_period_index = prompt_text[:1500].rfind(".")
                                                if last_period_index != -1:
                                                    chunk = prompt_text[:last_period_index+1].strip()
                                                    prompt_text = prompt_text[last_period_index+1:].strip()
                                                else:
                                                    chunk = prompt_text[:1500].strip()
                                                    prompt_text = prompt_text[1500:].strip()
                                                chunks.append(chunk)
                                            chunks.append(prompt_text)
                                            for i, chunk in enumerate(chunks):
                                                embed = Embed(title=f"⚙️  Session Prompt (Part {i+1})", description=chunk, color=0x0000FF)
                                                await ctx.send(embed=embed, hidden=True)
                                                return
                                        else:
                                            embed = Embed(title="⚙️  Session Prompt", description=prompt_text, color=0x0000FF)
                                            await ctx.send(embed=embed, hidden=True)
                                            return

                                    elif manage_prompt == "clear":
                                        session.role["prompt"][role_index] = ''
                                        embed = Embed(title="", description="⚙️  Prompt Cleared!", color=0x0000FF)
                                        await ctx.send(embed=embed, hidden=True)
                                        return

                                except Exception as e:
                                    embed = Embed(title="Manage prompt error", description="", color=0x0000FF)
                                    await ctx.send(embed=embed, hidden=True)
                            asyncio.create_task(manage_session_prompt())
                            return
                            
                        if model is not None:
                            async def set_model():
                                try:
                                    if model == "custom":
                                        session.api_engine = "custom"
                                    else:
                                        session.model = model
                                        session.api_engine = "openai"
                                except Exception as e:
                                    embed = Embed(title="Model Error", description="", color=0x0000FF)
                                    await ctx.send(embed=embed, hidden=True)
                            asyncio.create_task(set_model())

                        if temperature is not None:
                            async def set_temperature():
                                try:
                                    session.temperature = float(temperature)
                                except Exception as e:
                                    embed = Embed(title="Temperature Error", description="", color=0x0000FF)
                                    await ctx.send(embed=embed, hidden=True)
                            asyncio.create_task(set_temperature())

                        if tokens is not None:
                            async def set_tokens():
                                try:
                                    session.tokens = int(tokens)
                                except Exception as e:
                                    embed = Embed(title="Token Error", description="", color=0x0000FF)
                                    await ctx.send(embed=embed, hidden=True)
                            asyncio.create_task(set_tokens())

                        if role is not None and (user_prompt is None and user_role is None):
                            async def set_role():
                                try:
                                    role_index = session.role["user_id"].index(author_id)
                                    session.role["user_role"][role_index] = role
                                except Exception as e:
                                    embed = Embed(title="Role Error", description="", color=0x0000FF)
                                    await ctx.send(embed=embed, hidden=True)
                            asyncio.create_task(set_role())

                        if frequency is not None:
                            async def set_frequency():
                                try:
                                    session.frequency = float(frequency)
                                except Exception as e:
                                    embed = Embed(title="Frequency Error", description="", color=0x0000FF)
                                    await ctx.send(embed=embed, hidden=True)
                            asyncio.create_task(set_frequency())

                        if presence is not None:
                            async def set_presence():
                                try:
                                    session.presence = float(presence)
                                except Exception as e:
                                    embed = Embed(title="Presence Error", description="", color=0x0000FF)
                                    await ctx.send(embed=embed, hidden=True)
                            asyncio.create_task(set_presence())

                        if top_p is not None:
                            async def set_top_p():
                                try:
                                    session.top_p = float(top_p)
                                except Exception as e:
                                    embed = Embed(title="Top_P Error", description="", color=0x0000FF)
                                    await ctx.send(embed=embed, hidden=True)
                            asyncio.create_task(set_top_p())

                        if image_model is not None:
                            async def set_image_model():
                                try:
                                    session.image_model = image_model
                                except Exception as e:
                                    embed = Embed(title="model Error", description="", color=0x0000FF)
                                    await ctx.send(embed=embed, hidden=True)
                            asyncio.create_task(set_image_model())

                        if style is not None:
                            async def set_style():
                                try:
                                    session.style = style
                                except Exception as e:
                                    embed = Embed(title="Style Error", description="", color=0x0000FF)
                                    await ctx.send(embed=embed, hidden=True)
                            asyncio.create_task(set_style())

                        if size is not None:
                            async def set_size():
                                try:
                                    session.size = size
                                except Exception as e:
                                    embed = Embed(title="Image Error", description="", color=0x0000FF)
                                    await ctx.send(embed=embed, hidden=True)
                            asyncio.create_task(set_size())

                        if number is not None:
                            async def set_number():
                                try:
                                    session.number = int(number)
                                except Exception as e:
                                    embed = Embed(title="Image Error", description="", color=0x0000FF)
                                    await ctx.send(embed=embed, hidden=True)
                            asyncio.create_task(set_number())

                        if revised_prompt is not None:
                            async def set_revised_prompt():
                                try:
                                    if revised_prompt == "True":
                                        session.revised_prompt = True
                                    elif revised_prompt == "False":
                                        session.revised_prompt = False
                                except Exception as e:
                                    embed = Embed(title="Revised Prompt Error", description="", color=0x0000FF)
                                    await ctx.send(embed=embed, hidden=True)
                            asyncio.create_task(set_revised_prompt())

                        if api_base is not None:
                            async def set_api_base():
                                try:
                                    if api_base == "default":
                                        session.api_base = session.api_base_default
                                    else:
                                        session.api_base = api_base
                                except Exception as e:
                                    embed = Embed(title="API Base Error", description="", color=0x0000FF)
                                    await ctx.send(embed=embed, hidden=True)
                            asyncio.create_task(set_api_base())

                        if top_k is not None:
                            async def set_top_k():
                                try:
                                    session.top_k = float(top_k)
                                except Exception as e:
                                    embed = Embed(title="Top_K Error", description="", color=0x0000FF)
                                    await ctx.send(embed=embed, hidden=True)
                            asyncio.create_task(set_top_k())

                        if repeat_penalty is not None:
                            async def set_repeat_penalty():
                                try:
                                    session.repeat_penalty = float(repeat_penalty)
                                except Exception as e:
                                    embed = Embed(title="Repeat Penalty Error", description="", color=0x0000FF)
                                    await ctx.send(embed=embed, hidden=True)
                            asyncio.create_task(set_repeat_penalty())

                        if custom_model_name is not None:
                            async def set_custom_model_name():
                                try:
                                    session.model = (custom_model_name)
                                except Exception as e:
                                    embed = Embed(title="Custom Model Name Error", description="", color=0x0000FF)
                                    await ctx.send(embed=embed, hidden=True)
                            asyncio.create_task(set_custom_model_name())

                        combined_objects = None
                        options = {
                            'add_prompt': add_prompt,
                            'manage_prompt': manage_prompt,
                            'user_role': user_role,
                            'user_prompt': user_prompt,
                            'model': model,
                            'api_base': api_base,
                            'assistant': assistant,
                            'temperature': temperature,
                            'tokens': tokens,
                            'role': role,
                            'frequency': frequency,
                            'presence': presence,
                            'top_p': top_p,
                            'top_k': top_k,
                            'api_base': api_base,
                            'repeat_penalty': repeat_penalty,
                            'custom_model_name': custom_model_name,
                            'image_model': image_model,
                            'style': style,
                            'size': size,
                            'number': number,
                            'revised_prompt': revised_prompt
                        }

                        combined_objects = "\n".join([f"- {option}: {value}" for option, value in options.items() if value is not None and option != 'add_prompt'])

                        if add_prompt:
                            truncated_prompt = ' '.join(add_prompt.split()[:25]) + '...'

                            embed_description = f"{combined_objects}\n- Prompt: {truncated_prompt}"

                            embed = Embed(title="✅  Session Configuration Updated!", description=embed_description, color=0x00FF00)
                            await ctx.send(embed=embed, hidden=True)
                        else:
                            embed = Embed(title="✅  Session Configuration Updated!", description=combined_objects, color=0x00FF00)
                            await ctx.send(embed=embed, hidden=True)

        else:
            embed = Embed(title="Um, this is awkward....", description="*No session matching this channel, check your sessions with `/manager [ session_management ] [ sessions ]`", color=0x0000FF)
            await ctx.send(embed=embed, hidden=True)

# <<--- sharing options and management --->>
@slash.slash(name="sharing-options", 
    description="Set session sharing options, invoke with no args to see shares",
    options=[
        create_option(
            name="view_shares",
            description="View current shares",
            option_type=3,
            required=False,
            choices=[
                create_choice(
                    name="all",
                    value="All"
                ),
                create_choice(
                    name="roles",
                    value="Roles"
                ),
                create_choice(
                    name="users",
                    value="Users"
                ),
            ]
        ),
        create_option(
            name="role_share",
            description="Give a role the ability to access session",
            option_type=8,
            required=False,
        ),
        create_option(
            name="user_share",
            description="Share access with a specific user",
            option_type=3,
            required=False,
        ),
        create_option(
            name="time",
            description="Define amount of time for user or role to have access",
            option_type=3,
            required=False,
        ),
        create_option(
            name="iterations",
            description="Define number of iterations for a role or user to have",
            option_type=3,
            required=False,
        ),
        create_option(
            name="share_type",
            description="Set the share type for all, user, or role",
            option_type=3,
            required=False,
            choices=[
                create_choice(
                    name="all",
                    value="All"
                ),
                create_choice(
                    name="chat",
                    value="Chat"
                ),
                create_choice(
                    name="image",
                    value="Image"
                ),
                create_choice(
                    name="visual",
                    value="Visual"
                ),
                create_choice(
                    name="fast_embed",
                    value="Fast_Embed"
                ),
                create_choice(
                    name="full_embed",
                    value="Full_Embed"
                ),
                create_choice(
                    name="set",
                    value="Set"
                ),
            ]
        ),
    ])
async def sharing_config(ctx, share_type=None, role_share=None, user_share=None, time=None, iterations=None, view_shares=None):
    global user_sessions, schedule, bot_login_time, bugs, homeserv, shared_sessions

    author_id = ctx.author.id
    channel = ctx.channel

    if isinstance(ctx.channel, discord.DMChannel):
        embed = Embed(title="", description=f"❌  No Share Options in Direct Message", color=0x0000FF)
        await ctx.send(embed=embed, hidden=True)
        return
    
    with active_sessions_fetch_lock:
        if any(session.channel_id == channel.id and session.author_id == author_id for session in active_sessions.values()):
            with user_sessions_fetch_lock:
                session_list = [session for key, sessions in user_sessions.items() for session in sessions if key.startswith(f"{author_id}-")]
                if session_list:
                    session = next((session for session in session_list if session.channel_id == channel.id), None)
                    if session is not None:      

                        options = (share_type, role_share, user_share, time, iterations, view_shares)
                        if all(option is None for option in options):
                            async def show_shares(): 
                                user_shares = ""
                                for user, share_data in session.user_share.items():
                                    current_time = datetime.datetime.now()
                                    time_limit = share_data.get('time')
                                    timestamp = datetime.datetime.strptime(share_data.get('timestamp'), "%Y-%m-%d %H:%M:%S")
                                    time_difference = current_time - timestamp
                                    time_status = ''
                                    if time_limit is not None and time_limit != "0":
                                        time_status = 'expired' if time_difference.total_seconds() >= session.parse_time_limit(time_limit).total_seconds() else 'active'

                                    user_shares += f"- User: {user}\n"
                                    user_shares += f"  - Time: {share_data.get('time')} {time_status}\n"
                                    user_shares += f"  - Iterations: {share_data.get('iterations')}\n"
                                    share_types = ', '.join(share_data.get('share_types'))  
                                    user_shares += f"  - Share Types: {share_types}\n" 

                                role_shares = ""
                                for role, share_data in session.role_share.items():
                                    current_time = datetime.datetime.now()
                                    time_limit = share_data.get('time')
                                    timestamp = datetime.datetime.strptime(share_data.get('timestamp'), "%Y-%m-%d %H:%M:%S")
                                    time_difference = current_time - timestamp
                                    time_status = ''
                                    if time_limit is not None and time_limit != "0":
                                        time_status = 'expired' if time_difference.total_seconds() >= session.parse_time_limit(time_limit).total_seconds() else 'active'

                                    role_shares += f"- Role: {role}\n"
                                    role_shares += f"  - Time: {share_data.get('time')} ({time_status})\n"
                                    role_shares += f"  - Iterations: {share_data.get('iterations')}\n"
                                    share_types = ', '.join(share_data.get('share_types'))  
                                    role_shares += f"  - Share Types: {share_types}\n"  

                                embed = Embed(title="Active Shares", description=f"{user_shares}{role_shares}", color=0x0000FF)
                                await ctx.send(embed=embed, hidden=True)
                            asyncio.create_task(show_shares())

                        if view_shares is not None:
                            async def show_shares():
                                if view_shares == "All":
                                    user_shares = ""
                                    for user, share_data in session.user_share.items():
                                        current_time = datetime.datetime.now()
                                        time_limit = share_data.get('time')
                                        timestamp = datetime.datetime.strptime(share_data.get('timestamp'), "%Y-%m-%d %H:%M:%S")
                                        time_difference = current_time - timestamp
                                        time_status = ''
                                        if time_limit is not None and time_limit != "0":
                                            time_status = 'expired' if time_difference.total_seconds() >= session.parse_time_limit(time_limit).total_seconds() else 'active'

                                        user_shares += f"- User: {user}\n"
                                        user_shares += f"  - Time: {share_data.get('time')} {time_status}\n"
                                        user_shares += f"  - Iterations: {share_data.get('iterations')}\n"
                                        share_types = ', '.join(share_data.get('share_types'))  
                                        user_shares += f"  - Share Types: {share_types}\n"  

                                    role_shares = ""
                                    for role, share_data in session.role_share.items():
                                        current_time = datetime.datetime.now()
                                        time_limit = share_data.get('time')
                                        timestamp = datetime.datetime.strptime(share_data.get('timestamp'), "%Y-%m-%d %H:%M:%S")
                                        time_difference = current_time - timestamp
                                        time_status = ''
                                        if time_limit is not None and time_limit != "0":
                                            time_status = 'expired' if time_difference.total_seconds() >= session.parse_time_limit(time_limit).total_seconds() else 'active'

                                        role_shares += f"- Role: {role}\n"
                                        role_shares += f"  - Time: {share_data.get('time')} ({time_status})\n"
                                        role_shares += f"  - Iterations: {share_data.get('iterations')}\n"
                                        share_types = ', '.join(share_data.get('share_types'))  
                                        role_shares += f"  - Share Types: {share_types}\n" 

                                    embed = Embed(title="Active Shares", description=f"{user_shares}{role_shares}", color=0x0000FF)
                                    await ctx.send(embed=embed, hidden=True)

                                elif view_shares == "Users":
                                    user_shares = ""
                                    for user, share_data in session.user_share.items():
                                        current_time = datetime.datetime.now()
                                        time_limit = share_data.get('time')
                                        timestamp = datetime.datetime.strptime(share_data.get('timestamp'), "%Y-%m-%d %H:%M:%S")
                                        time_difference = current_time - timestamp
                                        time_status = ''
                                        if time_limit is not None and time_limit != "0":
                                            time_status = 'expired' if time_difference.total_seconds() >= session.parse_time_limit(time_limit).total_seconds() else 'active'

                                        user_shares += f"- User: {user}\n"
                                        user_shares += f"  - Time: {share_data.get('time')} ({time_status})\n"
                                        user_shares += f"  - Iterations: {share_data.get('iterations')}\n"
                                        share_types = ', '.join(share_data.get('share_types'))  
                                        user_shares += f"  - Share Types: {share_types}\n"  

                                    embed = Embed(title="Active User Shares", description=f"{user_shares}", color=0x0000FF)
                                    await ctx.send(embed=embed, hidden=True)

                                elif view_shares == "Roles":
                                    role_shares = ""
                                    for role, share_data in session.role_share.items():
                                        current_time = datetime.datetime.now()
                                        time_limit = share_data.get('time')
                                        timestamp = datetime.datetime.strptime(share_data.get('timestamp'), "%Y-%m-%d %H:%M:%S")
                                        time_difference = current_time - timestamp
                                        time_status = ''
                                        if time_limit is not None and time_limit != "0":
                                            time_status = 'expired' if time_difference.total_seconds() >= session.parse_time_limit(time_limit).total_seconds() else 'active'

                                        role_shares += f"- Role: {role}\n"
                                        role_shares += f"  - Time: {share_data.get('time')} ({time_status})\n"
                                        role_shares += f"  - Iterations: {share_data.get('iterations')}\n"
                                        share_types = ', '.join(share_data.get('share_types'))  
                                        role_shares += f"  - Share Types: {share_types}\n"  

                                    embed = Embed(title="Active Role Shares", description=f"{role_shares}", color=0x0000FF)
                                    await ctx.send(embed=embed, hidden=True)

                            asyncio.create_task(show_shares())
                            return

                        if user_share is not None or role_share is not None:
                            global_shared = None
                            with shared_sessions_lock:
                                global_shared = ctx.channel.id in shared_sessions

                            if global_shared is not None:
                                if ctx.channel.id in shared_sessions and shared_sessions[ctx.channel.id] != ctx.author.id:
                                    embed = Embed(title="❌  Another session is being shared in this channel", description="", color=0x0000FF)
                                    await ctx.send(embed=embed, hidden=True)
                                    return

                            async def add_user_share_chat():
                                try:
                                    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    if user_share is not None or role_share is not None:
                                        if user_share is not None and role_share is not None:
                                            embed = Embed(title="❌  Share Error", description="Cannot add roles and users at same time", color=0x0000FF)
                                            await ctx.send(embed=embed, hidden=True)
                                            return
                                        
                                        if time is None and iterations is None and share_type is None:
                                            if user_share is not None:
                                                if user_share in session.user_share:
                                                    del session.user_share[user_share]
                                                    if not session.user_share and not session.role_share:
                                                        del shared_sessions[ctx.channel.id]

                                                    embed = Embed(title=f"✅  Removed: {user_share} from shares", description=f"", color=0x0000FF)
                                                    await ctx.send(embed=embed, hidden=True)
                                                    return

                                            else:
                                                if role_share in session.role_share:
                                                    del session.role_share[role_share]
                                                    if not session.user_share and not session.role_share:
                                                        del shared_sessions[ctx.channel.id]
                                                    embed = Embed(title=f"✅  Removed: {role_share} from shares", description=f"", color=0x0000FF)
                                                    await ctx.send(embed=embed, hidden=True)
                                                    return   
                                        
                                        # Early conflict check
                                        with shared_sessions_lock:
                                            server_share_copy = session.server_share.copy()
                                            for channel_id in server_share_copy:
                                                if channel_id in shared_sessions:
                                                    if len(session.server_share) == 1 and session.server_share[0] == channel_id:
                                                        session.server_share.remove(channel_id)
                                                    
                                            for channel_id in session.server_share:
                                                if channel_id not in shared_sessions:
                                                    if session.user_share or session.role_share:
                                                        shared_sessions[channel_id] = ctx.author.id
                                                        session.server_share.append(channel_id)
                                                    else:
                                                        session.server_share.append(channel_id)
                                                elif session.user_share or session.role_share:
                                                    continue
                                                else:
                                                    if channel_id not in session.server_share:
                                                        session.server_share.append(channel_id)

                                        share_types = []
                                        share_time = None
                                        share_iterations = 0 
                                        existing_share_types = []   
                                        if share_type == "All":
                                            share_types = ["Image", "Chat", "Fast_Embed", "Full_Embed", "Visual", "Set"]
                                            if user_share is not None:
                                                if user_share in session.user_share:
                                                    existing_share_types = session.user_share[user_share].get("share_types", [])
                                                    share_types = list(set(share_types) - set(existing_share_types)) + existing_share_types
                                            else:
                                                if role_share in session.role_share:
                                                    existing_share_types = session.role_share[role_share].get("share_types", [])
                                                    share_types = list(set(share_types) - set(existing_share_types)) + existing_share_types
                                         
                                        else:
                                            if user_share is not None:
                                                if user_share in session.user_share:
                                                    existing_share_types = session.user_share[user_share].get("share_types", [])
                                            else: 
                                                if role_share in session.role_share:
                                                    existing_share_types = session.role_share[role_share].get("share_types", [])

                                            if share_type is None:
                                                share_types = existing_share_types
                                            else:
                                                if share_type in existing_share_types:
                                                    existing_share_types.remove(share_type)
                                                    share_types = existing_share_types
                                                else: 
                                                    if existing_share_types:
                                                        share_types = existing_share_types + [share_type]
                                                    else:
                                                        share_types = [share_type]

                                        if iterations is None:
                                            if user_share is not None:
                                                if user_share in session.user_share:
                                                    share_iterations_original = session.user_share[user_share].get("iterations", 0)
                                                    share_iterations = share_iterations_original + share_iterations 
                                                else:
                                                    share_iterations = 0
                                            elif role_share is not None:
                                                if role_share in session.role_share:
                                                    share_iterations_original = session.role_share[role_share].get("iterations", 0)
                                                    share_iterations = share_iterations_original + share_iterations  
                                                else:
                                                    share_iterations = 0
                                        else:
                                            share_iterations = int(iterations)

                                        if time is None:
                                            if user_share is not None:
                                                if user_share in session.user_share:
                                                    share_time = session.user_share[user_share].get("time", "0")
                                                else:
                                                    share_time = '0' 
                                            else:
                                                if role_share in session.role_share:
                                                    share_time = session.role_share[role_share].get("time", "0")
                                                else:
                                                    share_time = '0'  
                                        else:
                                            share_time = time

                                        if user_share is not None:
                                            session.user_share[user_share] = {
                                                "iterations": share_iterations,
                                                "time": share_time,
                                                "timestamp": current_time,
                                                "share_types": share_types
                                            }
                                        else:
                                            session.role_share[role_share] = {
                                                "iterations": share_iterations,
                                                "time": share_time,
                                                "timestamp": current_time,
                                                "share_types": share_types
                                            }

                                        share_subject = None
                                        if user_share is not None:
                                            share_subject = user_share
                                            existing_share_types = session.user_share[user_share].get("share_types")
                                            existing_share_iterations = session.user_share[user_share].get("iterations")
                                            existing_share_time = session.user_share[user_share].get("time")
                                        else: 
                                            share_subject = role_share
                                            existing_share_types = session.role_share[role_share].get("share_types")
                                            existing_share_iterations = session.role_share[role_share].get("iterations")
                                            existing_share_time = session.role_share[role_share].get("time")

                                        share_types_str = ", ".join(existing_share_types)

                                        embed = Embed(title="✅  Added Share!", description=f"- Shared: {share_subject}\n- Iterations: {existing_share_iterations}\n- Time: {existing_share_time}\n- Access: {share_types_str}", color=0x0000FF)
                                        await ctx.send(embed=embed, hidden=True)
                                        
                                    else:
                                        embed = Embed(title="❌  Share Error", description="Must select either a user or role to share with", color=0x0000FF)
                                        await ctx.send(embed=embed, hidden=True)

                                    with shared_sessions_lock:
                                        if ctx.channel.id not in shared_sessions:
                                            shared_sessions[ctx.channel.id] = ctx.author.id
                                        for channel_id in session.server_share:
                                            if channel_id not in shared_sessions:
                                                shared_sessions[channel_id] = ctx.author.id

                                except Exception as e:
                                    print(f"Share Error: {e}")
                                    embed = Embed(title="❌  Share Error", description="", color=0x0000FF)
                                    await ctx.send(embed=embed, hidden=True)

                            asyncio.create_task(add_user_share_chat())

        else:
            embed = Embed(title="Um, this is awkward....", description="*No session matching this channel, check your sessions with `/manager [ session_management ] [ sessions ]`", color=0x0000FF)
            await ctx.send(embed=embed, hidden=True)

# <<--- chatbot configurations --->>          
@slash.slash(name="chatbot-options", 
    description="Set Discord chatbot related options",
    options=[
        create_option(
            name="context_amount",
            description="Set context amount",
            option_type=3,
            required=False,
            choices=[
                create_choice(
                    name="0",
                    value="0"
                ),
                create_choice(
                    name="1",
                    value="1"
                ),
                create_choice(
                    name="2",
                    value="2"
                ),
                create_choice(
                    name="3",
                    value="3"
                ),
                create_choice(
                    name="4",
                    value="4"
                ),
                create_choice(
                    name="5",
                    value="5"
                ),
                create_choice(
                    name="6",
                    value="6"
                ),
                create_choice(
                    name="7",
                    value="7"
                ),
                create_choice(
                    name="8",
                    value="8"
                ),
                create_choice(
                    name="9",
                    value="9"
                ),
                create_choice(
                    name="10",
                    value="10"
                ),
            ]
        ),
        create_option(
            name="context_type",
            description="Context contains only message author messages",
            option_type=3,
            required=False,
            choices=[
                create_choice(
                    name="combined",
                    value="combined"
                ),
                create_choice(
                    name="stacked",
                    value="stacked"
                ),
                create_choice(
                    name="segmented",
                    value="segmented"
                ),
            ]
        ),
        create_option(
            name="context_cleaner",
            description="Remove user mentions <!@> Discord mentions (enabled by default)",
            option_type=3,
            required=False,
            choices=[
                create_choice(
                    name="enable",
                    value="True"
                ),
                create_choice(
                    name="disable",
                    value="False"
                ),
            ]
        ),
        create_option(
            name="nicknames",
            description="Enable ChatGPT to see nicknames in context",
            option_type=3,
            required=False,
            choices=[
                create_choice(
                    name="enable",
                    value="True"
                ),
                create_choice(
                    name="disable",
                    value="False"
                ),
            ]
        ),
        create_option(
            name="no_mention",
            description="Disable bot mention requirement",
            option_type=3,
            required=False,
            choices=[
                create_choice(
                    name="enable",
                    value="True"
                ),
                create_choice(
                    name="disable",
                    value="False"
                ),
            ]
        ),
    ])
async def chatbot_options(ctx, context_amount=None, nicknames=None, no_mention=None, context_type=None, context_cleaner=None):
    global user_sessions, schedule, bot_login_time, bugs, homeserv

    author_id = ctx.author.id
    channel = ctx.channel
  
    with active_sessions_fetch_lock:
        if any(session.channel_id == channel.id and session.author_id == author_id for session in active_sessions.values()):
            with user_sessions_fetch_lock:
                session_list = [session for key, sessions in user_sessions.items() for session in sessions if key.startswith(f"{author_id}-")]
                if session_list:
                    session = next((session for session in session_list if session.channel_id == channel.id), None)
                    if session is not None:

                        options = (context_amount, nicknames, no_mention, context_type)
                        if all(option is None for option in options):
                            async def get_stats_task(ctx, session):
                                try:
                                    context_value = session.context
                                    nicknames_value = session.nicknames
                                    session_nomention_value = session.no_mention
                                    if session.combined_context == "True":
                                        context_type_value = "combined"
                                    elif session.stacked_context == "True":
                                        context_type_value = "stacked"
                                    elif session.segmented_context == "True":
                                        context_type_value = "segmented"
                                    embed = Embed(title="⚙️  Session Stats", description="", color=0x0000FF)
                                    embed.add_field(name="💬 **| Chat Config**", value=f"- **No Mention:** {session_nomention_value}\n- **Context Amount:** {context_value}\n- **Context Type:** {context_type_value}\n- **Nicknames:** {nicknames_value}", inline=True)
                                    embed.set_footer(text="Use /ether [manager] [prompt-view] to view full prompt or /ether [manager] [sessions] to see all sessions & extensions. Use /ether [manager] [session-save] OR [session-load] to save or load a session configuration.")
                                    await ctx.send(embed=embed, hidden=True)
                                    
                                except Exception as e:
                                    print(f"Error displaying stats card: {e}")
                            asyncio.create_task(get_stats_task(ctx, session))
                            return
                        
                        if context_amount is not None:
                            async def set_context_amount():
                                try:                 
                                    session.context = int(context_amount)
                                except Exception as e:
                                    embed = Embed(title="❌  Context Error", description="", color=0x0000FF)
                                    await ctx.send(embed=embed, hidden=True)
                            asyncio.create_task(set_context_amount())
                        
                        if context_cleaner is not None:
                            async def set_context_cleaner():
                                try:                 
                                    session.chat_sanitizer = int(context_cleaner)
                                except Exception as e:
                                    embed = Embed(title="❌  Context Error", description="", color=0x0000FF)
                                    await ctx.send(embed=embed, hidden=True)
                            asyncio.create_task(set_context_cleaner())

                        if nicknames is not None:
                            async def set_nicknames():
                                try:
                                    session.nicknames = nicknames
                                except Exception as e:
                                    embed = Embed(title="❌  Nicknames Error", description="", color=0x0000FF)
                                    await ctx.send(embed=embed, hidden=True)
                            asyncio.create_task(set_nicknames())

                        if context_type is not None:
                            if context_type == "segmented":
                                async def set_segmentation():
                                    try:
                                        session.stacked_context = "False" 
                                        session.combined_context = "False"
                                        session.segmented_context = "True"
                                        
                                    except Exception as e:
                                        embed = Embed(title="❌  Segmentation Error", description="", color=0x0000FF)
                                        await ctx.send(embed=embed, hidden=True)
                                asyncio.create_task(set_segmentation())
                            if context_type == "stacked":
                                async def set_segmentation():
                                    try:
                                        session.stacked_context = "True"
                                        session.combined_context = "False"
                                        session.segmented_context = "False"
                                        
                                    except Exception as e:
                                        embed = Embed(title="❌  Segmentation Error", description="", color=0x0000FF)
                                        await ctx.send(embed=embed, hidden=True)
                                asyncio.create_task(set_segmentation())
                            if context_type == "combined":
                                async def set_segmentation():
                                    try:
                                        session.stacked_context = "False" 
                                        session.combined_context = "True"
                                        session.segmented_context = "False" 
                                        
                                    except Exception as e:
                                        embed = Embed(title="❌  Segmentation Error", description="", color=0x0000FF)
                                        await ctx.send(embed=embed, hidden=True)
                                asyncio.create_task(set_segmentation())

                        if no_mention is not None:
                            async def set_nomention():
                                try:
                                    if session.no_mention == False:
                                        session.no_mention = True
                                    else:
                                        session.no_mention = False
                                except Exception as e:
                                    embed = Embed(title="❌  No Mention Error", description="", color=0x0000FF)
                                    await ctx.send(embed=embed, hidden=True)
                            asyncio.create_task(set_nomention())
                      
                        combined_objects = None
                        options = {
                            'context_amount': context_amount,
                            'nicknames': nicknames,
                            'no_mention': no_mention,
                            'context_type': context_type,
                            'context_cleaner': context_cleaner
                        }
                        combined_objects = "\n".join([f"- {label}: {value}" for label, value in options.items() if value is not None])

                        if combined_objects:
                            embed = Embed(title="✅  Session Configuration Updated!", description=combined_objects, color=0x00FF00)
                            await ctx.send(embed=embed, hidden=True)

        else:
            embed = Embed(title="Um, this is awkward....", description="*No session matching this channel, check your sessions with `/manager [ session_management ] [ sessions ]`", color=0x0000FF)
            await ctx.send(embed=embed, hidden=True)

# <<--- viewing, agreeing, revoking terms --->>
@slash.slash(name="terms", 
    description="View or agree to Ether's terms",
    options=[
        create_option(
            name="terms",
            description="Agree, revoke, or view terms",
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
async def terms(ctx, terms=None):
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
    
    if ctx.guild is None:
        embed = Embed(title="", description="Commands in DM is not supported at this time...", color=0x00FF00)
        await ctx.send(embed=embed)
        return
    
    if terms is not None:

        if terms == "view":
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
        
        elif terms == "agree":
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
        
        elif terms == "revoke":
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
        return

# <<--- viewing, agreeing, revoking terms --->>
@slash.slash(name="ether", 
    description="View Ether or OpenAI status",
    )
async def ether(ctx):
    async def get_status(ctx):
        embed = Embed(title="Getting Status... █░░░░", color=0x00FF00)
        status_message = await ctx.send(embed=embed)
        await get_ether(ctx, status_message)
    asyncio.create_task(get_status(ctx)) 
    return

# section for ether prompts: status, help, join, terms [--->            
async def get_ether(ctx, status_message):
    async def get_ether_task():
        try:
            serverCount = len(bot.guilds)
        
            current_time = datetime.datetime.now()
            uptime = current_time - bot_login_time  
            
            days = uptime.days
            hours, remainder = divmod(uptime.seconds, 3600)
            minutes, _ = divmod(remainder, 60)

            async def fetch_feed():
                return feedparser.parse("https://status.openai.com/history.rss")

            try:
                feed = await asyncio.wait_for(fetch_feed(), timeout=3)
                items = feed.entries[:3]
            except asyncio.TimeoutError:
                feed = None
                items = []

            embed = Embed(title="Getting Status... ███░░", color=0x00FF00)
            await status_message.edit(embed=embed)
           
            try:
                url = 'https://ether-2.gitbook.io/ether/changelog-and-bugs/bugs'
                response = requests.get(url, timeout=5)
                response.raise_for_status()  # Check for any HTTP errors
                html_content = response.text
                

                embed = Embed(title="Getting Status... ████░", color=0x00FF00)
                await status_message.edit(embed=embed)

                soup = BeautifulSoup(html_content, "html.parser")

                expandable_objects = soup.find_all(lambda tag: tag.name == "a" and "❌" in tag.get_text())

                unique_headers = set()
                header_values = []

                pattern = r'❌.*?</a>'

                matches = re.findall(pattern, html_content, re.DOTALL)

                header_values = [re.sub('<.*?>', '', match) for match in matches]

                header_values = [re.sub('❌ = active, ✖️ = anomaly', '', header) for header in header_values]

                for expandable_object in expandable_objects:
                    header = expandable_object.text.strip()  

                    if header not in unique_headers:
                        header_values.append(f"- `{header}`")
                        unique_headers.add(header)

            except requests.exceptions.RequestException as e:
                print("Error fetching GitBook:", e)
            except Exception as e:
                print("An error occurred:", e)

            current_datetime = datetime.datetime.now()
            embed = Embed(title="▶️  Ether Status", color=0x00FF00)
            embed.add_field(name="", value=current_datetime.strftime("\n%Y-%m-%d %H:%M:%S"), inline=False)
            embed.add_field(name="- Uptime", value=f" * {days} days, {hours} hours, {minutes} minutes", inline=False)
            embed.add_field(name="- Server Count", value=f" * Serving in {serverCount} servers!", inline=False)
            embed.add_field(name="- Schedule", value=f" * {schedule}", inline=False)
            if feed is not None:
                field_value = "\n".join([f"- `{item.published}`\n * {item.title}" for item in items])
                embed.add_field(name="- OpenAI API", value=f"{field_value}", inline=False)
            else:
                embed.add_field(name="- OpenAI API [Status](https://status.openai.com/#)", value="See [Status](https://status.openai.com/#)\nError fetching API", inline=False)
            if header_values:
                header_list = "\n".join(header_values)
                embed.add_field(name="- Active Bot Errors", value=header_list, inline=False)
            embed.add_field(name="", value=f"See [EtherCereal]({homeserv}) support, OpenAI [Status](https://status.openai.com/#), Ether [Knowlede Base](https://ether-2.gitbook.io/ether/)", inline=False)
          
            await status_message.edit(embed=embed)
        except Exception as e:
            embed = Embed(title="Ether Error", description="", color=0x0000FF)
    await asyncio.create_task(get_ether_task())

async def join(ctx):

    author_id = ctx.author.id
    is_blacklisted = False

    with blacklist_lock:
        for blacklisted_user_id in blacklist_dict["user_ids"]:
            if int(blacklisted_user_id) == author_id:
                is_blacklisted = True
                break

    if is_blacklisted:
        return

    embed = Embed(title="**Hello!**", color=0x00FF00)
    embed.add_field(name="", value="To use Ether bot you must ether agree to terms using /terms", inline=False)
    embed.add_field(name="Server", value=f"Join [EtherCereal]({homeserv})", inline=True)
    embed.add_field(name="Terms", value="View terms [here](https://ether-2.gitbook.io/ether/terms-faq-help/ether-terms-and-privacy)", inline=True)
    await ctx.channel.send(embed=embed)
    return
# <---]

# UserSession class instances and utilities [--->>
class UserSession:
    
    def __init__(self, ctx, session_number=None, roleStatus=None):

        # base objects [>
        self.ctx = ctx
        self.bot = bot
        self.ether_id = 1130638110196256828
        # <]

        # session flags [>
        self.learning_session = False
        self.chat_session = False
        self.image_session = False
        # <]

        # user objects [>
        self.selected_api_key = None
        self.session_user_id = None
        self.log_file_path = None
        self.log_file_object = None  
        self.author_id = ctx.author.id
        self.dm_channel = ctx.author.dm_channel
        self.role_status = roleStatus
        # <]

        # session management [>
        self.channel = ctx.channel
        self.channel_id = ctx.channel.id
        self.extend = "True"
        self.extendable = "True"
        # <]

        # session & chatbot configuration [>
        self.unique_name = "Chat"
        self.session_type = "Chat"
        self.session_number = session_number
        self.nicknames = False
        self.no_mention = False
        self.default = False
        self.eco = True
        self.context = 4
        self.session_set = False
        self.advanced_mode = False
        self.segmented_context = "False"
        self.stacked_context = "False"
        self.combined_context = "True"
        self.chat_sanitizer = "True"
        # <]

        # openai configuration [>
        self.model = "gpt-3.5-turbo"
        self.assistant = None
        self.image_model = "dalle3"
        self.prompt = ''
        self.temperature = 0.3
        self.tokens = 2000
        self.role = {"user_id": [], "user_role": [], "prompt": []}
        self.selected_role = 'user'
        self.number = 1
        self.size = '1024x1024'
        self.style = "vivid"
        self.frequency = 0
        self.presence = 0
        self.top_p = 0
        self.revised_prompt = False 
        self.api_engine = "openai"
        # Set the base URL for the local server
        self.api_base = ''
        self.api_base_default = openai.api_base
        self.top_k = 0
        self.repeat_penalty = 0
        self.custom_model_name = "local-model"


        # Set a dummy API key
        self.dummy_api_key = 'not-needed'
        # <]
        
        # associations objects [>
        self.sharedAssociations = False
        self.associations_share = []
        self.associations = {}
        self.previous_associations = []
        # <]
        
        # utilities [>
        self.send_dummy_requests = False
        self.listener_task = None
        self.loop = asyncio.new_event_loop() 
        self.dummy_request_interval = 6 * 60 * 60  
        self.dummy_request_event = asyncio.Event()
        # <]

        # advanced sharing [> 
        self.role_share = {}
        self.user_share = {} 
        self.server_share = []
        self.server_all_share = {}
        # <]

        # beginning of custom keyword creations [>
        self.artwords = {
            'draw': ['draw', 'create'],
            'variate': ['variate'],
        }
        self.custom_artwords = {}
        self.embedwords = {
            'en': ['embed'],
        }
        self.configwords = {
            'en': ['set'],
        }
        # <]
        
        # index lock, self queue, and embedding stats [>
        self.count = 0 # count of attachments
        self.char = 0 # character count
        self.time = 0 # time it takes to index
        self.index = None # initialize the index
        self.prompt_helper = None # initialize prompt helper
        self.llm_predictor = None # initialize predictor
        self.waiting_queue = queue.Queue()
        self.index_lock = asyncio.Lock() # initialize index lock
        self.lock = threading.Lock()
        self.executor = concurrent.futures.ThreadPoolExecutor()
        # <]

    def __hash__(self):
        return hash(self.ctx.author.id)
    
    def __eq__(self, other):
        return self.ctx.author.id == other.ctx.author.id

    # backup heartbeat for heavy processes [>>
    async def heartbeat(self):
        await bot.wait_until_ready()  
        while not bot.is_closed():
            await asyncio.sleep(60)
            try:
                await bot.change_presence(status=discord.Status.online)
            except Exception as e:
                print(f"Heartbeat error: {e}")
    # <<]

    # receive api key & invoke validation [>>
    async def select_api_key(self, manager):

        # objects for transaction [>
        dm_channel = await self.ctx.author.create_dm()
        self.dm_channel = dm_channel
        channel_link = f'[direct messages](https://discord.com/channels/@me/{self.dm_channel.id})'
        # <]

        # send istruction if not in direct message [>
        if not isinstance(self.ctx.channel, discord.DMChannel):
            embed = Embed(title="📩  Direct Message Sent", color=0x00FF00)
            embed.add_field(name="", value=f"Please check your {channel_link} to initialize session.", inline=False)
            embed.set_footer(text="If you do not receive the message, please check that you have direct messages from server members enabled in your Discord settings.")
            self.message = await self.ctx.send(embed=embed, hidden=True)
        # <]

        # start loop for validator options [>>    
        while True:
            try:
                await asyncio.sleep(1)
                # prompt for key [>
                embed = Embed(title="🔑  OpenAI API Key", color=0x00FF00)
                embed.add_field(name="", value="Respond with your OpenAI API key or C to cancel", inline=False)
                embed.set_footer(text="Keys are protected & private. Ether will only use the key in your session while your session is active.")
                message = await dm_channel.send(embed=embed)
                # <]

                # function to check key message [>
                def check_key(message):
                    return (
                        message.author == dm_channel.recipient and
                        len(message.content.strip()) <= 60 and
                        (message.content.lower() == 'c' or message.content.startswith('sk-'))
                    )
                # <]
                
                # obtain key message or optional cancel [>
                key_message = await bot.wait_for('message', check=check_key, timeout=60)
                if key_message.content.lower() == 'c':
                    embed = Embed(title="", color=0x00FF00)
                    embed.add_field(name="❎  Process Cancelled!", value="", inline=False)
                    await self.dm_channel.send(embed=embed)
                    await self.exit_session_instance()
                    return None
                # <]
                
                # update the validator embed [>
                embed.title = ""  # Remove the title
                embed.description = "Key detected. Validating..." # Update the description
                embed.clear_fields() # Remove all fields
                embed.set_footer(text="") # Remove the footer
                await message.edit(embed=embed)
                # <]

                # validate api key [>
                is_valid_key = await self.check_api_key(key_message.content.strip())
                if not is_valid_key:
                    embed.title = "❌  Key Error\n\n"
                    embed.description = "The key is either invalid, max quota, or there was an error communicating with OpenAI.\n\nTry your key again, or try a different key.\n\nOpenAI [Account](https://platform.openai.com/account/org-settings)\nEther's [Support Server](https://discord.gg/cc3fX93Nvu)."
                    embed.color = 0xFFA500
                    await message.edit(embed=embed)
                    continue
                # <]

                # return api key to class instance [>
                selected_api_key = key_message.content.strip()
                return selected_api_key
                # <]

            # handle timeouts or errors [>
            except asyncio.TimeoutError:
                embed = Embed(title="No Response", color=0xFFA500)
                embed.add_field(name="Process aborted...", value="", inline=False)
                await self.dm_channel.send(embed=embed)
                return None
            except discord.Forbidden:
                embed = Embed(title="❌  Error", description="Failed to send direct message.\nPlease enable direct messages from server members in your account settings.", color=0x00FF00)
                await self.message.edit(embed=embed)
                return None
            # <]
        # end of loop <<]
    # <<]

    # clean and exit session [>>
    async def exit_session_instance(self):
        global user_sessions, active_sessions, shared_sessions
        # initial objects to disable [>
        self.chat_session = False
        self.image_session = False
        self.learning_session = False
        
        asyncio.create_task(self.stop_sending_dummy_requests())
        # <]

        # disable predictors, index, prompt helper [>
        if self.llm_predictor is not None:
            self.llm_predictor = None
        if self.index is not None:
            self.index = None
        if self.prompt_helper is not None:
            self.prompt_helper = None
        # <]

        # clean from shared, active, user sessions [>
        try:
            user_id = self.ctx.author.id
            channel_id = self.ctx.channel.id
            with user_sessions_fetch_lock:
                with active_sessions_fetch_lock:
                    with shared_sessions_lock:
                        server_share_copy = self.server_share.copy()
                     
                        for channel_id in server_share_copy:
                            if channel_id in shared_sessions.keys():
                                del shared_sessions[channel_id]
                                self.server_share.remove(channel_id)
                        if channel_id in shared_sessions.keys():
                            del shared_sessions[channel_id]
                        self.server_share = []

                        for session_key, session_list in user_sessions.items():
                            key_parts = session_key.split("-")
                            if key_parts[0] == str(user_id) and int(key_parts[2]) == channel_id:
                                session_to_remove = None
                                for session in session_list:
                                    if session.channel_id == self.channel_id:  # Use self.channel_id instead of channel_id
                                        session_to_remove = session
                                        break

                                if session_to_remove:
                                    session_list.remove(session_to_remove)
                                    active_sessions.pop(session_to_remove.channel.id, None)

                                    if not session_list:
                                        del user_sessions[session_key]
                                        del active_sessions[session_key]
                                        break
        except asyncio.TimeoutError:
            print("Timeout error occurred. Unable to acquire locks within the specified timeout.")
        except Exception as e:
            print(f"An error occurred: {e}")
        # done cleaning session <]
        
        # invoke the garbage collector [>        
        gc.collect()
        # <]
    # <<]

    # loop and block for validator [>>
    async def check_api_key(self, api_key):
        openai.api_key = api_key

        try:
            loop = asyncio.get_event_loop()
            response = await asyncio.wait_for(
                loop.run_in_executor(None, self.call_openai_api),
                timeout=10  # Timeout after 10 seconds
            )

            if response is not None and "error_message" not in response:
                return True
            else:
                return False

        except openai.error.AuthenticationError:
            return False
        except openai.error.APIError as e:
            return False
        except asyncio.TimeoutError:
            return False

    # api call for key validation [>>
    def call_openai_api(self):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": "Hello"}
                ],
                max_tokens=1,
                n=1
            )
            return response

        except Exception as e:
            print(f"An error occurred during the API call: {e}")
            return None
    
    # function to calculate time duration during indexing [>>
    async def format_time(self, time_passed):
        minutes, seconds = divmod(time_passed.total_seconds(), 60)  
        minutes = int(minutes)
        seconds = int(seconds)
        if minutes > 0:
            return f"{minutes} minutes and {seconds} seconds"
        else:
            return f"{seconds} seconds"
    # <<]

    # engine for indexing and embedding data [>>>>>
    async def indexing_process(self, user_session_dir, all_documents, embed_message, embed):
        with self.lock:
            with semaphore:

                # check global semaphore queue [>>>>
                if semaphore._value == 0:
                    dm_channel = await self.ctx.author.create_dm()
                    current_datetime = datetime.datetime.now()
                    embed = Embed(title="*Process in queue*", description="Our system is currently in high demand. You're request is queued and will process very soon.", color=0xFFA500)
                    embed.set_footer(text=current_datetime.strftime("%Y-%m-%d %H:%M:%S"))
                    await dm_channel.send(embed=embed)
                    self.waiting_queue.put(self.ctx.author.id)
                    self.ctx.author.id.pause_function()
                # <<<<]

                else:
                    # prepare payload [>>>
                    max_input_size = 4096
                    num_outputs = 512
                    max_chunk_overlap = 20
                    chunk_size_limit = 500
                    self.prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)
                    self.llm_predictor = LLMPredictor(
                        llm=ChatOpenAI(
                            temperature=self.temperature,
                            max_tokens=num_outputs,
                            openai_api_key=self.selected_api_key,
                            model=self.model,
                        )
                    )
                    # <<<]

                    # check directory path [>>
                    directory_path = os.path.dirname(all_documents[0]["text_file_path"])  
                    documents = SimpleDirectoryReader(directory_path).load_data()
                    # <<]

                    # perform indexing with threading [>
                    if documents:
                        if self.index is None:
                            async with rate_limit_semaphore:    
                                timeout = 300  
                                start_time = datetime.datetime.now()
                                thread = threading.Thread(target=lambda: setattr(self, 'index', GPTSimpleVectorIndex(documents, llm_predictor=self.llm_predictor, prompt_helper=self.prompt_helper)))
                                thread.start()   
                                while self.index is None:
                                    if embed_message is not None:
                                        await asyncio.sleep(2)  
                                        embed.set_field_at(1, name="", value="⌛  Indexing Data... ⟳", inline=True)
                                        await embed_message.edit(embed=embed)
                                        await asyncio.sleep(2)  
                                        embed.set_field_at(1, name="", value="⌛  Indexing Data... ↻", inline=True)
                                        await embed_message.edit(embed=embed)
                                    elapsed_time = (datetime.datetime.now() - start_time).seconds
                                    if elapsed_time >= timeout:
                                        await self.dm_channel.send("The indexing process took too long and has been cancelled.")
                                        return
                                end_time = datetime.datetime.now()  
                                time_passed = end_time - start_time  

                                formatted_time = await self.format_time(time_passed)
                                self.time = formatted_time
                                return True
                        else:
                            return
                    # <]
    # <<<<<]

    # loop manager for predictor call [>
    def run_chatbot(self, conversationLog):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(self.chatbot(conversationLog))
        loop.close()
        return response
    # <]

    # function to pass message to thread for predictor [>
    async def chatbot(self, conversationLog):
        index = self.index
        if index is not None:
            await self.index_lock.acquire() 
            try:
                response = await asyncio.wait_for(
                    asyncio.to_thread(index.query, conversationLog),
                    timeout=60
                ) 
                return response.response
            except asyncio.TimeoutError:
                return "Timeout error: index.query took too long to respond"
            finally:
                self.index_lock.release()
        else:
            return
    # <]

    # loop manager for quick pass predictor embeddings [> 
    def run_mini_bot(self, instruction):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(self.mini_bot_relay(instruction))
        return response
    # <]

    # function to quick pass instruction to predictor [>
    async def mini_bot_relay(self, instruction):  
        index = self.index
        if index is not None:
            async with self.index_lock:
                response = index.query(instruction)
                return response.response
        else:
            print("error")
    # <]

    # function to download associations to file [>
    async def download_associations(self):
        dm_channel = await self.ctx.author.create_dm()
        self.dm_channel = dm_channel
        if self.associations:
            associations_string = ""
            associations_dict = self.associations
            for keyword, associations_list in associations_dict.items():
                if not associations_list:
                    continue
                associations_string += f"{keyword}: {', '.join(associations_list)}\n"
            if associations_string:
                channel_link = f'#{self.ctx.channel.mention}'
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
                content = f"Associations from {channel_link} ({timestamp})"  
                file = discord.File(io.StringIO(associations_string), filename="associations.txt")
                await dm_channel.send(content=content, file=file)
            else:
                await dm_channel.send("No associations found.")
    # <]

    # function to upload associations from a file [>                   
    async def upload_associations(self):
        dm_channel = await self.ctx.author.create_dm()
        self.dm_channel = dm_channel
        embed = Embed(title="🔼  Upload Associations File", color=0x00FF00)
        embed.add_field(name="", value="Send your associations .txt file as an attachment", inline=False)
        message = await dm_channel.send(embed=embed)

        def check(message):
            return message.author == self.ctx.author and message.attachments

        try:
            message = await self.bot.wait_for('message', check=check, timeout=60)
            uploaded_file = message.attachments[0]
            if uploaded_file.filename.endswith(".txt"):
                file_content = await uploaded_file.read()
                file_content = file_content.decode("utf-8")
                lines = file_content.split("\n")
                for line in lines:
                    if line:
                        parts = line.split(":", 1) 
                        if len(parts) == 2:
                            keyword = parts[0].strip()
                            associations = parts[1].split(",")  
                            associations = [association.strip() for association in associations]
                            self.associations[keyword] = associations
                      
                embed = Embed(title="✅  Done!", description=(f"Your associations have been uploaded into your session.\n#{self.ctx.channel.name} {self.ctx.channel.mention}"), color=0xFFA500)
                await dm_channel.send(embed=embed)
            else:
                embed = Embed(title="❌  Error\n\n", description=("The file must be a .txt file in the format you would receive it from Ether."), color=0xFFA500)
                await dm_channel.send(embed=embed)
        except asyncio.TimeoutError:
            embed.description = "Operation Timed Out: No file uploaded."
            await message.edit(embed=embed)
    # <]
    
    # function to send dummy requests -- fork to task in future [>
    async def send_dummy_request(self):
        await asyncio.get_running_loop().run_in_executor(None, self.run_chatbot, "hello")
    # <]

    # function to schedule dummy requests [>
    async def schedule_dummy_requests(self):
        while self.send_dummy_requests:
            await self.send_dummy_request()
            await asyncio.sleep(self.dummy_request_interval)
            self.dummy_request_event.clear()
    # <]

    # function to invoke the dummy scheduler [>
    async def start_sending_dummy_requests(self):
        if not self.send_dummy_requests:
            self.send_dummy_requests = True
            await self.schedule_dummy_requests()
    # <]

    # function to stop the dummy service [>
    async def stop_sending_dummy_requests(self):
        self.send_dummy_requests = False
        self.dummy_request_event.set()
    # <]

    # function to jump start session listener [>
    def start_listener(self):
        if self.listener_task is None or self.listener_task.done():
            self.listener_task = self.loop.create_task(self.listener())
    # <]

    # function to stop the listener [>
    def stop_listener(self):
        if self.listener_task is not None:
            self.listener_task.cancel()
            self.listener_task = None
    # <]

    # loop handler for start listener [>
    def invoke_listener(self):
        self.loop.create_task(self.listener())
    # <]

    # event loop manager [>>
    def start_event_loop(self):
        self.loop.run_forever()
    def stop_event_loop(self):
        self.loop.stop()
        self.loop.close()
    # <]

    async def check_access(self, message):
        role_time_status = False
        role_iterations_status = False
        user_time_status = False
        user_iterations_status = False
        for role in message.author.roles:
            if role in self.role_share:
                iterations = self.role_share[role].get("iterations")
                time_limit = self.role_share[role].get("time")
                if int(time_limit) != 0:
                    current_time = datetime.datetime.now()
                    timestamp = datetime.datetime.strptime(self.role_share[role].get("timestamp"), "%Y-%m-%d %H:%M:%S")
                    time_difference = current_time - timestamp
                    if time_difference.total_seconds() >= self.parse_time_limit(time_limit).total_seconds():
                        role_time_status = False
                    else:
                        role_time_status = True
                else:
                    self.role_share[role]["iterations"] = int(iterations) - 1
                    if self.role_share[role]["iterations"] <= 0:
                        role_iterations_status = False
                    else:
                        role_iterations_status = True

                if int(time_limit) == 0 and iterations == "0":
                    role_iterations_status = False
                    role_time_status = False

        user_key = f"<@{message.author.id}>"
        if user_key in self.user_share:
            user_share = self.user_share[user_key]
            time_limit = user_share.get("time")
            iterations = user_share.get("iterations")
            if time_limit != "0":
                current_time = datetime.datetime.now()
                timestamp = datetime.datetime.strptime(user_share.get("timestamp"), "%Y-%m-%d %H:%M:%S")
                time_difference = current_time - timestamp
                if time_difference.total_seconds() >= self.parse_time_limit(time_limit).total_seconds():
                    user_time_status = False
                else:
                    user_time_status = True
            else:
                if iterations is not None:
                    if user_share["iterations"] <= 0:
                        user_iterations_status = False
                    else:
                        user_iterations_status = True

        if role_iterations_status or role_time_status or user_iterations_status or user_time_status:
            return True
        else:
            return False

    async def deduct_iteration(self, message):
        role_time_ended = False
        user_iterations_ended = False
        user_time_ended = False

        user_key = f"<@{message.author.id}>"

        for role in message.author.roles:
            if role in self.role_share:
                time_limit = self.role_share[role].get("time")
                iterations = self.role_share[role].get("iterations")
                if time_limit is not None and time_limit != "0":
                    current_time = datetime.datetime.now()
                    timestamp = datetime.datetime.strptime(self.role_share[role].get("timestamp"), "%Y-%m-%d %H:%M:%S")
                    time_difference = current_time - timestamp
                    if time_difference.total_seconds() >= self.parse_time_limit(time_limit).total_seconds():
                        role_time_ended = True
                        break
                elif iterations is not None:
                    self.role_share[role]["iterations"] = int(iterations) - 1
                    if self.role_share[role]["iterations"] <= 0:
                        
                        role_time_ended = True
                        break

        if not role_time_ended:
            if user_key in self.user_share:
                user = self.user_share[user_key]
                time_limit = user.get("time")
                iterations = user.get("iterations")
                if time_limit is not None and time_limit != "0":
                    current_time = datetime.datetime.now()
                    timestamp = datetime.datetime.strptime(user.get("timestamp"), "%Y-%m-%d %H:%M:%S")
                    time_difference = current_time - timestamp
                    if time_difference.total_seconds() >= self.parse_time_limit(time_limit).total_seconds():
                        user_time_ended = True
                elif iterations is not None:
                    user["iterations"] = int(iterations) - 1
                    if user["iterations"] <= 0:
                        
                        user_iterations_ended = True
            else:
                user_iterations_ended = True

    def parse_time_limit(self, time_limit):
        match = re.match(r"(\d+)\s*(\w+)", time_limit)
        if match:
            amount = int(match.group(1))
            unit = match.group(2).lower()
            if unit in ["second", "seconds", "s"]:
                return datetime.timedelta(seconds=amount)
            elif unit in ["minute", "minutes", "m"]:
                return datetime.timedelta(minutes=amount)
            elif unit in ["hour", "hours", "h"]:
                return datetime.timedelta(hours=amount)
            elif unit in ["day", "days", "d"]:
                return datetime.timedelta(days=amount)
            elif unit in ["week", "weeks", "w"]:
                return datetime.timedelta(weeks=amount)
        return None

    async def chat(self, default, session_number):
        global user_sessions, shared_sessions, active_sessions     
        self.dm_channel = await self.ctx.author.create_dm()

        dm_channel = await self.ctx.author.create_dm()

        chat_channel = self.ctx.channel.id

        manager = False
        self.selected_api_key = await self.select_api_key(manager)
        if self.selected_api_key is None:
            await self.exit_session_instance()
            return
        self.chat_session = True

        if self.ctx.author.id not in self.role["user_id"]:
            self.role["user_id"].append(self.ctx.author.id)
            self.role["user_role"].append(self.selected_role)
            self.role["prompt"].append('')

        try:

            current_datetime = datetime.datetime.now()

            if isinstance(self.ctx.channel, discord.DMChannel):
                channel_link = "Direct Message"
            else:
                channel_link = f'{self.ctx.channel.mention}'

            if self.combined_context == "True":
                instance_context_type = "combined"
            if self.segmented_context == "True":
                instance_context_type = "segmented"
            if self.stacked_context == "True":
                instance_context_type = "stacked"

            if not isinstance(self.ctx.channel, discord.DMChannel):
                role_index = self.role["user_id"].index(self.author_id)
                prompt_index = self.role["user_id"].index(self.ctx.author.id)
                prompt_value = self.role["prompt"][prompt_index] if prompt_index < len(self.role["prompt"]) else None
                role_list = self.role.get("user_role", [])
                role_value = role_list[role_index] if role_index < len(role_list) else None
                embed = Embed(title="**⚙️  Chat Bot Initialized**", description=channel_link, color=0x00FF00)
                embed.add_field(name=f"ℹ️ **| Session** {self.session_number} **Name:** {self.unique_name}\n\n", value=f"", inline=False)
                embed.add_field(name="🎛️ **| OpenAI Config**", value=f"- **Model:** {self.model}\n- **Model Name:** {self.custom_model_name}\n **API Base: {self.api_base}\n- **Tokens:** {self.tokens}\n- **Temperature:** {self.temperature}\n- **Role:** {role_value}\n- **Presence:** {self.presence}\n- **Frequency:** {self.frequency}\n- **Top_P:** {self.top_p}\n- **Top_K:** {self.top_k} \n- **Repeat Penalty:** {self.repeat_penalty}", inline=True)
                embed.add_field(name="🎨 **| DALLE Config**", value=f"- **Model:** {self.image_model}\n- **Number:** {self.number}\n- **Style:** {self.style}\n- **Size:** {self.size}\n- Toggles: {self.revised_prompt}\n*Note: no variations in dalle3*", inline=True)
                embed.add_field(name="💬 **| Chat Config**", value=f"- **Context:** {self.context}\n- **Context Type:** {instance_context_type}\n- **Nicknames:** {self.nicknames}\n- **No Mention:** {self.no_mention}\n- **Embeddings:** {self.learning_session}", inline=True)
                embed.add_field(name="🗒️ **| Prompt:**", value=f"{prompt_value}", inline=True)
                embed.set_footer(text="Use /ether [manager] [prompt-view] to view full prompt or /ether [manager] [sessions] to see all sessions & extensions. Use /ether [manager] [session-save] OR [session-load] to save or load a session configuration.")
                await self.dm_channel.send(embed=embed) 

            embed = Embed(title="✅  ChatBot Initialized!\n\n", description="", color=0x00FF00)
            embed.set_footer(text="Chat mode is now active and Ether will respond to mentions or replies in this channel.")
            if not isinstance(self.ctx.channel, discord.DMChannel):
                await self.ctx.send(embed=embed, hidden=True)
            else:
                await self.dm_channel.send(embed=embed) 
            
            user_id = str(self.ctx.author.id)
            while self.chat_session:
                
                message = await self.bot.wait_for('message', check=lambda msg: (
                    (msg.channel == self.ctx.channel or msg.channel.id in self.server_share) or
                    (msg.author.id == self.ctx.author.id)
                ))

                has_session = None
                async with user_sessions_lock:
                    if not any(
                        key.split("-")[0] == str(self.author_id)
                        or message.channel in self.server_share
                        for key in user_sessions.keys()
                    ):
                        continue
                    else:
                        has_session = any(
                            key.split("-")[0] == str(message.author.id) and key.split("-")[2] == str(message.channel.id)
                            for key in user_sessions.keys()
                        )

                if (message.author.id == self.ctx.author.id or not has_session) and (message.channel.id == self.ctx.channel.id or message.channel.id in self.server_share):

                    if self.chat_session == False:
                        return
                
                    if message.author == bot.user:
                        continue

                    if message.type == discord.MessageType.pins_add:
                        continue

                    if message.author.bot:
                        continue

                    if (str(message.author.id) == user_id or f"<@{message.author.id}>" in self.user_share.keys() or any(role in self.role_share.keys() for role in message.author.roles)):

                        if (bot.user not in message.mentions or (message.reference and message.reference.resolved.author != bot.user)) and (message.channel == self.ctx.channel or message.channel.id in self.server_share):
                            user_id_pattern = r"<@[\d]+>"
                            content = message.content.strip()
                            content_without_user_ids = re.sub(user_id_pattern, "", content)
                            if not bot.user.mentioned_in(message):
                                words = content_without_user_ids.split()
                                for word in words:
                                    keyword = word.lower()  
                                    if keyword in self.associations and ">>" not in content:
                                        async def process_associations():
                                            keyword_associations = self.associations[keyword]
                                            if keyword_associations:
                                                try:
                                                    if len(keyword_associations) > 1:
                                                        while True:
                                                            random.shuffle(keyword_associations)
                                                            if keyword_associations[0] != self.previous_associations:
                                                                break
                                                        self.previous_associations = keyword_associations[0]
                                                    response = keyword_associations[0]
                                                    await message.channel.send(response)
                                                    return
                                                except Exception as e:
                                                    print(f"Error processing keyword: {e}")
                                        asyncio.create_task(process_associations())
                                        continue

                        if self.no_mention == False:
                            if bot.user in message.mentions or (message.reference and message.reference.resolved.author == bot.user):
                                pass

                        if self.no_mention == False:
                            if not bot.user.mentioned_in(message):
                                continue

                        async def rev_engine(self, user_id, dm_channel, message):
                            if str(message.author.id) == user_id:
                                shared_access = True
                                user_access = ["Chat", "Image", "Fast_Embed", "Full_Embed", "Set", "Visual"]
                            else:
                                async with asyncio.Lock():
                                    if (
                                        f"<@{message.author.id}>" in self.user_share.keys()
                                        and any(share_type in ['Chat', 'Image', 'Fast_Embed', "Full_Embed", 'Visual', 'Set'] for share_type in self.user_share.get(f"<@{message.author.id}>", {}).get('share_types', []))
                                    ) or (
                                        any(role in self.role_share.keys() for role in message.author.roles)
                                        and any(share_type in ['Chat', 'Image', 'Fast_Embed', "Full_Embed", 'Visual', 'Set'] for share_type in self.role_share.get(role, {}).get('share_types', []))
                                        for role in message.author.roles
                                    ):
                                        shared_access = await self.check_access(message)
                                        if shared_access == False:
                                            return
                                        else:
                                            user_access = []
                                            if f"<@{message.author.id}>" in self.user_share.keys():
                                                user_access.extend(self.user_share.get(f"<@{message.author.id}>", {}).get('share_types', []))
                                            for role in message.author.roles:
                                                if role in self.role_share.keys():
                                                    user_access.extend(self.role_share.get(role, {}).get('share_types', []))

                            if (str(message.author.id) == user_id or any(member.name == message.author.name for member in self.associations_share)) and '>>' in message.content:
                                bot_id_index = message.content.find(f"<@{bot.user.id}>")
                                content_without_bot_id = message.content[:bot_id_index] + message.content[bot_id_index + len(f"<@{bot.user.id}>"):]
                                parts = content_without_bot_id.split('>>')
                                try:
                                    if len(parts) == 2:
                                        keyword = parts[0].strip().lower()  
                                        association = parts[1].strip()
                                        async with asyncio.Lock():
                                            if keyword in self.associations:
                                                if association == "":
                                                    if message.reference and message.reference.resolved.content in self.associations[keyword]:
                                                        self.associations[keyword].remove(message.reference.resolved.content)
                                                        await message.add_reaction('✨')  
                                                    else:
                                                        del self.associations[keyword]
                                                        await message.add_reaction('✨')  
                                                    return
                                                else:
                                                    associations_to_add = association.split(',')
                                                    for item in associations_to_add:
                                                        self.associations[keyword].append(item.strip())  
                                                    await message.add_reaction('✨')  
                                                    return
                                            else:
                                                if association != "":
                                                    self.associations[keyword] = [item.strip() for item in association.split(',')]  
                                                    await message.add_reaction('✨')  
                                                    return
                                    else:
                                        await message.channel.send('Apologies, do it like this: keyword1 >> keyword2')
                                        return
                                except Exception as e:
                                    print(f"Error processing association: {e}")

                            if (str(message.author.id) == user_id or any(member.name == message.author.name for member in self.associations_share)) and '><' in message.content:
                                bot_id_index = message.content.find(f"<@{bot.user.id}>")
                                content_without_bot_id = message.content[:bot_id_index] + message.content[bot_id_index + len(f"<@{bot.user.id}>"):] 
                                parts = content_without_bot_id.split('><')

                                try:
                                    if len(parts) == 2:
                                        old_trigger = parts[0].strip().lower()  
                                        new_trigger = parts[1].strip().lower()  
                                        
                                        if old_trigger in self.associations:
                                            associations = self.associations[old_trigger]  
                                            del self.associations[old_trigger]  
                                            self.associations[new_trigger] = associations  
                                            
                                            await message.add_reaction('✨')  
                                        else:
                                            await message.channel.send(f"No associations found for trigger '{old_trigger}'")
                                    else:
                                        await message.channel.send('Apologies, do it like this: old_trigger >< new_trigger')
                                except Exception as e:
                                    print(f"Error processing trigger renaming: {e}")
                                return
                            
                            # saving translations regex for later, good for generating alternate unique words for navigating the off ramps
                            # translations_regex = '|'.join('(?:{})'.format('|'.join(words)) for words in self.artwords.values())

                            # if self.custom_artwords:
                                # translations_regex += '|' + '|'.join('(?:{})'.format(keyword) for keyword in self.custom_artwords.keys())

                            is_reply_to_bot = message.reference and message.reference.resolved.author.id == bot.user.id

                            if self.no_mention == False:
                                pattern = r'^\s*(draw|variate)'
                            else:
                                pattern = r'^(draw|variate)'

                            message_content = re.sub(r'<@!?1130638110196256828>', '', message.content)

                            if (re.search(pattern, message_content, re.IGNORECASE) or is_reply_to_bot) and "Image" in user_access:
                                if re.search(r'^\s*draw', message_content, re.IGNORECASE) or (self.no_mention == True and re.search(r'^(draw)', message_content, re.IGNORECASE)):

                                    async def draw_image(message):
                                        try:
                                            content_parts = message_content.split()
                                            draw_index = content_parts.index('draw')
                                            prompt = ' '.join(content_parts[draw_index + 1:]).strip()
                                            await message.channel.trigger_typing()
                                            chat_task = asyncio.create_task(self.handle_image(prompt, message, self.number, self.size))
                                            await chat_task
                                        except Exception as e:
                                            embed = Embed(title="Draw Error", description="", color=0x0000FF)
                                            print(f"Unexpected error occurred: {e}")
                                            await self.ctx.send(embed=embed, hidden=True)
                                    asyncio.create_task(draw_image(message))
                                    return

                                if re.search(r'^\s*variate', message_content, re.IGNORECASE) or (self.no_mention == True and re.search(r'^(variate)', message_content, re.IGNORECASE)):
                                    if self.image_model == "dalle2":
                                        async def variate_task():
                                            try:
                                                content_parts = message.content.split()
                                                variate_index = content_parts.index('variate')
                                                prompt = ' '.join(content_parts[variate_index + 1:]).strip()
                                                await message.channel.trigger_typing()

                                                if len(prompt) > 1000:
                                                    embed = Embed(title="", description="Invalid prompt. Please enter a prompt using less than 1,000 characters", color=0xFFA500)
                                                    await message.channel.send(embed=embed, hidden=True)
                                                    return

                                                if len(message.attachments) == 1:
                                                    attached_file = message.attachments[0]
                                                    await self.channel.trigger_typing()

                                                    allowed_extensions = (".png", ".jpg", ".jpeg") 
                                                    if attached_file.filename.lower().endswith(allowed_extensions):
                                                        async with aiohttp.ClientSession() as session:
                                                            async with session.get(attached_file.url) as response:
                                                                image_data = await response.read()

                                                        temp_dir = os.path.join(os.getcwd(), 'tmp')
                                                        os.makedirs(temp_dir, exist_ok=True)

                                                        temp_file_name = f"{user_id}_image.png"

                                                        temp_file_path = os.path.join(temp_dir, temp_file_name)
                                                        async with aiofiles.open(temp_file_path, "wb") as temp_file:
                                                            await temp_file.write(image_data)

                                                        mime_type = magic.Magic(mime=True).from_file(temp_file_path)

                                                        if mime_type not in ["image/png", "image/jpeg", "image/jpg"]:
                                                            os.remove(temp_file_path)
                                                            return "Invalid file type. Only PNG, JPEG, and JPG images are allowed."

                                                        if mime_type in ["image/jpeg", "image/jpg"]:
                                                            image = Image.open(temp_file_path)
                                                            temp_file_path = os.path.join(temp_dir, temp_file_name[:-4] + ".png")  
                                                            image.save(temp_file_path)
                                                            mime_type = "image/png"

                                                        with Image.open(temp_file_path) as img:
                                                            width, height = img.size
                                                            if width > 1024 or height > 1024:
                                                                with img.resize((1024, 1024)) as resized_img:
                                                                    resized_img.save(temp_file_path)
                                                            elif width < 1024 or height < 1024:
                                                                size_diff_256 = abs(width - 256) + abs(height - 256)
                                                                size_diff_512 = abs(width - 512) + abs(height - 512)
                                                                size_diff_1024 = abs(width - 1024) + abs(height - 1024)
                                                                
                                                                if size_diff_256 <= size_diff_512 and size_diff_256 <= size_diff_1024:
                                                                    target_resolution = (256, 256)
                                                                elif size_diff_512 <= size_diff_1024:
                                                                    target_resolution = (512, 512)
                                                                else:
                                                                    target_resolution = (1024, 1024)
                                                                
                                                                if target_resolution[0] != width or target_resolution[1] != height:
                                                                    with img.resize(target_resolution) as resized_img:
                                                                        resized_img.save(temp_file_path)

                                                                file_size_mb = os.path.getsize(temp_file_path) / (1024 * 1024)

                                                                if file_size_mb > 4:
                                                                    image = Image.open(temp_file_path)

                                                                    max_file_size = 4 * 1024 * 1024  
                                                                    file_size = len(image.fp.read())
                                                                    current_width, current_height = image.size

                                                                    new_width = current_width
                                                                    new_height = current_height
                                                                    next_sizes = [(245, 245), (512, 512), (1024, 1024)]
                                                                    for size in next_sizes:
                                                                        if size[0] < current_width and size[1] < current_height:
                                                                            new_width = size[0]
                                                                            new_height = size[1]
                                                                            break

                                                                    while file_size > max_file_size:
                                                                        image = image.resize((new_width, new_height), Image.ANTIALIAS)

                                                                        current_width, current_height = image.size
                                                                        file_size = len(image.fp.read())

                                                                        new_width = current_width
                                                                        new_height = current_height
                                                                        for size in next_sizes:
                                                                            if size[0] < current_width and size[1] < current_height:
                                                                                new_width = size[0]
                                                                                new_height = size[1]
                                                                                break

                                                                    image.save(temp_file_path)

                                                        loop = asyncio.get_event_loop()
                                                        chat_task = asyncio.create_task(self.variate_image_command(user_id, prompt, temp_file_path, self.selected_api_key, self.number, self.size, loop, message))
                                                        await chat_task
                                                        return

                                                    else:
                                                        await self.ctx.channel.send("Please upload a file with a valid image format (png, jpg, jpeg).")
                                                        return
                                                else:
                                                    await self.ctx.channel.send("Either no image was attached, or, there were multiple images. Please try again with a single image attachment.")
                                                    return
                                            
                                            except Exception as e:
                                                embed = Embed(title="Variate Error", description="", color=0x0000FF)
                                                await self.ctx.send(embed=embed, hidden=True)
                                        asyncio.create_task(variate_task())
                                        return
                                    else:
                                        embed = Embed(title="❌  Change the image model to dalle 2 for variations", description="", color=0x00FF00)
                                        embed.set_footer(text="")
                                        await self.ctx.send(embed=embed, hidden=True)
                                        return
                        
                            if re.sub(r'<@1130638110196256828>', '', message.content).strip().startswith('embed') == False and (0 < len(message.attachments) <= 2) and ("Fast_Embed" in user_access or "Visual" in user_access):
                                
                                if message.attachments:
                                
                                    attachment = message.attachments[0]
                                    file_extension = attachment.filename.split('.')[-1]
                                    if file_extension in ['jpg', 'jpeg', 'png', 'webp']:
                                        if "Visual" in user_access:
                                            async def image_vision():
                                                if len(message.attachments) > 0 and len(message.attachments) <= 2:
                                                    image_urls = [attachment.url for attachment in message.attachments]
                                                    vision_message = None
                                                    temp_image_files = []
                                                    await message.channel.trigger_typing()

                                                    for i, image_url in enumerate(image_urls):
                                                        response = requests.get(image_url)
                                                        image = Image.open(BytesIO(response.content))
                                                        image_filename = f"temp/{message.author.id}_image_{i}.{image.format.lower()}"
                                                        image.save(image_filename, format=image.format)  
                                                        temp_image_files.append(image_filename)

                                                    if not message.content:
                                                        prompt = "Please describe the graphic"
                                                    else:
                                                        prompt = message.content

                                                    if len(message.attachments) == 1:
                                                        vision_message = {
                                                            "role": "user",
                                                            "content": [
                                                                {"type": "image_url", "image_url": image_urls[0]},
                                                                {"type": "text", "text": prompt},
                                                            ],
                                                        }
                                                    elif len(message.attachments) == 2:
                                                        vision_message = {
                                                            "role": "user",
                                                            "content": [
                                                                {"type": "image_url", "image_url": image_urls[0]},
                                                                {"type": "text", "text": prompt},
                                                                {"type": "image_url", "image_url": image_urls[1]},
                                                            ],
                                                        }
                                                    else:
                                                        await message.reply("Please attach one or two images")
                                                        return

                                                    try:
                                                        response = openai.ChatCompletion.create(
                                                            model="gpt-4-vision-preview",
                                                            messages=[vision_message],
                                                            api_key=self.selected_api_key,
                                                            max_tokens=self.tokens,
                                                        )
                                                    except Exception as e:
                                                        print("Error during API request:", e)

                                                    chatbot_response = response['choices'][0]['message']['content']

                                                    if response['choices'][0]['message'].get('truncated', False):
                                                        completion_id = response['id']
                                                        full_response = openai.Completion.retrieve(completion_id)
                                                        chatbot_response = full_response['choices'][0]['message']['content']

                                                    if len(chatbot_response) > 2000:
                                                        await message.channel.trigger_typing()

                                                        chunks = []
                                                        while len(chatbot_response) > 2000:
                                                            last_period_index = chatbot_response[:2000].rfind(".")

                                                            if last_period_index != -1:
                                                                chunk = chatbot_response[:last_period_index+1].strip()
                                                                chatbot_response = chatbot_response[last_period_index+1:].strip()
                                                            else:
                                                                chunk = chatbot_response[:2000].strip()
                                                                chatbot_response = chatbot_response[2000:].strip()

                                                            chunks.append(chunk)

                                                        chunks.append(chatbot_response)
                                                        sent_message = await message.reply(chunks[0])
                                                        for chunk in chunks[1:]:
                                                            sent_message = await message.channel.send(chunk)

                                                    else:
                                                        sent_message = await message.channel.send(chatbot_response)

                                                    if sent_message:
                                                        if message.author.id != self.ctx.author.id:
                                                            await self.deduct_iteration(message)
                                                    
                                                    for image_file in temp_image_files:
                                                        os.remove(image_file)

                                            asyncio.create_task(image_vision())
                                            return
                                        
                                    # This line has not been updated to include the most recent filetype additions    
                                    if file_extension in ['txt', 'docx', 'pdf', 'rtf', 'odt', 'doc', 'js', 'py', 'sh', 'lua', 'ps1', 'epub', 'c', 'cpp', 'rs', 'nim', 'csv']:
                                        if "Fast_Embed" in user_access:
                                            async def quick_embed():
                                                try:
                                                    instruction = message.content
                                                    if '<@1130638110196256828>' in instruction:
                                                        instruction = instruction.split('<@1130638110196256828>')[1].strip()

                                                    attachment = message.attachments[0]
                                                    file_extension = attachment.filename.split('.')[-1]

                                                    await message.channel.trigger_typing()
                                                    user_id = str(self.ctx.author.id)
                                                    data_dir = os.path.join('data')

                                                    if not os.path.exists(data_dir):
                                                        os.makedirs(data_dir)

                                                    user_docs_dir = None
                                                    user_session_dir = None

                                                    session_folder = f"{user_id}_session{session_number}"
                                                    user_session_dir = os.path.join(data_dir, session_folder)

                                                    if os.path.exists(user_session_dir):
                                                        shutil.rmtree(user_session_dir)

                                                    os.makedirs(user_session_dir)

                                                    user_docs_dir = os.path.join(user_session_dir, 'docs')
                                                    os.makedirs(user_docs_dir, exist_ok=True)
                                                    attachments_data = []

                                                    await attachment.save(os.path.join(user_docs_dir, attachment.filename))
                                                    file_path = os.path.join(user_docs_dir, attachment.filename)

                                                    attachments_data.append({
                                                        "file_path": file_path,
                                                        "file_extension": file_extension,
                                                        "text_file_path": None
                                                    })
                                                    all_documents = []
                                                    for attachment_data in attachments_data:
                                                        file_path = attachment_data["file_path"]
                                                        file_extension = attachment_data["file_extension"]
                                                        raw_text, text_file_path = await self.process_file(file_path, file_extension)
                                                        if raw_text is not None:
                                                            all_documents.append({"raw_text": raw_text, "text_file_path": text_file_path})
                                                    processed_files = []

                                                    max_character_count = 20000

                                                    for file in os.listdir(user_docs_dir):
                                                        if file.endswith('.txt'):
                                                            file_path = os.path.join(user_docs_dir, file)
                                                            with open(file_path, 'r', encoding='latin-1') as text_file:
                                                                content = text_file.read()
                                                                self.char += len(content)

                                                                if len(content) > max_character_count:
                                                                    content = content[:max_character_count]

                                                            batch_file_name = f"{file[:-4]}_truncated.txt"
                                                            batch_file_path = os.path.join(user_docs_dir, batch_file_name)
                                                            with open(batch_file_path, 'w', encoding='latin-1') as batch_file:
                                                                batch_file.write(content)

                                                            processed_files.append(file)

                                                            os.remove(file_path)
                                                
                                                    try:
                                                        embed = None
                                                        embed_message = None
                                                        if not await asyncio.wait_for(self.indexing_process(user_session_dir, all_documents, embed, embed_message), timeout=30):
                                                            if os.path.exists(user_session_dir):
                                                                try:
                                                                    shutil.rmtree(user_session_dir)
                                                                except Exception as e:
                                                                    print(f"Error while deleting the user session directory: {e}")
                                                            
                                                    except asyncio.TimeoutError:
                                                        if self.llm_predictor is not None:
                                                            self.llm_predictor = None

                                                        if self.index is not None:
                                                            self.index = None

                                                        if self.prompt_helper is not None:
                                                            self.prompt_helper = None
                                                        
                                                        if os.path.exists(user_session_dir):
                                                            try:
                                                                shutil.rmtree(user_session_dir)
                                                            except Exception as e:
                                                                print(f"Error while deleting the user session directory: {e}")
                                                                                        
                                                    if os.path.exists(user_session_dir):
                                                        try:
                                                            shutil.rmtree(user_session_dir)
                                                        except Exception as e:
                                                            print(f"Error while deleting the user session directory: {e}")

                                                    try:
                                                        response = await asyncio.wait_for(
                                                            asyncio.get_event_loop().run_in_executor(self.executor, self.run_mini_bot, instruction),
                                                            timeout=20
                                                        )

                                                        if len(response) > 2000:
                                                            await message.channel.trigger_typing()

                                                            chunks = []
                                                            while len(response) > 2000:
                                                                last_period_index = response[:2000].rfind(".")

                                                                if last_period_index != -1:
                                                                    chunk = response[:last_period_index+1].strip()
                                                                    response = response[last_period_index+1:].strip()
                                                                else:
                                                                    chunk = response[:2000].strip()
                                                                    response = response[2000:].strip()

                                                                chunks.append(chunk)
                                                            chunks.append(response)
                                                            sent_message = await message.reply(chunks[0])

                                                            for chunk in chunks[1:]:
                                                                sent_message = await message.channel.send(chunk)

                                                        else:
                                                            await message.channel.send(response)

                                                        if sent_message:
                                                            if message.author.id != self.ctx.author.id:
                                                                await self.deduct_iteration(message)

                                                    except asyncio.TimeoutError:
                                                        await self.ctx.channel.send("oops, I think we broke the transaction...")
                                                        if self.llm_predictor is not None:
                                                            self.llm_predictor = None

                                                        if self.index is not None:
                                                            self.index = None

                                                        if self.prompt_helper is not None:
                                                            self.prompt_helper = None
                                                        
                                                    if self.llm_predictor is not None:
                                                        self.llm_predictor = None

                                                    if self.index is not None:
                                                        self.index = None

                                                    if self.prompt_helper is not None:
                                                        self.prompt_helper = None

                                                except Exception as e:
                                                    embed = Embed(title="Embed Error", description="", color=0x0000FF)
                                                    print(f"Unexpected error occurred: {e}")
                                                    await self.ctx.send(embed=embed, hidden=True)
                                            asyncio.create_task(quick_embed())
                                            return
                        
                            if re.sub(r'<@1130638110196256828>', '', message.content).strip().startswith('embed') and "Full_Embed" in user_access:
                                
                                if self.learning_session == False:
                                    member_id = self.ctx.author.id

                                    # objects for transaction [>
                                    dm_channel = await self.ctx.author.create_dm()
                                    self.dm_channel = dm_channel

                                    if isinstance(message.channel, discord.DMChannel):
                                        channel_link = f'Direct Message'
                                    else:
                                        channel_link = f'[direct messages](https://discord.com/channels/@me/{self.dm_channel.id})'

                                    original_channel_link = f"<#{message.channel.id}>"
                                    
                                    dm_embed_notif = None
                                    if not message.attachments:

                                        # send istruction if not in direct message [>
                                        if not isinstance(self.ctx.channel, discord.DMChannel):
                                            embed = Embed(title="📩  Direct Message Sent", color=0x00FF00)
                                            embed.add_field(name="", value=f"Please check your {channel_link} to initialize embedding", inline=False)
                                            embed.set_footer(text="If you do not receive the message, please check that you have direct messages from server members enabled in your Discord settings.")
                                            self.message = await self.ctx.send(embed=embed, hidden=True)

                                        while True:
                                            try:
                                                user_id = str(self.ctx.author.id)
                                                data_dir = os.path.join('data')

                                                if not os.path.exists(data_dir):
                                                    os.makedirs(data_dir)

                                                session_folder = f"{user_id}_session{session_number}"
                                                user_session_dir = os.path.join(data_dir, session_folder)

                                                if os.path.exists(user_session_dir):
                                                    shutil.rmtree(user_session_dir)

                                                os.makedirs(user_session_dir)

                                                user_docs_dir = os.path.join(user_session_dir, 'docs')
                                                os.makedirs(user_docs_dir, exist_ok=True)
                                                attachments_data = await self.gather_files(dm_channel, member_id, user_docs_dir, self.role_status, session_number)
                                                if attachments_data is None:
                                                    if os.path.exists(user_session_dir):
                                                        try:
                                                            shutil.rmtree(user_session_dir)
                                                        except Exception as e:
                                                            print(f"Error while deleting the user session directory: {e}")
                                                    else:
                                                        print(f"The user session directory '{user_session_dir}' does not exist.")
                                                    self.learning_session = False
                                                    asyncio.create_task(self.stop_sending_dummy_requests())

                                                    if self.llm_predictor is not None:
                                                        self.llm_predictor = None

                                                    if self.index is not None:
                                                        self.index = None

                                                    if self.prompt_helper is not None:
                                                        self.prompt_helper = None

                                                    return
                                                all_documents = []
                                                for attachment_data in attachments_data:
                                                    file_path = attachment_data["file_path"]
                                                    file_extension = attachment_data["file_extension"]
                                                    raw_text, text_file_path = await self.process_file(file_path, file_extension)
                                                    if raw_text is not None:
                                                        all_documents.append({"raw_text": raw_text, "text_file_path": text_file_path})

                                                embed = Embed(title="", description="✅  Initializing...", color=0x00FF00)
                                                embed.add_field(name="", value="⌛  Processing data...", inline=False)

                                                embed_message = await self.dm_channel.send(embed=embed)
                                                await self.batch_files_check(user_docs_dir, dm_channel, self.role_status)
                                                if len(os.listdir(user_docs_dir)) == 0:
                                                    embed = discord.Embed(title="Data Error", color=0x00ff00)
                                                    embed.add_field(name="", value="The data directory is empty or corrupted, and the process cannot continue", inline=False)
                                                    embed.add_field(name="", value="Create Error Report: (https://discord.com/channels/907301373387898950/1139905745945640980)\nCreate Support Ticket: (https://discord.com/channels/907301373387898950/1097214187949801692)", inline=False)
                                                    embed.add_field(name="Would you like to upload other data? Reply Y/n. Y will allow re-upload, N will cancel operations.", value="", inline=False)
                                                    def check(message):
                                                        return message.author == self.ctx.author and (message.content.isdigit() or message.content.lower() == 'n' or message.content.lower() == 'y')
                                                    await self.dm_channel.send(embed=embed)
                                                    reply_message = await bot.wait_for('message', check=check, timeout=120)
                                                    content = reply_message.content.strip()

                                                    if content.upper() == 'N':
                                                        if os.path.exists(user_session_dir):
                                                            try:
                                                                shutil.rmtree(user_session_dir)
                                                            except Exception as e:
                                                                print(f"Error while deleting the user session directory: {e}")
                                                        else:
                                                            print(f"The user session directory '{user_session_dir}' does not exist.")
                                                        return
                                                    if content.upper() == 'Y':
                                                        continue
                                                else:
                                                    break
                                            
                                            except asyncio.TimeoutError:
                                                embed = Embed(title="**Session Expired**", color=0xFFA500)
                                                embed.add_field(name="*No response received. Process canceled...*", value="", inline=False)
                                                await self.dm_channel.send(embed=embed)
                                                if os.path.exists(user_session_dir):
                                                    try:
                                                        shutil.rmtree(user_session_dir)
                                                    except Exception as e:
                                                        print(f"Error while deleting the user session directory: {e}")
                                                else:
                                                    print(f"The user session directory '{user_session_dir}' does not exist.")
                                                await self.exit_session_instance()
                                                return None
                                                                
                                    else: 
                                        if message.attachments:
                                            attachment = message.attachments[0]
                                            file_extension = attachment.filename.split('.')[-1]
                                            num_attachments = 0

                                            if file_extension in ['txt', 'doc', 'docx', 'odt', 'rtf', 'python', 'lua', 'epub', 'c', 'cpp', 'rust', 'nim', 'csv', 'excel', 'js', 'sh', 'ps1', 'css', 'php', 'html', 'conf', 'log', 'pcap', 'ocsf', 'xml', 'json', 'sql']:
                                                if self.role_status == 'limited':
                                                    num_attachments = min(len(message.attachments), 10)  
                                                else:
                                                    num_attachments = min(len(message.attachments), 10)  

                                                self.count = num_attachments
                                                try:
                                                    attachment = message.attachments[0]
                                                    file_extension = attachment.filename.split('.')[-1]

                                                    user_id = str(self.ctx.author.id)
                                                    data_dir = os.path.join('data')

                                                    if not os.path.exists(data_dir):
                                                        os.makedirs(data_dir)

                                                    session_folder = f"{user_id}_session{self.session_number}"
                                                    user_session_dir = os.path.join(data_dir, session_folder)

                                                    if os.path.exists(user_session_dir):
                                                        shutil.rmtree(user_session_dir)

                                                    os.makedirs(user_session_dir)

                                                    user_docs_dir = os.path.join(user_session_dir, 'docs')
                                                    os.makedirs(user_docs_dir, exist_ok=True)
                                                    
                                                    attachments_data = []

                                                    embed = Embed(title="", description="✅  Initializing...", color=0x00FF00)
                                                    embed.add_field(name="", value="⌛  Processing data...", inline=False)
                                                    embed_message = await message.channel.send(embed=embed)

                                                    for attachment in message.attachments[:num_attachments]:
                                                        file_extension = attachment.filename.split('.')[-1]
                                                        await attachment.save(os.path.join(user_docs_dir, attachment.filename))
                                                        file_path = os.path.join(user_docs_dir, attachment.filename)
                                                        attachments_data.append({
                                                            "file_path": file_path,
                                                            "file_extension": file_extension,
                                                            "text_file_path": None
                                                        })
                                                    all_documents = []
                                                    for attachment_data in attachments_data:
                                                        file_path = attachment_data["file_path"]
                                                        file_extension = attachment_data["file_extension"]
                                                        raw_text, text_file_path = await self.process_file(file_path, file_extension)
                                                        if raw_text is not None:
                                                            all_documents.append({"raw_text": raw_text, "text_file_path": text_file_path})

                                                    await self.batch_files_check(user_docs_dir, dm_channel, self.role_status)
                                                    if len(os.listdir(user_docs_dir)) == 0:
                                                        embed = discord.Embed(title="Data Error", color=0x00ff00)
                                                        embed.add_field(name="", value="The data directory is empty or corrupted, and the process cannot continue", inline=False)
                                                        embed.add_field(name="", value="Create Error Report: (https://discord.com/channels/907301373387898950/1139905745945640980)\nCreate Support Ticket: (https://discord.com/channels/907301373387898950/1097214187949801692)", inline=False)
                                                        
                                                        if os.path.exists(user_session_dir):
                                                            try:
                                                                shutil.rmtree(user_session_dir)
                                                            except Exception as e:
                                                                print(f"Error while deleting the user session directory: {e}")
                                                        else:
                                                            print(f"The user session directory '{user_session_dir}' does not exist.")
                                                        

                                                except Exception as e:
                                                    embed = Embed(title="Embed Error", description="", color=0x0000FF)
                                                    print(f"Unexpected error occurred: {e}")
                                                    await self.ctx.send(embed=embed, hidden=True)

                                            else:
                                                embed = Embed(title="Unsupported Filetype", description="", color=0x0000FF)
                                                await self.ctx.send(embed=embed, hidden=True)
                                                return
                                        
                                    embed.set_field_at(0, name="", value="✅  Data Ready!", inline=False)
                                    embed.add_field(name="", value="⌛  Indexing Data... ↻", inline=True)
                                    await embed_message.edit(embed=embed)
                                
                                
                                    try:
                                        if not await asyncio.wait_for(self.indexing_process(user_session_dir, all_documents, embed_message, embed), timeout=300):
                                            if os.path.exists(user_session_dir):
                                                try:
                                                    shutil.rmtree(user_session_dir)
                                                except Exception as e:
                                                    print(f"Error while deleting the user session directory: {e}")

                                    except asyncio.TimeoutError:
                                        print("Timeout occurred during indexing process. Continuing operation.")
                                        if self.llm_predictor is not None:
                                            self.llm_predictor = None

                                        if self.index is not None:
                                            self.index = None

                                        if self.prompt_helper is not None:
                                            self.prompt_helper = None
                                        
                                        if os.path.exists(user_session_dir):
                                            try:
                                                shutil.rmtree(user_session_dir)
                                            except Exception as e:
                                                print(f"Error while deleting the user session directory: {e}")
                            
                                    if os.path.exists(user_session_dir):
                                        try:
                                            shutil.rmtree(user_session_dir)
                                        except Exception as e:
                                            print(f"Error while deleting the user session directory: {e}")
                                    
                                    embed.set_field_at(1, name="", value="✅  Indexing Complete!", inline=False)
                                    embed.add_field(name="Location", value=original_channel_link, inline=False)
                                    embed.add_field(name="Embedded", value=f"{self.char} characters in {self.time}", inline=False)
                                    embed.set_footer(text=current_datetime.strftime("%Y-%m-%d %H:%M:%S"))
                                    await embed_message.edit(embed=embed)

                                    self.learning_session = True
                                    asyncio.create_task(self.start_sending_dummy_requests())
                            
                                    return
                                else:
                                    embed = Embed(title="", description="This session already has an active embedding", color=0x0000FF)
                                    await self.ctx.send(embed=embed, hidden=True)
                                    return
                        
                            if re.sub(r'<@1130638110196256828>', '', message.content).strip().startswith('set') and "Set" in user_access:
                              
                                self.session_set = True

                            if "Chat" in user_access:
                                
                                if self.learning_session == True:
                                    if re.sub(r'<@1130638110196256828>', '', message.content).strip().startswith('exit') and "Full_Embed" in user_access:

                                        self.learning_session = False
                                        asyncio.create_task(self.stop_sending_dummy_requests())

                                        if self.llm_predictor is not None:
                                            self.llm_predictor = None

                                        if self.index is not None:
                                            self.index = None

                                        if self.prompt_helper is not None:
                                            self.prompt_helper = None

                                        embed = Embed(title="", description="✅  Embedding Discarded", color=0x00FF00)
                                        await message.channel.send(embed=embed)

                                        return
                                    
                                    await message.channel.trigger_typing()

                                    message_content = []

                                    if self.context > 0:
                                        channel = message.channel  

                                        async for prev_message in channel.history(limit=self.context, before=message):
                                            message_content.append(prev_message.content)

                                    message_content.append(message.content)
                                    role_index = self.role["user_id"].index(message.author.id)
                                    user_role = self.role["user_role"][role_index]
                                    prompt = self.role["prompt"][role_index]

                                    input_text = ' '.join([prompt] + message_content)
                                    user_id_pattern = r"<@[\d]+>"
                                    input_text = re.sub(user_id_pattern, "", input_text)
                                    await message.channel.trigger_typing()

                                    async def api_call():

                                        response = await asyncio.get_running_loop().run_in_executor(self.executor, self.run_chatbot, input_text)

                                        message_content = []  

                                        if len(response) > 2000:
                                            await message.channel.trigger_typing()

                                            chunks = []
                                            while len(response) > 2000:
                                                last_period_index = response[:2000].rfind(".")

                                                if last_period_index != -1:
                                                    chunk = response[:last_period_index+1].strip()
                                                    response = response[last_period_index+1:].strip()
                                                else:
                                                    chunk = response[:2000].strip()
                                                    response = response[2000:].strip()

                                                chunks.append(chunk)
                                            chunks.append(response)

                                            sent_message = await message.reply(chunks[0])

                                            for chunk in chunks[1:]:
                                                sent_message = await message.channel.send(chunk)
                                            
                                        else:
                                            sent_message = await message.channel.send(response)

                                        if sent_message:
                                            if message.author.id != self.ctx.author.id:
                                                await self.deduct_iteration(message)
                                            
                                    asyncio.create_task(api_call())
                                    return

                                else:

                                    conversationLog = []

                                    if self.session_set == False:
                                        await message.channel.trigger_typing()
                                        user_role = "user"
                                        if self.context == 0:
                                            if self.nicknames == "True":
                                                def resolve_user_nickname(user_id):
                                                    member = message.guild.get_member(int(user_id))
                                                    if member:
                                                        return member.nick if member.nick else member.name
                                                    else:
                                                        return "Unknown User"
                                                nickname = resolve_user_nickname(message.author.id)
                                            if message.author.id in self.role["user_id"]:
                                                role_index = self.role["user_id"].index(message.author.id)
                                                user_role = self.role["user_role"][role_index]
                                                instance_prompt = self.role["prompt"][role_index]

                                            else:
                                                user_role = 'user'
                                                instance_prompt = ''

                                            if self.nicknames == "True":
                                                conversationLog.append({'role': user_role, 'content': f'{instance_prompt} {nickname} {message.content}'})
                                            else:
                                                conversationLog.append({'role': user_role, 'content': f'{instance_prompt} {message.content}'})
                                        
                                        else:
                                            if self.segmented_context == "True":
                                                prevMessages = []
                                                async for msg in message.channel.history():
                                                    if msg.author.id == message.author.id:
                                                        prevMessages.append(msg.content)
                                                        if len(prevMessages) == self.context:
                                                            break

                                                prevMessages.reverse()
                                                combined_content = ' '.join(prevMessages)

                                                if message.author.id in self.role["user_id"]:
                                                    index = self.role["user_id"].index(message.author.id)
                                                    user_role = self.role["user_role"][index]
                                                    instance_prompt = self.role["prompt"][index]
                                                else:
                                                    if self.ctx.author.id in self.role["user_id"]:
                                                        index = self.role["user_id"].index(self.ctx.author.id)
                                                        user_role = self.role["user_role"][index]
                                                        instance_prompt = self.role["prompt"][index]

                                                conversationLog.append({'role': user_role, 'content': f'{instance_prompt} {combined_content}'}) 

                                            if self.stacked_context == "True":
                                                prev_messages = []
                                                async for msg in message.channel.history(limit=self.context + 1):
                                                    prev_messages.append(msg)                                                

                                                prev_messages.reverse()

                                                conversationLog = []

                                                for msg in prev_messages:
                                                    if msg.author.id in self.role["user_id"]:
                                                        role_index = self.role["user_id"].index(msg.author.id)
                                                        user_role = self.role["user_role"][role_index]
                                                        instance_prompt = self.role["prompt"][role_index]
                                                    else:
                                                        user_role = 'user'
                                                        instance_prompt = ''

                                                    conversationLog.append({
                                                        'role': user_role,
                                                        'content': f'{instance_prompt} {msg.content}',
                                                    })

                                            if self.combined_context == "True":
                                                prevMessages = []

                                                if self.nicknames == "True":
                                                    def resolve_user_nickname(user_id):
                                                        member = message.guild.get_member(int(user_id))
                                                        if member:
                                                            return member.nick if member.nick else member.name
                                                        else:
                                                            return "Unknown User"

                                                    async for msg in message.channel.history(limit=self.context + 1):
                                                        author_id = msg.author.id
                                                        nickname = resolve_user_nickname(author_id)  
                                                        message_content = f'{nickname} {msg.content}'  
                                                        prevMessages.append(message_content)
                                                else:
                                                    async for msg in message.channel.history(limit=self.context + 1):
                                                        prevMessages.append(msg.content)

                                                prevMessages.reverse()
                                                combined_content = ' '.join(prevMessages)

                                                if message.author.id in self.role["user_id"]:
                                                    index = self.role["user_id"].index(message.author.id)
                                                    user_role = self.role["user_role"][index]
                                                    instance_prompt = self.role["prompt"][index]
                                                else:
                                                    if self.ctx.author.id in self.role["user_id"]:
                                                        index = self.role["user_id"].index(self.ctx.author.id)
                                                        user_role = self.role["user_role"][index]
                                                        instance_prompt = self.role["prompt"][index]

                                                conversationLog.append({'role': user_role, 'content': f'{instance_prompt} {combined_content}'})

                                    else:
                                        role_index = self.role["user_id"].index(self.ctx.author.id)
                                        user_role = self.role["user_role"][role_index]

                                        tokens_words = ["tokens"]  
                                        context_words = ["context"] 
                                        model_words = ["model", "gpt 3.5", "gpt 4", "gpt-3.5-turbo gpt-4", "gpt-4-1106-preview", "gpt-4-0613", "gpt-4-0314", "gpt-3.5-turbo-16k-0613", "gpt-3.5-turbo-16k", "gpt-3.5-turbo-1106", "gpt-3.5-turbo-0613", "gpt-3.5-turbo-0301"] 
                                        size_words = ["size", "landscape", "portrait", "banner"] 
                                        number_words = ["number", "generations"] 
                                        style_words = ["style", "vivid", "natural"] 
                                        nicknames_words = ["nicknames", "user names"] 
                                        role_words = ["role"] 
                                        frequency_words = ["frequency"] 
                                        presence_words = ["presence"] 
                                        top_p_words = ["top_p"] 
                                        temperature_words = ["temperature", "creativity", "randomness"] 
                                        image_model_words = ["dalle", "dalle2", "dalle3"] 
                                        revised_prompt_words = ["revised", "revised prompt", "revised_prompt"] 
                                        prompt_words = ["prompt"] 
                                        time_words = ["s, second, seconds, m, minute, minutes, h, hour, hours, w, week, weeks"] 
                                        iterations_words = ["iterations", "generations"] 
                                        prompt = "extract the variables and figures from the message into json syntax, possible variables are: "

                                        if any(keyword in str(message) for keyword in tokens_words):
                                            prompt += "tokens (integer between 1 and 4000), "
                                        if any(keyword in str(message) for keyword in context_words):
                                            prompt += "context (integer between 1 and 10), "
                                        if any(keyword in str(message) for keyword in model_words):
                                            prompt += "model (string options: gpt-3.5-turbo, gpt-4, gpt-4-1106-preview, gpt-4-0613, gpt-4-0314, gpt-3.5-turbo-16k-0613, gpt-3.5-turbo-16k, gpt-3.5-turbo-1106, gpt-3.5-turbo-0613, gpt-3.5-turbo-0301), if the user mentions tokenizer the tokenizer integer is part of the model name, for example tokenizer 0301 would mean to use gpt-3.5-turbo-0301,  "
                                        if any(keyword in str(message) for keyword in size_words):
                                            prompt += "size (string dimension options 256x256, 512x512, 1024x1024, 1024x1792, 1792x1024), If the message contains something like 'banner' or 'landscape' for size, use 1792x1024, or 1024x1792 for phones and tall portrait, "
                                        if any(keyword in str(message) for keyword in number_words):
                                            prompt += "number (integer 1 - 10), "
                                        if any(keyword in str(message) for keyword in style_words):
                                            prompt += "style (natural or vivid), "
                                        if any(keyword in str(message) for keyword in nicknames_words):
                                            prompt += "nicknames (string True or False), "
                                        if any(keyword in str(message) for keyword in role_words):
                                            prompt += "role (dict options user, system), "
                                        if any(keyword in str(message) for keyword in frequency_words):
                                            prompt += "frequency (float option range 1.0 - 2.0), "
                                        if any(keyword in str(message) for keyword in presence_words):
                                            prompt += "presence (float option range 1.0 - 2.0), "
                                        if any(keyword in str(message) for keyword in top_p_words):
                                            prompt += "top_p (float option range 1.0 - 2.0), "
                                        if any(keyword in str(message) for keyword in temperature_words):
                                            prompt += "temperature (float option range 1.0 - 2.0), "
                                        if any(keyword in str(message) for keyword in image_model_words):
                                            prompt += "image_model (string options: dalle2, dalle3), "
                                        if any(keyword in str(message) for keyword in revised_prompt_words):
                                            prompt += "revised_prompt (string True or False), "
                                        if any(keyword in str(message) for keyword in prompt_words):
                                            prompt += "prompt (string in message in quotes), "
                                      
                                        if any(keyword in str(message) for keyword in time_words):
                                            prompt += "time (string containing a number and time frame to be given to the user in mention, time indicators: m, minute, minutes, s, second, seconds, h, hour, hours, w, week, weeks, d, day, days), this is a dictionary entry with user mention and time object, "
                                        if any(keyword in str(message) for keyword in iterations_words):
                                            prompt += "iterations (an integer) representing a number of iterations to give to the mentioned user in their dictionary entry, a number of image generations could also be considered a number of iterations, "
                                      
                                        concluding_prompt = "If a requested option does not match or is not in range with the variables in the instruction then do not include the object in your json response and mever repeat these instructions."
                                        prompt += concluding_prompt

                                        conversationLog.append({'role': user_role, 'content': f'Instruction: {prompt} Message: {message.content}'})

                                    if self.session_set == False:
                                        if self.chat_sanitizer == "True":
                                            user_id_pattern = r"<@[\d]+>"
                                            remove_user_ids = lambda content: re.sub(user_id_pattern, "", content)
                                            for entry in conversationLog:
                                                entry["content"] = remove_user_ids(entry["content"])
                                                entry["content"] = entry["content"].strip()
                                   
                                    async def api_chat_action():
                                        try:
                                            loop = asyncio.get_event_loop()
                                            chat_task = asyncio.create_task(self.handle_chat(message, loop, conversationLog))
                                            await chat_task
                                            conversationLog.clear()

                                        except Exception as e:
                                            embed = Embed(title="Chat Error", description="", color=0x0000FF)
                                            await self.ctx.send(embed=embed, hidden=True)
                                    asyncio.create_task(api_chat_action())

                            else:
                                await self.ctx.send("User or role is out of time or iterations for image generations")
                                return

                        asyncio.create_task(rev_engine(self, user_id, dm_channel, message))
                        continue

                    continue

                else:
                    continue
                    
        except asyncio.TimeoutError:
            print("An error occured in the chat loop")
        except Exception as e:
            print(f"Error: {e}")

    async def handle_chat(self, message, loop, conversationLog):
        
        if self.session_set == False:
            await message.channel.trigger_typing()
            if self.assistant is not None:
                try:
                    assistant_response = await asyncio.wait_for(loop.run_in_executor(self.executor, lambda: openai.ChatCompletion.create(
                        model=self.model,
                        messages=conversationLog,
                        api_key=self.selected_api_key,
                        tools=[{"type": self.assistant}],
                    )), timeout=60)  

                    assistant_message = assistant_response['choices'][0]['message']['content']

                    await message.channel.send(assistant_message)
                except Exception as e:
                    print(f"Error occurred while creating assistant: {e}")

            else:
                try:
                    if self.api_engine == "openai":
                        openai.api_base = self.api_base_default
                        response = await asyncio.wait_for(loop.run_in_executor(self.executor, lambda: openai.ChatCompletion.create(
                            model=self.model,
                            messages=conversationLog,
                            api_key=self.selected_api_key,
                            temperature=self.temperature,
                            max_tokens=self.tokens,
                            frequency_penalty=self.frequency,
                            presence_penalty=self.presence,
                            top_p=self.top_p
                        )), timeout=60)  

                        chatbot_response = response['choices'][0]['message']['content']
                    else:
                        openai.api_base = self.api_base
                        response = await asyncio.wait_for(loop.run_in_executor(self.executor, lambda: openai.ChatCompletion.create(
                            model=self.model,
                            messages=conversationLog,
                            temperature=self.temperature,
                            max_tokens=self.tokens,
                            top_k=self.top_k,
                            repeat_penalty=self.repeat_penalty,
                            top_p=self.top_p,
                        )), timeout=60)

                        chatbot_response = response.choices[0].message['content']

                        if self.chat_sanitizer == "True":
                            chatbot_response = response.choices[0].message['content'].replace("<|im_end|>", " ")
                            chatbot_response = response.choices[0].message['content'].replace("<|im_end||", " ")
            
                            chatbot_response = re.sub(r'<\|.*?\|>', '', chatbot_response)  # Remove <|...|> syntax
                            chatbot_response = re.sub(r'<@.*?>', '', chatbot_response)  # Remove <@...> syntax
                            chatbot_response = re.sub(r'<.*?>', '', chatbot_response)  # Remove <...> syntax
                            chatbot_response = re.sub(r'<\|/img\|\|', '', chatbot_response)  # Remove <|/img|| syntax
                            chatbot_response = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', chatbot_response)  # Remove URLs
                            chatbot_response = re.sub(r'```.*?```', '', chatbot_response, flags=re.DOTALL)  # Remove code blocks
                            chatbot_response = re.sub(r'print\(.*?\)', '', chatbot_response)  # Remove print statements
                            chatbot_response = chatbot_response.replace('<', '').replace('>', '')  # Remove < and >

                except asyncio.TimeoutError:
                    await message.channel.send("OpenAI API timed out...")
                    return

                if chatbot_response.startswith('Ether:'):
                    chatbot_response = chatbot_response[len('Ether:'):].strip()
                if chatbot_response.startswith(':'):
                    chatbot_response = chatbot_response[1:].strip()

                if len(chatbot_response) > 2000:
                    await message.channel.trigger_typing()

                    chunks = []
                    while len(chatbot_response) > 2000:
                        last_period_index = chatbot_response[:2000].rfind(".")

                        if last_period_index != -1:
                            chunk = chatbot_response[:last_period_index + 1].strip()
                            chatbot_response = chatbot_response[last_period_index + 1:].strip()
                        else:
                            chunk = chatbot_response[:2000].strip()
                            chatbot_response = chatbot_response[2000:].strip()

                        chunks.append(chunk)
                    chunks.append(chatbot_response)

                    sent_message = None
                    for chunk in chunks:
                        sent_message = await message.channel.send(chunk)
                else:
                    sent_message = await message.channel.send(chatbot_response)

                if sent_message:
                    if message.author.id != self.ctx.author.id:
                        await self.deduct_iteration(message)

        elif self.session_set == True:
            try:
                response = await asyncio.wait_for(loop.run_in_executor(self.executor, lambda: openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=conversationLog,
                    api_key=self.selected_api_key,
                    temperature=0.3,
                    max_tokens=500,
                )), timeout=60)  
            except asyncio.TimeoutError:
                await message.channel.send("OpenAI API timed out...")
                return

            chatbot_response = response['choices'][0]['message']['content']
            chatbot_response_json = json.loads(chatbot_response)

            variable_types = {
                "tokens": int,
                "context": int,
                "model": str,
                "size": str,
                "style": str,
                "number": int,
                "nicknames": str,
                "role": dict,
                "frequency": float,
                "presence": float,
                "top_p": float,
                "temperature": float,
                "image_model": str,
                "revised_prompt": str
            }

            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            updated_variables = {}  

            for variable, value in chatbot_response_json.items():
                if variable == "role":
                    self.role["user_role"][0] = value
                    updated_variables["role"] = value

                if variable == "prompt":
                    self.role["prompt"][0] = value
                    updated_variables["prompt"] = value

                if variable in variable_types and isinstance(value, variable_types[variable]):
                    setattr(self, variable, value)
                    updated_variables[variable] = value

            if "prompt" in updated_variables:
                updated_variables["prompt"] = ' '.join(updated_variables["prompt"].split()[:60]) + '...'

            embed = discord.Embed(title="Updated Session Variables", color=0x00ff00)  
            for variable, value in updated_variables.items():
                embed.add_field(name=variable, value=value, inline=False)

            sent_message = await message.channel.send(embed=embed)
            if sent_message is not None:
                if message.author.id != self.ctx.author.id:
                    await self.deduct_iteration(message)

            self.session_set = False

    async def handle_image(self, prompt, message, number, size):

        async def make_art():
            if self.image_model == "dalle2":
                try:
                    if self.size not in ["256x256", "512x512", "1024x1024"]:
                        await message.channel.send("DALL E 2 only supports image sizes 256x256, 512x512, and 1024x1024, see `/ether [size]`")
                        return
                    payload = {
                        "prompt": prompt,
                        "n": self.number,
                        "size": self.size
                    }
                    headers = {
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {self.selected_api_key}"
                    }

                    async with aiohttp.ClientSession() as session:
                        async with session.post("https://api.openai.com/v1/images/generations", json=payload, headers=headers) as response:
                            response_json = await response.json()

                        if 'data' in response_json:
                            image_files = []
                            revised_prompt = None

                            for i, image_data in enumerate(response_json['data']):
                                image_url = image_data['url']

                                async with session.get(image_url) as image_response:
                                    image_data = io.BytesIO(await image_response.read())

                                image_files.append(discord.File(image_data, filename=f"{message.author.id}{i+1}.png"))

                            sent_message = await message.reply(files=image_files)

                            if sent_message:
                                if message.author.id != self.ctx.author.id:
                                    for _ in range(number):
                                        await self.deduct_iteration(message)

                        else:
                            await message.reply("There was an API error....")

                except Exception as e:
                    print(f"An error occurred: {e}")
         
            else:
                try:
                    if self.size not in ["1024x1024", "1792x1024", "1024x1792"]:
                        await message.channel.send("DALL E 3 only supports image sizes 1024x1024, 1792x1024, and 1024x1792, see `/openai-options [size]`")
                        return
                    payload = {
                        "model": "dall-e-3",
                        "prompt": prompt,
                        "n": 1,
                        "size": self.size,
                        "style": self.style
                    }
                    headers = {
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {self.selected_api_key}"
                    }

                    async with aiohttp.ClientSession() as session:
                        image_files = []
                        revised_prompt = None

                        for _ in range(number):
                            async with session.post("https://api.openai.com/v1/images/generations", json=payload, headers=headers) as response:
                                response_json = await response.json()

                            if 'data' in response_json:
                                for i, image_data in enumerate(response_json['data']):
                                    image_url = image_data['url']

                                    async with session.get(image_url) as image_response:
                                        image_data = io.BytesIO(await image_response.read())

                                    image_files.append(discord.File(image_data, filename=f"{message.author.id}{i+1}.png"))

                                if self.number == 1 and self.revised_prompt == True:
                                    if 'revised_prompt' in response_json['data'][0]:
                                        revised_prompt = response_json['data'][0]['revised_prompt']
                        sent_message = None
                        if self.revised_prompt == True and self.number == 1:
                            if revised_prompt:
                                sent_message = await message.reply(content=revised_prompt, files=image_files)
                            else:
                                sent_message = await message.reply(files=image_files)
                        else:
                            if image_files:
                                sent_message = await message.reply(files=image_files)

                        if sent_message:
                            if message.author.id != self.ctx.author.id:
                                for _ in range(number):
                                    await self.deduct_iteration(message)

                        else:
                            await message.reply("There was an API error....")

                except Exception as e:
                    print(f"An error occurred: {e}")

        asyncio.create_task(make_art())

    async def variate_image_command(self, user_id, prompt, temp_file_path, selected_api_key, number, size, loop, message):
        async def variate_image(message):
            try:
                await self.channel.trigger_typing()
                # Set the OpenAI API key
                openai.api_key = self.selected_api_key
                response = await loop.run_in_executor(
                    self.executor,
                    lambda: openai.Image.create_variation(
                        image=open(temp_file_path, "rb"),
                        n=number,
                        size=size
                    )
                )

                image_files = []

                if isinstance(response, dict) and 'data' in response:
                    await self.channel.trigger_typing()
                    for i in range(number):
                        image_url = response['data'][i]['url']

                        async with aiohttp.ClientSession() as session:
                            async with session.get(image_url) as image_response:
                                image_data = await image_response.read()

                        image_file = discord.File(io.BytesIO(image_data), filename=f"{message.author.id}{i+1}.png")
                        image_files.append(image_file)

                    sent_message = await message.reply(files=image_files)

                    os.remove(temp_file_path)

                    if sent_message:
                        if message.author.id != self.ctx.author.id:
                            for _ in range(number):
                                await self.deduct_iteration(message)

            except Exception as e:
                await message.reply("Apologies, there was an error communicating with OpenAI.")
                return
        try:
            await asyncio.wait_for(variate_image(message), timeout=60)  
        except asyncio.TimeoutError:
            await message.reply("Apologies, communications with OpenAI timed out.")
            return

    async def gather_files(self, dm_channel, member_id, user_docs_dir, role_status, session_number):
        while True:
            num_attachments = 0
            attachments = None
            embed = Embed(title="📮  Choose Data", color=0x00FF00)
            embed.description = "*Reply with weblinks, attachments, or both*"
            embed.add_field(name="Supported File Types", value="txt, docx, doc, pdf, rtf, odt, js, py, sh, lua, ps1, epub, c, cpp, rs, nim, csv, xls, xlsx, html, php, css, conf, log, pcap, ocsf, xml, json, sql", inline=False)
            embed.set_footer(text="Reply with C to cancel")
            message_files = await dm_channel.send(embed=embed)

            try:
                def file_check(message):
                    return message.author == dm_channel.recipient and (message.attachments or message.content.lower().strip() == 'c' or "http" in message.content.lower().strip() or "https" in message.content.lower().strip())
                file_message = await bot.wait_for('message', check=file_check, timeout=120.0)  
            except asyncio.TimeoutError:
                embed = Embed(title="**Operation Timed Out**", color=0xFFA500)
                embed.add_field(name="*Have a good day! :)*", value="", inline=False)
                await dm_channel.send(embed=embed)
                
                return None
            
            if file_message.content.lower().strip() == 'c':
                embed = Embed(title="**Session Cancelled**", color=0xFFA500)
                embed.add_field(name="*Process cancelled...*", value="", inline=False)
                await self.dm_channel.send(embed=embed)
                
                return None
            
            user_id = self.ctx.author.id
            
            attachments_data = []  
            if file_message.attachments:
                if role_status == 'limited':
                    num_attachments = min(len(file_message.attachments), 2)  
                    attachments = file_message.attachments[:num_attachments]  
                else:
                    num_attachments = min(len(file_message.attachments), 10)  
                    attachments = file_message.attachments[:num_attachments] 

                self.count = num_attachments
                
                description = f"Acquiring {num_attachments} files please wait...⌛"
                embed = Embed(title="", description=description, color=0x00FF00)
                await message_files.edit(embed=embed)
                
                for attachment in attachments:
                    file_extension = attachment.filename.split('.')[-1]

                    if file_extension not in ['txt', 'docx', 'pdf', 'rtf', 'odt', 'doc', 'js', 'py', 'sh', 'lua', 'ps1', 'epub', 'c', 'cpp', 'rs', 'nim', 'csv', "xls", "xlsx", "html", "php", "css", "conf", "log", "pcap", "json", "xml", "ocsf", "sql"]:
                        embed = Embed(title="**Format Error**", color=0xFF0000)
                        embed.add_field(name="*Unsupported File Type Detected, Ignoring file instance...*", value="", inline=False)
                        await dm_channel.send(embed=embed)
                        continue

                    file_path = os.path.join(user_docs_dir, attachment.filename)

                    await attachment.save(file_path)

                    attachments_data.append({"file_path": file_path, "file_extension": file_extension, "text_file_path": None})

            web_links = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', file_message.content)

            if web_links:
                if role_status in ('limited', 'unlimited', 'sessions', 'data'):
                    if role_status == 'limited':
                        web_links = web_links[:2]  
                    else:
                        web_links = web_links[:6]
                if file_message.attachments:
                    description = f"Acquired {num_attachments} files...✅"
                    embed = Embed(title="", description=description, color=0x00FF00)
                    embed.add_field(name="", value=f"Attempting to fetch data from {len(web_links)}links...⌛", inline=False)
                    await message_files.edit(embed=embed)
                else:
                    embed = Embed(title="", description="", color=0x00FF00)
                    embed.add_field(name="", value=f"Attempting to fetch data from {len(web_links)}links...⌛", inline=False)
                    await message_files.edit(embed=embed)
                
                try:
                    web_data = await asyncio.wait_for(self.fetch_website_text(dm_channel, user_id, user_docs_dir, web_links, session_number), timeout=60)
                    if web_data is not None:
                        attachments_data.extend(web_data)
                        description = f"Acquired {num_attachments} files...✅"
                        embed = Embed(title="", description=description, color=0x00FF00)
                        embed.add_field(name="", value=f"Acquired data from one or more web links...✅", inline=False)
                        await message_files.edit(embed=embed)
                    else:
                        if file_message.attachments:
                            description = f"Acquired {num_attachments} files...✅"
                            embed = Embed(title="", description=description, color=0x00FF00)
                            embed.add_field(name="", value=f"Error fetching one or more weblinks...❌", inline=False)
                            await message_files.edit(embed=embed)
                        else:
                            embed = Embed(title="", description="", color=0x00FF00)
                            embed.add_field(name="", value=f"Error fetching one or more weblinks...❌", inline=False)
                            await message_files.edit(embed=embed)


                except asyncio.TimeoutError:
                    print("Fetch website text timed out")
                except Exception as e:
                    print(f"Error fetching website text: {e}")

            else:
                description = f"Acquired {num_attachments} files...✅"
                embed = Embed(title="", description=description, color=0x00FF00)
                await message_files.edit(embed=embed)

            if not attachments_data:
                embed = Embed(title="No attachments or websites in the dataset", color=0xFF0000)
                embed.description = "The file array is empty. \n\nWould you like to add other files or links? (y/n)"
                notification_message = await dm_channel.send(embed=embed)

                def check(message):
                    return message.author == dm_channel.recipient and message.content.strip().lower() in ['y', 'n']

                try:
                    response_message = await bot.wait_for("message", timeout=60, check=check)

                    if response_message.content.strip().lower() == "y":
                        await notification_message.delete()
                        continue

                    elif response_message.content.strip().lower() == "n":
                        await notification_message.delete()
                        embed = Embed(title="**Session Cancelled**", color=0xFFA500)
                        await self.dm_channel.send(embed=embed)
                        for attachment_data in attachments_data:
                            file_path = attachment_data["file_path"]
                            if os.path.exists(file_path):
                                os.remove(file_path)
                            active_sessions.pop(self.channel.id, None)
                            if self.dm_channel is not None:
                                self.dm_channel = None
                        return None
                except asyncio.TimeoutError:
                    await notification_message.delete()
                    embed = Embed(title="**Session Cancelled**", color=0xFFA500)
                    embed.add_field(name="*Process Timed Out...*", value="", inline=False)
                    await self.dm_channel.send(embed=embed)
                    for attachment_data in attachments_data:
                        file_path = attachment_data["file_path"]
                        if os.path.exists(file_path):
                            os.remove(file_path)
                    active_sessions.pop(self.channel.id, None)
                    return None

            return attachments_data

    async def fetch_website_text(self, dm_channel, user_id, user_docs_dir, web_links, session_number):
     
        file_path = os.path.join(user_docs_dir, 'website_text.txt')

        with open(file_path, 'w', encoding='utf-8') as file:
            pass

        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
        ]

        for web_link in web_links:
            timeout = aiohttp.ClientTimeout(total=10)  

            try:
                for user_agent in user_agents:
                    headers = {
                        'User-Agent': user_agent
                    }
                    async with aiohttp.ClientSession(timeout=timeout, connector=aiohttp.TCPConnector(ssl=False)) as session:
                        async with session.get(web_link, headers=headers) as response:
                            if response.status != 200:
                                embed = Embed(title="Website Fetch Error", description="Unable to fetch website content...", color=0xFF0000)
                                embed.set_footer(text="The website is unreachable or error 404...")
                                await dm_channel.send(embed=embed)

                            html_content = await response.text()
                            break  
            except asyncio.TimeoutError:
                return None

            except ClientConnectorError:
                embed = Embed(title="Website Fetch Error", description="Unable to connect to the website...", color=0xFF0000)
                embed.set_footer(text="The website hostname is invalid or network connection issue...")
                await dm_channel.send(embed=embed)
                return

            soup = BeautifulSoup(html_content, 'html.parser')
            visible_text = ''
            for element in soup.find_all(text=True):
                if element.parent.name in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'a']:
                    visible_text += element + '\n'

            if not visible_text.strip():
                await dm_channel.send("No visible text found on the web page. Please try another link.")
                continue
            
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(visible_text)
       
        if os.path.getsize(file_path) == 0:
            return None
        else:
            return [{"file_path": file_path, "file_extension": "txt", "text_file_path": file_path}]

    async def batch_files_check(self, user_docs_dir, dm_channel, role_status):
        if self.role_status == "limited":
            CHARACTER_LIMIT = 2000000
        elif self.role_status == "data":
            CHARACTER_LIMIT = 10000000
        elif self.role_status == "unlimited":
            CHARACTER_LIMIT = 10000000
        
        BATCH_SIZE = 100000

        processed_files = []
        total_character_count = 0
        source_files_count = 0
        batched_file_paths = []

        for file in os.listdir(user_docs_dir):
            if file.endswith('.txt'):
                file_path = os.path.join(user_docs_dir, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as text_file:
                        file_content = text_file.read()

                    cleaned_content = re.sub(r'[^a-zA-Z0-9\s\-\(\)]+', '', file_content)
                    cleaned_content = cleaned_content.strip()  

                    num_batches = (len(cleaned_content) + BATCH_SIZE - 1) // BATCH_SIZE

                    for i in range(num_batches):
                        start = i * BATCH_SIZE
                        end = start + BATCH_SIZE
                        batch_content = cleaned_content[start:end]

                        batch_file_name = f"{file[:-4]}batch{i+1}.txt"
                        batch_file_path = os.path.join(user_docs_dir, batch_file_name)
                        with open(batch_file_path, 'w', encoding='utf-8') as batch_file:
                            batch_file.write(batch_content)

                        total_character_count += len(batch_content)
                        if total_character_count >= CHARACTER_LIMIT:
                            break

                        batched_file_paths.append(batch_file_path)

                    if total_character_count >= CHARACTER_LIMIT:
                        os.remove(file_path)
                    else:
                        processed_files.append(file)
                        source_files_count += 1

                except IOError as e:
                    print(f"Error processing file {file}: {e}")

        for file in os.listdir(user_docs_dir):
            if file.endswith('.txt') and os.path.join(user_docs_dir, file) not in batched_file_paths:
                os.remove(os.path.join(user_docs_dir, file))

        self.char = total_character_count
        return batched_file_paths

    async def convert_pdf_to_text(self, file_path, text_file_path):
        try:
            with open(file_path, 'rb') as file:
                magic_number = magic.from_buffer(file.read(2048), mime=True)

            mime_type = magic_number if magic_number.startswith('application/pdf') else None
            if magic_number or mime_type:
                pdf_document = fitz.open(file_path)

                text = ''
                for page_number in range(pdf_document.page_count):
                    page = pdf_document.load_page(page_number)
                    page_text = page.get_text().strip()  
                    page_text = page_text.replace('\n', ' ')  
                    page_text = re.sub(r'[^a-zA-Z0-9\s]', '', page_text)  
                    text += page_text

                pdf_document.close()

                with open(text_file_path, 'w', encoding='utf-8') as text_file:
                    text_file.write(text)

                os.remove(file_path)

                return text
            else:
                quarantine_directory = "quarantine"
                shutil.move(file_path, os.path.join(quarantine_directory, os.path.basename(file_path)))

                await self.check_offenses(file_path)

                return None

        except Exception as e:
            print(f"Error during PDF conversion: {e}")
            return None
        
    async def convert_doc_docx_to_text(self, file_path, text_file_path):
        try:
            mime_type = magic.from_file(file_path, mime=True)

            if mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
              
                document = Document(file_path)
                paragraphs = [para.text for para in document.paragraphs]
                text = '\n'.join(paragraphs)
            elif mime_type == "application/msword" and file_path.endswith('.doc'):
               
                soffice_command = r"/usr/bin/soffice" 

                cmd = [soffice_command, "--headless", "--convert-to", "txt:Text", "--outdir", os.path.dirname(text_file_path), file_path]

                subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                file_name, _ = os.path.splitext(os.path.basename(file_path))
                converted_file_path = os.path.join(os.path.dirname(text_file_path), f"{file_name}.txt")

                with open(converted_file_path, "r", encoding="latin-1") as txt_file:
                    text = txt_file.read()

            else:

                quarantine_directory = "quarantine"
                shutil.move(file_path, os.path.join(quarantine_directory, os.path.basename(file_path)))

                await self.check_offenses(file_path)

                return None

            with open(text_file_path, 'w', encoding='utf-8') as text_file:
                text_file.write(text)

            os.remove(file_path)

            return text

        except Exception as e:
            print(f"Error during DOC/DOCX conversion: {e}")
            return None

    async def convert_txt_to_text(self, file_path, text_file_path):
        try:
            mime_type = magic.from_file(file_path, mime=True)

            if mime_type == "text/plain":
                with codecs.open(file_path, 'r', encoding='utf-8', errors='replace') as txt_file:
                    text = txt_file.read()

                os.remove(file_path)

                text_file_path = text_file_path.replace(".txt", "_raw.txt")

                with open(text_file_path, 'w', encoding='utf-8') as text_file:
                    text_file.write(text)

                return text
            else:
                quarantine_directory = "quarantine"
                shutil.move(file_path, os.path.join(quarantine_directory, os.path.basename(file_path)))

                await self.check_offenses(file_path)

                return None

        except Exception as e:
            print(f"Error during TXT conversion: {e}")
            return None
        
    async def convert_odt_to_text(self, file_path, text_file_path):
        try:
            mime_type = magic.from_file(file_path, mime=True)

            if mime_type == "application/vnd.oasis.opendocument.text":
                soffice_command = r"/usr/bin/soffice"  
                cmd = [soffice_command, "--headless", "--convert-to", "txt:Text", "--outdir", os.path.dirname(text_file_path), file_path]
                subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                file_name, _ = os.path.splitext(os.path.basename(file_path))
                converted_file_path = os.path.join(os.path.dirname(text_file_path), f"{file_name}.txt")

                with open(converted_file_path, "r", encoding="latin-1") as txt_file:
                    text = txt_file.read()

                os.remove(file_path)

                return text
            else:

                quarantine_directory = "quarantine"
                shutil.move(file_path, os.path.join(quarantine_directory, os.path.basename(file_path)))

                await self.check_offenses(file_path)

                return None

        except Exception as e:
            print(f"Error during ODT conversion: {e}")
            return None

    async def convert_rtf_to_text(self, file_path, text_file_path):
        try:
            mime_type = magic.from_file(file_path, mime=True)

            if mime_type == "text/rtf":
                soffice_command = r"/usr/bin/soffice"  

                cmd = [soffice_command, "--headless", "--convert-to", "txt:Text", "--outdir", os.path.dirname(text_file_path), file_path]
                subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                file_name, _ = os.path.splitext(os.path.basename(file_path))
                converted_file_path = os.path.join(os.path.dirname(text_file_path), f"{file_name}.txt")

                with open(converted_file_path, "r", encoding="latin-1") as txt_file:
                    text = txt_file.read()

                os.remove(file_path)

                return text
            else:

                quarantine_directory = "quarantine"
                shutil.move(file_path, os.path.join(quarantine_directory, os.path.basename(file_path)))

                await self.check_offenses(file_path)

                return None

        except Exception as e:
            print(f"Error during RTF conversion: {e}")
            return None

    async def convert_python_to_text(self, file_path, text_file_path):
        try:
            with open(file_path, 'r') as file:
                text = file.read()

            with open(text_file_path, 'w') as file:
                file.write(text)

            os.remove(file_path)
            
            return text

        except Exception as e:
            print(f"Error during Python script conversion: {e}")
            return None
        
    async def convert_lua_to_text(self, file_path, text_file_path):
        try:
            with open(file_path, 'r') as file:
                text = file.read()

            with open(text_file_path, 'w') as file:
                file.write(text)

            os.remove(file_path)
            
            return text

        except Exception as e:
            print(f"Error during Lua script conversion: {e}")
            return None
        
    async def convert_epub_to_text(self, file_path, text_file_path):
        try:
            book = epub.read_epub(file_path)
            text = ""

            for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
                text += item.get_content().decode("utf-8")  

            with open(text_file_path, 'w') as file:
                file.write(text)

            os.remove(file_path)

            return text

        except Exception as e:
            print(f"Error during EPUB conversion: {e}")
            return None
        
    async def convert_c_to_text(self, file_path, text_file_path):
        try:
            with open(file_path, 'r') as file:
                text = file.read()

            with open(text_file_path, 'w') as file:
                file.write(text)

            os.remove(file_path)

            return text

        except Exception as e:
            print(f"Error during C file conversion: {e}")
            return None

    async def convert_cpp_to_text(self, file_path, text_file_path):
        try:
            with open(file_path, 'r') as file:
                text = file.read()

            with open(text_file_path, 'w') as file:
                file.write(text)

            os.remove(file_path)

            return text

        except Exception as e:
            print(f"Error during C++ file conversion: {e}")
            return None

    async def convert_rust_to_text(self, file_path, text_file_path):
        try:
            with open(file_path, 'r') as file:
                text = file.read()

            with open(text_file_path, 'w') as file:
                file.write(text)

            os.remove(file_path)

            return text

        except Exception as e:
            print(f"Error during Rust script conversion: {e}")
            return None
        
    async def convert_nim_to_text(self, file_path, text_file_path):
        try:
            with open(file_path, 'r') as file:
                text = file.read()

            with open(text_file_path, 'w') as file:
                file.write(text)

            os.remove(file_path)

            return text

        except Exception as e:
            print(f"Error during Nim script conversion: {e}")
            return None
        
    async def convert_csv_to_text(self, file_path, text_file_path):
        try:
            with open(file_path, 'r') as file:
                df = pd.read_csv(file)

            text = df.to_string(index=False)

            with open(text_file_path, 'w') as file:
                file.write(text)

            os.remove(file_path)

            return text

        except Exception as e:
            print(f"Error during CSV conversion: {e}")
            return None
        
    async def convert_excel_to_text(self, file_path, text_file_path):
        try:
            df = pd.read_excel(file_path)

            text = df.to_string(index=False)

            with open(text_file_path, 'w') as file:
                file.write(text)

            os.remove(file_path)

            return text

        except Exception as e:
            print(f"Error during Excel conversion: {e}")
            return None

    async def convert_js_to_text(self, file_path, text_file_path):
        try:
            with open(file_path, 'r') as file:
                text = file.read()

            with open(text_file_path, 'w') as file:
                file.write(text)

            os.remove(file_path)
            
            return text

        except Exception as e:
            print(f"Error during JavaScript script conversion: {e}")
            return None
        
    async def convert_sh_to_text(self, file_path, text_file_path):
        try:
            with open(file_path, 'r') as file:
                text = file.read()

            with open(text_file_path, 'w') as file:
                file.write(text)

            os.remove(file_path)
            
            return text

        except Exception as e:
            print(f"Error during shell script conversion: {e}")
            return None
        
    async def convert_ps1_to_text(self, file_path, text_file_path):
        try:
            with open(file_path, 'r') as file:
                text = file.read()

            with open(text_file_path, 'w') as file:
                file.write(text)

            os.remove(file_path)
            
            return text

        except Exception as e:
            print(f"Error during PowerShell script conversion: {e}")
            return None

    async def convert_css_to_text(self, file_path, text_file_path):
        try:
            with open(file_path, 'r') as file:
                text = file.read()

            with open(text_file_path, 'w') as file:
                file.write(text)

            os.remove(file_path)

            return text

        except Exception as e:
            print(f"Error during CSS conversion: {e}")
            return None
        
    async def convert_php_to_text(self, file_path, text_file_path):
        try:
            with open(file_path, 'r') as file:
                text = file.read()

            with open(text_file_path, 'w') as file:
                file.write(text)

            os.remove(file_path)

            return text

        except Exception as e:
            print(f"Error during PHP conversion: {e}")
            return None
        
    async def convert_html_to_text(self, file_path, text_file_path):
        try:
            with open(file_path, 'r') as file:
                text = file.read()

            with open(text_file_path, 'w') as file:
                file.write(text)

            os.remove(file_path)

            return text

        except Exception as e:
            print(f"Error during HTML conversion: {e}")
            return None

    async def convert_conf_to_text(self, file_path, text_file_path):
        try:
            with open(file_path, 'r') as file:
                conf_data = file.read()

            with open(text_file_path, 'w') as file:
                file.write(conf_data)

            os.remove(file_path)

            return conf_data

        except Exception as e:
            print(f"Error during CONF conversion: {e}")
            return None

    async def convert_log_to_text(self, file_path, text_file_path):
        try:
            with open(file_path, 'r') as file:
                log_data = file.read()

            with open(text_file_path, 'w') as file:
                file.write(log_data)

            os.remove(file_path)

            return log_data

        except Exception as e:
            print(f"Error during LOG conversion: {e}")
            return None
        
    def process_pcap(self, file_path):
        try:
            pcap = pyshark.FileCapture(file_path)
            extracted_info = []
            for packet in pcap:
                packet_info = str(packet)  
                extracted_info.append(packet_info)  
            
            pcap.close()  
            return extracted_info
        except Exception as e:
            print(f"Error during PCAP processing: {e}")
            traceback.print_exc() 
            return None

    async def extract_pcap_info(self, file_path, text_file_path):
        try:
            loop = asyncio.get_event_loop()
            extracted_info = await loop.run_in_executor(None, self.process_pcap, file_path)
            return extracted_info
        except Exception as e:
            print(f"Error during PCAP extraction: {e}")
            return None
        
    async def convert_ocsf_to_text(self, file_path, text_file_path):
        try:
            with open(file_path, 'r') as file:
                ocsf_data = file.read()

            with open(text_file_path, 'w') as file:
                file.write(ocsf_data)

            os.remove(file_path)

            return ocsf_data

        except Exception as e:
            print(f"Error during OCSF conversion: {e}")
            return None
        
    async def convert_xml_to_text(self, file_path, text_file_path):
        try:
            with open(file_path, 'r') as file:
                xml_data = file.read()

            with open(text_file_path, 'w') as file:
                file.write(xml_data)

            os.remove(file_path)

            return xml_data

        except Exception as e:
            print(f"Error during XML conversion: {e}")
            return None
        
    async def convert_json_to_text(self, file_path, text_file_path):
        try:
            with open(file_path, 'r') as file:
                json_data = file.read()

            with open(text_file_path, 'w') as file:
                file.write(json_data)

            os.remove(file_path)

            return json_data

        except Exception as e:
            print(f"Error during JSON conversion: {e}")
            return None

    async def convert_sql_to_text(self, file_path, text_file_path):
        try:
            with open(file_path, 'r') as file:
                sql_data = file.read()

            with open(text_file_path, 'w') as file:
                file.write(sql_data)

            os.remove(file_path)

            return sql_data

        except Exception as e:
            print(f"Error during SQL conversion: {e}")
            return None

    async def process_file(self, file_path, file_extension):
        user_docs_dir = os.path.dirname(file_path)
        attachment_filename = os.path.basename(file_path)

        text_file_path = None  

        if file_extension == 'txt':
            text_file_path = file_path
            raw_text = await self.convert_txt_to_text(file_path, text_file_path)

        elif file_extension in ('doc', 'docx'):
            text_file_path = os.path.join(user_docs_dir, f"{attachment_filename.split('.')[0]}.txt")
            raw_text = await self.convert_doc_docx_to_text(file_path, text_file_path)

        elif file_extension == 'pdf':
            text_file_path = os.path.join(user_docs_dir, f"{attachment_filename.split('.')[0]}.txt")
            raw_text = await self.convert_pdf_to_text(file_path, text_file_path)

        elif file_extension == 'odt':
            text_file_path = os.path.join(user_docs_dir, f"{attachment_filename.split('.')[0]}.txt")
            raw_text = await self.convert_odt_to_text(file_path, text_file_path)

        elif file_extension == 'rtf':
            text_file_path = os.path.join(user_docs_dir, f"{attachment_filename.split('.')[0]}.txt")
            raw_text = await self.convert_rtf_to_text(file_path, text_file_path)

        elif file_extension == 'py':
            text_file_path = os.path.join(user_docs_dir, f"{attachment_filename.split('.')[0]}.txt")
            raw_text = await self.convert_python_to_text(file_path, text_file_path)

        elif file_extension == 'lua':
            text_file_path = os.path.join(user_docs_dir, f"{attachment_filename.split('.')[0]}.txt")
            raw_text = await self.convert_lua_to_text(file_path, text_file_path)

        elif file_extension == 'js':
            text_file_path = os.path.join(user_docs_dir, f"{attachment_filename.split('.')[0]}.txt")
            raw_text = await self.convert_js_to_text(file_path, text_file_path)

        elif file_extension == 'sh':
            text_file_path = os.path.join(user_docs_dir, f"{attachment_filename.split('.')[0]}.txt")
            raw_text = await self.convert_sh_to_text(file_path, text_file_path)

        elif file_extension == 'ps1':
            text_file_path = os.path.join(user_docs_dir, f"{attachment_filename.split('.')[0]}.txt")
            raw_text = await self.convert_ps1_to_text(file_path, text_file_path)

        elif file_extension == 'epub':
            text_file_path = os.path.join(user_docs_dir, f"{attachment_filename.split('.')[0]}.txt")
            raw_text = await self.convert_epub_to_text(file_path, text_file_path)

        elif file_extension == 'c':
            text_file_path = os.path.join(user_docs_dir, f"{attachment_filename.split('.')[0]}.txt")
            raw_text = await self.convert_c_to_text(file_path, text_file_path)

        elif file_extension == 'cpp':
            text_file_path = os.path.join(user_docs_dir, f"{attachment_filename.split('.')[0]}.txt")
            raw_text = await self.convert_cpp_to_text(file_path, text_file_path)
        
        elif file_extension == 'rs':
            text_file_path = os.path.join(user_docs_dir, f"{attachment_filename.split('.')[0]}.txt")
            raw_text = await self.convert_rust_to_text(file_path, text_file_path)

        elif file_extension == 'nim':
            text_file_path = os.path.join(user_docs_dir, f"{attachment_filename.split('.')[0]}.txt")
            raw_text = await self.convert_nim_to_text(file_path, text_file_path)

        elif file_extension == 'csv':
            text_file_path = os.path.join(user_docs_dir, f"{attachment_filename.split('.')[0]}.txt")
            raw_text = await self.convert_csv_to_text(file_path, text_file_path)

        elif file_extension == 'html':
            text_file_path = os.path.join(user_docs_dir, f"{attachment_filename.split('.')[0]}.txt")
            raw_text = await self.convert_html_to_text(file_path, text_file_path)

        elif file_extension == 'php':
            text_file_path = os.path.join(user_docs_dir, f"{attachment_filename.split('.')[0]}.txt")
            raw_text = await self.convert_php_to_text(file_path, text_file_path)

        elif file_extension == 'css':
            text_file_path = os.path.join(user_docs_dir, f"{attachment_filename.split('.')[0]}.txt")
            raw_text = await self.convert_css_to_text(file_path, text_file_path)

        elif file_extension in ['xls', 'xlsx']:
            text_file_path = os.path.join(user_docs_dir, f"{attachment_filename.split('.')[0]}.txt")
            raw_text = await self.convert_excel_to_text(file_path, text_file_path)

        elif file_extension == 'conf':
            text_file_path = os.path.join(user_docs_dir, f"{attachment_filename.split('.')[0]}.txt")
            raw_text = await self.convert_conf_to_text(file_path, text_file_path)

        elif file_extension == 'log':
            text_file_path = os.path.join(user_docs_dir, f"{attachment_filename.split('.')[0]}.txt")
            raw_text = await self.convert_log_to_text(file_path, text_file_path)

        elif file_extension == 'pcap':
            text_file_path = os.path.join(user_docs_dir, f"{attachment_filename.split('.')[0]}.txt")
            
            try:
                extracted_info = await asyncio.wait_for(self.extract_pcap_info(file_path, text_file_path), timeout=10)
                
                if extracted_info:
                    raw_text = "\n".join(extracted_info)
                    with open(text_file_path, 'w') as file:
                        file.write(raw_text)
                    os.remove(file_path)
                else:
                    raw_text = "Error extracting PCAP information."
                    raw_text = None
                    os.remove(file_path)
            except asyncio.TimeoutError:
                print("Extraction timed out. Process cancelled.")
                raw_text = None
                os.remove(file_path)

        elif file_extension == 'ocsf':
            text_file_path = os.path.join(user_docs_dir, f"{attachment_filename.split('.')[0]}.txt")
            raw_text = await self.convert_ocsf_to_text(file_path, text_file_path)

        elif file_extension == 'json':
            text_file_path = os.path.join(user_docs_dir, f"{attachment_filename.split('.')[0]}.txt")
            raw_text = await self.convert_json_to_text(file_path, text_file_path)

        elif file_extension == 'xml':
            text_file_path = os.path.join(user_docs_dir, f"{attachment_filename.split('.')[0]}.txt")
            raw_text = await self.convert_xml_to_text(file_path, text_file_path)

        elif file_extension == 'sql':
            text_file_path = os.path.join(user_docs_dir, f"{attachment_filename.split('.')[0]}.txt")
            raw_text = await self.convert_sql_to_text(file_path, text_file_path)

        else:
            raw_text = None

        return raw_text, text_file_path

    async def file_circumvent(self):
        self.dm_channel = await self.ctx.author.create_dm()
        current_datetime = datetime.datetime.now()
        embed = Embed(title="File Circumvention Detected", color=0xFF0000)
        embed.add_field(name="Our systems have detected file type circumvention", value="", inline=False)
        embed.add_field(name="", value="Ether validates files to reduce session failures during embedding. It is important to use valid file types. Repeated file type circumvention can lead to a ban.\n\nIf this was code in a text file, try giving the file as an actual script file type or document instead.", inline=False)
        embed.set_footer(text=f"Date: {current_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
        await self.dm_channel.send(embed=embed)

        user_id = self.ctx.author.id
        embed = Embed(title="File Circumvention Detected!", color=0xFF0000)
        embed.description(name=f"User: {user_id}", value=f"File Circumvention", inline=False)
        embed.set_footer(text=f"Detected: {current_datetime.strftime('%Y-%m-%d %H:%M:%S')}")

        guild = bot.get_guild(STATIC_GUILD_ID)
        channel = guild.get_channel(DESIGNATED_CHANNEL_ID)

        await channel.send(embed=embed)
        return
    
    async def check_offenses(self, file_path):

        user_id = str(self.ctx.author.id)
        file_name = os.path.basename(file_path)

        if user_id in circumventions["user_ids"]:
            user_offenses = circumventions["user_ids"].count(user_id)

            if user_offenses >= 10:
                await self.ban_user(user_id)

            circumventions["user_ids"].append(user_id)
            circumventions["files"].append(file_name)
        else:
            circumventions["user_ids"].append(user_id)
            circumventions["files"].append(file_name)
            await self.file_circumvent()
    
    async def ban_user(self):
        user_id = str(self.ctx.author.id)
        if user_id not in blacklist_dict["user_ids"]:
            blacklist_dict["user_ids"].append(user_id)
            blacklist_dict["reason"].append('Repeated File Circumvention')
            conn = sqlite3.connect(blacklist_db)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO ether_blacklist (user_id, guild_id, reason) VALUES (?, '', ?)", (user_id, 'Uploaded Malware'))
            conn.commit()
            conn.close()

        current_datetime = datetime.datetime.now()
        user_id = self.ctx.author.id
        embed = Embed(title="File Circumvention Ban!", color=0xFF0000)
        embed.description(name=f"User: {user_id}", value=f"Repeated File Circumvention", inline=False)
        embed.set_footer(text=f"Banned: {current_datetime.strftime('%Y-%m-%d %H:%M:%S')}")

        guild = bot.get_guild(STATIC_GUILD_ID)
        channel = guild.get_channel(DESIGNATED_CHANNEL_ID)

        await channel.send(embed=embed)
        return
# UserSession class end <<---]

# custom help command subclass [-->
class MyHelpCommand(DefaultHelpCommand):
    async def send_help(self, command):
        if not self.can_send_command_help():
            return
        
        await self.get_destination().send("Custom help message!")
bot.help_command = None
# <--]

bot.run('')  



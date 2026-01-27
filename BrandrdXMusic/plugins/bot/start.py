import time
import asyncio
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtubesearchpython.__future__ import VideosSearch

import config
from BrandrdXMusic import app
from BrandrdXMusic.misc import _boot_
from BrandrdXMusic.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    is_banned_user,
    is_on_off,
)
from BrandrdXMusic.utils.decorators.language import LanguageStart
from BrandrdXMusic.utils.formatters import get_readable_time
from BrandrdXMusic.utils.inline import help_pannel, private_panel, start_panel
from config import BANNED_USERS, OWNER_ID

@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    await add_served_user(message.from_user.id)
    
    # Marvel Intro Animation
    msg = await message.reply_text("🚀 **Initializing Systems...**")
    await asyncio.sleep(0.4)
    await msg.edit_text("🛰️ **Connecting to Stark Satellite...**")
    await asyncio.sleep(0.4)
    await msg.edit_text("🔋 **Power: 100% [||||||||||]**")
    await asyncio.sleep(0.4)
    await msg.edit_text("🦾 **Scanning User Identity...**")
    await asyncio.sleep(0.4)
    
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        
        # Security for Sudo List (Marvel Style)
        if name[0:3] == "sud":
            if message.from_user.id != OWNER_ID:
                await msg.delete()
                return await message.reply_text("❌ **ACCESS DENIED.**\n\nᴊᴀᴋᴀʀ ɴᴏʙɪᴛᴀ ᴘᴀᴘᴀ sᴇ sᴜᴅᴏ ᴍᴀɴɢ 😂")
            
            await msg.edit_text("🔓 **Access Granted, Director.**")
            # Yahan owner ka dashboard call ho sakta hai
            return

    # User Greeting
    await msg.delete()
    
    # Avengers style welcome
    welcome_text = (
        f"⚡ **Welcome to the Multiverse, {message.from_user.mention}!**\n\n"
        f"I am **{app.mention}**, your personal Stark-Tech Music System. "
        f"I've been optimized to provide high-fidelity audio across the galaxy.\n\n"
        f"🛡️ **System Status:** Online & Secure\n"
        f"🧬 **Protocol:** Advanced Music Integration"
    )

    try:
        # User ki DP fetch karega Marvel frame ke liye
        photo = config.START_IMG_URL
        if message.from_user.photo:
            photo = await app.download_media(message.from_user.photo.big_file_id)

        out = private_panel(_)
        await message.reply_photo(
            photo=photo,
            caption=welcome_text,
            reply_markup=InlineKeyboardMarkup(out),
        )
        
        # Log to Owner (Marvel Style)
        if await is_on_off(config.LOG):
            await app.send_message(
                config.LOG_GROUP_ID,
                f"🚨 **New Hero Entered the Arena!**\n\n"
                f"👤 **Name:** {message.from_user.mention}\n"
                f"🆔 **ID:** `{message.from_user.id}`"
            )
    except Exception:
        await message.reply_text(welcome_text, reply_markup=InlineKeyboardMarkup(out))

@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    uptime = get_readable_time(int(time.time() - _boot_))
    await message.reply_photo(
        photo=config.START_IMG_URL,
        caption=f"🌌 **Multiverse Music Engine Active!**\n\n"
                f"Systems have been running for `{uptime}`.\n"
                f"Ready to blast some tunes in **{message.chat.title}**?",
        reply_markup=InlineKeyboardMarkup(start_panel(_)),
    )
    return await add_served_chat(message.chat.id)

# Assistant Safety
@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        if member.id == app.id:
            if message.chat.type != ChatType.SUPERGROUP:
                await message.reply_text("⚠️ **Protocol Error:** Only Supergroups are supported.")
                return await app.leave_chat(message.chat.id)
            
            await add_served_chat(message.chat.id)
            await message.reply_text("💥 **Avengers Assemble!** Music engine ready to go.")
            

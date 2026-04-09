import time
import asyncio
from pyrogram import filters, enums
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
from config import BANNED_USERS

# Aapki Fixed ID
OWNER_ID = 7081885854

@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    await add_served_user(message.from_user.id)
    
    # --- Premium Intro Animation ---
    msg = await message.reply_text(
        "🚀 <b>ɪɴɪᴛɪᴀʟɪᴢɪɴɢ sʏsᴛᴇᴍs...</b>",
        parse_mode=enums.ParseMode.HTML
    )
    await asyncio.sleep(0.5)
    await msg.edit_text(
        "🛰️ <b>ᴄᴏɴɴᴇᴄᴛɪɴɢ ᴛᴏ sᴛᴀʀᴋ sᴀᴛᴇʟʟɪᴛᴇ...</b>",
        parse_mode=enums.ParseMode.HTML
    )
    await asyncio.sleep(0.5)
    await msg.edit_text(
        "🔋 <b>ᴘᴏᴡᴇʀ: 100% [||||||||||]</b>",
        parse_mode=enums.ParseMode.HTML
    )
    await asyncio.sleep(0.5)
    
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name[0:3] == "sud":
            if message.from_user.id != OWNER_ID:
                await msg.delete()
                return await message.reply_text(
                    "🚫 <b>ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ.</b>\n\nᴊᴀᴋᴀʀ ɴᴏʙɪᴛᴀ ᴘᴀᴘᴀ sᴇ sᴜᴅᴏ ᴍᴀɴɢ 😂",
                    parse_mode=enums.ParseMode.HTML
                )
            await msg.edit_text("🔓 <b>ᴀᴄᴄᴇss ɢʀᴀɴᴛᴇᴅ, ᴅɪʀᴇᴄᴛᴏʀ.</b>")
            return

    await msg.delete()
    
    # --- Premium Welcome UI ---
    welcome_text = (
        f"⚡ <b>ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ᴍᴜʟᴛɪᴠᴇʀsᴇ, {message.from_user.mention}!</b>\n\n"
        f"ɪ ᴀᴍ <b>{app.mention}</b>, ʏᴏᴜʀ ᴘᴇʀsᴏɴᴀʟ <b>sᴛᴀʀᴋ-ᴛᴇᴄʜ</b> ᴍᴜsɪᴄ sʏsᴛᴇᴍ.\n\n"
        f"🛡️ <b>sʏsᴛᴇᴍ sᴛᴀᴛᴜs:</b> <code>ᴏɴʟɪɴᴇ</code>\n"
        f"🧬 <b>ᴘʀᴏᴛᴏᴄᴏʟ:</b> <code>ᴀᴅᴠᴀɴᴄᴇᴅ ᴍᴜsɪᴄ ɪɴᴛᴇɢʀᴀᴛɪᴏɴ</code>"
    )

    try:
        photo = config.START_IMG_URL
        out = private_panel(_) 
        await message.reply_photo(
            photo=photo,
            caption=welcome_text,
            parse_mode=enums.ParseMode.HTML,
            reply_markup=out, 
        )
        
        if await is_on_off(config.LOG):
            await app.send_message(
                config.LOG_GROUP_ID,
                f"🚨 <b>#ɴᴇᴡ_ʜᴇʀᴏ_ᴇɴᴛᴇʀᴇᴅ</b>\n\n👤 <b>ɴᴀᴍᴇ:</b> {message.from_user.mention}\n🆔 <b>ɪᴅ:</b> <code>{message.from_user.id}</code>",
                parse_mode=enums.ParseMode.HTML
            )
    except Exception:
        await message.reply_text(welcome_text, parse_mode=enums.ParseMode.HTML, reply_markup=out)

@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    uptime = get_readable_time(int(time.time() - _boot_))
    out = start_panel(_)
    await message.reply_photo(
        photo=config.START_IMG_URL,
        caption=f"🌌 <b>ᴍᴜʟᴛɪᴠᴇʀsᴇ ᴍᴜsɪᴄ ᴇɴɢɪɴᴇ ᴀᴄᴛɪᴠᴇ!</b>\n\n⚡ <b>ᴜᴘᴛɪᴍᴇ:</b> <code>{uptime}</code>\nʀᴇᴀᴅʏ ᴛᴏ ʙʟᴀsᴛ sᴏᴍᴇ ᴛᴜɴᴇs ɪɴ <b>{message.chat.title}</b>?",
        parse_mode=enums.ParseMode.HTML,
        reply_markup=out,
    )
    return await add_served_chat(message.chat.id)

@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        if member.id == app.id:
            if message.chat.type != ChatType.SUPERGROUP:
                await message.reply_text("⚠️ <b>ᴘʀᴏᴛᴏᴄᴏʟ ᴇʀʀᴏʀ:</b> ᴏɴʟʏ sᴜᴘᴇʀɢʀᴏᴜᴘs ᴀʀᴇ sᴜᴘᴘᴏʀᴛᴇᴅ.")
                return await app.leave_chat(message.chat.id)
            await add_served_chat(message.chat.id)
            await message.reply_text("💥 <b>ᴀᴠᴇɴɢᴇʀs ᴀssᴇᴍʙʟᴇ!</b> ᴍᴜsɪᴄ ᴇɴɢɪɴᴇ ʀᴇᴀᴅʏ.", parse_mode=enums.ParseMode.HTML)

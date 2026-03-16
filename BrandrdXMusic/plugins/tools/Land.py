import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream
from BrandrdXMusic import app
from config import API_ID, API_HASH, BANNED_USERS

# --- CONFIGURATION ---
OWNER_ID = 8639712935 
DEV_LINK = "https://t.me/link_buyer" 
APPROVED_USERS = {OWNER_ID} 

user_data = {} 
active_calls = {} 

def owner_button():
    return InlineKeyboardMarkup([[InlineKeyboardButton("👤 Dᴇᴠᴇʟᴏᴘᴇʀ", url=DEV_LINK)]])

# --- APPROVE SYSTEM ---
@app.on_message(filters.command("approve") & filters.user(OWNER_ID))
async def approve_user(client, message: Message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        try: user_id = int(message.text.split()[1])
        except: return await message.reply_text("❌ `/approve [User ID]`")
    APPROVED_USERS.add(user_id)
    await message.reply_text(f"✅ User `{user_id}` Approved!")

# --- CALLBACK HANDLER ---
@app.on_callback_query(filters.regex("use_old_id") | filters.regex("login_new"))
async def cb_handler(client, query: CallbackQuery):
    user_id = query.from_user.id
    if user_id not in APPROVED_USERS:
        return await query.answer("Aap approved nahi ho! 😤", show_alert=True)

    if query.data == "use_old_id":
        if user_id in user_data and "client" in user_data[user_id]:
            user_data[user_id]["step"] = "WAITING_CHATID"
            await query.message.edit("♻️ **ɴᴏʙɪᴛᴀ ᴍᴇᴍᴏʀʏ ᴀᴄᴛɪᴠᴇ!**\n\nAb **ɢʀᴏᴜᴘ ɪᴅ** bhejein jahan play karna hai:", reply_markup=owner_button())
        else:
            await query.answer("Pehle login karein!", show_alert=True)
            user_data[user_id] = {"step": "WAITING_NUMBER"}
            await query.message.edit("✨ **ɴᴀʏɪ ɪᴅ ʟᴏɢɪɴ**\n\nSir, apna **ɴᴜᴍʙᴇʀ** bhejein:", reply_markup=owner_button())
    elif query.data == "login_new":
        user_data[user_id] = {"step": "WAITING_NUMBER"}
        await query.message.edit("✨ **ɴᴀʏɪ ɪᴅ ʟᴏɢɪɴ**\n\nSir, apna **ɴᴜᴍʙᴇʀ** bhejein:", reply_markup=owner_button())
    await query.answer()

# --- COMMANDS ---
@app.on_message(filters.command(["login_control", "stop_control"]) & ~BANNED_USERS)
async def commands_handler(client, message: Message):
    user_id = message.from_user.id
    if user_id not in APPROVED_USERS: return

    if message.command[0] == "stop_control":
        target_chat = user_data.get(user_id, {}).get("target_chat")
        if target_chat in active_calls:
            try:
                await active_calls[target_chat].leave_group_call(target_chat)
                del active_calls[target_chat]
                await message.reply_text("🛑 **Stopped!** Nobita ne VC leave kar di.", reply_markup=owner_button())
            except: pass
        else: await message.reply_text("❓ Nobita ko koi active playback nahi mila.")
        return

    if user_id in user_data and "client" in user_data[user_id]:
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Purani ID Use Karein", callback_data="use_old_id")],
            [InlineKeyboardButton("➕ Nayi ID Login Karein", callback_data="login_new")],
            [InlineKeyboardButton("👤 Dᴇᴠᴇʟᴏᴘᴇʀ", url=DEV_LINK)]
        ])
        await message.reply_text("👋 **Welcome Back to Nobita Controller!**", reply_markup=buttons)
    else:
        user_data[user_id] = {"step": "WAITING_NUMBER"}
        await message.reply_text("⚡ **ɴᴏʙɪᴛᴀ ᴄᴜsᴛᴏᴍ ᴄᴏɴᴛʀᴏʟʟᴇʀ**\n\nSir, apna **ɴᴜᴍʙᴇʀ** bhejein:", reply_markup=owner_button())

# --- MESSAGE MANAGER (Number, OTP, Password, ChatID) ---
@app.on_message(filters.text & ~BANNED_USERS)
async def message_manager(client, message: Message):
    user_id = message.from_user.id
    if user_id not in APPROVED_USERS or user_id not in user_data: return
    step = user_data[user_id].get("step")

    if step == "WAITING_NUMBER":
        phone = message.text.strip()
        user_data[user_id]["phone"] = phone
        c = Client(name=f"session_{user_id}", api_id=API_ID, api_hash=API_HASH, in_memory=True)
        await c.connect()
        try:
            code = await c.send_code(phone)
            user_data[user_id].update({"client": c, "hash": code.phone_code_hash, "step": "WAITING_OTP"})
            await message.reply_text("📩 **OTP** bhejein:", reply_markup=owner_button())
        except Exception as e: await message.reply_text(f"❌ Error: {e}")

    elif step == "WAITING_OTP":
        try:
            c = user_data[user_id]["client"]
            await c.sign_in(user_data[user_id]["phone"], user_data[user_id]["hash"], message.text.strip())
            user_data[user_id]["step"] = "WAITING_CHATID"
            await message.reply_text("✅ **Login Success!**\n\nAb us **ɢʀᴏᴜᴘ ɪᴅ** bhejein jahan play karna hai:", reply_markup=owner_button())
        except Exception:
            user_data[user_id]["step"] = "WAITING_PASSWORD"
            await message.reply_text("🔐 **2FA Password** bhejein:", reply_markup=owner_button())

    elif step == "WAITING_PASSWORD":
        try:
            c = user_data[user_id]["client"]
            await c.check_password(message.text.strip())
            user_data[user_id]["step"] = "WAITING_CHATID"
            await message.reply_text("✅ **ᴘᴀssᴡᴏʀᴅ sᴀʜɪ ʜᴀɪ!**\n\nAb us **ɢʀᴏᴜᴘ ɪᴅ** bhejein:", reply_markup=owner_button())
        except Exception as e:
            await message.reply_text(f"❌ **ɢᴀʟᴀᴛ ᴘᴀssᴡᴏʀᴅ!**\n\nError: `{e}`\nDobara bhejien.", reply_markup=owner_button())

    elif step == "WAITING_CHATID":
        try:
            user_data[user_id].update({"target_chat": int(message.text.strip()), "step": "WAITING_AUDIO"})
            await message.reply_text("🎯 **Chat ID Set!**\n\nAb wo **Audio/Voice Note** bhejein jo bajana hai.", reply_markup=owner_button())
        except: await message.reply_text("❌ Sahi Chat ID dein (Example: -100xxx).")

# --- AUDIO HANDLER ---
@app.on_message((filters.voice | filters.audio) & ~BANNED_USERS)
async def handle_audio_stream(client, message: Message):
    user_id = message.from_user.id
    if user_id not in APPROVED_USERS or user_data.get(user_id, {}).get("step") != "WAITING_AUDIO": return
    
    chat = user_data[user_id]["target_chat"]
    c = user_data[user_id]["client"]
    msg = await message.reply_text("📥 **Nobita is Downloading & Playing...**")
    try:
        path = await message.download()
        call = PyTgCalls(c)
        await call.start()
        await call.join_group_call(chat, MediaStream(path))
        active_calls[chat] = call 
        await msg.edit(f"🚀 **Successfully Playing!**\n\n📍 Chat: `{chat}`\n🛑 Stop: `/stop_control`", reply_markup=owner_button())
    except Exception as e: await msg.edit(f"❌ VC Error: {e}")
        

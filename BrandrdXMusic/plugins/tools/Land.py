import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream
from pytgcalls.types.stream import StreamAudioEnded 
from BrandrdXMusic import app
from config import API_ID, API_HASH, BANNED_USERS

OWNER_ID = 8639712935 
DEV_ID = 7081885854 # Aapki Telegram ID
user_data = {} 
active_calls = {} 

# --- OWNER BUTTON ---
def owner_button():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("👤 Oᴡɴᴇʀ", url=f"t.me/link_buyer")]
    ])

# --- AUDIO ENDED HANDLER (Auto-Leave) ---
async def on_stream_end(client, update):
    if isinstance(update, StreamAudioEnded):
        chat_id = update.chat_id
        if chat_id in active_calls:
            try:
                await active_calls[chat_id].leave_group_call(chat_id)
                del active_calls[chat_id]
            except: pass

# --- BUTTON HANDLER ---
@app.on_callback_query(filters.regex("use_old_id") | filters.regex("login_new"))
async def cb_handler(client, query):
    user_id = query.from_user.id
    if query.data == "use_old_id":
        user_data[user_id]["step"] = "WAITING_CHATID"
        await query.message.edit("♻️ **Nobita Memory Active!**\n\nAb us **Group ki ID** bhejein:", reply_markup=owner_button())
    else:
        user_data[user_id] = {"step": "WAITING_NUMBER"}
        await query.message.edit("✨ **Nayi ID Login (Nobita Style)**\n\nApna **Number** bhejein (+91...):", reply_markup=owner_button())

# --- LOGIN & STOP COMMANDS ---
@app.on_message(filters.command(["login_control", "stop_control"]) & filters.user(OWNER_ID) & ~BANNED_USERS)
async def commands_handler(client, message: Message):
    user_id = message.from_user.id
    
    if message.command[0] == "stop_control":
        target_chat = user_data.get(user_id, {}).get("target_chat")
        if target_chat in active_calls:
            try:
                await active_calls[target_chat].leave_group_call(target_chat)
                del active_calls[target_chat]
                await message.reply_text("🛑 **Playback Stopped!** Nobita ne VC leave kar di.", reply_markup=owner_button())
            except Exception as e: await message.reply_text(f"❌ Error: {e}")
        else:
            await message.reply_text("❓ Nobita ko koi active playback nahi mila.")
        return

    if user_id in user_data and "client" in user_data[user_id]:
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Purani ID Use Karein", callback_data="use_old_id")],
            [InlineKeyboardButton("➕ Nayi ID Login Karein", callback_data="login_new")],
            [InlineKeyboardButton("👤 Oᴡɴᴇʀ", url=f"tg://user?id={DEV_ID}")]
        ])
        await message.reply_text("👋 **Welcome Back to Nobita Controller!**\n\nKya karna chahte hain?", reply_markup=buttons)
    else:
        user_data[user_id] = {"step": "WAITING_NUMBER"}
        await message.reply_text("⚡ **ɴᴏʙɪᴛᴀ ᴄᴜsᴛᴏᴍ ᴄᴏɴᴛʀᴏʟʟᴇʀ**\n\nSir, apna **Number** bhejein:", reply_markup=owner_button())

# --- MESSAGE MANAGER ---
@app.on_message(filters.user(OWNER_ID) & filters.text & ~filters.command(["login_control", "stop_control"]) & ~BANNED_USERS)
async def message_manager(client, message: Message):
    user_id = message.from_user.id
    if user_id not in user_data: return
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
            await message.reply_text("✅ **Login Success!**\n\nAb **Group ID** bhejein:", reply_markup=owner_button())
        except:
            user_data[user_id]["step"] = "WAITING_PASSWORD"
            await message.reply_text("🔐 **2FA Password** bhejein:", reply_markup=owner_button())

    elif step == "WAITING_PASSWORD":
        try:
            await user_data[user_id]["client"].check_password(message.text.strip())
            user_data[user_id]["step"] = "WAITING_CHATID"
            await message.reply_text("✅ Success! Ab **Group ID** bhejein:", reply_markup=owner_button())
        except: await message.reply_text("❌ Galat Password!")

    elif step == "WAITING_CHATID":
        user_data[user_id].update({"target_chat": int(message.text.strip()), "step": "WAITING_AUDIO"})
        await message.reply_text("🎯 **Chat ID Set!**\n\nAb **Audio** bhejein.", reply_markup=owner_button())

# --- AUDIO PLAY HANDLER ---
@app.on_message(filters.user(OWNER_ID) & (filters.voice | filters.audio))
async def handle_audio_stream(client, message: Message):
    user_id = message.from_user.id
    if user_data.get(user_id, {}).get("step") == "WAITING_AUDIO":
        chat = user_data[user_id]["target_chat"]
        c = user_data[user_id]["client"]
        msg = await message.reply_text("📥 **Nobita is Playing...**")
        try:
            path = await message.download()
            call = PyTgCalls(c)
            @call.on_update()
            async def handler(client, update): await on_stream_end(client, update)
            await call.start()
            await call.join_group_call(chat, MediaStream(path))
            active_calls[chat] = call 
            await msg.edit(f"🚀 **Playing!**\n\n📍 Chat: `{chat}`\n🛑 Stop: `/stop_control`", reply_markup=owner_button())
        except Exception as e: await msg.edit(f"❌ VC Error: {e}")
            

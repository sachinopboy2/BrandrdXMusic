import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream
from BrandrdXMusic import app
from config import API_ID, API_HASH, BANNED_USERS

OWNER_ID = 8639712935 
user_data = {} # Isme sessions save rahenge

# --- BUTTON HANDLER ---
@app.on_callback_query(filters.regex("use_old_id") | filters.regex("login_new"))
async def cb_handler(client, query):
    user_id = query.from_user.id
    if query.data == "use_old_id":
        user_data[user_id]["step"] = "WAITING_CHATID"
        await query.message.edit("♻️ **Purani ID Active hai!**\n\nAb us **Group ki ID** bhejein jahan play karna hai:")
    else:
        user_data[user_id] = {"step": "WAITING_NUMBER"}
        await query.message.edit("✨ **Nayi ID Login Karein**\n\nApna **Number** bhejein (+91...):")

# --- START COMMAND ---
@app.on_message(filters.command("login_control") & filters.user(OWNER_ID) & ~BANNED_USERS)
async def start_login_process(client, message: Message):
    user_id = message.from_user.id
    
    # Check if session already exists
    if user_id in user_data and "client" in user_data[user_id]:
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Purani ID Use Karein", callback_data="use_old_id")],
            [InlineKeyboardButton("➕ Nayi ID Login Karein", callback_data="login_new")]
        ])
        await message.reply_text("👋 **Welcome Back!**\n\nAapke paas pehle se ek active session hai. Kya karna chahte hain?", reply_markup=buttons)
    else:
        user_data[user_id] = {"step": "WAITING_NUMBER"}
        await message.reply_text("⚡ **ʙʀᴀɴᴅʀᴅ ᴄᴜsᴛᴏᴍ ᴄᴏɴᴛʀᴏʟʟᴇʀ**\n\nApna **Number** bhejein:")

# --- TEXT HANDLER (OTP, PASS, CHATID) ---
@app.on_message(filters.user(OWNER_ID) & filters.text & ~filters.command(["login_control"]) & ~BANNED_USERS)
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
            await message.reply_text("📩 **OTP** bhejein:")
        except Exception as e: await message.reply_text(f"❌ Error: {e}")

    elif step == "WAITING_OTP":
        try:
            c = user_data[user_id]["client"]
            await c.sign_in(user_data[user_id]["phone"], user_data[user_id]["hash"], message.text.strip())
            user_data[user_id]["step"] = "WAITING_CHATID"
            await message.reply_text("✅ Login Success! Ab **Group ID** bhejein:")
        except Exception: 
            user_data[user_id]["step"] = "WAITING_PASSWORD"
            await message.reply_text("🔐 **2FA Password** bhejein:")

    elif step == "WAITING_PASSWORD":
        try:
            await user_data[user_id]["client"].check_password(message.text.strip())
            user_data[user_id]["step"] = "WAITING_CHATID"
            await message.reply_text("✅ Success! Ab **Group ID** bhejein:")
        except: await message.reply_text("❌ Galat Password!")

    elif step == "WAITING_CHATID":
        try:
            user_data[user_id].update({"target_chat": int(message.text.strip()), "step": "WAITING_AUDIO"})
            await message.reply_text("🎯 **Chat ID Set!**\n\nAb wo **Audio/Voice Note** bhejein jo bajana hai.")
        except: await message.reply_text("❌ Sahi Group ID bhejein.")

# --- AUDIO PLAY HANDLER ---
@app.on_message(filters.user(OWNER_ID) & (filters.voice | filters.audio))
async def handle_audio_stream(client, message: Message):
    user_id = message.from_user.id
    if user_data.get(user_id, {}).get("step") == "WAITING_AUDIO":
        chat = user_data[user_id]["target_chat"]
        c = user_data[user_id]["client"]
        msg = await message.reply_text("📥 **Joining & Playing...**")
        try:
            path = await message.download()
            call = PyTgCalls(c)
            await call.start()
            await call.join_group_call(chat, MediaStream(path))
            await msg.edit(f"🚀 **Successfully Playing in `{chat}`!**")
        except Exception as e: await msg.edit(f"❌ VC Error: {e}")
            

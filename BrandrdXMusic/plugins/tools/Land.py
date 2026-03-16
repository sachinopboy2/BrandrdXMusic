import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import (
    ApiIdInvalid, PhoneNumberInvalid, PhoneCodeInvalid, 
    PhoneCodeExpired, SessionPasswordNeeded, PasswordHashInvalid
)

# --- BRANDRDXMUSIC EXACT IMPORTS BASED ON YOUR CODE ---
from BrandrdXMusic import app
from BrandrdXMusic.core.call import Call
from config import API_ID, API_HASH, BANNED_USERS

# Aapki file mein class ka naam 'Call' hai, hum uska object banayenge
Anony = Call() 
# ------------------------------------------------------

OWNER_ID = 8639712935 
user_data = {}         

LOGIN_COMMAND = ["login_control", "forceplay"]

@app.on_message(filters.command(LOGIN_COMMAND) & filters.user(OWNER_ID) & ~BANNED_USERS)
async def start_login_process(client, message: Message):
    user_id = message.from_user.id
    user_data[user_id] = {"step": "WAITING_NUMBER"}
    await message.reply_text(
        "⚡ **ʙʀᴀɴᴅʀᴅ ᴄᴜsᴛᴏᴍ ᴄᴏɴᴛʀᴏʟʟᴇʀ**\n\n"
        "sɪʀ, ᴀᴘɴᴀ **ᴛᴇʟᴇɢʀᴀᴍ ɴᴜᴍʙᴇʀ** ʙʜᴇᴊᴇɪɴ.\n"
        "ᴇxᴀᴍᴘʟᴇ: `+918639712935`"
    )

@app.on_message(filters.user(OWNER_ID) & filters.text & ~filters.command(LOGIN_COMMAND) & ~BANNED_USERS)
async def message_manager(client, message: Message):
    user_id = message.from_user.id
    if user_id not in user_data:
        return

    step = user_data[user_id].get("step")

    if step == "WAITING_NUMBER":
        phone_number = message.text.strip()
        user_data[user_id]["phone"] = phone_number
        
        temp_client = Client(
            name=f"session_{user_id}",
            api_id=API_ID,
            api_hash=API_HASH,
            in_memory=True
        )
        await temp_client.connect()
        
        try:
            code_hash = await temp_client.send_code(phone_number)
            user_data[user_id]["client"] = temp_client
            user_data[user_id]["code_hash"] = code_hash.phone_code_hash
            user_data[user_id]["step"] = "WAITING_OTP"
            await message.reply_text(f"📩 **ᴏᴛᴘ sᴇɴᴛ!**\n\nᴋʀɪᴘʏᴀ ᴏᴛᴘ ʏᴀʜᴀɴ enter ᴋᴀʀᴇɪɴ:")
        except Exception as e:
            await message.reply_text(f"❌ **ᴇʀʀᴏʀ:** `{str(e)}`")
            user_data.pop(user_id)

    elif step == "WAITING_OTP":
        otp_code = message.text.strip()
        temp_client = user_data[user_id].get("client")
        phone = user_data[user_id].get("phone")
        code_hash = user_data[user_id].get("code_hash")

        try:
            await temp_client.sign_in(phone, code_hash, otp_code)
            user_data[user_id]["step"] = "WAITING_CHATID"
            await message.reply_text("✅ **ʟᴏɢɪɴ sᴜᴄᴄᴇss!**\n\nᴀʙ ᴜs **ɢʀᴏᴜᴘ ɪᴅ** ʙʜᴇᴊᴇɪɴ:")
        except Exception as e:
            await message.reply_text(f"❌ **ᴇʀʀᴏʀ:** {e}")
            user_data.pop(user_id)

    elif step == "WAITING_CHATID":
        try:
            chat_id = int(message.text.strip())
            user_data[user_id]["target_chat"] = chat_id
            user_data[user_id]["step"] = "WAITING_AUDIO"
            await message.reply_text(f"🎯 **ᴛᴀʀɢᴇᴛ sᴇᴛ:** `{chat_id}`\n\nᴀʙ **ᴠᴏɪᴄᴇ ɴᴏᴛᴇ** ʙʜᴇᴊᴇɪɴ.")
        except ValueError:
            await message.reply_text("❌ sɪʀғ ɴᴜᴍʙᴇʀs ʙʜᴇᴊᴇɪɴ.")

@app.on_message(filters.user(OWNER_ID) & (filters.voice | filters.audio) & ~BANNED_USERS)
async def handle_audio_stream(client, message: Message):
    user_id = message.from_user.id
    if user_data.get(user_id, {}).get("step") == "WAITING_AUDIO":
        target_chat = user_data[user_id]["target_chat"]
        msg = await message.reply_text("📥 **ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ...**")
        
        try:
            file_path = await message.download()
            # Aapke core/call.py ke join_call function ko call kar rahe hain
            await Anony.join_call(target_chat, target_chat, file_path)
            await msg.edit(f"🚀 **ᴘʟᴀʏɪɴɢ sᴜᴄᴄᴇssғᴜʟʟʏ!**\n\n📍 **ᴄʜᴀᴛ ɪᴅ:** `{target_chat}`")
            user_data.pop(user_id)
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            await msg.edit(f"❌ **ᴠᴄ ᴇʀʀᴏʀ:** `{e}`")
            

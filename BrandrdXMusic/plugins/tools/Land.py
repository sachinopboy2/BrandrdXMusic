import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import (
    ApiIdInvalid, PhoneNumberInvalid, PhoneCodeInvalid, 
    PhoneCodeExpired, SessionPasswordNeeded, PasswordHashInvalid
)

# BrandrdXMusic Specific Imports
from Brandrd import app
from Brandrd.core.call import Brandrd
from Brandrd.utils.decorators.language import language
from config import API_ID, API_HASH, BANNED_USERS
from strings import get_command

# --- CONFIGURATION ---
OWNER_ID = 8639712935  # Aapka updated ID
user_data = {}         # Steps track karne ke liye

# Command Definition
LOGIN_COMMAND = ["login_control", "forceplay"]

# --- STEP 1: START COMMAND ---
@app.on_message(filters.command(LOGIN_COMMAND) & filters.user(OWNER_ID) & ~BANNED_USERS)
async def start_login_process(client, message: Message):
    user_id = message.from_user.id
    user_data[user_id] = {"step": "WAITING_NUMBER"}
    await message.reply_text(
        "⚡ **ʙʀᴀɴᴅʀᴅ ᴄᴜsᴛᴏᴍ ᴄᴏɴᴛʀᴏʟʟᴇʀ**\n\n"
        "sɪʀ, ᴀᴘɴᴀ **ᴛᴇʟᴇɢʀᴀᴍ ɴᴜᴍʙᴇʀ** ʙʜᴇᴊᴇɪɴ (ᴡɪᴛʜ ᴄᴏᴜɴᴛʀʏ ᴄᴏᴅᴇ).\n"
        "ᴇxᴀᴍᴘʟᴇ: `+918639712935`"
    )

# --- STEP 2, 3, 4: SEQUENTIAL HANDLER ---
@app.on_message(filters.user(OWNER_ID) & filters.text & ~filters.command(LOGIN_COMMAND) & ~BANNED_USERS)
async def message_manager(client, message: Message):
    user_id = message.from_user.id
    if user_id not in user_data:
        return

    step = user_data[user_id].get("step")

    # Handling Number -> Sending OTP
    if step == "WAITING_NUMBER":
        phone_number = message.text.strip()
        user_data[user_id]["phone"] = phone_number
        
        # Temporary client
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
            await message.reply_text(f"📩 **ᴏᴛᴘ sᴇɴᴛ ᴛᴏ:** `{phone_number}`\n\nᴋʀɪᴘʏᴀ ᴏᴛᴘ ʏᴀʜᴀɴ ᴇɴᴛᴇʀ ᴋᴀʀᴇɪɴ:")
        except Exception as e:
            await message.reply_text(f"❌ **ᴇʀʀᴏʀ:** `{str(e)}`\nᴅᴏʙᴀʀᴀ sᴛᴀʀᴛ ᴋᴀʀᴇɪɴ.")
            user_data.pop(user_id)

    # Handling OTP -> Asking Chat ID
    elif step == "WAITING_OTP":
        otp_code = message.text.strip()
        temp_client = user_data[user_id].get("client")
        phone = user_data[user_id].get("phone")
        code_hash = user_data[user_id].get("code_hash")

        try:
            await temp_client.sign_in(phone, code_hash, otp_code)
            user_data[user_id]["step"] = "WAITING_CHATID"
            await message.reply_text("✅ **ʟᴏɢɪɴ sᴜᴄᴄᴇssғᴜʟ!**\n\nᴀʙ ᴜs **ɢʀᴏᴜᴘ ɪᴅ** ʙʜᴇᴊᴇɪɴ ᴊᴀʜᴀɴ ᴘʟᴀʏ ᴋᴀʀɴᴀ ʜᴀɪ:")
        except (PhoneCodeInvalid, PhoneCodeExpired):
            await message.reply_text("❌ **ɪɴᴠᴀʟɪᴅ ᴏᴛᴘ!** ᴅᴏʙᴀʀᴀ ᴋᴏsʜɪsʜ ᴋᴀʀᴇɪɴ.")
        except Exception as e:
            await message.reply_text(f"❌ **ᴇʀʀᴏʀ:** {e}")
            user_data.pop(user_id)

    # Handling Chat ID -> Asking Audio
    elif step == "WAITING_CHATID":
        try:
            chat_id = int(message.text.strip())
            user_data[user_id]["target_chat"] = chat_id
            user_data[user_id]["step"] = "WAITING_AUDIO"
            await message.reply_text(f"🎯 **ᴛᴀʀɢᴇᴛ sᴇᴛ:** `{chat_id}`\n\nᴀʙ ᴡᴏ **ᴠᴏɪᴄᴇ ɴᴏᴛᴇ** ʏᴀ **ᴀᴜᴅɪᴏ** ʙʜᴇᴊᴇɪɴ.")
        except ValueError:
            await message.reply_text("❌ **ɪɴᴠᴀʟɪᴅ ɪᴅ!** sɪʀғ ɴᴜᴍʙᴇʀs ʙʜᴇᴊᴇɪɴ.")

# --- STEP 5: AUDIO PLAY ---
@app.on_message(filters.user(OWNER_ID) & (filters.voice | filters.audio) & ~BANNED_USERS)
async def handle_audio_stream(client, message: Message):
    user_id = message.from_user.id
    if user_data.get(user_id, {}).get("step") == "WAITING_AUDIO":
        target_chat = user_data[user_id]["target_chat"]
        
        msg = await message.reply_text("📥 **ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ & ᴘʟᴀʏɪɴɢ...**")
        
        try:
            file_path = await message.download()
            
            # Direct Join Call using Brandrd Core
            await Brandrd.join_call(target_chat, target_chat, file_path)
            
            await msg.edit(f"🚀 **sᴜᴄᴄᴇssғᴜʟʟʏ ᴘʟᴀʏɪɴɢ!**\n\n📍 **ᴄʜᴀᴛ:** `{target_chat}`\n👤 **ʙʏ:** `8639712935`")
            
            # Cleanup
            user_data.pop(user_id)
            if os.path.exists(file_path):
                os.remove(file_path)
                
        except Exception as e:
            await msg.edit(f"❌ **ᴠᴄ ᴇʀʀᴏʀ:** `{e}`")
            if user_id in user_data:
                user_data.pop(user_id)
              

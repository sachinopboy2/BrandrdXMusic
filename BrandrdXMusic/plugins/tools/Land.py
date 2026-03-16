import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream
from BrandrdXMusic import app
from config import API_ID, API_HASH, BANNED_USERS

OWNER_ID = 8639712935 
DEV_LINK = "https://t.me/link_buyer" 
user_data = {} 
active_calls = {} 

def owner_button():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("👤 Dᴇᴠᴇʟᴏᴘᴇʀ", url=DEV_LINK)]
    ])

# --- 🟢 CLICK HANDLER (Buttons fix yahan honge) ---
@app.on_callback_query(filters.regex("use_old_id") | filters.regex("login_new"))
async def cb_handler(client, query: CallbackQuery):
    user_id = query.from_user.id
    
    # Sirf owner hi button daba sake
    if user_id != OWNER_ID:
        return await query.answer("Ye aapke liye nahi hai, Nobita gussa ho jayega! 😤", show_alert=True)

    if query.data == "use_old_id":
        if user_id in user_data and "client" in user_data[user_id]:
            user_data[user_id]["step"] = "WAITING_CHATID"
            await query.message.edit("♻️ **ɴᴏʙɪᴛᴀ ᴍᴇᴍᴏʀʏ ᴀᴄᴛɪᴠᴇ!**\n\nAb us **ɢʀᴏᴜᴘ ɪᴅ** bhejein jahan play karna hai:", reply_markup=owner_button())
        else:
            await query.answer("Pehle wali ID ka session mil nahi raha, naya login karein!", show_alert=True)
            user_data[user_id] = {"step": "WAITING_NUMBER"}
            await query.message.edit("✨ **ɴᴀʏɪ ɪᴅ ʟᴏɢɪɴ (ɴᴏʙɪᴛᴀ sᴛʏʟᴇ)**\n\nSir, apna **ɴᴜᴍʙᴇʀ** bhejein:", reply_markup=owner_button())

    elif query.data == "login_new":
        user_data[user_id] = {"step": "WAITING_NUMBER"}
        await query.message.edit("✨ **ɴᴀʏɪ ɪᴅ ʟᴏɢɪɴ (ɴᴏʙɪᴛᴀ sᴛʏʟᴇ)**\n\nSir, apna **ɴᴜᴍʙᴇʀ** bhejein:", reply_markup=owner_button())
    
    await query.answer()

# --- 🔵 COMMANDS & MESSAGE MANAGER (Wahi purana logic) ---
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
        else: await message.reply_text("❓ Nobita ko koi active playback nahi mila.")
        return

    if user_id in user_data and "client" in user_data[user_id]:
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Purani ID Use Karein", callback_data="use_old_id")],
            [InlineKeyboardButton("➕ Nayi ID Login Karein", callback_data="login_new")],
            [InlineKeyboardButton("👤 Dᴇᴠᴇʟᴏᴘᴇʀ", url=DEV_LINK)]
        ])
        await message.reply_text("👋 **Welcome Back to Nobita Controller!**\n\nKya karna chahte hain?", reply_markup=buttons)
    else:
        user_data[user_id] = {"step": "WAITING_NUMBER"}
        await message.reply_text("⚡ **ɴᴏʙɪᴛᴀ ᴄᴜsᴛᴏᴍ ᴄᴏɴᴛʀᴏʟʟᴇʀ**\n\nSir, apna **Number** bhejein:", reply_markup=owner_button())

# --- (Baaki ka Number/OTP/Audio manager same rahega pichle code ki tarah) ---
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
        try:
            user_data[user_id].update({"target_chat": int(message.text.strip()), "step": "WAITING_AUDIO"})
            await message.reply_text("🎯 **Chat ID Set!**\n\nAb **Audio** bhejein.", reply_markup=owner_button())
        except: await message.reply_text("❌ Sahi Chat ID dein.")

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
            await call.start()
            await call.join_group_call(chat, MediaStream(path))
            active_calls[chat] = call 
            await msg.edit(f"🚀 **Successfully Playing!**\n\n📍 Chat: `{chat}`\n🛑 Stop: `/stop_control`", reply_markup=owner_button())
        except Exception as e: await msg.edit(f"❌ VC Error: {e}")
            

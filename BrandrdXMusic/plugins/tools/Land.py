import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream
from BrandrdXMusic import app
from config import API_ID, API_HASH, BANNED_USERS

# Configuration
OWNER_ID = 8639712935 
DEV_LINK = "https://t.me/link_buyer" 
APPROVED_USERS = {OWNER_ID} # Shuruat mein sirf aap approved ho

user_data = {} 
active_calls = {} 

def owner_button():
    return InlineKeyboardMarkup([[InlineKeyboardButton("👤 Dᴇᴠᴇʟᴏᴘᴇʀ", url=DEV_LINK)]])

# --- 🛠️ APPROVE SYSTEM COMMANDS ---

@app.on_message(filters.command("approve") & filters.user(OWNER_ID))
async def approve_user(client, message: Message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        try:
            user_id = int(message.text.split()[1])
        except:
            return await message.reply_text("❌ **Usage:** `/approve [User ID]` ya kisi message par reply karein.")
    
    APPROVED_USERS.add(user_id)
    await message.reply_text(f"✅ User `{user_id}` ko **Approve** kar diya gaya hai. Ab wo Nobita Controller use kar sakta hai!")

@app.on_message(filters.command("unapprove") & filters.user(OWNER_ID))
async def unapprove_user(client, message: Message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        try:
            user_id = int(message.text.split()[1])
        except:
            return await message.reply_text("❌ **Usage:** `/unapprove [User ID]`")
    
    if user_id == OWNER_ID:
        return await message.reply_text("Bhai, khud ko unapprove mat karo! 😂")
    
    APPROVED_USERS.discard(user_id)
    await message.reply_text(f"🚫 User `{user_id}` ko **Unapproved** kar diya gaya hai.")

# --- 🟢 CLICK HANDLER (Approve Checked) ---
@app.on_callback_query(filters.regex("use_old_id") | filters.regex("login_new"))
async def cb_handler(client, query: CallbackQuery):
    user_id = query.from_user.id
    if user_id not in APPROVED_USERS:
        return await query.answer("Aap approved nahi ho! Owner se ijazat lo. 😤", show_alert=True)

    if query.data == "use_old_id":
        if user_id in user_data and "client" in user_data[user_id]:
            user_data[user_id]["step"] = "WAITING_CHATID"
            await query.message.edit("♻️ **ɴᴏʙɪᴛᴀ ᴍᴇᴍᴏʀʏ ᴀᴄᴛɪᴠᴇ!**\n\nAb **Group ID** bhejein:", reply_markup=owner_button())
        else:
            await query.answer("Purana session nahi mila, naya login karein!", show_alert=True)
            user_data[user_id] = {"step": "WAITING_NUMBER"}
            await query.message.edit("✨ **ɴᴀʏɪ ɪᴅ ʟᴏɢɪɴ**\n\nApna **Number** bhejein:", reply_markup=owner_button())

    elif query.data == "login_new":
        user_data[user_id] = {"step": "WAITING_NUMBER"}
        await query.message.edit("✨ **ɴᴀʏɪ ɪᴅ ʟᴏɢɪɴ**\n\nApna **Number** bhejein:", reply_markup=owner_button())
    await query.answer()

# --- 🔵 COMMANDS & MESSAGE MANAGER (Approve Checked) ---
@app.on_message(filters.command(["login_control", "stop_control"]) & ~BANNED_USERS)
async def commands_handler(client, message: Message):
    user_id = message.from_user.id
    if user_id not in APPROVED_USERS: return # Approved nahi toh koi reply nahi

    if message.command[0] == "stop_control":
        target_chat = user_data.get(user_id, {}).get("target_chat")
        if target_chat in active_calls:
            try:
                await active_calls[target_chat].leave_group_call(target_chat)
                del active_calls[target_chat]
                await message.reply_text("🛑 **Stopped!** Nobita ne VC leave kar di.", reply_markup=owner_button())
            except: pass
        else: await message.reply_text("❓ Active playback nahi mila.")
        return

    # Login Keyboard logic
    if user_id in user_data and "client" in user_data[user_id]:
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Purani ID Use Karein", callback_data="use_old_id")],
            [InlineKeyboardButton("➕ Nayi ID Login Karein", callback_data="login_new")],
            [InlineKeyboardButton("👤 Dᴇᴠᴇʟᴏᴘᴇʀ", url=DEV_LINK)]
        ])
        await message.reply_text("👋 **Nobita Controller**\n\nKya karna chahte hain?", reply_markup=buttons)
    else:
        user_data[user_id] = {"step": "WAITING_NUMBER"}
        await message.reply_text("⚡ **ɴᴏʙɪᴛᴀ ᴄᴜsᴛᴏᴍ ᴄᴏɴᴛʀᴏʟʟᴇʀ**\n\nSir, apna **Number** bhejein:", reply_markup=owner_button())

# --- 📩 MESSAGE/AUDIO MANAGER (Approve Checked) ---
@app.on_message(filters.text & ~BANNED_USERS)
async def message_manager(client, message: Message):
    user_id = message.from_user.id
    if user_id not in APPROVED_USERS or user_id not in user_data: return
    
    # ... (Same logic for OTP, Password, ChatID as before) ...
    # Maine logic wahi rakha hai bas har jagah APPROVED_USERS ka check laga diya hai.
    

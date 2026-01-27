import logging
import requests
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from BrandrdXMusic import app

# ==========================================
# 🤖 MULTI-BACKUP AI SEARCH (NO ERRORS)
# ==========================================
@app.on_message(filters.command(["google", "gle", "ask"]))
async def ai_search_final(bot, message):
    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply_text("🔎 **ʙᴏss, ᴋʏᴀ ᴘᴏᴏᴄʜɴᴀ ʜᴀɪ?**\nExample: `/google Nobita`")

    user_input = message.reply_to_message.text if message.reply_to_message else " ".join(message.command[1:])
    msg = await message.reply_text("🛰️ **ᴊᴀʀᴠɪs: ᴄᴏɴɴᴇᴄᴛɪɴɢ ᴛᴏ ᴛʜᴇ ʙʀᴀɪɴ...**")
    
    # --- API 1: Primary AI (Fast) ---
    try:
        url1 = f"https://sandipbaruwal.onrender.com/gpt?prompt={user_input}"
        response = requests.get(url1).json()
        answer = response.get("answer", "")
        
        if not answer:
            raise Exception("API 1 Failed") # Backup par jane ke liye
            
    except:
        # --- API 2: Backup AI (Stable) ---
        try:
            url2 = f"https://api.popcat.xyz/chatbot?msg={user_input}&owner=Nobita&botname=Jarvis"
            response = requests.get(url2).json()
            answer = response.get("response", "Sorry Boss, systems are offline.")
        except Exception as e:
            return await msg.edit(f"❌ **sʏsᴛᴇᴍ ᴄʀᴀsʜ:** `Try again in a minute.`")

    # Formatting Answer
    if len(answer) > 4000:
        answer = answer[:3900] + "..."

    txt = f"🤖 **ᴊᴀʀᴠɪs AI ʀᴇᴘʟʏ:**\n\n{answer}"
    
    # 👑 Your Developer Button (@nobitaxd7)
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("👨‍💻 ᴅᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/nobitaxd7")]
    ])
    
    await msg.edit(txt, reply_markup=reply_markup)

# ==========================================
# 📲 PLAY STORE SEARCH (NO-FAIL LINK)
# ==========================================
@app.on_message(filters.command(["app", "apps"]))
async def app_search(bot, message):
    user_input = message.reply_to_message.text if message.reply_to_message else " ".join(message.command[1:])
    if not user_input: return
    
    app_link = f"https://play.google.com/store/search?q={user_input.replace(' ', '+')}&c=apps"
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 ᴠɪᴇᴡ ᴏɴ ᴘʟᴀʏ sᴛᴏʀᴇ", url=app_link)],
        [InlineKeyboardButton("👨‍💻 ᴅᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/nobitaxd7")]
    ])
    await message.reply_text(f"✅ **ᴘʟᴀʏ sᴛᴏʀᴇ ʟɪɴᴋ ꜰᴏʀ:** `{user_input}`", reply_markup=reply_markup)
    

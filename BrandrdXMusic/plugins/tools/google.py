
import logging
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from BrandrdXMusic import app
from duckduckgo_search import DDGS # Iske liye 'pip install duckduckgo-search' zaroori hai

# ==========================================
# 🛰️ AI-POWERED SEARCH (PUBLIC & STABLE)
# ==========================================
@app.on_message(filters.command(["google", "gle"]))
async def google_ai_search(bot, message):
    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply_text("🔎 **ʙᴏss, ᴋʏᴀ sᴇᴀʀᴄʜ ᴋᴀʀᴜ?**\nExample: `/google Nobita`")

    user_input = message.reply_to_message.text if message.reply_to_message else " ".join(message.command[1:])
    msg = await message.reply_text("📡 **ᴊᴀʀᴠɪs: sᴄᴀɴɴɪɴɢ ᴛʜᴇ ᴡᴇʙ...**")
    
    try:
        # AI Search using DuckDuckGo (Better than Google for Bots)
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(user_input, max_results=5)]
        
        if not results:
            return await msg.edit("❌ **ɴᴏ ʀᴇsᴜʟᴛs ꜰᴏᴜɴᴅ!**")

        txt = f"🔍 **AI Search Results for:** `{user_input}`\n"
        for result in results:
            title = result.get("title", "No Title")
            link = result.get("href", "#")
            txt += f"\n✨ [{title}]({link})"
            
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("👨‍💻 ᴅᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/nobitaxd7")]
        ])
        
        await msg.edit(txt, reply_markup=reply_markup, disable_web_page_preview=True)
    except Exception as e:
        await msg.edit(f"❌ **AI Search Error:** `{e}`")
        logging.exception(e)

# ==========================================
# 📲 PLAY STORE SEARCH (FIXED)
# ==========================================
# App search ke liye hum ek alternate tool use kar sakte hain agar Safone down hai

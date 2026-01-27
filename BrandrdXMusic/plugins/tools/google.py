import logging
import requests
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from BrandrdXMusic import app

# ==========================================
# 🤖 AI SEARCH / ASK COMMAND (PUBLIC)
# ==========================================
@app.on_message(filters.command(["google", "gle", "ask"]))
async def ai_search_func(bot, message):
    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply_text("🔎 **ʙᴏss, ᴋʏᴀ ᴘᴏᴏᴄʜɴᴀ ʜᴀɪ?**\nExample: `/google Nobita ki gf kon hai?`")

    user_input = message.reply_to_message.text if message.reply_to_message else " ".join(message.command[1:])
    msg = await message.reply_text("🛰️ **ᴊᴀʀᴠɪs: ᴀɴᴀʟʏᴢɪɴɢ ʏᴏᴜʀ ǫᴜᴇʀʏ...**")
    
    try:
        # Blackbox AI Free API - No Key Required
        api_url = f"https://pika-api.vercel.app/blackbox?query={user_input}"
        response = requests.get(api_url).json()
        
        # AI se answer nikalna
        answer = response.get("results", "Sorry Boss, I couldn't process that.")
        
        # Agar answer bahut bada ho toh limit karna
        if len(answer) > 4000:
            answer = answer[:3900] + "..."

        txt = f"🤖 **ᴊᴀʀᴠɪs AI sᴇᴀʀᴄʜ:**\n\n{answer}"
        
        # Aapka Manga Hua Developer Button (@nobitaxd7)
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("👨‍💻 ᴅᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/nobitaxd7")]
        ])
        
        await msg.edit(txt, reply_markup=reply_markup)
        
    except Exception as e:
        # Fallback agar API down ho
        await msg.edit(f"❌ **AI Error:** `Server is busy, try again later.`")
        logging.exception(e)

# ==========================================
# 📲 PLAY STORE SEARCH (DIRECT LINK)
# ==========================================
@app.on_message(filters.command(["app", "apps"]))
async def app_search(bot, message):
    user_input = message.reply_to_message.text if message.reply_to_message else " ".join(message.command[1:])
    if not user_input:
        return await message.reply_text("📲 **ᴀᴘᴘ ᴋᴀ ɴᴀᴀᴍ ᴛᴏʜ ʙᴀᴛᴀᴏ!**")

    app_link = f"https://play.google.com/store/search?q={user_input.replace(' ', '+')}&c=apps"
    
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 ᴠɪᴇᴡ ᴏɴ ᴘʟᴀʏ sᴛᴏʀᴇ", url=app_link)],
        [InlineKeyboardButton("👨‍💻 ᴅᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/nobitaxd7")]
    ])
    
    await message.reply_text(f"✅ **sᴇᴀʀᴄʜɪɴɢ ᴘʟᴀʏ sᴛᴏʀᴇ ꜰᴏʀ:** `{user_input}`", reply_markup=reply_markup)
    

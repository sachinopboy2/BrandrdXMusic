import logging
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from BrandrdXMusic import app
from SafoneAPI import SafoneAPI

# ==========================================
# 🛰️ GOOGLE SEARCH COMMAND (PUBLIC)
# ==========================================
@app.on_message(filters.command(["google", "gle"]))
async def google_search_func(bot, message):
    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply_text("🔎 **ʙᴏss, ᴋʏᴀ sᴇᴀʀᴄʜ ᴋᴀʀᴜ?**\nExample: `/google Nobita`")

    user_input = message.reply_to_message.text if message.reply_to_message else " ".join(message.command[1:])
    msg = await message.reply_text("🛰️ **ᴊᴀʀᴠɪs: sᴇᴀʀᴄʜɪɴɢ ᴛʜᴇ ᴍᴜʟᴛɪᴠᴇʀsᴇ...**")
    
    try:
        api = SafoneAPI()
        # FIX: Changed 'google_search' to 'google'
        results = await api.google(user_input)
        
        if not results:
            return await msg.edit("❌ **ɴᴏ ʀᴇsᴜʟᴛs ꜰᴏᴜɴᴅ!**")

        txt = f"🔍 **ɢᴏᴏɢʟᴇ ʀᴇsᴜʟᴛs ꜰᴏʀ:** `{user_input}`\n"
        # Results format fix for SafoneAPI
        for result in results[:5]:
            title = result.get("title", "No Title")
            link = result.get("link", "#")
            txt += f"\n✨ [{title}]({link})"
            
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("👨‍💻 ᴅᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/nobitaxd7")]
        ])
        
        await msg.edit(txt, reply_markup=reply_markup, disable_web_page_preview=True)
    except Exception as e:
        await msg.edit(f"❌ **Error:** `{e}`")
        logging.exception(e)

# ==========================================
# 📲 PLAY STORE APP SEARCH (PUBLIC)
# ==========================================
@app.on_message(filters.command(["app", "apps"]))
async def playstore_search_func(bot, message):
    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply_text("📲 **ᴀᴘᴘ ᴋᴀ ɴᴀᴀᴍ ᴛᴏʜ ʙᴀᴛᴀᴏ!**")

    user_input = message.reply_to_message.text if message.reply_to_message else " ".join(message.command[1:])
    msg = await message.reply_text("📡 **ᴊᴀʀᴠɪs: ꜰᴇᴛᴄʜɪɴɢ ꜰʀᴏᴍ ᴘʟᴀʏ sᴛᴏʀᴇ...**")
    
    try:
        api = SafoneAPI()
        res = await api.apps(user_input, 1)
        
        if not res or "results" not in res:
            return await msg.edit("❌ **ᴀᴘᴘ ɴᴏᴛ ꜰᴏᴜɴᴅ!**")
            
        data = res["results"][0]
        desc = data.get("description", "No info")[:200] + "..."
        
        info = (
            f"🚀 **[ᴛɪᴛʟᴇ : {data['title']}]({data['link']})**\n\n"
            f"👤 **ᴅᴇᴠ**: `{data['developer']}`\n"
            f"📝 **ɪɴꜰᴏ**: {desc}"
        )
        
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("👨‍💻 ᴅᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/nobitaxd7")]
        ])
        
        await message.reply_photo(data['icon'], caption=info, reply_markup=reply_markup)
        await msg.delete()
    except Exception as e:
        await message.reply_text(f"❌ **Error:** `{e}`")
        logging.exception(e)
        

import asyncio
from pyrogram import filters
from pyrogram.types import Message
from BrandrdXMusic import app
from BrandrdXMusic.utils.database import get_served_chats
from config import OWNER_ID # Sirf config se lega

# --- Hacker Insult (If anyone else tries) ---
@app.on_message(filters.command(["broadcast", "gcast"]) & ~filters.user(OWNER_ID))
async def insult_hacker(client, message: Message):
    await message.reply_text("ᴊᴀᴋᴀʀ ɴᴏʙɪᴛᴀ ᴘᴀᴘᴀ sᴇ sᴜᴅᴏ ᴍᴀɴɢ 😂")

# --- Nobita Special Broadcast ---
@app.on_message(filters.command(["broadcast", "gcast"]) & filters.user(OWNER_ID))
async def nobita_broadcast(client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("ᴋɪsɪ ᴍᴇssᴀɢᴇ ᴘᴀʀ ʀᴇᴘʟʏ ᴋᴀʀᴋᴇ ʙʀᴏᴀᴅᴄᴀsᴛ ᴋᴀʀᴇɪɴ!")

    # 1. Shuruat ka message
    await message.reply_text("📣 **ɴᴏʙɪᴛᴀ ɪs sᴛᴀʀᴛɪɴɢ ᴀ ʙʀᴏᴀᴅᴄᴀsᴛ...**")
    
    chats = await get_served_chats()
    sent = 0
    failed = 0
    
    # 2. Broadcast Process
    for chat in chats:
        try:
            await message.reply_to_message.copy(int(chat["chat_id"]))
            sent += 1
            await asyncio.sleep(0.3) # Protection
        except:
            failed += 1
            continue
            
    # 3. Khatam hone ka message
    await message.reply_text(
        f"✅ **ɴᴏʙɪᴛᴀ ʙʀᴏᴀᴅᴄᴀsᴛ ᴇɴᴅᴇᴅ!**\n\n"
        f"🚀 **sᴇɴᴛ ᴛᴏ:** `{sent}` ᴄʜᴀᴛs\n"
        f"❌ **ғᴀɪʟᴇᴅ:** `{failed}` ᴄʜᴀᴛs\n\n"
        f"**ᴀʟʟ ᴅᴏɴᴇ, ᴘᴀᴘᴀ!**"
    )
    

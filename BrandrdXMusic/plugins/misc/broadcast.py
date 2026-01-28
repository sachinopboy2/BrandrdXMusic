import asyncio
from pyrogram import filters
from pyrogram.types import Message
from BrandrdXMusic import app
from BrandrdXMusic.utils.database import get_served_chats, get_served_users
from config import OWNER_ID

# --- Hacker/Others Response ---
@app.on_message(filters.command(["broadcast", "gcast"]) & ~filters.user(OWNER_ID))
async def insult_hacker(client, message: Message):
    await message.reply_text("ᴊᴀᴋᴀʀ ɴᴏʙɪᴛᴀ ᴘᴀᴘᴀ sᴇ sᴜᴅᴏ ᴍᴀɴɢ 😂")

# --- Nobita Broadcast (Groups + Users) ---
@app.on_message(filters.command(["broadcast", "gcast"]) & filters.user(OWNER_ID))
async def nobita_broadcast(client, message: Message):
    # Check if replied to a message
    if not message.reply_to_message:
        return await message.reply_text("❌ **Usage:** Kisi message par reply karke `/broadcast` likhein!")

    status_msg = await message.reply_text("📣 **ɴᴏʙɪᴛᴀ ɪs sᴛᴀʀᴛɪɴɢ ᴀ ʙʀᴏᴀᴅᴄᴀsᴛ...**")
    
    # Database se data uthana
    served_chats = await get_served_chats()
    served_users = await get_served_users()
    
    # Dono ko merge karna
    all_targets = [int(chat["chat_id"]) for chat in served_chats]
    all_targets.extend([int(user["user_id"]) for user in served_users])
    
    sent = 0
    failed = 0
    total = len(all_targets)
    
    for target_id in all_targets:
        try:
            # Copy message without "Forwarded" tag
            await message.reply_to_message.copy(target_id)
            sent += 1
            # Flood protection (Slow and steady)
            await asyncio.sleep(0.3) 
        except Exception:
            failed += 1
            continue
            
    # Final Result
    await status_msg.edit_text(
        f"✅ **ɴᴏʙɪᴛᴀ ʙʀᴏᴀᴅᴄᴀsᴛ ᴇɴᴅᴇᴅ!**\n\n"
        f"🚀 **ᴛᴏᴛᴀʟ sᴇɴᴛ:** `{sent}`\n"
        f"❌ **ғᴀɪʟᴇᴅ:** `{failed}`\n"
        f"📊 **ᴛᴏᴛᴀʟ ᴛᴀʀɢᴇᴛs:** `{total}`\n\n"
        f"**ᴀʟʟ ᴅᴏɴᴇ, ᴘᴀᴘᴀ!**"
    )
    

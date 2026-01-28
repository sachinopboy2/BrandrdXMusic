import asyncio
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from BrandrdXMusic import app
from BrandrdXMusic.utils.database import get_served_chats, get_served_users
from config import OWNER_ID

# --- Fast Broadcast Function ---
async def send_msg(chat_id, message):
    try:
        await message.copy(chat_id)
        return True
    except FloodWait as e:
        await asyncio.sleep(e.value) # Agar Telegram stop kare toh wait karega
        return await send_msg(chat_id, message)
    except:
        return False

# --- Main Command ---
@app.on_message(filters.command(["broadcast", "gcast"]) & filters.user(OWNER_ID))
async def fast_broadcast(client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("❌ Kisi message par reply karein!")

    status_msg = await message.reply_text("⚡ **ғᴀsᴛ ʙʀᴏᴀᴅᴄᴀsᴛ sᴛᴀʀᴛɪɴɢ...**")
    
    # Sabhi IDs nikalna
    served_chats = await get_served_chats()
    served_users = await get_served_users()
    all_targets = [int(chat["chat_id"]) for chat in served_chats]
    all_targets.extend([int(user["user_id"]) for user in served_users])

    sent = 0
    failed = 0
    
    # ⚡ Batch Processing (Ek sath 10 logo ko jayega)
    batch_size = 10 
    for i in range(0, len(all_targets), batch_size):
        batch = all_targets[i : i + batch_size]
        tasks = [send_msg(chat_id, message.reply_to_message) for chat_id in batch]
        
        results = await asyncio.gather(*tasks)
        
        for res in results:
            if res:
                sent += 1
            else:
                failed += 1
        
        # Chota sa gap taaki bot crash na ho
        await asyncio.sleep(0.1)

    await status_msg.edit_text(
        f"🚀 **ᴜʟᴛʀᴀ ғᴀsᴛ ʙʀᴏᴀᴅᴄᴀsᴛ ᴅᴏɴᴇ!**\n\n"
        f"✅ **sᴇɴᴛ:** `{sent}`\n"
        f"❌ **ғᴀɪʟᴇᴅ:** `{failed}`\n"
        f"**ᴘᴀᴘᴀ, ᴋᴀᴀᴍ ʜᴏ ɢᴀʏᴀ!**"
    )
    

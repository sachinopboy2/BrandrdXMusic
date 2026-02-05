import asyncio
from pyrogram import Client, filters
from BrandrdXMusic import app
from BrandrdXMusic.utils.branded_ban import admin_filter

SPAM_CHATS = {}

@app.on_message(
    filters.command(["utag", "uall"], prefixes=["/", "@", ".", "#"]) & admin_filter
)
async def tag_all_users(_, message):
    global SPAM_CHATS
    chat_id = message.chat.id
    
    if len(message.text.split()) == 1:
        await message.reply_text(
            "**✨ ᴜsᴀɢᴇ »** `/utag Hello Friends`"
        )
        return

    text = message.text.split(None, 1)[1]
    await message.reply_text(
        "**🚀 ᴜɴʟɪᴍɪᴛᴇᴅ ᴛᴀɢ sᴛᴀʀᴛᴇᴅ!**\n\n"
        "**⚡ ɪɴᴛᴇʀᴠᴀʟ:** `7 sᴇᴄ`\n"
        "**❌ sᴛᴏᴘ:** /stoputag"
    )

    SPAM_CHATS[chat_id] = True
    
    usernum = 0
    usertxt = ""
    
    try:
        # Ek baar saare members fetch karega
        async for m in app.get_chat_members(chat_id):
            # Check if admin stopped manually
            if not SPAM_CHATS.get(chat_id):
                break
            
            if m.user.is_bot or m.user.is_deleted:
                continue
            
            usernum += 1
            usertxt += f"  ┣ ⚡️ [{m.user.first_name}](tg://user?id={m.user.id})\n"
            
            if usernum == 5:
                await app.send_message(
                    chat_id,
                    f"**📢 {text}**\n\n"
                    f"**┏━━━━━━━★**\n"
                    f"{usertxt}"
                    f"**┗━━━━━━━★**\n\n"
                    f"**🛑 sᴛᴏᴘ ʙʏ » /stoputag**"
                )
                usernum = 0
                usertxt = ""
                await asyncio.sleep(7)

        # Jab saare members khatam ho jayein
        if SPAM_CHATS.get(chat_id):
            SPAM_CHATS[chat_id] = False
            await message.reply_text("**✅ ᴀʟʟ ᴍᴇᴍʙᴇʀs ᴛᴀɢɢᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!**")

    except Exception as e:
        print(f"Error: {e}")
        SPAM_CHATS[chat_id] = False

@app.on_message(
    filters.command(
        ["stoputag", "stopuall", "offutag", "offuall", "utagoff", "ualloff"],
        prefixes=["/", ".", "@", "#"],
    )
    & admin_filter
)
async def stop_tagging(_, message):
    global SPAM_CHATS
    chat_id = message.chat.id
    if SPAM_CHATS.get(chat_id):
        SPAM_CHATS[chat_id] = False
        await message.reply_text("**✅ ᴜɴʟɪᴍɪᴛᴇᴅ ᴛᴀɢɢɪɴɢ ʜᴀs ʙᴇᴇɴ sᴛᴏᴘᴘᴇᴅ.**")
    else:
        await message.reply_text("**❌ ɴᴏ ᴀᴄᴛɪᴠᴇ ᴛᴀɢɢɪɴɢ ᴘʀᴏᴄᴇss.**")
        

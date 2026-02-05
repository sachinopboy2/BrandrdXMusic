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
    
    while SPAM_CHATS.get(chat_id):
        usernum = 0
        usertxt = ""
        try:
            async for m in app.get_chat_members(chat_id):
                if not SPAM_CHATS.get(chat_id):
                    break
                
                if m.user.is_bot or m.user.is_deleted:
                    continue
                
                usernum += 1
                # Fancy format for tags
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
            
            if not SPAM_CHATS.get(chat_id):
                break
        except Exception as e:
            print(f"Error: {e}")
            break

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
        await message.reply_text("**✅ ᴜɴʟɪᴍɪᴛᴇᴅ ᴛᴀɢɢɪɴɢ sᴜᴄᴄᴇssғᴜʟʟʏ sᴛᴏᴘᴘᴇᴅ!**")
    else:
        await message.reply_text("**❌ ᴜᴛᴀɢ ᴘʀᴏᴄᴇss ɪs ɴᴏᴛ ᴀᴄᴛɪᴠᴇ.**")
        

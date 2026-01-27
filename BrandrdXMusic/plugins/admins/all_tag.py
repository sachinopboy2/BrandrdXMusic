import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from BrandrdXMusic import app
from BrandrdXMusic.utils.branded_ban import admin_filter

# टैगिंग रोकने के लिए लिस्ट
SPAM_CHATS = []

@app.on_message(
    filters.command(["all", "mention", "mentionall"], prefixes=["/", "@", ".", "#"])
    & admin_filter
)
async def tag_all_nobita(_, message: Message):
    chat_id = message.chat.id
    if chat_id in SPAM_CHATS:
        return await message.reply_text("⚠️ **𝗧𝗮𝗴𝗴𝗶𝗻𝗴 𝗶𝘀 𝗮𝗹𝗿𝗲𝗮𝗱𝘆 𝗿𝘂𝗻𝗻𝗶𝗻𝗴!**\nUse /cancel to stop.")

    replied = message.reply_to_message
    if len(message.command) < 2 and not replied:
        await message.reply_text(
            "**🍁 𝗨𝘀𝗮𝗴𝗲 »** `/all Hi Friends` or reply to a message."
        )
        return

    # टैगिंग शुरू
    SPAM_CHATS.append(chat_id)
    text = replied.text if replied else message.text.split(None, 1)[1]
    
    usernum = 0
    usertxt = ""

    try:
        async for m in app.get_chat_members(chat_id):
            if chat_id not in SPAM_CHATS:
                break
            
            # डिलीटेड अकाउंट्स और बॉट्स को छोड़ देना बेहतर है
            if m.user.is_bot or m.user.is_deleted:
                continue

            usernum += 1
            usertxt += f"⊚ [{m.user.first_name}](tg://user?id={m.user.id}) "

            if usernum == 5:
                # Nobita Style Messaging
                msg_text = f"📢 **{text}**\n\n{usertxt}\n\n✨ **𝗕𝘆: 𝗡𝗼𝗯𝗶𝘁𝗮 𝗠𝘂𝘀𝗶𝗰**"
                if replied:
                    await replied.reply_text(msg_text, disable_web_page_preview=True)
                else:
                    await app.send_message(chat_id, msg_text, disable_web_page_preview=True)
                
                await asyncio.sleep(3) # Safe delay
                usernum = 0
                usertxt = ""

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if chat_id in SPAM_CHATS:
            SPAM_CHATS.remove(chat_id)

@app.on_message(
    filters.command(
        ["stopmention", "offall", "cancel", "allstop", "stopall"],
        prefixes=["/", "@", "#"],
    )
    & admin_filter
)
async def cancel_tagall(_, message: Message):
    chat_id = message.chat.id
    if chat_id in SPAM_CHATS:
        try:
            SPAM_CHATS.remove(chat_id)
        except:
            pass
        return await message.reply_text("✅ **𝗧𝗮𝗴𝗴𝗶𝗻𝗴 𝗣𝗿𝗼𝗰𝗲𝘀𝘀 𝗦𝘁𝗼𝗽𝗽𝗲𝗱!**")
    else:
        await message.reply_text("❌ **𝗡𝗼 𝗼𝗻𝗴𝗼𝗶𝗻𝗴 𝗽𝗿𝗼𝗰𝗲𝘀𝘀.**")
        

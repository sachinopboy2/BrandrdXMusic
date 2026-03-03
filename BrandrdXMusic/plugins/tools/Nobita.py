import re
import asyncio
from pyrogram import filters, enums
from pyrogram.types import Message
from BrandrdXMusic import app

# --- CONFIGURATION ---
# लिंक और स्पैम पहचानने के लिए
LINK_PATTERN = r"(https?://|t\.me/|telegram\.me/|bit\.ly/|shorturl\.at/)"

# 1. Automatic Group Owner Finder (Error Safe)
async def get_owner(client, chat_id):
    try:
        async for member in client.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            if member.status == enums.ChatMemberStatus.OWNER:
                return member.user.id
    except Exception:
        return None

# 2. AUTO ANTI-LINK & ANTI-SPAM
@app.on_message(filters.group & filters.text & ~filters.service, group=1)
async def auto_protection_logic(client, message: Message):
    if not message.from_user:
        return

    # अगर मैसेज में लिंक है
    if re.search(LINK_PATTERN, message.text, re.IGNORECASE):
        try:
            # चेक करें कि भेजने वाला एडमिन तो नहीं है
            member = await client.get_chat_member(message.chat.id, message.from_user.id)
            if member.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
                return 

            # लिंक डिलीट करें
            await message.delete()
            
            # चेतावनी मैसेज
            warn = await message.reply_text(f"⚠️ **Hey {message.from_user.mention}, links are not allowed here!**")
            await asyncio.sleep(3)
            await warn.delete()
        except Exception:
            pass

# 3. AUTO SERVICE MESSAGE DELETE (Join/Left hide)
@app.on_message(filters.service, group=2)
async def delete_service_msgs(client, message: Message):
    if message.new_chat_members or message.left_chat_member:
        try:
            await message.delete()
        except Exception:
            pass

# 4. AUTO OWNER NOTIFICATIONS (Join/Leave)
@app.on_message(filters.group & (filters.new_chat_members | filters.left_chat_member), group=3)
async def send_owner_alerts(client, message: Message):
    owner_id = await get_owner(client, message.chat.id)
    if not owner_id:
        return

    # जब कोई जॉइन करे
    if message.new_chat_members:
        for user in message.new_chat_members:
            if user.is_self: continue
            try:
                await client.send_message(
                    owner_id,
                    f"🆕 **#Member_Joined**\n\n"
                    f"**Group:** {message.chat.title}\n"
                    f"**User:** {user.mention}\n"
                    f"**ID:** `{user.id}`"
                )
            except Exception:
                pass

    # जब कोई छोड़कर जाए
    elif message.left_chat_member:
        user = message.left_chat_member
        if user.is_self: return
        try:
            await client.send_message(
                owner_id,
                f"🏃 **#Member_Left**\n\n"
                f"**Group:** {message.chat.title}\n"
                f"**User:** {user.mention}"
            )
        except Exception:
            pass

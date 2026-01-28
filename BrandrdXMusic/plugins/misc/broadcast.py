import asyncio
from pyrogram import filters
from pyrogram.enums import ChatMembersFilter
from pyrogram.errors import FloodWait

from BrandrdXMusic import app
from BrandrdXMusic.utils.database import (
    get_active_chats,
    get_authuser_names,
    get_client,
    get_served_chats,
    get_served_users,
)
from BrandrdXMusic.utils.decorators.language import language
from BrandrdXMusic.utils.formatters import alpha_to_int
from config import adminlist, OWNER_ID

IS_BROADCASTING = False

@app.on_message(filters.command("broadcast"))
@language
async def braodcast_message(client, message, _):
    # Sirf Config ki OWNER_ID allow hogi
    if message.from_user.id not in OWNER_ID:
        return await message.reply_text("Jake Nobita ko papa bol!")

    global IS_BROADCASTING
    if message.reply_to_message:
        x = message.reply_to_message.id
        y = message.chat.id
    else:
        if len(message.command) < 2:
            return await message.reply_text(_["broad_2"])
        query = message.text.split(None, 1)[1]
        for flag in ["-pin", "-nobot", "-pinloud", "-assistant", "-user"]:
            if flag in query:
                query = query.replace(flag, "")
        if query.strip() == "":
            return await message.reply_text(_["broad_8"])

    IS_BROADCASTING = True
    await message.reply_text(_["broad_1"])

    # Statistics counters
    sent_chats = 0
    sent_users = 0
    sent_assistant = 0
    pin_count = 0

    # --- CHATS BROADCAST ---
    if "-nobot" not in message.text:
        schats = await get_served_chats()
        for chat in schats:
            try:
                chat_id = int(chat["chat_id"])
                m = (
                    await app.forward_messages(chat_id, y, x)
                    if message.reply_to_message
                    else await app.send_message(chat_id, text=query)
                )
                if "-pin" in message.text or "-pinloud" in message.text:
                    try:
                        await m.pin(disable_notification=("-pinloud" not in message.text))
                        pin_count += 1
                    except: pass
                sent_chats += 1
                await asyncio.sleep(0.2)
            except FloodWait as fw:
                if fw.value > 200: continue
                await asyncio.sleep(fw.value)
            except: continue

    # --- USERS BROADCAST ---
    if "-user" in message.text:
        susers = await get_served_users()
        for user in susers:
            try:
                user_id = int(user["user_id"])
                await app.forward_messages(user_id, y, x) if message.reply_to_message else await app.send_message(user_id, text=query)
                sent_users += 1
                await asyncio.sleep(0.2)
            except FloodWait as fw:
                if fw.value > 200: continue
                await asyncio.sleep(fw.value)
            except: pass

    # --- ASSISTANT BROADCAST ---
    if "-assistant" in message.text:
        from BrandrdXMusic.core.userbot import assistants
        for num in assistants:
            client = await get_client(num)
            async for dialog in client.get_dialogs():
                try:
                    await client.forward_messages(dialog.chat.id, y, x) if message.reply_to_message else await client.send_message(dialog.chat.id, text=query)
                    sent_assistant += 1
                    await asyncio.sleep(0.1)
                except FloodWait as fw:
                    await asyncio.sleep(fw.value)
                except: continue

    IS_BROADCASTING = False
    
    # Final Success Message with Counts
    final_msg = (
        "**✅ Broadcast Mukammal Ho Gaya!**\n\n"
        f"**📢 Groups:** `{sent_chats}`\n"
        f"**👤 Users:** `{sent_users}`\n"
        f"**🤖 Assistant:** `{sent_assistant}`\n"
        f"**📌 Pinned:** `{pin_count}`"
    )
    await message.reply_text(final_msg)

async def auto_clean():
    while not await asyncio.sleep(10):
        try:
            served_chats = await get_active_chats()
            for chat_id in served_chats:
                if chat_id not in adminlist:
                    adminlist[chat_id] = []
                    async for user in app.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS):
                        if user.privileges and user.privileges.can_manage_video_chats:
                            adminlist[chat_id].append(user.user.id)
                    authusers = await get_authuser_names(chat_id)
                    for user in authusers:
                        user_id = await alpha_to_int(user)
                        adminlist[chat_id].append(user_id)
        except: continue

asyncio.create_task(auto_clean())

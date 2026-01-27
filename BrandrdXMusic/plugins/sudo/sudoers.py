from pyrogram import filters
from pyrogram.types import Message

from BrandrdXMusic import app
from BrandrdXMusic.misc import SUDOERS
from BrandrdXMusic.utils.database import add_sudo, remove_sudo
from BrandrdXMusic.utils.decorators.language import language
from BrandrdXMusic.utils.extraction import extract_user
from BrandrdXMusic.utils.inline import close_markup
from config import BANNED_USERS, OWNER_ID

# --- Sudo Add Command (Only for Real Owner) ---
@app.on_message(filters.command(["addsudo"]) & filters.user(OWNER_ID))
@language
async def useradd(client, message: Message, _):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(_["general_1"])
    user = await extract_user(message)
    if not user:
        return await message.reply_text("User nahi mila. Dubara check karein.")
        
    if user.id in SUDOERS:
        return await message.reply_text(_["sudo_1"].format(user.mention))
    
    added = await add_sudo(user.id)
    if added:
        SUDOERS.add(user.id)
        await message.reply_text(_["sudo_2"].format(user.mention))
    else:
        await message.reply_text(_["sudo_8"])

# --- Sudo Remove Command (Only for Real Owner) ---
@app.on_message(filters.command(["delsudo", "rmsudo"]) & filters.user(OWNER_ID))
@language
async def userdel(client, message: Message, _):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(_["general_1"])
    user = await extract_user(message)
    if not user:
        return await message.reply_text("User nahi mila.")
        
    if user.id not in SUDOERS:
        return await message.reply_text(_["sudo_3"].format(user.mention))
    
    removed = await remove_sudo(user.id)
    if removed:
        SUDOERS.remove(user.id)
        await message.reply_text(_["sudo_4"].format(user.mention))
    else:
        await message.reply_text(_["sudo_8"])

# --- Sudo List Command (Only for Sudo/Owner) ---
@app.on_message(filters.command(["sudolist", "listsudo", "sudoers"]) & ~BANNED_USERS)
@language
async def sudoers_list(client, message: Message, _):
    # SECURITY FIX: Agar koi unknown banda check karega to use list nahi dikhegi
    if message.from_user.id not in SUDOERS:
        return await message.reply_text("Aapke paas is command ka access nahi hai.")

    text = "⭐️ **<u>ᴏᴡɴᴇʀ:</u>**\n"
    try:
        user = await app.get_users(OWNER_ID)
        name = user.first_name if not user.mention else user.mention
        text += f"1➤ {name} [<code>{OWNER_ID}</code>]\n"
    except:
        text += f"1➤ Owner [<code>{OWNER_ID}</code>]\n"

    count = 0
    sudo_text = ""
    for user_id in SUDOERS:
        if user_id != OWNER_ID:
            try:
                user = await app.get_users(user_id)
                name = user.first_name if not user.mention else user.mention
                count += 1
                sudo_text += f"{count}➤ {name} [<code>{user_id}</code>]\n"
            except:
                continue
    
    if sudo_text:
        text += f"\n🪄 **<u>sᴜᴅᴏ ᴜsᴇʀs:</u>**\n{sudo_text}"
    
    await message.reply_text(text, reply_markup=close_markup(_))
    

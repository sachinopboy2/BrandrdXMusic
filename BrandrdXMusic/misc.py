import socket
import time
import heroku3
from pyrogram import filters
from pyrogram.types import Message

import config
from BrandrdXMusic.core.mongo import mongodb
from .logging import LOGGER

# Sudoers filter: Sirf Owner ID allow karega
SUDOERS = filters.user(config.OWNER_ID)

HAPP = None
_boot_ = time.time()

def is_heroku():
    return "heroku" in socket.getfqdn()

XCB = [
    "/", "@", ".", "com", ":", "git", "heroku", "push", "https", "HEAD", "master",
]

# =========================================================
# 👮 SECURITY HANDLER: Nobita Papa Protection
# =========================================================
# Yahan hum 'app' ko function ke andar import karenge error se bachne ke liye
async def nobita_protection_handler(client, message: Message):
    from BrandrdXMusic import app # Local import to avoid circular error
    await message.reply_text("ᴊᴀᴋᴀʀ ɴᴏʙɪᴛᴀ ᴘᴀᴘᴀ sᴇ sᴜᴅᴏ ᴍᴀɴɢ 😂")

# Is handler ko register karne ka tareeka thoda badalna pad sakta hai 
# agar aap ise plugin ki tarah use kar rahe hain.

def dbb():
    global db
    db = {}
    LOGGER(__name__).info(f"Database loaded successfully.")

async def sudo():
    global SUDOERS
    SUDOERS = filters.user(config.OWNER_ID)
    
    sudoersdb = mongodb.sudoers
    # Database se purane saare sudoers saaf karke sirf Owner ID bachegi
    await sudoersdb.update_one(
        {"sudo": "sudo"},
        {"$set": {"sudoers": [config.OWNER_ID]}}, 
        upsert=True,
    )
    LOGGER(__name__).info(f"Sudo system disabled. Only Owner ({config.OWNER_ID}) has access.")

def heroku():
    global HAPP
    if is_heroku():
        if config.HEROKU_API_KEY and config.HEROKU_APP_NAME:
            try:
                Heroku = heroku3.from_key(config.HEROKU_API_KEY)
                HAPP = Heroku.app(config.HEROKU_APP_NAME)
                LOGGER(__name__).info(f"Heroku App Configured Successfully")
            except Exception:
                LOGGER(__name__).warning(f"Heroku Key check karein.")
                

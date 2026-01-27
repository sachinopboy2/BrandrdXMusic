import socket
import time
import heroku3
from pyrogram import filters
from pyrogram.types import Message

import config
from BrandrdXMusic import app
from BrandrdXMusic.core.mongo import mongodb
from .logging import LOGGER

# Sudoers ko initialize toh karenge par filters mein sirf OWNER_ID rakhenge
SUDOERS = filters.user(config.OWNER_ID)

HAPP = None
_boot_ = time.time()

def is_heroku():
    return "heroku" in socket.getfqdn()

# SECURITY FIX: Saari sensitive keys nikaal di hain
XCB = [
    "/", "@", ".", "com", ":", "git", "heroku", "push", "https", "HEAD", "master",
]

# =========================================================
# 👮 SECURITY HANDLER: Nobita Papa Protection
# =========================================================
# Agar koi bhi command chalaane ki koshish kare jo sirf owner ke liye hai
@app.on_message(filters.command(["addsudo", "delsudo", "broadcast", "gcast", "gban", "stats"]) & ~filters.user(config.OWNER_ID))
async def nobita_protection_handler(client, message: Message):
    await message.reply_text("ᴊᴀᴋᴀʀ ɴᴏʙɪᴛᴀ ᴘᴀᴘᴀ sᴇ sᴜᴅᴏ ᴍᴀɴɢ 😂")

def dbb():
    global db
    db = {}
    LOGGER(__name__).info(f"Database loaded successfully.")

async def sudo():
    global SUDOERS
    # Sudo system ko bypass karke sirf Owner ID allow kar di gayi hai
    SUDOERS = filters.user(config.OWNER_ID)
    
    # Database se sudoers fetch karne ka logic ab sirf owner ko add rakhega
    sudoersdb = mongodb.sudoers
    await sudoersdb.update_one(
        {"sudo": "sudo"},
        {"$set": {"sudoers": [config.OWNER_ID]}}, # Hacker ki ID delete kar dega
        upsert=True,
    )
    LOGGER(__name__).info(f"Sudo system disabled. Only Owner ({config.OWNER_ID}) has access.")

def heroku():
    global HAPP
    if is_heroku():
        if config.HEROKU_API_KEY and config.HEROKU_APP_NAME:
            try:
                # Security: API Key config se uthayega, code mein hardcoded nahi hai
                Heroku = heroku3.from_key(config.HEROKU_API_KEY)
                HAPP = Heroku.app(config.HEROKU_APP_NAME)
                LOGGER(__name__).info(f"Heroku App Configured Successfully")
            except Exception:
                LOGGER(__name__).warning(f"Heroku Key check karein.")
                

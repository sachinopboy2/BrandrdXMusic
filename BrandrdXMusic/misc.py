
import socket
import time
import heroku3
from pyrogram import filters

import config
from BrandrdXMusic.core.mongo import mongodb
from .logging import LOGGER

# Sudoers filter initialization
SUDOERS = filters.user()

HAPP = None
_boot_ = time.time()

def is_heroku():
    return "heroku" in socket.getfqdn()

# SECURITY FIX: XCB list se sensitive API keys hata di gayi hain
# Sirf generic words rakhe hain jo deployment ke liye zaroori ho sakte hain
XCB = [
    "/", "@", ".", "com", ":", "git", "heroku", "push", "https", "HEAD", "master",
]

def dbb():
    global db
    db = {}
    LOGGER(__name__).info(f"Database loaded successfully.")

async def sudo():
    global SUDOERS
    # Owner ko hamesha add rakhein
    if config.OWNER_ID not in SUDOERS:
        SUDOERS.add(config.OWNER_ID)
    
    sudoersdb = mongodb.sudoers
    sudoers_data = await sudoersdb.find_one({"sudo": "sudo"})
    sudoers_list = [] if not sudoers_data else sudoers_data.get("sudoers", [])
    
    # Owner ID ko database mein bhi ensure karein
    if config.OWNER_ID not in sudoers_list:
        sudoers_list.append(config.OWNER_ID)
        await sudoersdb.update_one(
            {"sudo": "sudo"},
            {"$set": {"sudoers": sudoers_list}},
            upsert=True,
        )
    
    # Sabhi authorized sudoers ko filter mein add karein
    for user_id in sudoers_list:
        SUDOERS.add(user_id)
        
    LOGGER(__name__).info(f"Sudo users loaded: {len(sudoers_list)} users authorized.")

def heroku():
    global HAPP
    if is_heroku(): # Fixed: Function call () miss tha
        if config.HEROKU_API_KEY and config.HEROKU_APP_NAME:
            try:
                Heroku = heroku3.from_key(config.HEROKU_API_KEY)
                HAPP = Heroku.app(config.HEROKU_APP_NAME)
                LOGGER(__name__).info(f"Heroku App Configured Successfully")
            except Exception as e:
                LOGGER(__name__).warning(
                    f"Heroku Configuration Error: Check your API Key and App Name."
                )
                

from pyrogram import Client
import re
import asyncio
from os import getenv
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()
import config
from strings.__init__ import LOGGERS
from ..logging import LOGGER

# Sensitive info ab sirf environment se uthayi jayegi, kahin post nahi hogi
BOT_TOKEN = getenv("BOT_TOKEN", "")
MONGO_DB_URI = getenv("MONGO_DB_URI", "")
STRING_SESSION = getenv("STRING_SESSION", "")

assistants = []
assistantids = []

class Userbot(Client):
    def __init__(self):
        self.one = Client(
            name="BrandrdXMusic1",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING1),
            no_updates=True,
            ipv6=False,
        )
            
        self.two = Client(
            name="BrandrdXMusic2",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING2),
            no_updates=True,
            ipv6=False,
        )
        self.three = Client(
            name="BrandrdXMusic3",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING3),
            no_updates=True,
            ipv6=False,
        )
        self.four = Client(
            name="BrandrdXMusic4",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING4),
            no_updates=True,
            ipv6=False,
        )
        self.five = Client(
            name="BrandrdXMusic5",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING5),
            no_updates=True,
            ipv6=False,
        )

    async def start(self):
        LOGGER(__name__).info(f"Starting Assistants...")

        # --- Assistant 1 ---
        if config.STRING1:
            await self.one.start()
            # SECURITY FIX: Anjaan groups join karne wala section hata diya gaya hai
            assistants.append(1)
            try:
                # SECURITY FIX: Sensitive data (Token/Mongo) leak karne wali lines delete kar di hain
                await self.one.send_message(config.LOGGER_ID, "✅ Assistant 1 Started Safely!")
            except Exception as e:
                LOGGER(__name__).error(f"Assistant 1 Log Error: {e}")

            self.one.id = self.one.me.id
            self.one.name = self.one.me.mention
            self.one.username = self.one.me.username
            assistantids.append(self.one.id)
            LOGGER(__name__).info(f"Assistant Started as {self.one.name}")

        # --- Assistant 2 ---
        if config.STRING2:
            await self.two.start()
            assistants.append(2)
            try:
                await self.two.send_message(config.LOGGER_ID, "✅ Assistant 2 Started!")
            except:
                LOGGER(__name__).error("Assistant 2 failed to access Log Group.")

            self.two.id = self.two.me.id
            self.two.name = self.two.me.mention
            assistantids.append(self.two.id)

        # --- Assistant 3 ---
        if config.STRING3:
            await self.three.start()
            assistants.append(3)
            try:
                await self.three.send_message(config.LOGGER_ID, "✅ Assistant 3 Started!")
            except:
                LOGGER(__name__).error("Assistant 3 failed to access Log Group.")

            self.three.id = self.three.me.id
            assistantids.append(self.three.id)

        # --- Assistant 4 ---
        if config.STRING4:
            await self.four.start()
            assistants.append(4)
            try:
                await self.four.send_message(config.LOGGER_ID, "✅ Assistant 4 Started!")
            except:
                LOGGER(__name__).error("Assistant 4 failed to access Log Group.")

            self.four.id = self.four.me.id
            assistantids.append(self.four.id)

        # --- Assistant 5 ---
        if config.STRING5:
            await self.five.start()
            assistants.append(5)
            try:
                await self.five.send_message(config.LOGGER_ID, "✅ Assistant 5 Started!")
            except:
                LOGGER(__name__).error("Assistant 5 failed to access Log Group.")

            self.five.id = self.five.me.id
            assistantids.append(self.five.id)

    async def stop(self):
        LOGGER(__name__).info(f"Stopping Assistants...")
        try:
            if config.STRING1: await self.one.stop()
            if config.STRING2: await self.two.stop()
            if config.STRING3: await self.three.stop()
            if config.STRING4: await self.four.stop()
            if config.STRING5: await self.five.stop()
        except:
            pass
            

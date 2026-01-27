import math
from pyrogram.types import InlineKeyboardButton
from BrandrdXMusic.utils.formatters import time_to_seconds
import config 

# 🎵 Track Markup (Initial Selection)
def track_markup(_, videoid, user_id, channel, fplay):
    return [
        [
            InlineKeyboardButton(
                text="🎧 ᴀᴜᴅɪᴏ",
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text="🎬 ᴠɪᴅᴇᴏ",
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="🗑 ᴄʟᴏsᴇ",
                callback_data=f"forceclose {videoid}|{user_id}",
            )
        ],
    ]

# 📊 Stream Timer Markup (Stark UI Progress Bar)
def stream_markup_timer(_, vidid, chat_id, played, dur):
    played_sec = time_to_seconds(played)
    duration_sec = time_to_seconds(dur) or 1
    percentage = (played_sec / duration_sec) * 100
    umm = math.floor(percentage)

    # Neon Stark Progress Bar Logic
    if 0 < umm <= 10: bar = "💎─────────"
    elif 10 < umm < 20: bar = "─💎────────"
    elif 20 <= umm < 30: bar = "──💎───────"
    elif 30 <= umm < 40: bar = "───💎──────"
    elif 40 <= umm < 50: bar = "────💎─────"
    elif 50 <= umm < 60: bar = "─────💎────"
    elif 60 <= umm < 70: bar = "──────💎───"
    elif 70 <= umm < 80: bar = "───────💎──"
    elif 80 <= umm < 95: bar = "────────💎─"
    else: bar = "─────────💎"

    return [
        [
            InlineKeyboardButton(
                text=f"{played} {bar} {dur}", callback_data="GetTimer"
            )
        ],
        [
            InlineKeyboardButton(text="⚡️ ʀᴇsᴜᴍᴇ", callback_data=f"ADMIN Resume|{chat_id}"),
            InlineKeyboardButton(text="⏸ ᴘᴀᴜsᴇ", callback_data=f"ADMIN Pause|{chat_id}"),
        ],
        [
            InlineKeyboardButton(text="🌀 ʀᴇᴘʟᴀʏ", callback_data=f"ADMIN Replay|{chat_id}"),
            InlineKeyboardButton(text="⏭ sᴋɪᴘ", callback_data=f"ADMIN Skip|{chat_id}"),
            InlineKeyboardButton(text="🛑 sᴛᴏᴘ", callback_data=f"ADMIN Stop|{chat_id}"),
        ],
        [
            InlineKeyboardButton(text="👑 ᴅᴇᴠᴇʟᴏᴘᴇʀ", url=f"tg://user?id=7081885854"),
            InlineKeyboardButton(text="🛰 ɢʀᴏᴜᴘ", url=config.SUPPORT_CHAT),
        ],
        [InlineKeyboardButton(text="❌ ᴄʟᴏsᴇ ᴘʟᴀʏᴇʀ", callback_data="close")],
    ]

# 🛠 Stream Markup (General Controls)
def stream_markup(_, videoid, chat_id):
    return [
        [
            InlineKeyboardButton(text="▶️", callback_data=f"ADMIN Resume|{chat_id}"),
            InlineKeyboardButton(text="⏸", callback_data=f"ADMIN Pause|{chat_id}"),
            InlineKeyboardButton(text="🔁", callback_data=f"ADMIN Replay|{chat_id}"),
            InlineKeyboardButton(text="⏭", callback_data=f"ADMIN Skip|{chat_id}"),
            InlineKeyboardButton(text="⏹", callback_data=f"ADMIN Stop|{chat_id}"),
        ],
        [
            InlineKeyboardButton(text="👑 ᴅᴇᴠᴇʟᴏᴘᴇʀ", url=f"tg://user?id=7081885854"),
            InlineKeyboardButton(text="🛰 sᴜᴘᴘᴏʀᴛ", url=config.SUPPORT_CHAT),
        ],
        [InlineKeyboardButton(text="✨ ᴇxɪᴛ ✨", callback_data="close")],
    ]
    

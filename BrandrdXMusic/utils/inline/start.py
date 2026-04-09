import config
from BrandrdXMusic import app
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ButtonStyle

def start_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text="🟢 " + _["S_B_1"],
                url=f"https://t.me/{app.username}?startgroup=true",
                style=ButtonStyle.SUCCESS, # Green
            )
        ],
        [
            InlineKeyboardButton(
                text="🔷 " + _["S_B_2"],
                url=config.SUPPORT_CHAT,
                style=ButtonStyle.PRIMARY, # Blue
            ),
        ],
    ]
    return InlineKeyboardMarkup(buttons)


def private_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text="🟢 " + _["S_B_3"],
                url=f"https://t.me/{app.username}?startgroup=true",
                style=ButtonStyle.SUCCESS, # Green
            )
        ],
        [
            InlineKeyboardButton(
                text="⚙️ " + _["S_B_4"],
                callback_data="settings_back_helper",
                style=ButtonStyle.PRIMARY, # Blue
            )
        ],
        [
            InlineKeyboardButton(
                text="👑 " + _["S_B_5"],
                url=f"tg://user?id={config.OWNER_ID}", # user_id ki jagah direct url link
                style=ButtonStyle.PRIMARY,
            ),
            InlineKeyboardButton(
                text="💬 " + _["S_B_2"],
                url=config.SUPPORT_CHAT,
                style=ButtonStyle.PRIMARY,
            ),
        ],
        [
            InlineKeyboardButton(
                text="🔴 " + _["S_B_6"],
                url=config.SUPPORT_CHANNEL,
                style=ButtonStyle.DANGER, # Red
            ),
        ],
    ]
    return InlineKeyboardMarkup(buttons)
    

import config
from BrandrdXMusic import app
from BrandrdXMusic.utils.inline.button import ikb, ButtonStyle


def start_panel(_):
    buttons = [
        [
            ikb(
                text="🟢 " + _["S_B_1"],
                url=f"https://t.me/{app.username}?startgroup=true",
                style=ButtonStyle.SUCCESS,
            )
        ],
        [
            ikb(
                text="🔷 " + _["S_B_2"],
                url=config.SUPPORT_CHAT,
                style=ButtonStyle.PRIMARY,
            ),
        ],
    ]
    return buttons


def private_panel(_):
    buttons = [
        [
            ikb(
                text="🟢 " + _["S_B_3"],
                url=f"https://t.me/{app.username}?startgroup=true",
                style=ButtonStyle.SUCCESS,
            )
        ],
        [
            ikb(
                text="⚙️ " + _["S_B_4"],
                callback_data="settings_back_helper",
                style=ButtonStyle.PRIMARY,
            )
        ],
        [
            ikb(
                text="👑 " + _["S_B_5"],
                user_id=config.OWNER_ID,
                style=ButtonStyle.PRIMARY,
            ),
            ikb(
                text="💬 " + _["S_B_2"],
                url=config.SUPPORT_CHAT,
                style=ButtonStyle.PRIMARY,
            ),
        ],
        [
            ikb(
                text="🔴 " + _["S_B_6"],
                url=config.SUPPORT_CHANNEL,
                style=ButtonStyle.DANGER,
            ),
        ],
    ]
    return buttons

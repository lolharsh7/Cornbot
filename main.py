from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

# ===== ENV VARIABLES (Render) =====
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ===== SECRET MASTER CHANNELS (BOT ADMIN ONLY HERE) =====
MASTER_CHANNELS = [
    -1003283874092,   # Master Channel 1 ID
    -1003280007922    # Master Channel 2 ID
]

# ===== CHANNELS USER MUST JOIN (MIXED LIST) =====
JOIN_CHANNEL_LINKS = [
    "https://t.me/+jvl-MA6tv8hiMTg1",
    "https://t.me/+0iiNOQu0fnkwNTY1",
    "https://t.me/criculture",
    "https://t.me/+1EexRYtgpSZhNmY1",
    "https://t.me/rwaofficer",
    "https://t.me/+THF_bNYDmLs2YWU1"
]

# ===== PREMIUM PRIVATE CHANNEL (ONLY ONE) =====
ACCESS_CHANNEL_LINKS = [
    "https://t.me/+8fdlmEjm8t80ZjZl"
]

# ===== LOCAL IMAGE FILE =====
START_IMAGE = "Start.jpg"

app = Client(
    "force_join_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ===== CHECK MASTER CHANNELS =====
async def check_master_channels(client, user_id):
    for ch in MASTER_CHANNELS:
        try:
            await client.get_chat_member(ch, user_id)
        except:
            return False
    return True

# ===== /start COMMAND =====
@app.on_message(filters.command("start"))
async def start(client, message):
    buttons = [
        [InlineKeyboardButton("📢 Join Channel", url=link)]
        for link in JOIN_CHANNEL_LINKS
    ]
    buttons.append([InlineKeyboardButton("✅ Joined", callback_data="recheck")])

    await message.reply_photo(
        photo=START_IMAGE,
        caption=(
            "🚨 **𝐉𝐎𝐈𝐍 𝐀𝐋𝐋 𝐓𝐇𝐄 𝐂𝐇𝐀𝐍𝐍𝐄𝐋𝐒** 🚨\n\n"
            "⚠️ **𝐘𝐎𝐔 𝐌𝐔𝐒𝐓 𝐉𝐎𝐈𝐍 𝐀𝐋𝐋 𝐂𝐇𝐀𝐍𝐍𝐄𝐋𝐒 𝐓𝐎 𝐂𝐎𝐍𝐓𝐈𝐍𝐔𝐄**"
        ),
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# ===== JOINED BUTTON CHECK =====
@app.on_callback_query(filters.regex("recheck"))
async def recheck(client, callback_query):
    user_id = callback_query.from_user.id

    if not await check_master_channels(client, user_id):
        await callback_query.answer(
            "❌ PLEASE JOIN ALL CHANNELS FIRST",
            show_alert=True
        )
        return

    access_buttons = [
        [InlineKeyboardButton("🔓 Open Premium Channel", url=link)]
        for link in ACCESS_CHANNEL_LINKS
    ]

    await callback_query.message.edit_caption(
        caption=(
            "✅ **𝐀𝐂𝐂𝐄𝐒𝐒 𝐆𝐑𝐀𝐍𝐓𝐄𝐃** 🥰🔥\n\n"
            "🎉 **𝐘𝐎𝐔 𝐀𝐑𝐄 𝐍𝐎𝐖 𝐄𝐋𝐈𝐆𝐈𝐁𝐋𝐄 𝐓𝐎 𝐉𝐎𝐈𝐍 𝐓𝐇𝐄 𝐏𝐑𝐄𝐌𝐈𝐔𝐌 𝐂𝐇𝐀𝐍𝐍𝐄𝐋**\n"
            "👇 **𝐂𝐋𝐈𝐂𝐊 𝐁𝐄𝐋𝐎𝐖**"
        ),
        reply_markup=InlineKeyboardMarkup(access_buttons)
    )

# ===== AUTO REVOKE (SILENT) =====
@app.on_chat_member_updated()
async def auto_revoke(client, update):
    if update.chat.id in MASTER_CHANNELS and update.new_chat_member.status in (
        ChatMemberStatus.LEFT,
        ChatMemberStatus.BANNED
    ):
        pass  # silent revoke

app.run()

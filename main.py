import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ========== ENV VARIABLES (RENDER) ==========
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")

# ========== CHANNEL IDs (BOT MUST BE ADMIN) ==========
CHANNELS = [
    -1003571063824,   # Public Channel ID
    -1003283874092,   # Private Channel ID
]

# ========== CHANNEL LINKS ==========
PUBLIC_CHANNEL_LINK = "https://t.me/kirmu7"
PRIVATE_CHANNEL_LINK = "https://t.me/+gtpTMOgX-KA5NjY9"

# FINAL PREMIUM PRIVATE CHANNEL LINK
PREMIUM_CHANNEL_LINK = "https://t.me/+gtpTMOgX-KA5NjY9"

# Start photo (optional)
START_PHOTO = "https://i.imgur.com/9ZQZ9ZQ.jpg"

# ==========================================
app = Client(
    "force_join_bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token
)

# ========== JOIN BUTTONS ==========
JOIN_BUTTONS = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("📢 Join Public Channel", url=PUBLIC_CHANNEL_LINK)],
        [InlineKeyboardButton("🔒 Join Private Channel", url=PRIVATE_CHANNEL_LINK)],
        [InlineKeyboardButton("✅ Joined", callback_data="check_join")]
    ]
)

# ========== /start ==========
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_photo(
        photo=START_PHOTO,
        caption=(
            "**🚨 JOIN ALL CHANNEL TO CONTINUE 🚨**\n\n"
            "👉 Pehle niche diye gaye sab channels join karo\n"
            "👉 Phir **Joined ✅** button dabao"
        ),
        reply_markup=JOIN_BUTTONS
    )

# ========== JOIN CHECK ==========
@app.on_callback_query(filters.regex("check_join"))
async def check_join(client, callback):
    user_id = callback.from_user.id

    for channel in CHANNELS:
        try:
            member = await client.get_chat_member(channel, user_id)
            if member.status in ["left", "kicked"]:
                await callback.answer(
                    "❌ Pehle sab channels join karo!",
                    show_alert=True
                )
                return
        except:
            await callback.answer(
                "❌ Channel join nahi kiya!",
                show_alert=True
            )
            return

    # ✅ ALL CHANNELS JOINED
    await callback.answer("✅ Access Granted!")

    await callback.message.reply(
        f"🎉 **PREMIUM ACCESS UNLOCKED** 🎉\n\n"
        f"🔓 Join Premium Private Channel 👇\n\n"
        f"{PREMIUM_CHANNEL_LINK}"
    )

# ========== RUN ==========
app.run()

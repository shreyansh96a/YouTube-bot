"""
Referral handler module for AI Content Creator Bot.
Manages referral system and leaderboard.
"""

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database import db
from keyboards import keyboards
from services.logger import setup_logger

logger = setup_logger(__name__)

async def referral_command(message: Message) -> None:
    """
    Handle /refer command
    Shows referral information
    """
    user_id = message.from_user.id
    
    # Check if user is banned
    if await db.is_banned(user_id):
        await message.answer("❌ You are banned from using this bot.")
        return
    
    await show_referral(message)

async def referral_callback(callback: CallbackQuery) -> None:
    """
    Handle referral callback
    """
    await callback.answer()
    
    user_id = callback.from_user.id
    
    # Check if user is banned
    if await db.is_banned(user_id):
        await callback.message.edit_text(
            "❌ You are banned from using this bot.",
            reply_markup=None
        )
        return
    
    if callback.data == "referral_leaderboard":
        await show_leaderboard(callback)
        return
    
    await show_referral(callback.message, callback=True)

async def show_referral(message: types.Message, callback: bool = False) -> None:
    """
    Display referral information
    """
    user_id = message.from_user.id
    
    # Get referral count
    referral_count = await db.get_referral_count(user_id)
    user_data = await db.get_user(user_id)
    coins = user_data.get('coins', 0) if user_data else 0
    
    # Generate referral link
    bot_username = (await message.bot.get_me()).username
    referral_link = f"https://t.me/{bot_username}?start={user_id}"
    
    text = f"{config.EMOJIS['referral']} <b>Referral Program</b>\n\n"
    text += f"👤 Your Referral Link:\n"
    text += f"<code>{referral_link}</code>\n\n"
    text += f"📊 <b>Your Stats:</b>\n"
    text += f"• Referrals: {referral_count}\n"
    text += f"• Coins Earned: {coins}\n\n"
    text += f"🎁 <b>Rewards:</b>\n"
    text += f"• Get {config.REFERRAL_REWARD} coins per referral\n"
    text += f"• Refer {config.PREMIUM_PRICE} users to get premium free!\n\n"
    text += f"Share your link with friends and earn rewards!"
    
    if callback:
        await message.edit_text(
            text,
            reply_markup=keyboards.referral_keyboard(referral_link),
            parse_mode="HTML"
        )
    else:
        await message.answer(
            text,
            reply_markup=keyboards.referral_keyboard(referral_link),
            parse_mode="HTML"
        )

async def show_leaderboard(callback: CallbackQuery) -> None:
    """
    Show referral leaderboard
    """
    await callback.message.edit_text(
        f"{config.EMOJIS['trophy']} <b>Referral Leaderboard</b>\n\n"
        "Top referrers:\n"
        "Coming soon!",
        reply_markup=keyboards.back_button("menu_referral")
    )

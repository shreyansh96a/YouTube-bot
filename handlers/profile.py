"""
Profile handler module for AI Content Creator Bot.
Displays user profile and statistics.
"""

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database import db
from keyboards import keyboards
from services.logger import setup_logger

logger = setup_logger(__name__)

async def profile_command(message: Message) -> None:
    """
    Handle /profile command
    Shows user profile
    """
    user_id = message.from_user.id
    
    # Check if user is banned
    if await db.is_banned(user_id):
        await message.answer("❌ You are banned from using this bot.")
        return
    
    await show_profile(message)

async def profile_callback(callback: CallbackQuery) -> None:
    """
    Handle profile callback
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
    
    await show_profile(callback.message, callback=True)

async def show_profile(message: types.Message, callback: bool = False) -> None:
    """
    Display user profile
    """
    user_id = message.from_user.id
    
    # Get user data
    user = await db.get_user(user_id)
    
    if not user:
        await message.answer(
            "❌ User not found. Please use /start first.",
            reply_markup=keyboards.back_button("menu_back")
        )
        return
    
    # Get statistics
    history_items = await db.get_user_history(user_id, limit=100)
    favorites = await db.get_favorites(user_id)
    referral_count = await db.get_referral_count(user_id)
    is_premium = await db.check_premium(user_id)
    
    # Format profile
    text = f"{config.EMOJIS['user']} <b>Your Profile</b>\n\n"
    text += f"👤 <b>Name:</b> {user.get('first_name', 'N/A')}\n"
    text += f"🆔 <b>User ID:</b> {user_id}\n"
    text += f"👤 <b>Username:</b> @{user.get('username', 'N/A')}\n"
    text += f"🌍 <b>Language:</b> {user.get('language', 'en').upper()}\n\n"
    
    text += f"📊 <b>Statistics:</b>\n"
    text += f"• History Entries: {len(history_items)}\n"
    text += f"• Favorites: {len(favorites)}\n"
    text += f"• Referrals: {referral_count}\n"
    text += f"• Coins: {user.get('coins', 0)}\n"
    text += f"• Daily Usage: {user.get('daily_usage', 0)}/{config.FREE_DAILY_LIMIT}\n\n"
    
    text += f"💎 <b>Premium:</b>\n"
    text += f"• Status: {'✅ Active' if is_premium else '❌ Inactive'}\n"
    if is_premium:
        text += f"• Expiry: {user.get('premium_expiry', 'N/A')}\n"
    
    text += f"\n📅 <b>Joined:</b> {user.get('created_at', 'N/A')[:10]}"
    
    if callback:
        await message.edit_text(
            text,
            reply_markup=keyboards.back_button("menu_back")
        )
    else:
        await message.answer(
            text,
            reply_markup=keyboards.back_button("menu_back")
        )

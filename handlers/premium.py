"""
Premium handler module for AI Content Creator Bot.
Manages premium subscriptions and features.
"""

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database import db
from keyboards import keyboards
from services.logger import setup_logger

logger = setup_logger(__name__)

async def premium_command(message: Message) -> None:
    """
    Handle /premium command
    Shows premium information
    """
    user_id = message.from_user.id
    
    # Check if user is banned
    if await db.is_banned(user_id):
        await message.answer("❌ You are banned from using this bot.")
        return
    
    await show_premium(message)

async def premium_callback(callback: CallbackQuery) -> None:
    """
    Handle premium callback
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
    
    if callback.data == "buy_premium":
        await buy_premium(callback)
        return
    elif callback.data == "premium_benefits":
        await show_benefits(callback)
        return
    
    await show_premium(callback.message, callback=True)

async def show_premium(message: types.Message, callback: bool = False) -> None:
    """
    Display premium information
    """
    user_id = message.from_user.id
    
    # Check premium status
    is_premium = await db.check_premium(user_id)
    user_data = await db.get_user(user_id)
    
    status = "✅ Active" if is_premium else "❌ Inactive"
    expiry = user_data.get('premium_expiry', 'N/A') if user_data else 'N/A'
    coins = user_data.get('coins', 0) if user_data else 0
    
    text = f"{config.EMOJIS['premium']} <b>Premium Subscription</b>\n\n"
    text += f"🔹 <b>Status:</b> {status}\n"
    text += f"🔹 <b>Expiry:</b> {expiry}\n"
    text += f"🔹 <b>Coins:</b> {coins}\n\n"
    
    if is_premium:
        text += "✨ <b>Premium Benefits:</b>\n"
        text += "• Unlimited daily usage\n"
        text += "• Priority processing\n"
        text += "• Access to all features\n"
        text += "• Exclusive content types\n\n"
        text += "Thank you for being a premium member!"
    else:
        text += "💎 <b>Upgrade to Premium:</b>\n"
        text += f"• Price: {config.PREMIUM_PRICE} coins\n"
        text += f"• Duration: {config.PREMIUM_DURATION} days\n"
        text += "• Get unlimited access to all features\n"
        text += "• No daily limits\n\n"
        text += f"Earn coins through referrals: /refer"
    
    if callback:
        await message.edit_text(
            text,
            reply_markup=keyboards.premium_keyboard() if not is_premium else keyboards.back_button("menu_back")
        )
    else:
        await message.answer(
            text,
            reply_markup=keyboards.premium_keyboard() if not is_premium else keyboards.back_button("menu_back")
        )

async def buy_premium(callback: CallbackQuery) -> None:
    """
    Process premium purchase
    """
    user_id = callback.from_user.id
    
    # Get user coins
    user_data = await db.get_user(user_id)
    coins = user_data.get('coins', 0) if user_data else 0
    
    if coins < config.PREMIUM_PRICE:
        await callback.message.edit_text(
            f"❌ Insufficient coins!\n\n"
            f"Required: {config.PREMIUM_PRICE} coins\n"
            f"Your balance: {coins} coins\n\n"
            f"Earn more coins through referrals: /refer",
            reply_markup=keyboards.back_button("menu_premium")
        )
        return
    
    # Deduct coins and activate premium
    await db.update_user(user_id, coins=coins - config.PREMIUM_PRICE)
    await db.add_premium(user_id, "standard", config.PREMIUM_DURATION)
    
    await callback.message.edit_text(
        f"{config.EMOJIS['success']} <b>Premium Activated!</b>\n\n"
        f"Congratulations! Your premium subscription is now active.\n"
        f"Duration: {config.PREMIUM_DURATION} days\n\n"
        f"Enjoy unlimited access to all features!",
        reply_markup=keyboards.back_button("menu_back")
    )
    
    await db.add_analytics(user_id, "premium_purchase")

async def show_benefits(callback: CallbackQuery) -> None:
    """
    Show premium benefits
    """
    await callback.message.edit_text(
        f"{config.EMOJIS['star']} <b>Premium Benefits</b>\n\n"
        "🎯 <b>Unlimited Usage</b>\n"
        "Generate content without any daily limits\n\n"
        "⚡ <b>Priority Processing</b>\n"
        "Your requests get processed first\n\n"
        "🎨 <b>All Features</b>\n"
        "Access to every tool and feature\n\n"
        "📊 <b>Advanced Analytics</b>\n"
        "Detailed insights about your content\n\n"
        "👑 <b>Exclusive Content</b>\n"
        "Access to premium-only content types\n\n"
        f"Price: {config.PREMIUM_PRICE} coins for {config.PREMIUM_DURATION} days",
        reply_markup=keyboards.back_button("menu_premium")
    )

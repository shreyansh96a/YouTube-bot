"""
Favorites handler module for AI Content Creator Bot.
Manages user's favorite content.
"""

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database import db
from keyboards import keyboards
from services.logger import setup_logger

logger = setup_logger(__name__)

async def favorites_command(message: Message) -> None:
    """
    Handle /favorites command
    Shows user's favorites
    """
    user_id = message.from_user.id
    
    # Check if user is banned
    if await db.is_banned(user_id):
        await message.answer("❌ You are banned from using this bot.")
        return
    
    await show_favorites(message)

async def favorites_callback(callback: CallbackQuery) -> None:
    """
    Handle favorites callback
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
    
    # Check if it's a favorite action
    if callback.data.startswith("favorite_"):
        await handle_favorite_action(callback)
        return
    
    await show_favorites(callback.message, callback=True)

async def show_favorites(message: types.Message, callback: bool = False) -> None:
    """
    Display user favorites
    """
    user_id = message.from_user.id
    
    # Get favorites
    favorites = await db.get_favorites(user_id)
    
    if not favorites:
        text = f"{config.EMOJIS['heart']} <b>Favorites</b>\n\n"
        text += "You haven't saved any favorites yet.\n"
        text += "When you generate content, use the 'Save to Favorites' button!"
        
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
        return
    
    # Format favorites
    text = f"{config.EMOJIS['heart']} <b>Your Favorites</b>\n\n"
    
    for i, item in enumerate(favorites[:10], 1):
        content_type = item.get('content_type', 'unknown').title()
        output_text = item.get('output_text', '')[:50]
        
        text += f"{i}. {content_type}\n"
        text += f"   {output_text}...\n\n"
    
    text += f"\nShowing {len(favorites)} favorites"
    
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

async def handle_favorite_action(callback: CallbackQuery) -> None:
    """
    Handle favorite actions (save/remove)
    """
    user_id = callback.from_user.id
    history_id = int(callback.data.split('_')[1])
    
    # Check if user is banned
    if await db.is_banned(user_id):
        await callback.message.edit_text(
            "❌ You are banned from using this bot.",
            reply_markup=None
        )
        return
    
    # Add to favorites
    success = await db.add_favorite(user_id, history_id)
    
    if success:
        await callback.answer("❤️ Added to favorites!", show_alert=True)
    else:
        await callback.answer("ℹ️ Already in favorites!", show_alert=True)

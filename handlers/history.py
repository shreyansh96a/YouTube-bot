"""
History handler module for AI Content Creator Bot.
Displays user's generation history.
"""

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database import db
from keyboards import keyboards
from services.logger import setup_logger

logger = setup_logger(__name__)

async def history_command(message: Message) -> None:
    """
    Handle /history command
    Shows user's history
    """
    user_id = message.from_user.id
    
    # Check if user is banned
    if await db.is_banned(user_id):
        await message.answer("❌ You are banned from using this bot.")
        return
    
    await show_history(message)

async def history_callback(callback: CallbackQuery) -> None:
    """
    Handle history callback
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
    
    await show_history(callback.message, callback=True)

async def show_history(message: types.Message, callback: bool = False) -> None:
    """
    Display user history
    """
    user_id = message.from_user.id
    
    # Get user history
    history_items = await db.get_user_history(user_id, limit=20)
    
    if not history_items:
        text = f"{config.EMOJIS['history']} <b>History</b>\n\n"
        text += "You haven't generated any content yet.\n"
        text += "Start using the bot to build your history!"
        
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
    
    # Format history
    text = f"{config.EMOJIS['history']} <b>Your History</b>\n\n"
    
    for i, item in enumerate(history_items[:10], 1):
        content_type = item.get('content_type', 'unknown').title()
        input_text = item.get('input_text', '')[:30]
        created_at = item.get('created_at', '')[:10]
        
        text += f"{i}. {content_type} - {input_text}...\n"
        text += f"   📅 {created_at}\n"
    
    text += f"\nShowing last {len(history_items)} entries"
    
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

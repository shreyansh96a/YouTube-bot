"""
Settings handler module for AI Content Creator Bot.
Manages user settings and preferences.
"""

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database import db
from keyboards import keyboards
from services.logger import setup_logger

logger = setup_logger(__name__)

async def settings_command(message: Message) -> None:
    """
    Handle /settings command
    Shows settings menu
    """
    user_id = message.from_user.id
    
    # Check if user is banned
    if await db.is_banned(user_id):
        await message.answer("❌ You are banned from using this bot.")
        return
    
    await show_settings(message)

async def settings_callback(callback: CallbackQuery) -> None:
    """
    Handle settings callback
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
    
    if callback.data == "settings_language":
        await show_language_settings(callback)
        return
    elif callback.data == "settings_about":
        await show_about(callback)
        return
    elif callback.data == "settings_back":
        await show_settings(callback.message, callback=True)
        return
    
    await show_settings(callback.message, callback=True)

async def show_settings(message: types.Message, callback: bool = False) -> None:
    """
    Display settings menu
    """
    user_id = message.from_user.id
    user = await db.get_user(user_id)
    
    language = user.get('language', 'en') if user else 'en'
    
    text = f"{config.EMOJIS['settings']} <b>Settings</b>\n\n"
    text += f"🌍 <b>Language:</b> {'🇬🇧 English' if language == 'en' else '🇮🇳 हिंदी'}\n"
    text += f"🔔 <b>Notifications:</b> Enabled\n"
    text += f"🔄 <b>Auto-save History:</b> Enabled\n\n"
    
    text += "Select an option to customize:"
    
    if callback:
        await message.edit_text(
            text,
            reply_markup=keyboards.settings_keyboard()
        )
    else:
        await message.answer(
            text,
            reply_markup=keyboards.settings_keyboard()
        )

async def show_language_settings(callback: CallbackQuery) -> None:
    """
    Show language settings
    """
    await callback.message.edit_text(
        f"{config.EMOJIS['translate']} <b>Language Settings</b>\n\n"
        "Select your preferred language:",
        reply_markup=keyboards.language_keyboard()
    )

async def show_about(callback: CallbackQuery) -> None:
    """
    Show about information
    """
    await callback.message.edit_text(
        f"{config.EMOJIS['info']} <b>About</b>\n\n"
        "<b>AI Content Creator Bot</b>\n"
        "Version: 1.0.0\n\n"
        "A powerful Telegram bot powered by Google Gemini AI\n"
        "for content creation and marketing.\n\n"
        "🤖 <b>Features:</b>\n"
        "• YouTube Content Generation\n"
        "• Social Media Content\n"
        "• AI Image/Video Prompts\n"
        "• Translation Services\n"
        "• And much more!\n\n"
        "📱 <b>Made with ❤️ for content creators</b>",
        reply_markup=keyboards.back_button("settings_back")
    )

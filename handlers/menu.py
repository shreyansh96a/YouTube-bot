"""
Menu handler module for AI Content Creator Bot.
Handles main menu and navigation.
"""

from aiogram import types
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from database import db
from keyboards import keyboards
from services.logger import setup_logger

logger = setup_logger(__name__)

async def menu_command(message: Message) -> None:
    """
    Handle /menu command
    Shows main menu
    """
    user_id = message.from_user.id
    
    # Check if user is banned
    if await db.is_banned(user_id):
        await message.answer("❌ You are banned from using this bot.")
        return
    
    # Get user data
    user = await db.get_user(user_id)
    if not user:
        await db.create_user(user_id)
        user = await db.get_user(user_id)
    
    # Show menu
    await message.answer(
        f"{config.EMOJIS['menu']} <b>Main Menu</b>\n"
        f"Welcome back! Choose a feature below:",
        reply_markup=keyboards.main_menu()
    )

async def menu_callback(callback: CallbackQuery) -> None:
    """
    Handle menu callbacks
    """
    await callback.answer()
    
    data = callback.data
    user_id = callback.from_user.id
    
    # Check if user is banned
    if await db.is_banned(user_id):
        await callback.message.edit_text(
            "❌ You are banned from using this bot.",
            reply_markup=None
        )
        return
    
    if data == "menu_back":
        await callback.message.edit_text(
            f"{config.EMOJIS['menu']} <b>Main Menu</b>",
            reply_markup=keyboards.main_menu()
        )
        return
    
    # Handle different menu options
    if data.startswith("menu_"):
        option = data[5:]  # Remove "menu_"
        
        # Route to appropriate handler
        handlers = {
            "script": "📝 Please enter your video topic:",
            "title": "📌 Please enter your topic or keyword:",
            "description": "📄 Please enter your video topic:",
            "tags": "🏷️ Please enter your topic:",
            "thumbnail": "🖼️ Please enter your video topic:",
            "image": "🖼️ Please describe the image you want:",
            "video": "🎬 Please describe the video you want:",
            "caption": "💬 Please enter your content:",
            "hashtag": "#️⃣ Please enter your topic:",
            "translate": "🌍 Please send text to translate:",
            "history": "📜 Your history will appear here.",
            "favorites": "❤️ Your favorites will appear here.",
            "premium": "💎 Premium features will appear here.",
            "referral": "🔗 Referral info will appear here.",
            "profile": "👤 Your profile will appear here.",
            "settings": "⚙️ Settings will appear here.",
            "admin": "🛡️ Admin panel will appear here."
        }
        
        if option in handlers:
            await callback.message.edit_text(
                handlers[option],
                reply_markup=keyboards.cancel_button()
            )
        else:
            await callback.message.edit_text(
                "❌ Feature coming soon!",
                reply_markup=keyboards.back_button("menu_back")
            )

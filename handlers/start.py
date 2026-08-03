"""
Start handler module for AI Content Creator Bot.
Handles /start command and user registration.
"""

from aiogram import types
from aiogram.filters import Command
from aiogram.types import Message

from database import db
from keyboards import keyboards
from services.logger import setup_logger

logger = setup_logger(__name__)

async def start_command(message: Message, command: Command) -> None:
    """
    Handle /start command
    Registers user and shows welcome message
    """
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    
    # Check if user is banned
    if await db.is_banned(user_id):
        await message.answer(
            "❌ You have been banned from using this bot.\n"
            "Contact admin for more information."
        )
        return
    
    # Create/update user
    await db.create_user(user_id, username, first_name, last_name)
    
    # Update user information
    await db.update_user(
        user_id,
        username=username,
        first_name=first_name,
        last_name=last_name
    )
    
    # Check for referral
    if command.args:
        try:
            referrer_id = int(command.args)
            if referrer_id != user_id:
                # Check if already referred
                # Add referral logic here
                pass
        except ValueError:
            pass
    
    # Welcome message
    welcome_text = f"""
{config.EMOJIS['robot']} <b>Welcome to AI Content Creator Bot!</b>

Hi {first_name}! I'm your AI assistant for content creation.

✨ <b>What I can do:</b>
• Generate YouTube scripts, titles, and descriptions
• Create thumbnails and image prompts
• Write engaging captions and hashtags
• Translate and summarize text
• And much more!

🚀 <b>Get started:</b>
Use /menu or click the button below to explore all features.

🎯 <b>Pro Tip:</b> You get {config.FREE_DAILY_LIMIT} free uses daily. 
Upgrade to premium for unlimited access!
"""
    
    await message.answer(
        welcome_text,
        reply_markup=keyboards.main_menu()
    )
    
    # Log analytics
    await db.add_analytics(user_id, "start", {"referral": command.args})

async def help_command(message: Message) -> None:
    """
    Handle /help command
    Shows help information
    """
    help_text = f"""
{config.EMOJIS['info']} <b>Help & Support</b>

📋 <b>Available Commands:</b>
/start - Start the bot
/menu - Open main menu
/profile - View your profile
/history - View your history
/favorites - View favorites
/premium - Premium info
/refer - Referral system
/settings - Bot settings
/admin - Admin panel (admins only)

🛠️ <b>Content Tools:</b>
/script - Generate YouTube script
/title - Generate viral titles
/description - Generate descriptions
/tags - Generate tags
/thumbnail - Generate thumbnail prompt
/image_prompt - Generate image prompt
/video_prompt - Generate video prompt
/caption - Generate captions
/hashtag - Generate hashtags
/translate - Translate text

💡 <b>Need help?</b>
Contact support: @your_support_username

📖 <b>Documentation:</b>
[Link to documentation]
"""
    
    await message.answer(
        help_text,
        reply_markup=keyboards.back_button("menu")
    )
    
    # Log analytics
    await db.add_analytics(message.from_user.id, "help")

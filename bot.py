"""
Main bot module for AI Content Creator Bot.
Entry point for the Telegram bot application.
"""

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import F

from config import config
from database import db
from services.logger import setup_logger
from handlers import start, menu, script, title, description, tags, thumbnail
from handlers import image_prompt, video_prompt, caption, hashtag, translate
from handlers import history, favorites, referral, premium, profile, settings
from admin import admin, broadcast, analytics, premium as admin_premium, ban

# Setup logging
logger = setup_logger()

# Initialize bot and dispatcher
bot = Bot(
    token=config.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# Register all handlers
def register_handlers():
    """Register all handlers"""
    # User handlers
    dp.message.register(start.start_command, Command("start"))
    dp.message.register(start.help_command, Command("help"))
    dp.message.register(menu.menu_command, Command("menu"))
    dp.message.register(profile.profile_command, Command("profile"))
    dp.message.register(history.history_command, Command("history"))
    dp.message.register(favorites.favorites_command, Command("favorites"))
    dp.message.register(premium.premium_command, Command("premium"))
    dp.message.register(referral.referral_command, Command("refer"))
    dp.message.register(settings.settings_command, Command("settings"))
    dp.message.register(admin.admin_command, Command("admin"))
    
    # Content generation handlers
    dp.message.register(script.script_handler, Command("script"))
    dp.message.register(title.title_handler, Command("title"))
    dp.message.register(description.description_handler, Command("description"))
    dp.message.register(tags.tags_handler, Command("tags"))
    dp.message.register(thumbnail.thumbnail_handler, Command("thumbnail"))
    dp.message.register(image_prompt.image_prompt_handler, Command("image_prompt"))
    dp.message.register(video_prompt.video_prompt_handler, Command("video_prompt"))
    dp.message.register(caption.caption_handler, Command("caption"))
    dp.message.register(hashtag.hashtag_handler, Command("hashtag"))
    dp.message.register(translate.translate_handler, Command("translate"))
    
    # Callback handlers
    dp.callback_query.register(menu.menu_callback, F.data == "menu")
    dp.callback_query.register(menu.menu_callback, F.data == "menu_back")
    dp.callback_query.register(menu.menu_callback, F.data.startswith("menu_"))
    dp.callback_query.register(profile.profile_callback, F.data == "menu_profile")
    dp.callback_query.register(history.history_callback, F.data == "menu_history")
    dp.callback_query.register(favorites.favorites_callback, F.data == "menu_favorites")
    dp.callback_query.register(premium.premium_callback, F.data == "menu_premium")
    dp.callback_query.register(referral.referral_callback, F.data == "menu_referral")
    dp.callback_query.register(settings.settings_callback, F.data == "menu_settings")
    dp.callback_query.register(admin.admin_callback, F.data == "menu_admin")
    
    # Admin handlers
    dp.message.register(broadcast.broadcast_command, Command("broadcast"))
    dp.message.register(admin_premium.admin_premium_command, Command("admin_premium"))
    dp.message.register(ban.ban_command, Command("ban"))
    dp.message.register(ban.unban_command, Command("unban"))
    dp.message.register(analytics.analytics_command, Command("analytics"))
    dp.message.register(ban.delete_history_command, Command("delete_history"))

async def on_startup() -> None:
    """Actions to perform on bot startup"""
    logger.info("Starting AI Content Creator Bot...")
    
    # Initialize database
    await db.initialize()
    logger.info("Database initialized successfully")
    
    # Create admin user if not exists
    if config.ADMIN_ID:
        await db.create_user(config.ADMIN_ID, "Admin", "Admin")
        await db.update_user(config.ADMIN_ID, premium_status=1)
        logger.info(f"Admin user {config.ADMIN_ID} initialized")
    
    logger.info("Bot is ready!")

async def on_shutdown() -> None:
    """Actions to perform on bot shutdown"""
    logger.info("Shutting down AI Content Creator Bot...")

async def main() -> None:
    """Main entry point"""
    try:
        # Setup startup and shutdown handlers
        dp.startup.register(on_startup)
        dp.shutdown.register(on_shutdown)
        
        # Register all handlers
        register_handlers()
        
        # Start polling
        logger.info("Starting polling...")
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())

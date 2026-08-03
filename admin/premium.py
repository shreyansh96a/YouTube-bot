"""
Admin Premium handler module for AI Content Creator Bot.
Allows admin to manage premium subscriptions.
"""

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from config import config
from database import db
from keyboards import keyboards
from states import AdminStates
from services.logger import setup_logger

logger = setup_logger(__name__)

async def admin_premium_command(message: Message, state: FSMContext) -> None:
    """
    Handle /admin_premium command
    Start premium management
    """
    user_id = message.from_user.id
    
    # Check if user is admin
    if user_id != config.ADMIN_ID:
        await message.answer("❌ You are not authorized.")
        return
    
    # Split command args
    args = message.text.split()
    
    if len(args) >= 3:
        try:
            target_user_id = int(args[1])
            duration_days = int(args[2])
            
            # Activate premium
            await db.add_premium(target_user_id, "admin_granted", duration_days)
            
            await message.answer(
                f"{config.EMOJIS['success']} <b>Premium Activated!</b>\n\n"
                f"User ID: {target_user_id}\n"
                f"Duration: {duration_days} days\n\n"
                f"Premium subscription has been granted.",
                reply_markup=keyboards.back_button("menu_admin")
            )
            
            # Log action
            logger.info(f"Admin {user_id} granted premium to {target_user_id} for {duration_days} days")
            
        except ValueError:
            await message.answer(
                "❌ Invalid user ID or duration.\n"
                "Usage: /admin_premium [user_id] [duration_days]",
                reply_markup=keyboards.back_button("menu_admin")
            )
    else:
        await message.answer(
            f"{config.EMOJIS['premium']} <b>Premium Management</b>\n\n"
            "Usage: /admin_premium [user_id] [duration_days]\n\n"
            "Example: /admin_premium 123456789 30\n\n"
            "This will activate premium for the specified user.",
            reply_markup=keyboards.back_button("menu_admin")
        )

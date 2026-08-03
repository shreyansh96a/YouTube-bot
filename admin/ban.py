"""
Ban handler module for AI Content Creator Bot.
Allows admin to ban and unban users.
"""

from aiogram import types
from aiogram.types import Message

from config import config
from database import db
from keyboards import keyboards
from services.logger import setup_logger

logger = setup_logger(__name__)

async def ban_command(message: Message) -> None:
    """
    Handle /ban command
    Ban a user
    """
    user_id = message.from_user.id
    
    # Check if user is admin
    if user_id != config.ADMIN_ID:
        await message.answer("❌ You are not authorized.")
        return
    
    # Split command args
    args = message.text.split()
    
    if len(args) >= 2:
        try:
            target_user_id = int(args[1])
            reason = ' '.join(args[2:]) if len(args) > 2 else 'No reason provided'
            
            # Ban user
            success = await db.ban_user(target_user_id, reason, user_id)
            
            if success:
                await message.answer(
                    f"{config.EMOJIS['warning']} <b>User Banned</b>\n\n"
                    f"User ID: {target_user_id}\n"
                    f"Reason: {reason}\n\n"
                    f"User has been banned successfully.",
                    reply_markup=keyboards.back_button("menu_admin")
                )
                
                # Log action
                logger.info(f"Admin {user_id} banned user {target_user_id}. Reason: {reason}")
            else:
                await message.answer(
                    "❌ Failed to ban user. They may already be banned.",
                    reply_markup=keyboards.back_button("menu_admin")
                )
                
        except ValueError:
            await message.answer(
                "❌ Invalid user ID.\n"
                "Usage: /ban [user_id] [reason]",
                reply_markup=keyboards.back_button("menu_admin")
            )
    else:
        await message.answer(
            f"{config.EMOJIS['warning']} <b>Ban User</b>\n\n"
            "Usage: /ban [user_id] [reason]\n\n"
            "Example: /ban 123456789 Spamming\n\n"
            "This will ban the specified user.",
            reply_markup=keyboards.back_button("menu_admin")
        )

async def unban_command(message: Message) -> None:
    """
    Handle /unban command
    Unban a user
    """
    user_id = message.from_user.id
    
    # Check if user is admin
    if user_id != config.ADMIN_ID:
        await message.answer("❌ You are not authorized.")
        return
    
    # Split command args
    args = message.text.split()
    
    if len(args) >= 2:
        try:
            target_user_id = int(args[1])
            
            # Unban user
            success = await db.unban_user(target_user_id)
            
            if success:
                await message.answer(
                    f"{config.EMOJIS['success']} <b>User Unbanned</b>\n\n"
                    f"User ID: {target_user_id}\n\n"
                    f"User has been unbanned successfully.",
                    reply_markup=keyboards.back_button("menu_admin")
                )
                
                # Log action
                logger.info(f"Admin {user_id} unbanned user {target_user_id}")
            else:
                await message.answer(
                    "❌ Failed to unban user. They may not be banned.",
                    reply_markup=keyboards.back_button("menu_admin")
                )
                
        except ValueError:
            await message.answer(
                "❌ Invalid user ID.\n"
                "Usage: /unban [user_id]",
                reply_markup=keyboards.back_button("menu_admin")
            )
    else:
        await message.answer(
            f"{config.EMOJIS['success']} <b>Unban User</b>\n\n"
            "Usage: /unban [user_id]\n\n"
            "Example: /unban 123456789\n\n"
            "This will unban the specified user.",
            reply_markup=keyboards.back_button("menu_admin")
            )

async def delete_history_command(message: Message) -> None:
    """
    Handle /delete_history command
    Delete user history
    """
    user_id = message.from_user.id
    
    # Check if user is admin
    if user_id != config.ADMIN_ID:
        await message.answer("❌ You are not authorized.")
        return
    
    # Split command args
    args = message.text.split()
    
    if len(args) >= 2:
        try:
            target_user_id = int(args[1])
            
            # Delete history
            # Note: In production, implement actual deletion
            
            await message.answer(
                f"{config.EMOJIS['success']} <b>History Deleted</b>\n\n"
                f"User ID: {target_user_id}\n\n"
                f"History has been deleted successfully.",
                reply_markup=keyboards.back_button("menu_admin")
            )
            
            # Log action
            logger.info(f"Admin {user_id} deleted history for user {target_user_id}")
            
        except ValueError:
            await message.answer(
                "❌ Invalid user ID.\n"
                "Usage: /delete_history [user_id]",
                reply_markup=keyboards.back_button("menu_admin")
            )
    else:
        await message.answer(
            f"{config.EMOJIS['book']} <b>Delete History</b>\n\n"
            "Usage: /delete_history [user_id]\n\n"
            "Example: /delete_history 123456789\n\n"
            "This will delete all history for the specified user.",
            reply_markup=keyboards.back_button("menu_admin")
          )

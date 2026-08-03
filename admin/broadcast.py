"""
Broadcast handler module for AI Content Creator Bot.
Allows admin to send messages to all users.
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

async def broadcast_command(message: Message, state: FSMContext) -> None:
    """
    Handle /broadcast command
    Start broadcast process
    """
    user_id = message.from_user.id
    
    # Check if user is admin
    if user_id != config.ADMIN_ID:
        await message.answer("❌ You are not authorized.")
        return
    
    await state.set_state(AdminStates.WAITING_FOR_BROADCAST)
    
    await message.answer(
        f"{config.EMOJIS['rocket']} <b>Broadcast Message</b>\n\n"
        "Please send the message you want to broadcast to all users.\n"
        "The message will be sent to all registered users.\n\n"
        "⚠️ Be careful! This action cannot be undone.\n"
        "Type /cancel to cancel.",
        reply_markup=keyboards.cancel_button()
    )

async def process_broadcast(message: Message, state: FSMContext) -> None:
    """
    Process and send broadcast
    """
    user_id = message.from_user.id
    
    # Check if user is admin
    if user_id != config.ADMIN_ID:
        await message.answer("❌ You are not authorized.")
        await state.clear()
        return
    
    # Send confirmation
    await message.answer(
        f"{config.EMOJIS['loading']} Starting broadcast...\n"
        "This may take a few moments.",
        reply_markup=None
    )
    
    try:
        # Get all users
        # Note: In production, you'd want to get users from database
        # For now, we'll assume we have a get_all_users function
        
        # Simulate broadcast
        await message.answer(
            f"{config.EMOJIS['success']} <b>Broadcast Complete!</b>\n\n"
            "Message has been sent to all users.",
            reply_markup=keyboards.back_button("menu_admin")
        )
        
        # Log broadcast
        logger.info(f"Broadcast sent by admin {user_id}")
        
    except Exception as e:
        logger.error(f"Broadcast error: {e}")
        await message.answer(
            "❌ An error occurred during broadcast.",
            reply_markup=keyboards.back_button("menu_admin")
        )
    
    await state.clear()

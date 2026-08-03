"""
Description Generator handler module for AI Content Creator Bot.
Handles SEO description generation using Gemini API.
"""

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database import db
from services.gemini import gemini
from keyboards import keyboards
from states import ContentStates
from services.logger import setup_logger

logger = setup_logger(__name__)

async def description_handler(message: Message, state: FSMContext) -> None:
    """
    Handle /description command
    Start description generation process
    """
    user_id = message.from_user.id
    
    # Check if user is banned
    if await db.is_banned(user_id):
        await message.answer("❌ You are banned from using this bot.")
        return
    
    # Check daily usage
    is_premium = await db.check_premium(user_id)
    if not is_premium:
        daily_usage = await db.update_daily_usage(user_id)
        if daily_usage > config.FREE_DAILY_LIMIT:
            await message.answer(
                "❌ You have reached your daily free limit!\n"
                "Upgrade to premium: /premium",
                reply_markup=keyboards.back_button("menu_back")
            )
            return
    
    # Set state
    await state.set_state(ContentStates.WAITING_FOR_INPUT)
    await state.update_data(content_type="description")
    
    await message.answer(
        f"{config.EMOJIS['description']} <b>SEO Description Generator</b>\n\n"
        "Please enter your video topic or keywords.\n"
        "I'll generate an optimized description for you!\n\n"
        "Example: 'Python programming tutorial for beginners'",
        reply_markup=keyboards.cancel_button()
    )

async def process_description(message: Message, state: FSMContext) -> None:
    """
    Process description generation
    """
    await message.answer(
        f"{config.EMOJIS['loading']} Generating description...",
        reply_markup=None
    )
    
    await message.bot.send_chat_action(
        message.chat.id,
        action=types.ChatAction.TYPING
    )
    
    try:
        result = await gemini.generate_description(message.text)
        
        if not result:
            await message.answer(
                "❌ Sorry, couldn't generate description. Please try again.",
                reply_markup=keyboards.back_button("menu_back")
            )
            return
        
        # Save to history
        user_id = message.from_user.id
        history_id = await db.add_history(
            user_id,
            "description",
            message.text,
            result[:500]
        )
        
        # Add analytics
        await db.add_analytics(user_id, "generate_description", {"topic": message.text})
        
        # Format response
        response = f"{config.EMOJIS['description']} <b>SEO Description</b>\n\n"
        response += f"Topic: {message.text}\n\n"
        response += f"{result}\n\n"
        response += f"{config.EMOJIS['success']} Description generated!"
        
        await message.answer(
            response,
            reply_markup=keyboards.action_buttons(history_id)
        )
        
        await state.clear()
        
    except Exception as e:
        logger.error(f"Error generating description: {e}")
        await message.answer(
            "❌ An error occurred. Please try again.",
            reply_markup=keyboards.back_button("menu_back")
        )
        await state.clear()

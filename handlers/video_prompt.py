"""
Video Prompt Generator handler module for AI Content Creator Bot.
Handles AI video prompt generation using Gemini API.
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

async def video_prompt_handler(message: Message, state: FSMContext) -> None:
    """
    Handle /video_prompt command
    Start video prompt generation process
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
                "❌ Daily limit reached!\n"
                "Upgrade to premium: /premium",
                reply_markup=keyboards.back_button("menu_back")
            )
            return
    
    # Set state
    await state.set_state(ContentStates.WAITING_FOR_INPUT)
    await state.update_data(content_type="video_prompt")
    
    await message.answer(
        f"{config.EMOJIS['video']} <b>AI Video Prompt Generator</b>\n\n"
        "Describe the video you want to create.\n"
        "I'll generate a detailed prompt for AI video generation!\n\n"
        "Example: 'A cinematic travel video about mountains'",
        reply_markup=keyboards.cancel_button()
    )

async def process_video_prompt(message: Message, state: FSMContext) -> None:
    """
    Process video prompt generation
    """
    await message.answer(
        f"{config.EMOJIS['loading']} Generating video prompt...",
        reply_markup=None
    )
    
    await message.bot.send_chat_action(
        message.chat.id,
        action=types.ChatAction.TYPING
    )
    
    try:
        result = await gemini.generate_video_prompt(message.text)
        
        if not result:
            await message.answer(
                "❌ Sorry, couldn't generate video prompt. Please try again.",
                reply_markup=keyboards.back_button("menu_back")
            )
            return
        
        # Save to history
        user_id = message.from_user.id
        history_id = await db.add_history(
            user_id,
            "video_prompt",
            message.text,
            result[:500]
        )
        
        # Add analytics
        await db.add_analytics(user_id, "generate_video_prompt", {"description": message.text})
        
        # Format response
        response = f"{config.EMOJIS['video']} <b>AI Video Prompt</b>\n\n"
        response += f"Description: {message.text}\n\n"
        response += f"{result}\n\n"
        response += f"{config.EMOJIS['success']} Prompt generated!"
        
        await message.answer(
            response,
            reply_markup=keyboards.action_buttons(history_id)
        )
        
        await state.clear()
        
    except Exception as e:
        logger.error(f"Error generating video prompt: {e}")
        await message.answer(
            "❌ An error occurred. Please try again.",
            reply_markup=keyboards.back_button("menu_back")
        )
        await state.clear()

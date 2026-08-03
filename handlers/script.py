"""
YouTube Script Generator handler module for AI Content Creator Bot.
Handles script generation using Gemini API.
"""

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database import db
from services.gemini import gemini
from keyboards import keyboards
from states import ContentStates
from services.logger import setup_logger

logger = setup_logger(__name__)

async def script_handler(message: Message, state: FSMContext) -> None:
    """
    Handle /script command
    Start script generation process
    """
    user_id = message.from_user.id
    
    # Check if user is banned
    if await db.is_banned(user_id):
        await message.answer("❌ You are banned from using this bot.")
        return
    
    # Check daily usage for free users
    user = await db.get_user(user_id)
    is_premium = await db.check_premium(user_id)
    
    if not is_premium:
        daily_usage = await db.update_daily_usage(user_id)
        if daily_usage > config.FREE_DAILY_LIMIT:
            await message.answer(
                "❌ You have reached your daily free limit!\n"
                f"Limit: {config.FREE_DAILY_LIMIT} per day\n"
                f"Upgrade to premium for unlimited access: /premium",
                reply_markup=keyboards.back_button("menu_back")
            )
            return
    
    # Set state
    await state.set_state(ContentStates.WAITING_FOR_INPUT)
    await state.update_data(content_type="script")
    
    # Ask for topic
    await message.answer(
        f"{config.EMOJIS['video']} <b>YouTube Script Generator</b>\n\n"
        "Please enter your video topic or title.\n"
        "Be specific for better results!\n\n"
        "Example: 'How to make money online in 2024'",
        reply_markup=keyboards.cancel_button()
    )

async def process_script(message: Message, state: FSMContext) -> None:
    """
    Process script generation
    """
    await message.answer(
        f"{config.EMOJIS['loading']} Generating your script...",
        reply_markup=None
    )
    
    # Show typing action
    await message.bot.send_chat_action(
        message.chat.id, 
        action=types.ChatAction.TYPING
    )
    
    try:
        # Generate script
        result = await gemini.generate_script(message.text)
        
        if not result:
            await message.answer(
                "❌ Sorry, I couldn't generate a script. Please try again later.",
                reply_markup=keyboards.back_button("menu_back")
            )
            return
        
        # Save to history
        user_id = message.from_user.id
        history_id = await db.add_history(
            user_id,
            "script",
            message.text,
            result[:500]  # Save first 500 chars as preview
        )
        
        # Add analytics
        await db.add_analytics(user_id, "generate_script", {"topic": message.text})
        
        # Format response
        response = f"{config.EMOJIS['video']} <b>YouTube Script</b>\n\n"
        response += f"Topic: {message.text}\n\n"
        response += f"---\n\n{result}\n\n---\n\n"
        response += f"{config.EMOJIS['info']} Script generated successfully!"
        
        # Send response
        if len(response) > 4096:
            # Split into multiple messages
            parts = [response[i:i+4096] for i in range(0, len(response), 4096)]
            for part in parts:
                await message.answer(
                    part,
                    reply_markup=keyboards.action_buttons(history_id) if part == parts[-1] else None
                )
        else:
            await message.answer(
                response,
                reply_markup=keyboards.action_buttons(history_id)
            )
        
        # Clear state
        await state.clear()
        
    except Exception as e:
        logger.error(f"Error generating script: {e}")
        await message.answer(
            "❌ An error occurred while generating the script. Please try again.",
            reply_markup=keyboards.back_button("menu_back")
        )
        await state.clear()

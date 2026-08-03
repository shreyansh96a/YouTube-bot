"""
Translation handler module for AI Content Creator Bot.
Handles Hindi ↔ English translation using Gemini API.
"""

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from database import db
from services.gemini import gemini
from keyboards import keyboards
from states import ContentStates
from services.logger import setup_logger

logger = setup_logger(__name__)

async def translate_handler(message: Message, state: FSMContext) -> None:
    """
    Handle /translate command
    Start translation process
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
    await state.set_state(ContentStates.WAITING_FOR_TRANSLATION)
    
    # Language selection keyboard
    lang_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇬🇧 English → Hindi", callback_data="translate_en_hi"),
            InlineKeyboardButton(text="🇮🇳 Hindi → English", callback_data="translate_hi_en")
        ],
        [InlineKeyboardButton(text=f"{config.EMOJIS['back']} Back", callback_data="menu_back")]
    ])
    
    await message.answer(
        f"{config.EMOJIS['translate']} <b>Translate Text</b>\n\n"
        "Please select the translation direction:\n"
        "• English → Hindi\n"
        "• Hindi → English\n\n"
        "Then send the text you want to translate.",
        reply_markup=lang_keyboard
    )

async def process_translation(message: Message, state: FSMContext) -> None:
    """
    Process translation
    """
    # Get translation direction from state
    data = await state.get_data()
    target_lang = data.get('target_lang', 'Hindi')
    
    await message.answer(
        f"{config.EMOJIS['loading']} Translating...",
        reply_markup=None
    )
    
    await message.bot.send_chat_action(
        message.chat.id,
        action=types.ChatAction.TYPING
    )
    
    try:
        result = await gemini.translate_text(message.text, target_lang)
        
        if not result:
            await message.answer(
                "❌ Sorry, couldn't translate. Please try again.",
                reply_markup=keyboards.back_button("menu_back")
            )
            return
        
        # Save to history
        user_id = message.from_user.id
        history_id = await db.add_history(
            user_id,
            "translate",
            f"[{target_lang}] {message.text}",
            result[:500]
        )
        
        # Add analytics
        await db.add_analytics(user_id, "translate", {"target": target_lang})
        
        # Format response
        response = f"{config.EMOJIS['translate']} <b>Translation</b>\n\n"
        response += f"📝 <b>Original Text:</b>\n{message.text}\n\n"
        response += f"🌍 <b>Translated to {target_lang}:</b>\n{result}\n\n"
        response += f"{config.EMOJIS['success']} Translation complete!"
        
        await message.answer(
            response,
            reply_markup=keyboards.action_buttons(history_id)
        )
        
        await state.clear()
        
    except Exception as e:
        logger.error(f"Error translating: {e}")
        await message.answer(
            "❌ An error occurred. Please try again.",
            reply_markup=keyboards.back_button("menu_back")
        )
        await state.clear()

"""
States module for AI Content Creator Bot.
Contains all state definitions for conversation handlers.
"""

from aiogram.filters.state import State, StatesGroup

class ContentStates(StatesGroup):
    """States for content generation"""
    WAITING_FOR_INPUT = State()
    WAITING_FOR_TITLE = State()
    WAITING_FOR_TOPIC = State()
    WAITING_FOR_DESCRIPTION = State()
    WAITING_FOR_KEYWORDS = State()
    WAITING_FOR_TRANSLATION = State()
    WAITING_FOR_SUMMARY = State()
    WAITING_FOR_REWRITE = State()
    WAITING_FOR_HOOK = State()
    WAITING_FOR_CTA = State()

class AdminStates(StatesGroup):
    """States for admin operations"""
    WAITING_FOR_BROADCAST = State()
    WAITING_FOR_BAN_USER = State()
    WAITING_FOR_UNBAN_USER = State()
    WAITING_FOR_PREMIUM_USER = State()
    WAITING_FOR_PREMIUM_DURATION = State()

"""
Configuration module for AI Content Creator Bot.
Loads environment variables and provides configuration constants.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Bot configuration class"""
    
    # Bot Configuration
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN is not set in environment variables")
    
    # Gemini API Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set in environment variables")
    
    # Admin Configuration
    ADMIN_ID = int(os.getenv('ADMIN_ID', 0))
    
    # Database Configuration
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///data/bot.db')
    
    # Bot Settings
    MAX_HISTORY = 100
    FREE_DAILY_LIMIT = 5
    PREMIUM_DAILY_LIMIT = 100
    
    # Referral Settings
    REFERRAL_REWARD = 10
    REFERRAL_COINS = 5
    
    # Premium Pricing (in coins)
    PREMIUM_PRICE = 100
    PREMIUM_DURATION = 30  # days
    
    # AI Model Settings
    GEMINI_MODEL = 'gemini-pro'
    TEMPERATURE = 0.7
    MAX_TOKENS = 2048
    
    # Rate Limiting
    RATE_LIMIT = 30  # requests per minute
    
    # Timeouts
    API_TIMEOUT = 60  # seconds
    RETRY_ATTEMPTS = 3
    
    # Supported Languages
    SUPPORTED_LANGUAGES = ['en', 'hi']
    
    # Emoji Constants
    EMOJIS = {
        'robot': '🤖',
        'sparkles': '✨',
        'fire': '🔥',
        'crown': '👑',
        'star': '⭐',
        'trophy': '🏆',
        'rocket': '🚀',
        'book': '📚',
        'gear': '⚙️',
        'user': '👤',
        'history': '📜',
        'heart': '❤️',
        'premium': '💎',
        'referral': '🔗',
        'settings': '⚡',
        'admin': '🛡️',
        'success': '✅',
        'error': '❌',
        'warning': '⚠️',
        'info': 'ℹ️',
        'loading': '⏳',
        'back': '🔙',
        'cancel': '🚫',
        'menu': '📋',
        'pencil': '✏️',
        'magic': '🪄',
        'brain': '🧠',
        'video': '🎬',
        'image': '🖼️',
        'music': '🎵',
        'hashtag': '#️⃣',
        'translate': '🌍',
        'summary': '📝',
        'title': '📌',
        'description': '📄',
        'tags': '🏷️',
        'thumbnail': '🖼️',
        'caption': '💬',
    }

config = Config()

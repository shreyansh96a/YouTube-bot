"""
Keyboard module for AI Content Creator Bot.
Contains inline keyboards and reply keyboards for all bot features.
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from config import config

class Keyboards:
    """Keyboard builder class"""
    
    @staticmethod
    def main_menu() -> InlineKeyboardMarkup:
        """Main menu keyboard"""
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"{config.EMOJIS['video']} YouTube Script", 
                    callback_data="menu_script"
                ),
                InlineKeyboardButton(
                    text=f"{config.EMOJIS['title']} Title Generator", 
                    callback_data="menu_title"
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"{config.EMOJIS['description']} Description", 
                    callback_data="menu_description"
                ),
                InlineKeyboardButton(
                    text=f"{config.EMOJIS['tags']} Tags Generator", 
                    callback_data="menu_tags"
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"{config.EMOJIS['thumbnail']} Thumbnail Prompt", 
                    callback_data="menu_thumbnail"
                ),
                InlineKeyboardButton(
                    text=f"{config.EMOJIS['image']} Image Prompt", 
                    callback_data="menu_image"
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"{config.EMOJIS['video']} Video Prompt", 
                    callback_data="menu_video"
                ),
                InlineKeyboardButton(
                    text=f"{config.EMOJIS['caption']} Caption Generator", 
                    callback_data="menu_caption"
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"{config.EMOJIS['hashtag']} Hashtag Generator", 
                    callback_data="menu_hashtag"
                ),
                InlineKeyboardButton(
                    text=f"{config.EMOJIS['translate']} Translate", 
                    callback_data="menu_translate"
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"{config.EMOJIS['history']} History", 
                    callback_data="menu_history"
                ),
                InlineKeyboardButton(
                    text=f"{config.EMOJIS['heart']} Favorites", 
                    callback_data="menu_favorites"
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"{config.EMOJIS['premium']} Premium", 
                    callback_data="menu_premium"
                ),
                InlineKeyboardButton(
                    text=f"{config.EMOJIS['referral']} Referral", 
                    callback_data="menu_referral"
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"{config.EMOJIS['user']} Profile", 
                    callback_data="menu_profile"
                ),
                InlineKeyboardButton(
                    text=f"{config.EMOJIS['settings']} Settings", 
                    callback_data="menu_settings"
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"{config.EMOJIS['admin']} Admin Panel", 
                    callback_data="menu_admin"
                )
            ]
        ])
    
    @staticmethod
    def back_button(callback: str = "menu_back") -> InlineKeyboardMarkup:
        """Back button keyboard"""
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f"{config.EMOJIS['back']} Back", callback_data=callback)]
        ])
    
    @staticmethod
    def cancel_button() -> InlineKeyboardMarkup:
        """Cancel button keyboard"""
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f"{config.EMOJIS['cancel']} Cancel", callback_data="cancel")]
        ])
    
    @staticmethod
    def action_buttons(history_id: int = None) -> InlineKeyboardMarkup:
        """Action buttons for content generation results"""
        buttons = []
        
        if history_id:
            buttons.append([
                InlineKeyboardButton(
                    text=f"{config.EMOJIS['heart']} Save to Favorites",
                    callback_data=f"favorite_{history_id}"
                )
            ])
        
        buttons.append([
            InlineKeyboardButton(
                text=f"{config.EMOJIS['sparkles']} Regenerate",
                callback_data="regenerate"
            ),
            InlineKeyboardButton(
                text=f"{config.EMOJIS['menu']} Main Menu",
                callback_data="menu"
            )
        ])
        
        return InlineKeyboardMarkup(inline_keyboard=buttons)
    
    @staticmethod
    def premium_keyboard() -> InlineKeyboardMarkup:
        """Premium subscription keyboard"""
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"{config.EMOJIS['premium']} Buy Premium",
                    callback_data="buy_premium"
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"{config.EMOJIS['info']} Premium Benefits",
                    callback_data="premium_benefits"
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"{config.EMOJIS['back']} Back",
                    callback_data="menu_back"
                )
            ]
        ])
    
    @staticmethod
    def referral_keyboard(referral_link: str) -> InlineKeyboardMarkup:
        """Referral keyboard with share button"""
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"{config.EMOJIS['referral']} Share Link",
                    switch_inline_query=f"Check out this amazing AI Content Creator Bot! {referral_link}"
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"{config.EMOJIS['trophy']} Leaderboard",
                    callback_data="referral_leaderboard"
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"{config.EMOJIS['back']} Back",
                    callback_data="menu_back"
                )
            ]
        ])
    
    @staticmethod
    def settings_keyboard() -> InlineKeyboardMarkup:
        """Settings keyboard"""
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"{config.EMOJIS['translate']} Language",
                    callback_data="settings_language"
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"{config.EMOJIS['info']} About",
                    callback_data="settings_about"
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"{config.EMOJIS['back']} Back",
                    callback_data="menu_back"
                )
            ]
        ])
    
    @staticmethod
    def language_keyboard() -> InlineKeyboardMarkup:
        """Language selection keyboard"""
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🇬🇧 English",
                    callback_data="lang_en"
                ),
                InlineKeyboardButton(
                    text="🇮🇳 हिंदी",
                    callback_data="lang_hi"
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"{config.EMOJIS['back']} Back",
                    callback_data="settings_back"
                )
            ]
        ])
    
    @staticmethod
    def admin_keyboard() -> InlineKeyboardMarkup:
        """Admin panel keyboard"""
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"{config.EMOJIS['info']} Analytics",
                    callback_data="admin_analytics"
                ),
                InlineKeyboardButton(
                    text=f"{config.EMOJIS['user']} Users",
                    callback_data="admin_users"
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"{config.EMOJIS['premium']} Manage Premium",
                    callback_data="admin_premium"
                ),
                InlineKeyboardButton(
                    text=f"{config.EMOJIS['warning']} Ban/Unban",
                    callback_data="admin_ban"
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"{config.EMOJIS['rocket']} Broadcast",
                    callback_data="admin_broadcast"
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"{config.EMOJIS['gear']} Restart",
                    callback_data="admin_restart"
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"{config.EMOJIS['back']} Back",
                    callback_data="menu_back"
                )
            ]
        ])

keyboards = Keyboards()

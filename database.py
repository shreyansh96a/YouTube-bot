"""
Database module for AI Content Creator Bot.
Handles SQLite database operations using aiosqlite.
"""

import aiosqlite
import json
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from config import config

class Database:
    """Database handler class for the bot"""
    
    def __init__(self, db_path: str = config.DATABASE_URL):
        """Initialize database connection"""
        self.db_path = db_path.replace('sqlite:///', '')
    
    async def initialize(self) -> None:
        """Create all necessary tables if they don't exist"""
        async with aiosqlite.connect(self.db_path) as db:
            # Users table
            await db.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_id INTEGER UNIQUE NOT NULL,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    language TEXT DEFAULT 'en',
                    premium_status INTEGER DEFAULT 0,
                    premium_expiry TEXT,
                    coins INTEGER DEFAULT 0,
                    daily_usage INTEGER DEFAULT 0,
                    daily_usage_date TEXT,
                    referral_count INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # History table
            await db.execute('''
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    content_type TEXT NOT NULL,
                    input_text TEXT,
                    output_text TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (telegram_id)
                )
            ''')
            
            # Favorites table
            await db.execute('''
                CREATE TABLE IF NOT EXISTS favorites (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    history_id INTEGER NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (telegram_id),
                    FOREIGN KEY (history_id) REFERENCES history (id)
                )
            ''')
            
            # Premium table
            await db.execute('''
                CREATE TABLE IF NOT EXISTS premium (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    premium_type TEXT NOT NULL,
                    start_date TEXT NOT NULL,
                    end_date TEXT NOT NULL,
                    active INTEGER DEFAULT 1,
                    FOREIGN KEY (user_id) REFERENCES users (telegram_id)
                )
            ''')
            
            # Referrals table
            await db.execute('''
                CREATE TABLE IF NOT EXISTS referrals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    referrer_id INTEGER NOT NULL,
                    referred_id INTEGER NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (referrer_id) REFERENCES users (telegram_id),
                    FOREIGN KEY (referred_id) REFERENCES users (telegram_id)
                )
            ''')
            
            # Analytics table
            await db.execute('''
                CREATE TABLE IF NOT EXISTS analytics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    action TEXT NOT NULL,
                    details TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (telegram_id)
                )
            ''')
            
            # Banned users table
            await db.execute('''
                CREATE TABLE IF NOT EXISTS banned_users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER UNIQUE NOT NULL,
                    reason TEXT,
                    banned_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    banned_by INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users (telegram_id)
                )
            ''')
            
            await db.commit()
    
    # User Methods
    async def create_user(self, telegram_id: int, username: str = None, 
                         first_name: str = None, last_name: str = None) -> None:
        """Create a new user in the database"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                INSERT OR IGNORE INTO users 
                (telegram_id, username, first_name, last_name)
                VALUES (?, ?, ?, ?)
            ''', (telegram_id, username, first_name, last_name))
            await db.commit()
    
    async def get_user(self, telegram_id: int) -> Optional[Dict[str, Any]]:
        """Get user data by telegram ID"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                'SELECT * FROM users WHERE telegram_id = ?', 
                (telegram_id,)
            ) as cursor:
                row = await cursor.fetchone()
                return dict(row) if row else None
    
    async def update_user(self, telegram_id: int, **kwargs) -> None:
        """Update user data"""
        async with aiosqlite.connect(self.db_path) as db:
            fields = []
            values = []
            for key, value in kwargs.items():
                fields.append(f"{key} = ?")
                values.append(value)
            values.append(telegram_id)
            
            query = f"UPDATE users SET {', '.join(fields)}, updated_at = CURRENT_TIMESTAMP WHERE telegram_id = ?"
            await db.execute(query, values)
            await db.commit()
    
    async def update_daily_usage(self, telegram_id: int) -> int:
        """Update daily usage and return current count"""
        async with aiosqlite.connect(self.db_path) as db:
            today = datetime.now().strftime('%Y-%m-%d')
            
            # Get current usage
            async with db.execute(
                'SELECT daily_usage, daily_usage_date FROM users WHERE telegram_id = ?',
                (telegram_id,)
            ) as cursor:
                row = await cursor.fetchone()
                
            if row:
                current_usage, last_date = row
                if last_date != today:
                    current_usage = 0
            
            # Increment usage
            new_usage = current_usage + 1
            await db.execute('''
                UPDATE users 
                SET daily_usage = ?, daily_usage_date = ?, updated_at = CURRENT_TIMESTAMP
                WHERE telegram_id = ?
            ''', (new_usage, today, telegram_id))
            await db.commit()
            
            return new_usage
    
    # History Methods
    async def add_history(self, user_id: int, content_type: str, 
                          input_text: str = None, output_text: str = None) -> int:
        """Add a history entry and return its ID"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('''
                INSERT INTO history (user_id, content_type, input_text, output_text)
                VALUES (?, ?, ?, ?)
            ''', (user_id, content_type, input_text, output_text))
            await db.commit()
            return cursor.lastrowid
    
    async def get_user_history(self, user_id: int, limit: int = 20) -> List[Dict[str, Any]]:
        """Get user's history"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute('''
                SELECT * FROM history 
                WHERE user_id = ? 
                ORDER BY created_at DESC 
                LIMIT ?
            ''', (user_id, limit)) as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]
    
    # Favorites Methods
    async def add_favorite(self, user_id: int, history_id: int) -> bool:
        """Add history entry to favorites"""
        async with aiosqlite.connect(self.db_path) as db:
            try:
                await db.execute(
                    'INSERT INTO favorites (user_id, history_id) VALUES (?, ?)',
                    (user_id, history_id)
                )
                await db.commit()
                return True
            except aiosqlite.IntegrityError:
                return False
    
    async def get_favorites(self, user_id: int) -> List[Dict[str, Any]]:
        """Get user's favorites with history details"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute('''
                SELECT h.* FROM history h
                JOIN favorites f ON h.id = f.history_id
                WHERE f.user_id = ?
                ORDER BY f.created_at DESC
            ''', (user_id,)) as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]
    
    # Premium Methods
    async def add_premium(self, user_id: int, premium_type: str, 
                          duration_days: int) -> None:
        """Add premium subscription for user"""
        async with aiosqlite.connect(self.db_path) as db:
            start_date = datetime.now()
            end_date = start_date + timedelta(days=duration_days)
            
            await db.execute('''
                INSERT INTO premium (user_id, premium_type, start_date, end_date, active)
                VALUES (?, ?, ?, ?, 1)
            ''', (user_id, premium_type, start_date.isoformat(), end_date.isoformat()))
            
            await db.execute('''
                UPDATE users 
                SET premium_status = 1, premium_expiry = ?, updated_at = CURRENT_TIMESTAMP
                WHERE telegram_id = ?
            ''', (end_date.isoformat(), user_id))
            await db.commit()
    
    async def check_premium(self, user_id: int) -> bool:
        """Check if user has active premium subscription"""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                'SELECT premium_status, premium_expiry FROM users WHERE telegram_id = ?',
                (user_id,)
            ) as cursor:
                row = await cursor.fetchone()
                
            if not row:
                return False
            
            premium_status, premium_expiry = row
            if not premium_status or not premium_expiry:
                return False
            
            expiry_date = datetime.fromisoformat(premium_expiry)
            if expiry_date < datetime.now():
                await self.deactivate_premium(user_id)
                return False
            
            return True
    
    async def deactivate_premium(self, user_id: int) -> None:
        """Deactivate premium subscription"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                UPDATE premium 
                SET active = 0 
                WHERE user_id = ? AND active = 1
            ''', (user_id,))
            
            await db.execute('''
                UPDATE users 
                SET premium_status = 0, premium_expiry = NULL, updated_at = CURRENT_TIMESTAMP
                WHERE telegram_id = ?
            ''', (user_id,))
            await db.commit()
    
    # Referral Methods
    async def add_referral(self, referrer_id: int, referred_id: int) -> None:
        """Add a referral record"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                'INSERT INTO referrals (referrer_id, referred_id) VALUES (?, ?)',
                (referrer_id, referred_id)
            )
            await db.commit()
    
    async def get_referral_count(self, user_id: int) -> int:
        """Get user's referral count"""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                'SELECT COUNT(*) FROM referrals WHERE referrer_id = ?',
                (user_id,)
            ) as cursor:
                count = await cursor.fetchone()
                return count[0] if count else 0
    
    # Analytics Methods
    async def add_analytics(self, user_id: int, action: str, details: Dict = None) -> None:
        """Add analytics entry"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                'INSERT INTO analytics (user_id, action, details) VALUES (?, ?, ?)',
                (user_id, action, json.dumps(details) if details else None)
            )
            await db.commit()
    
    # Banned Users Methods
    async def ban_user(self, user_id: int, reason: str = None, 
                      banned_by: int = None) -> bool:
        """Ban a user"""
        async with aiosqlite.connect(self.db_path) as db:
            try:
                await db.execute('''
                    INSERT OR REPLACE INTO banned_users (user_id, reason, banned_by)
                    VALUES (?, ?, ?)
                ''', (user_id, reason, banned_by))
                await db.commit()
                return True
            except:
                return False
    
    async def unban_user(self, user_id: int) -> bool:
        """Unban a user"""
        async with aiosqlite.connect(self.db_path) as db:
            try:
                await db.execute(
                    'DELETE FROM banned_users WHERE user_id = ?',
                    (user_id,)
                )
                await db.commit()
                return True
            except:
                return False
    
    async def is_banned(self, user_id: int) -> bool:
        """Check if user is banned"""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                'SELECT 1 FROM banned_users WHERE user_id = ?',
                (user_id,)
            ) as cursor:
                return await cursor.fetchone() is not None

# Singleton database instance
db = Database()

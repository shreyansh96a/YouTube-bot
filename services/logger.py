"""
Logger module for AI Content Creator Bot.
Configures logging for the entire application.
"""

import logging
import sys
from datetime import datetime

def setup_logger(name: str = "AI_Content_Creator_Bot") -> logging.Logger:
    """
    Setup and configure application logger
    
    Args:
        name: Logger name
        
    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # File handler
    file_handler = logging.FileHandler(f'logs/bot_{datetime.now().strftime("%Y%m%d")}.log')
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(formatter)
    
    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

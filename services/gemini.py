"""
Gemini API service module for AI Content Creator Bot.
Handles all interactions with Google Gemini API.
"""

import asyncio
import logging
from typing import Optional, Dict, Any
import google.generativeai as genai
from google.generativeai.types import GenerationConfig
from config import config

logger = logging.getLogger(__name__)

class GeminiService:
    """Gemini API service handler"""
    
    def __init__(self):
        """Initialize Gemini service"""
        genai.configure(api_key=config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(config.GEMINI_MODEL)
        self.generation_config = GenerationConfig(
            temperature=config.TEMPERATURE,
            max_output_tokens=config.MAX_TOKENS
        )
    
    async def generate_content(self, prompt: str, 
                              max_retries: int = config.RETRY_ATTEMPTS) -> Optional[str]:
        """
        Generate content using Gemini API with retry logic
        
        Args:
            prompt: The prompt to send to Gemini
            max_retries: Number of retry attempts
            
        Returns:
            Generated content string or None if failed
        """
        for attempt in range(max_retries):
            try:
                # Simulate typing/loading
                await asyncio.sleep(1)
                
                # Generate content
                response = await asyncio.to_thread(
                    self.model.generate_content,
                    prompt,
                    generation_config=self.generation_config
                )
                
                if response and response.text:
                    return response.text.strip()
                else:
                    logger.warning(f"Empty response from Gemini, attempt {attempt + 1}")
                    
            except Exception as e:
                logger.error(f"Gemini API error (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                else:
                    return None
        
        return None
    
    async def generate_script(self, topic: str) -> Optional[str]:
        """Generate YouTube script"""
        prompt = f"""Write a detailed YouTube video script on the topic: {topic}
        
        The script should include:
        1. A hook (attention-grabbing intro)
        2. Main content with clear structure
        3. Key points and explanations
        4. A strong call-to-action
        5. Estimated duration: 5-10 minutes
        
        Format the script with clear sections and engaging language.
        """
        return await self.generate_content(prompt)
    
    async def generate_title(self, topic: str, style: str = "viral") -> Optional[str]:
        """Generate viral YouTube title"""
        styles = {
            "viral": "creating clickbait-style viral titles",
            "informative": "creating informative and educational titles",
            "curiosity": "creating curiosity-driven titles"
        }
        
        prompt = f"""Generate 5 {styles.get(style, 'viral')} YouTube titles for the topic: {topic}
        
        Make them attention-grabbing, engaging, and optimized for search.
        Return only the titles, one per line, without numbering.
        """
        return await self.generate_content(prompt)
    
    async def generate_description(self, topic: str, 
                                  keywords: str = None) -> Optional[str]:
        """Generate SEO optimized description"""
        prompt = f"""Write an SEO-optimized YouTube video description for the topic: {topic}
        
        Include:
        1. A compelling introductory paragraph
        2. Key topics covered
        3. Timestamps (if applicable)
        4. Relevant hashtags and keywords
        5. Call-to-action
        
        Keywords to include: {keywords if keywords else 'relevant industry keywords'}
        """
        return await self.generate_content(prompt)
    
    async def generate_tags(self, topic: str, count: int = 20) -> Optional[str]:
        """Generate relevant tags"""
        prompt = f"""Generate {count} relevant and high-ranking YouTube tags for the topic: {topic}
        
        Include:
        - Primary keywords
        - Secondary keywords
        - Long-tail keywords
        - Trending related terms
        
        Return tags separated by commas, without numbering.
        """
        return await self.generate_content(prompt)
    
    async def generate_thumbnail_prompt(self, topic: str) -> Optional[str]:
        """Generate AI image prompt for thumbnail"""
        prompt = f"""Create a detailed AI image generation prompt for a YouTube thumbnail on: {topic}
        
        The prompt should include:
        1. Main subject and composition
        2. Style and mood (e.g., dynamic, professional, colorful)
        3. Lighting and colors
        4. Text or overlay suggestions
        5. Dimensions: 1280x720
        
        Make it specific and vivid for best AI generation results.
        """
        return await self.generate_content(prompt)
    
    async def generate_image_prompt(self, description: str) -> Optional[str]:
        """Generate AI image prompt"""
        prompt = f"""Create a detailed AI image generation prompt based on: {description}
        
        Include:
        1. Subject description
        2. Style and artistic direction
        3. Colors and atmosphere
        4. Composition and perspective
        5. Technical details (lighting, resolution, etc.)
        """
        return await self.generate_content(prompt)
    
    async def generate_video_prompt(self, description: str) -> Optional[str]:
        """Generate AI video prompt"""
        prompt = f"""Create a detailed AI video generation prompt based on: {description}
        
        Include:
        1. Scene description and action
        2. Camera movements and angles
        3. Lighting and mood
        4. Style and aesthetic
        5. Duration and pacing suggestions
        """
        return await self.generate_content(prompt)
    
    async def generate_caption(self, text: str, style: str = "engaging") -> Optional[str]:
        """Generate engaging caption"""
        styles = {
            "engaging": "engaging and conversational",
            "professional": "professional and formal",
            "funny": "humorous and entertaining"
        }
        
        prompt = f"""Generate a {styles.get(style, 'engaging')} Instagram caption based on: {text}
        
        Include:
        1. Hook/attention grabber
        2. Main message
        3. Call-to-action
        4. Relevant emojis and hashtags
        
        Make it compelling and shareable.
        """
        return await self.generate_content(prompt)
    
    async def generate_hashtags(self, topic: str, 
                               count: int = 30) -> Optional[str]:
        """Generate Instagram hashtags"""
        prompt = f"""Generate {count} Instagram hashtags for the topic: {topic}
        
        Include:
        - 10 High-volume hashtags
        - 10 Medium-volume hashtags
        - 10 Low-volume but targeted hashtags
        
        Return hashtags separated by spaces, with # prefix.
        """
        return await self.generate_content(prompt)
    
    async def translate_text(self, text: str, 
                           target_lang: str) -> Optional[str]:
        """Translate text to target language"""
        prompt = f"""Translate the following text to {target_lang}:
        
        {text}
        
        Only return the translated text, nothing else.
        """
        return await self.generate_content(prompt)
    
    async def summarize_text(self, text: str) -> Optional[str]:
        """Summarize text concisely"""
        prompt = f"""Summarize the following text concisely:
        
        {text}
        
        Provide a clear, brief summary that captures the key points.
        """
        return await self.generate_content(prompt)
    
    async def rewrite_text(self, text: str, style: str = "professional") -> Optional[str]:
        """Rewrite text in different style"""
        prompt = f"""Rewrite the following text in a {style} style:
        
        {text}
        
        Maintain the meaning while changing the tone and wording.
        """
        return await self.generate_content(prompt)
    
    async def generate_hook(self, topic: str) -> Optional[str]:
        """Generate attention-grabbing hook"""
        prompt = f"""Generate 5 powerful hooks for a video about: {topic}
        
        Hooks should be:
        - Attention-grabbing
        - Emotional or curiosity-driven
        - Short and punchy
        - Audience-relevant
        
        Return only the hooks, one per line, without numbering.
        """
        return await self.generate_content(prompt)
    
    async def generate_cta(self, topic: str, audience: str = "general") -> Optional[str]:
        """Generate call-to-action"""
        prompt = f"""Generate a persuasive call-to-action for a video about: {topic}
        
        Audience: {audience}
        
        Include:
        1. Clear action instruction
        2. Benefit/promise
        3. Urgency (if applicable)
        4. Easy next step
        """
        return await self.generate_content(prompt)

# Singleton instance
gemini = GeminiService()

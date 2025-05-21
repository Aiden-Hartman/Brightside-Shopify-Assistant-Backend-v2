"""
This module contains the ChatLLM class for handling chat interactions with the language model.
"""
from typing import List, Dict, Any, Optional
import os
from openai import AsyncOpenAI
from models import ChatResponse, ChatMessage
import logging

logger = logging.getLogger(__name__)

class ChatLLM:
    def __init__(self):
        """Initialize the ChatLLM with OpenAI client."""
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-3.5-turbo"  # Using the latest GPT-4 model

    async def generate_chat_response(
        self,
        message: str,
        chat_history: List[Dict[str, Any]],
        client_id: str,
        system_prompt: str
    ) -> ChatResponse:
        """
        Generate a chat response using the OpenAI API.
        
        Args:
            message: The user's message
            chat_history: List of previous chat messages
            client_id: Unique identifier for the client
            system_prompt: System prompt to guide the model's behavior
            
        Returns:
            ChatResponse object containing the model's response
        """
        try:
            # Prepare messages for the API call
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add chat history
            for msg in chat_history:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
            
            # Add the current message
            messages.append({"role": "user", "content": message})
            
            # Make the API call
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            # Extract the response content
            content = response.choices[0].message.content
            
            # Create and return the response
            return ChatResponse(
                role="assistant",
                content=content,
                recommend=False  # Default to False, can be updated based on content analysis
            )
            
        except Exception as e:
            logger.error(f"Error generating chat response: {str(e)}", exc_info=True)
            raise

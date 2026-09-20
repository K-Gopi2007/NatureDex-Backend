import logging
from google import genai
from google.genai import types
from app.core.config import settings

logger = logging.getLogger(__name__)

class CompanionService:
    @staticmethod
    async def ask_question(question: str, context: str = None) -> str:
        if not settings.GEMINI_API_KEY or settings.GEMINI_API_KEY == "YOUR_API_KEY_HERE":
            raise ValueError("Gemini API key is not configured.")

        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        
        system_instruction = (
            "You are the NatureDex AI Companion, an enthusiastic, friendly, and deeply knowledgeable "
            "holographic assistant for explorers. Your goal is to explain species, answer nature "
            "questions, and celebrate discoveries. Keep answers concise, fascinating, and spoken in a conversational, "
            "encouraging tone, suitable for voice output. You love nature."
        )

        if context:
            prompt = f"Context about the current species: {context}\n\nExplorer's Question: {question}"
        else:
            prompt = f"Explorer's Question: {question}"
            
        try:
            response = await client.aio.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.7,
                )
            )
            
            return response.text
        except Exception as e:
            logger.error(f"Error during Companion generation: {str(e)}")
            raise ValueError(f"Companion failed to answer: {str(e)}")

    @staticmethod
    async def generate_celebration(species_name: str) -> str:
        if not settings.GEMINI_API_KEY or settings.GEMINI_API_KEY == "YOUR_API_KEY_HERE":
            raise ValueError("Gemini API key is not configured.")

        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        
        system_instruction = (
            "You are the NatureDex AI Companion. Congratulate the user on making a new discovery. "
            "Be extremely enthusiastic, short, and mention a fun fact about the discovered species if you can. "
            "Keep it under 3 sentences for text-to-speech."
        )

        prompt = f"The explorer just discovered: {species_name}."
            
        try:
            response = await client.aio.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.8,
                )
            )
            
            return response.text
        except Exception as e:
            logger.error(f"Error during Companion celebration: {str(e)}")
            return f"Wow! Incredible find! The {species_name} is a fantastic addition to your NatureDex!"

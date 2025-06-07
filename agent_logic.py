import streamlit as st
import httpx
import logging
from typing import List

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Load Gemini API Key from Streamlit secrets
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

# Gemini API endpoint
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

# Supported languages
SUPPORTED_LANGUAGES = ["Arabic", "Spanish", "French", "Urdu", "Chinese (Simplified)", "German"]

async def translate_text(input_text: str, target_language: str) -> str:
    """Translate text to the target language using Gemini API."""
    logger.info(f"Translating text to {target_language}: {input_text[:50]}...")

    if not input_text.strip():
        logger.error("Input text is empty.")
        raise ValueError("Input text cannot be empty.")
    if target_language not in SUPPORTED_LANGUAGES:
        logger.error(f"Unsupported target language: {target_language}")
        raise ValueError(f"Target language '{target_language}' is not supported. Choose from: {', '.join(SUPPORTED_LANGUAGES)}")

    prompt = f"Translate the following text to {target_language} accurately, preserving tone and context:\n\n'{input_text}'"

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    params = {"key": GEMINI_API_KEY}

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            logger.info("Sending request to Gemini API")
            response = await client.post(GEMINI_API_URL, params=params, json=payload)
            response.raise_for_status()

            data = response.json()
            logger.info("Received response from Gemini API")
            try:
                translated_text = data["candidates"][0]["content"]["parts"][0]["text"]
                logger.info("Translation successful")
                return translated_text
            except (KeyError, IndexError) as e:
                logger.error(f"Failed to parse API response: {str(e)}")
                raise Exception(f"Failed to parse API response: {str(e)}")
        except httpx.HTTPStatusError as e:
            error_msg = response.json().get("error", {}).get("message", response.text)
            logger.error(f"API request failed (status {response.status_code}): {error_msg}")
            raise Exception(f"API request failed: {error_msg}")
        except httpx.RequestError as e:
            logger.error(f"Network error during API request: {str(e)}")
            raise Exception(f"Network error: {str(e)}")

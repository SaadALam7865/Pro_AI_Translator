import streamlit as st
import asyncio
import logging
from agent_logic import translate_text, SUPPORTED_LANGUAGES

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

st.set_page_config(page_title="AI Translator 💬", page_icon="🌍")
st.title("🌍 Pro AI Translator")
st.markdown("Translate anything using **Gemini AI**")

# Initialize session state
if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""
if "error_message" not in st.session_state:
    st.session_state.error_message = ""
if "text_to_translate" not in st.session_state:
    st.session_state.text_to_translate = ""

# Input fields
st.session_state.text_to_translate = st.text_area("Enter text to translate", value=st.session_state.text_to_translate, height=150)
target_language = st.selectbox("Choose target language", SUPPORTED_LANGUAGES)

# Buttons
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Translate 🔄"):
        if not st.session_state.text_to_translate.strip():
            st.warning("Please enter some text to translate.")
            logger.warning("Empty input text provided")
        else:
            with st.spinner("Translating..."):
                try:
                    logger.info("Starting translation process")
                    st.session_state.translated_text = asyncio.run(translate_text(st.session_state.text_to_translate, target_language))
                    st.session_state.error_message = ""
                    st.success("Translation complete ✅")
                    logger.info("Translation completed successfully")
                except ValueError as e:
                    st.session_state.error_message = f"Invalid input: {str(e)}"
                    st.error(st.session_state.error_message)
                    logger.error(f"ValueError: {str(e)}")
                except Exception as e:
                    st.session_state.error_message = "Translation failed. Please check your input or try again later."
                    st.error(st.session_state.error_message)
                    logger.error(f"Translation error: {str(e)}")
with col2:
    if st.button("Clear 🗑️"):
        st.session_state.text_to_translate = ""
        st.session_state.translated_text = ""
        st.session_state.error_message = ""
        st.rerun()

# Display translated text
if st.session_state.translated_text:
    st.text_area("Translated Text", st.session_state.translated_text, height=150, disabled=True)

# Display error details for debugging (optional)
if st.session_state.error_message:
    st.markdown("**Debug Info**: Check logs for detailed error information.")
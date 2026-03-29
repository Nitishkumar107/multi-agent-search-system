import streamlit as st
import requests
from app.config.settings import Settings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

st.title("AI Agent UI")

model_name = st.selectbox("Select Model", Settings.ALLOWED_MODEL_NAMES)

system_prompt = st.text_area("System Prompt", "You are a helpful assistant.", height=70)

user_input = st.text_area("User Input", height=170)

allow_search = st.checkbox("Allow Web Search")

if st.button("Send") and user_input.strip():
    payload = {
        "model_name": model_name,
        "system_prompt": system_prompt,
        "user_input": [user_input],
        "allow_search": allow_search
    }
    try:
        logger.info("Sending request to backend")
        response = requests.post("http://127.0.0.1:8000/chat", json=payload)
        logger.info("Successfully received response from backend")

        if response.status_code == 200:
            agent_response = response.json()["response"]
            logger.info("Successfully received response from AI agent")
            st.subheader("AI Agent Response")
            st.markdown(agent_response.replace("\n", "<br>"), unsafe_allow_html=True)
        else:
            detail = response.json()["detail"]
            logger.error(f"Error received response from backend: {detail}")
            st.error(f"Error: {detail}")

    except Exception as e:
        error_msg = str(CustomException("Error received while sending request to the backend", error_detail=str(e)))
        logger.error(f"Error received while sending request to the backend: {e}")
        st.error(f"Error: {error_msg}")

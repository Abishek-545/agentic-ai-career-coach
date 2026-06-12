import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_MODEL = "gemini-flash-latest"


def get_secret(name: str):
    try:
        return st.secrets[name]
    except Exception:
        return os.getenv(name)


def get_gemini_client():
    api_key = get_secret("GEMINI_API_KEY")

    if not api_key:
        st.error("GEMINI_API_KEY not found. Add it to .env or Streamlit secrets.")
        st.stop()

    return genai.Client(api_key=api_key)


def get_adzuna_credentials():
    return get_secret("ADZUNA_APP_ID"), get_secret("ADZUNA_APP_KEY")
from langchain_mistralai import ChatMistralAI

from src.settings import app_settings


def get_llm() -> ChatMistralAI:
    return ChatMistralAI(
        model=app_settings.MISTRAL_MODEL,
        mistral_api_key=app_settings.MISTRAL_API_KEY,
        temperature=0,
    )

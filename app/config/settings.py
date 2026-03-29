from dotenv import load_dotenv
import os


load_dotenv()

class Settings:
    openrouter_api_key = os.getenv("openrouter_api_key")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    

    ALLOWED_MODEL_NAMES = [
        "qwen/qwen3-235b-a22b-thinking-2507",
        "upstage/solar-pro-3:free",
        "openai/gpt-oss-120b:free",
        "meta-llama/llama-3.3-70b-instruct:free",
        "x-ai/grok-4.1-fast:free",
    ]


settings = Settings()












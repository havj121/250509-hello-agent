import os
from dotenv import load_dotenv

load_dotenv()


def load_config():
    return {
        "deepseek_api_key": os.getenv("DEEPSEEK_API_KEY"),
        "deepseek_base_url": os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
        "deepseek_model": os.getenv("DEEPSEEK_MODEL", "deepseek-v4-flash"),
        "tavily_api_key": os.getenv("TAVILY_API_KEY"),
    }

# src/utils/config_loader.py
import os
from dotenv import load_dotenv

load_dotenv()

def get_openrouter_api_key():
    return os.getenv("OPENROUTER_API_KEY")

def get_huggingface_api_key():
    return os.getenv("HUGGINGFACE_API_KEY")

def get_perplexity_api_key():
    return os.getenv("PERPLEXITY_API_KEY")

def get_youtube_api_key():
    return os.getenv("YOUTUBE_API_KEY")

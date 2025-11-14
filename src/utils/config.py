"""Configuration module for loading environment variables."""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Ghost CMS Configuration
GHOST_URL = os.getenv("GHOST_URL")
GHOST_ADMIN_API_KEY = os.getenv("GHOST_ADMIN_API_KEY")

# LLM Provider
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")

# Observability Configuration
ENABLE_OBSERVABILITY = os.getenv("ENABLE_OBSERVABILITY", "true").lower() == "true"
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT", "blog-post-creator")
ENABLE_LANGSMITH = os.getenv("ENABLE_LANGSMITH", "false").lower() == "true"
EXPORT_METRICS = os.getenv("EXPORT_METRICS", "true").lower() == "true"

# Evaluation Configuration
ENABLE_EVALUATION = os.getenv("ENABLE_EVALUATION", "true").lower() == "true"
EXPORT_EVALUATION = os.getenv("EXPORT_EVALUATION", "true").lower() == "true"
MIN_QUALITY_SCORE = float(os.getenv("MIN_QUALITY_SCORE", "70"))  # Minimum acceptable quality score

def validate_config():
    """Validate that all required configuration is present."""
    missing = []

    if LLM_PROVIDER == "openai" and not OPENAI_API_KEY:
        missing.append("OPENAI_API_KEY")
    elif LLM_PROVIDER == "anthropic" and not ANTHROPIC_API_KEY:
        missing.append("ANTHROPIC_API_KEY")

    if not TAVILY_API_KEY:
        missing.append("TAVILY_API_KEY")

    if not GHOST_URL:
        missing.append("GHOST_URL")

    if not GHOST_ADMIN_API_KEY:
        missing.append("GHOST_ADMIN_API_KEY")

    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

    return True

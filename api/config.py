"""
Configuration management for Browser-Use API Server.
Loads environment variables and defines configuration constants.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .browser-use.env
ENV_FILE = Path.home() / ".browser-use.env"
load_dotenv(ENV_FILE)

# API Server Configuration
API_SERVER_KEY = os.getenv("API_SERVER_KEY")
if not API_SERVER_KEY:
    raise ValueError(
        "API_SERVER_KEY not found in environment. "
        f"Please add it to {ENV_FILE}"
    )

API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))

# Chrome CDP Configuration
CHROME_CDP_URL = os.getenv("CHROME_CDP_URL", "http://localhost:9222")

# Database Configuration
PROJECT_ROOT = Path(__file__).parent.parent
DATABASE_PATH = os.getenv(
    "DATABASE_PATH",
    str(PROJECT_ROOT / "api" / "tasks.db")
)

# Task Queue Configuration
MAX_QUEUE_SIZE = int(os.getenv("MAX_QUEUE_SIZE", "100"))
DEFAULT_TASK_TIMEOUT = int(os.getenv("DEFAULT_TASK_TIMEOUT", "300"))  # 5 minutes
MIN_TASK_TIMEOUT = 30  # 30 seconds
MAX_TASK_TIMEOUT = 3600  # 1 hour

# Webhook Configuration
WEBHOOK_RETRY_ATTEMPTS = int(os.getenv("WEBHOOK_RETRY_ATTEMPTS", "3"))
WEBHOOK_RETRY_DELAY = int(os.getenv("WEBHOOK_RETRY_DELAY", "2"))  # seconds
WEBHOOK_TIMEOUT = int(os.getenv("WEBHOOK_TIMEOUT", "10"))  # seconds

# Logging Configuration
LOG_DIR = PROJECT_ROOT / "logs"
LOG_FILE = LOG_DIR / "api.log"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Ensure log directory exists
LOG_DIR.mkdir(exist_ok=True)

# Browser-use API Keys (already loaded from .env)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
BROWSER_USE_API_KEY = os.getenv("BROWSER_USE_API_KEY")

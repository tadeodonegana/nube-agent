import os

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
TIENDANUBE_ACCESS_TOKEN = os.environ.get("TIENDANUBE_ACCESS_TOKEN", "")
TIENDANUBE_STORE_ID = os.environ.get("TIENDANUBE_STORE_ID", "")

MODEL = "openai:gpt-4o-mini"
USER_AGENT = os.environ.get("USER_AGENT", "Nube Agent")
BASE_URL = f"https://api.tiendanube.com/2025-03/{TIENDANUBE_STORE_ID}"


def validate() -> None:
    """Validate that all required environment variables are set."""
    missing = []
    if not OPENAI_API_KEY:
        missing.append("OPENAI_API_KEY")
    if not TIENDANUBE_ACCESS_TOKEN:
        missing.append("TIENDANUBE_ACCESS_TOKEN")
    if not TIENDANUBE_STORE_ID:
        missing.append("TIENDANUBE_STORE_ID")
    if missing:
        raise SystemExit(
            f"Missing required environment variables: {', '.join(missing)}\n"
            "Copy .env.example to .env and fill in the values."
        )

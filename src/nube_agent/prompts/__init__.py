"""System prompt loader for the Nube Agent."""

from pathlib import Path


def load_system_prompt() -> str:
    """Load the system prompt from the text file."""
    prompt_path = Path(__file__).parent / "system_prompt.txt"
    return prompt_path.read_text(encoding="utf-8")

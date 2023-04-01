"""Configuration file for the project.
"""
from typing import Callable, Dict

# Model for the API call
OPEN_AI_MODEL = "gpt-3.5-turbo"

# System message config
system_message: Callable[[], Dict[str, str]] = lambda: {
    "role": "system",
    "content": "You are a helpful research assistant. Please explain"
    " the papers in point form with markdown format to your teammate.",
}

# User content config
user_content: Callable[[str], Dict[str, str]] = lambda page_text: {
    "role": "user",
    "content": f"Summarize this: {page_text}",
}

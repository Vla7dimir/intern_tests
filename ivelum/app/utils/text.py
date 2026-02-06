"""Text modification utilities (™ after 6-letter words)."""

import re

from app.logger import get_logger

logger = get_logger(__name__)

# Compiled regex for better performance
_TRADEMARK_PATTERN = re.compile(r"\b([a-zA-Z]{6})\b")


def add_trademark(text: str) -> str:
    """Add ™ after each word that is exactly 6 Latin letters.

    Args:
        text: Input text to process.

    Returns:
        Text with ™ added after 6-letter words.

    Examples:
        >>> add_trademark("The visual report")
        'The visual™ report™'
    """
    if not isinstance(text, str):
        logger.warning("Invalid input type", extra={"type": type(text).__name__})
        return str(text) if text is not None else ""
    return _TRADEMARK_PATTERN.sub(r"\1™", text)

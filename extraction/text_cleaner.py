# extraction/text_cleaner.py

import re


def clean_text(text: str) -> str:
    """
    Cleans text while preserving semantic integrity.
    Avoids over-destroying structure for BERT.
    """

    if not text:
        return ""

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    # Remove excessive special characters (but keep basic punctuation)
    text = re.sub(r"[^\w\s.,;:!?-]", "", text)

    return text.strip()

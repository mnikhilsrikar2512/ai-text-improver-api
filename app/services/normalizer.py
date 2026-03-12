import re


def normalize_text(text: str) -> str:

    text = text.strip()

    # remove multiple spaces
    text = re.sub(r"\s+", " ", text)

    # normalize quotes
    text = text.replace("’", "'")

    # lowercase first for processing
    text = text.lower()

    # basic capitalization
    if text:
        text = text[0].upper() + text[1:]

    return text
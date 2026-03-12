import re


def validate_input(text: str):

    text = text.strip()

    if len(text) < 2:
        raise ValueError("Text too short")

    if len(text) > 300:
        raise ValueError("Text too long")

    return text


def is_meaningful(text):

    # detect random keyboard spam
    if re.fullmatch(r"[a-zA-Z]{8,}", text.lower()):
        return False

    return True
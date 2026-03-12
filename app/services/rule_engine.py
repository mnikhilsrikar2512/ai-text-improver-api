import re

def rule_based_improvement(text: str):
    t = text.lower().strip()

    # Sick leave
    if re.search(r"\bsick\s*leave\b", t):
        return [
            "I will be taking sick leave today.",
            "I require sick leave today.",
            "I will be on sick leave today."
        ]

    # Not well / illness
    if re.search(r"\b(not\s*well|fever|ill|unwell)\b", t):
        return [
            "I am not feeling well today and will be unable to come to the office.",
            "Due to illness, I will be unable to attend the office today.",
            "I am unwell today and will not be able to come to the office."
        ]

    # Family related leave
    if re.search(r"\bfamily\b", t):
        return [
            "I need to take leave today due to a family matter.",
            "I will be unavailable today due to a family commitment.",
            "I need to attend to a family matter today and will be on leave."
        ]

    # Meeting absence
    if "can't attend" in t or "cannot attend" in t:
        return [
            "I will be unable to attend the meeting today.",
            "Unfortunately, I cannot attend the meeting today.",
            "I regret that I will not be able to attend the meeting today."
        ]

    return None
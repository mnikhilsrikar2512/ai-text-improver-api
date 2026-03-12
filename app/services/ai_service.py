import httpx
import json
import time
from app.config import OLLAMA_URL, MODEL_NAME, OLLAMA_TIMEOUT, OLLAMA_RETRIES
import re
import asyncio

PROMPT_TEMPLATE = """
You are a professional workplace writing assistant used in an HR leave management system.

Your job is to rewrite a user's message so it sounds clear, polite, and professional.

IMPORTANT RULES:

1. Preserve the original meaning exactly.
2. Correct grammar and spelling.
3. Improve professionalism.
4. Generate EXACTLY 3 improved versions.
5. Each sentence must be concise (max 20 words).
6. Do NOT repeat the original sentence.
7. Do NOT add explanations or commentary.
8. Do NOT ask questions or suggest actions.
9. Each sentence must begin with "I".
10. Each sentence must sound natural in workplace communication.

Examples of good rewrites:

Input: "i cant come office today because fever"
Output:
I will be unable to come to the office today due to a fever.
I cannot attend the office today as I am experiencing a fever.
I will not be able to come to the office today because I have a fever.

Input: "sick leave"
Output:
I will be taking sick leave today.
I need to take sick leave today.
I will be on sick leave today.

Now rewrite this sentence.

Sentence:
{text}

Return ONLY 3 sentences.
Each sentence must be on a new line.
Do not number them.
"""


async def call_ollama(prompt):
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                OLLAMA_URL,
                json={
                    "model": MODEL_NAME,
                    "prompt": prompt,
                    "stream": False
                }
            )
            data = response.json()
            return data.get("response")
    except Exception:
        return None


def parse_suggestions(text):

    lines = text.split("\n")

    suggestions = []

    for line in lines:

        clean = line.strip()

        if not clean:
            continue

        clean = re.sub(r'^[0-9]+[\.\)]\s*', '', clean)

        suggestions.append(clean)

    return suggestions[:3]


def fallback_suggestions(text):

    return [
        text,
        f"I would like to inform you that {text.lower()}",
        f"Please note that {text.lower()}."
    ]


async def generate_suggestions(text):

    prompt = PROMPT_TEMPLATE.format(text=text)

    result = await call_ollama(prompt)

    if not result:
        return fallback_suggestions(text)

    suggestions = parse_suggestions(result)

    if len(suggestions) < 3:
        return fallback_suggestions(text)

    return suggestions
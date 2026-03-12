import time
from fastapi import APIRouter, HTTPException, Request

from app.models.schemas import ImproveRequest
from app.services.ai_service import generate_suggestions
from app.services.cache_service import get_cache, set_cache
from app.services.validation_service import validate_input, is_meaningful
from app.services.rule_engine import rule_based_improvement
from app.services.semantic_cache import get_semantic_cache, set_semantic_cache
from app.services.rate_limiter import check_rate_limit
from app.utils.logger import logger
from app.services.normalizer import normalize_text
from app.services.deduplicator import deduplicate_suggestions
from app.services.metrics import increment
from app.services.vector_index import search_intent, learn_new_example
from app.services.template_service import get_template

router = APIRouter()


@router.post("/improve-text")
async def improve_text(request: ImproveRequest, req: Request):

    start = time.time()

    client_id = req.client.host
    check_rate_limit(client_id)

    try:
        text = normalize_text(validate_input(request.text))
        increment("requests_total")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not is_meaningful(text):
        return {
            "original": text,
            "suggestions": ["Unable to determine the request."],
            "cached": False,
            "latency_ms": 1
        }

    cache_key = f"text:{text.lower()}"

    # -----------------------------
    # Exact Cache
    # -----------------------------

    cached = get_cache(cache_key)

    if cached and not request.force_llm:

        increment("cache_hits")

        latency = int((time.time() - start) * 1000)

        logger.info(f"text='{text}' source='cache' latency={latency}ms")

        return {
            "original": text,
            "suggestions": cached,
            "cached": True,
            "latency_ms": latency
        }

    # -----------------------------
    # Rule Engine
    # -----------------------------

    if not request.force_llm:

        rule_result = rule_based_improvement(text)

        if rule_result:

            increment("rule_hits")

            set_cache(cache_key, rule_result)
            set_semantic_cache(text, rule_result)

            latency = int((time.time() - start) * 1000)

            logger.info(
                f"text='{text}' source='rule_engine' latency={latency}ms"
            )

            return {
                "original": text,
                "suggestions": rule_result,
                "cached": False,
                "latency_ms": latency
            }

    # -----------------------------
    # Semantic Cache
    # -----------------------------

    semantic_result = get_semantic_cache(text)

    if semantic_result and not request.force_llm:

        increment("semantic_hits")

        latency = int((time.time() - start) * 1000)

        logger.info(
            f"text='{text}' source='semantic_cache' latency={latency}ms"
        )

        return {
            "original": text,
            "suggestions": semantic_result,
            "cached": True,
            "latency_ms": latency
        }

    # -----------------------------
    # Vector Router
    # -----------------------------

    if not request.force_llm:

        intent = search_intent(text)

        if intent:

            template = get_template(intent)

            if template:

                increment("router_hits")

                set_cache(cache_key, template)
                set_semantic_cache(text, template)

                latency = int((time.time() - start) * 1000)

                logger.info(
                    f"text='{text}' source='vector_router' latency={latency}ms"
                )

                return {
                    "original": text,
                    "suggestions": template,
                    "cached": False,
                    "latency_ms": latency,
                    "source": "vector_router"
                }

    # -----------------------------
    # LLM Fallback
    # -----------------------------

    increment("llm_calls")

    suggestions = await generate_suggestions(text)

    suggestions = deduplicate_suggestions(suggestions)

    set_cache(cache_key, suggestions)
    set_semantic_cache(text, suggestions)

    # Adaptive Learning
    detected_intent = search_intent(text)

    if not detected_intent:

        if "sick" in text.lower() or "fever" in text.lower():
            learn_new_example(text, "sick_leave")

        elif "family" in text.lower() or "function" in text.lower():
            learn_new_example(text, "family_leave")

        elif "meeting" in text.lower():
            learn_new_example(text, "meeting_absence")

    latency = int((time.time() - start) * 1000)

    logger.info(
        f"text='{text}' source='llm' latency={latency}ms"
    )

    return {
        "original": text,
        "suggestions": suggestions,
        "cached": False,
        "latency_ms": latency
    }
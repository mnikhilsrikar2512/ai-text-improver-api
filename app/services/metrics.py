metrics = {
    "requests_total": 0,
    "cache_hits": 0,
    "semantic_hits": 0,
    "router_hits": 0,
    "rule_hits": 0,
    "llm_calls": 0
}


def increment(metric):

    if metric in metrics:
        metrics[metric] += 1


def get_metrics():
    return metrics
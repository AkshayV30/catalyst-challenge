def resolve_weights(mode_config: dict) -> dict:
    weights = mode_config["weights"]

    match = weights["match"]
    engagement = weights["engagement"]

    return {
        "match": round(match, 2),
        "engagement": round(engagement, 2),
    }
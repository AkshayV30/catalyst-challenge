MODE_WEIGHTS = {
    "very_loose":   {"match": 0.5,  "engagement": 0.5},
    "loose":        {"match": 0.55, "engagement": 0.45},
    "balanced":     {"match": 0.6,  "engagement": 0.4},
    "default":      {"match": 0.7,  "engagement": 0.3},
    "focused":      {"match": 0.75, "engagement": 0.25},
    "strict":       {"match": 0.85, "engagement": 0.15},
    "very_strict":  {"match": 0.9,  "engagement": 0.1},
}


def resolve_weights(input_weights: dict | None):
    DEFAULT_MODE = "default"
    MIN_MATCH = 0.5
    MAX_MATCH = 0.9

    match = None

    if input_weights and "match" in input_weights:
        try:
            match = float(input_weights["match"])
        except (ValueError, TypeError):
            match = None

 
    if match is None and input_weights and "mode" in input_weights:
        mode = input_weights["mode"]
        match = MODE_WEIGHTS.get(mode, MODE_WEIGHTS[DEFAULT_MODE])["match"]

   
    if match is None:
        match = MODE_WEIGHTS[DEFAULT_MODE]["match"]

   
    match = max(MIN_MATCH, min(MAX_MATCH, match))

  
    engagement = 1 - match

   
    match = round(match, 2)
    engagement = round(1 - match, 2)

    return {
        "match": match,
        "engagement": engagement,
    }
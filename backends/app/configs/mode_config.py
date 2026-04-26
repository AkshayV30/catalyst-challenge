from typing import Dict
MODE_CONFIG = {
    "very_loose": {
        "filter": {"min_skill_overlap": 1, "must_have_required": False},
        "weights": {"match": 0.5, "engagement": 0.5},
        "jd_prompt_mode": "very_loose"
    },

    "loose": {
        "filter": {"min_skill_overlap": 1, "must_have_required": False},
        "weights": {"match": 0.55, "engagement": 0.45},
        "jd_prompt_mode": "loose"
    },

    "balanced": {
        "filter": {"min_skill_overlap": 2, "must_have_required": False},
        "weights": {"match": 0.6, "engagement": 0.4},
        "jd_prompt_mode": "balanced"
    },

    "default": {
        "filter": {"min_skill_overlap": 2, "must_have_required": False},
        "weights": {"match": 0.7, "engagement": 0.3},
        "jd_prompt_mode": "balanced"
    },

    "focused": {
        "filter": {"min_skill_overlap": 3, "must_have_required": True},
        "weights": {"match": 0.75, "engagement": 0.25},
        "jd_prompt_mode": "focused"
    },

    "strict": {
        "filter": {"min_skill_overlap": 3, "must_have_required": True},
        "weights": {"match": 0.85, "engagement": 0.15},
        "jd_prompt_mode": "strict"
    },

    "very_strict": {
        "filter": {"min_skill_overlap": 4, "must_have_required": True},
        "weights": {"match": 0.9, "engagement": 0.1},
        "jd_prompt_mode": "very_strict"
    },
}
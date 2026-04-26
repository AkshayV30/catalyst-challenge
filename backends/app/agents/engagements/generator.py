def generate_recruiter_message(jd, candidate):
    return {
        "role": "recruiter",
        "message": (
            f"Hi {candidate['name']}, "
            f"we're hiring for {jd['role']} involving "
            f"{', '.join(jd.get('skills', [])[:3])}. "
            "Would you be open to explore this opportunity?"
        )
    }
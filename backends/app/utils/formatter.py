def format_candidate(c: dict) -> str:
    return f"""
Name: {c.get("name")}
Role: {c.get("role")}
Experience: {c.get("experience_years")} years
Skills: {", ".join(c.get("skills", []))}
Domain: {c.get("domain")}
Summary: {c.get("summary")}
"""
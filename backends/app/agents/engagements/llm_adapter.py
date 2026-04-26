from app.agents.engagements.prompts import engagement_prompt

async def llm_engagement(llm_router, jd, candidate):
    if not llm_router:
        return None

    prompt = engagement_prompt(jd, candidate)
    
    return await llm_router("engagement", prompt)
 



from app.agents.engagements.generator import generate_recruiter_message
from app.agents.engagements.simulator import simulate_response
from app.agents.engagements.llm_adapter import llm_engagement


class EngagementAgent:
    def __init__(self, llm_router):
        self.llm_router = llm_router

    async def engage(self, jd, candidate):
        message = generate_recruiter_message(jd, candidate)

        llm_resp = await llm_engagement(
            self.llm_router,
            jd,
            candidate
        )

        if llm_resp:
            response = llm_resp
        else:
            response = simulate_response(jd, candidate)

        if not response.get("interest_score"):
            response["interest_score"] = 50

        return {
            "conversation": [
                message,
                {"role": "candidate", "message": response["reply"]}
            ],
            "interest_score": response["interest_score"],
            "signals": response["signals"]
        }
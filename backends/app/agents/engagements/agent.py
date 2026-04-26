from app.agents.engagements.generator import generate_recruiter_message
from app.agents.engagements.simulator import simulate_response
from app.agents.engagements.llm_adapter import llm_engagement


# class EngagementAgent:
#     def __init__(self, llm_router):
#         self.llm_router = llm_router

#     async def engage(self, jd, candidate):
#         message = generate_recruiter_message(jd, candidate)

#         llm_resp = await llm_engagement(
#             self.llm_router,
#             jd,
#             candidate
#         )

#         if llm_resp:
#             response = llm_resp
#         else:
#             response = simulate_response(jd, candidate)

#         if not response.get("interest_score"):
#             response["interest_score"] = 50

#         return {
#             "conversation": [
#                 message,
#                 {"role": "candidate", "message": response["reply"]}
#             ],
#             "interest_score": response["interest_score"],
#             "signals": response["signals"]
#         }

from app.core.loggers import logger


class EngagementAgent:
    def __init__(self, llm_router):
        self.llm_router = llm_router

    async def engage(self, jd, candidate):
        log = logger.bind(
            stage="engagement",
            candidate_id=candidate.get("id"),
            name=candidate.get("name")
        )

        try:
            log.debug("Engagement started")

            # ---------------- MESSAGE GENERATION ----------------
            message = generate_recruiter_message(jd, candidate)

            log.debug(f"Recruiter message:\n{message}")

            # ---------------- LLM CALL ----------------
            llm_resp = await llm_engagement(
                self.llm_router,
                jd,
                candidate
            )

            # ---------------- RESPONSE SOURCE ----------------
            if llm_resp:
                response = llm_resp
                source = "llm"
                log.info("LLM engagement used")
            else:
                response = simulate_response(jd, candidate)
                source = "simulated"
                log.warning("Fallback to simulated response")

            log.debug(f"Raw response ({source}):\n{response}")

            # ---------------- VALIDATION ----------------
            if not isinstance(response, dict):
                log.error(f"Invalid response format: {response}")
                response = {
                    "interest_score": 0,
                    "signals": [],
                    "reply": ""
                }

            # fallback score
            if not response.get("interest_score"):
                log.warning("Missing interest_score → defaulting to 50")
                response["interest_score"] = 50

            # ---------------- FINAL STRUCT ----------------
            result = {
                "conversation": [
                    message,
                    {"role": "candidate", "message": response.get("reply", "")}
                ],
                "interest_score": response.get("interest_score", 0),
                "signals": response.get("signals", [])
            }

            log.info(
                f"Engagement complete | score={result['interest_score']} | source={source}"
            )

            return result

        except Exception as e:
            log.exception("Engagement failed")

            return {
                "conversation": [],
                "interest_score": 0,
                "signals": [],
                "error": str(e)
            }
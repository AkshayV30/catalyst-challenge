from app.router.llm_router import route
# import json

async def parse_jd(jd: str):
          prompt = f"""
      Extract structured JSON:

          {{
            "role": "",
            "skills": [],
            "experience_years": "",
            "must_have": [],
            "nice_to_have": []
          }}

      JD:
        {jd}
      """
          
          return await route("jd_parser", prompt)



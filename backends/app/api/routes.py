from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

from app.services.pipeline import run_pipeline


router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def root():
    return """
    <html>
        <head>
            <title>AI Recruiter Backend</title>
        </head>
        <body>
            <h1>🚀 Backend API is Running</h1>
            <p>Status: OK</p>
            <p>Use <code>/docs</code> for API testing</p>
        </body>
    </html>
    """


@router.post("/scout")
def scout(jd: dict):
    try:
        if "jd" not in jd:
            raise HTTPException(status_code=400, detail="Missing 'jd' field")

        return run_pipeline(jd["jd"])

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
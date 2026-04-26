from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from app.core.metrics import metrics
from app.services.pipeline_service import run_pipeline

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def root():
  
    return """
    <html>
        <head><title>AI Recruiter Backend</title></head>
        <body>
            <h1>Backend API is Running</h1>
            <p>Status: OK</p>
        </body>
    </html>
    """


@router.post("/scout")
async def scout(payload: dict):
    if not isinstance(payload, dict):
        raise HTTPException(status_code=400, detail="Invalid JSON body")

    jd = payload.get("jd")
    mode = payload.get("mode", "default")

    if not jd:
        raise HTTPException(status_code=400, detail="Missing 'jd' field")

    return await run_pipeline(jd, mode)


@router.get("/metrics")
def get_metrics():
    return metrics.snapshot()
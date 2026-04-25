from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

from app.services.pipeline_service import run_pipeline
from app.core.metrics import metrics

from app.utils.score_weights import resolve_weights

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def root():
    return """
    <html>
        <head>
            <title>AI Recruiter Backend</title>
        </head>
        <body>
            <h1> Backend API is Running</h1>
            <p>Status: OK</p>
           
        </body>
    </html>
    """

@router.post("/scout")
async def scout(payload: dict):
    jd = payload.get("jd")
    weights_input = payload.get("weights", {})

    if not jd:
        raise HTTPException(status_code=400, detail="Missing 'jd' field")

    weights = resolve_weights(weights_input)
    mode = weights_input.get("mode", "default")

    return await run_pipeline(jd, weights, mode)



@router.get("/metrics")
def get_metrics():
    return metrics.snapshot()
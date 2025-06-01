from fastapi import FastAPI, Depends, HTTPException, Request, status
from pydantic import BaseModel
import structlog
import hmac
import hashlib
import os
from .services.onboarding import onboard_organization

logger = structlog.get_logger()

SECRET_TOKEN = os.getenv("ONBOARDER_SECRET", "")

app = FastAPI(title="IPFS Onboarder", version="0.1.0")

class OnboardPayload(BaseModel):
    org_name: str
    owner_email: str
    tier: str

async def verify_request(request: Request):
    token = request.headers.get("X-Auth-Token")
    if not SECRET_TOKEN:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Secret not configured")
    if not token or not hmac.compare_digest(token, SECRET_TOKEN):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

@app.post("/onboard")
async def onboard(payload: OnboardPayload, request: Request = Depends(verify_request)):
    result = await onboard_organization(payload)
    return result

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

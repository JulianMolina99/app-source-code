from fastapi import APIRouter, Header, HTTPException, Request
from app.services.jwt_handler import verify_jwt
from app.core.config import settings

router = APIRouter()

# Define valid HTTP POST endpoint for '/DevOps'
@router.post("/DevOps")
async def devops_endpoint(
    request: Request,
    X_Parse_REST_API_Key: str = Header(...),
    X_JWT_KWY: str = Header(...),
):
    # Validate API Key
    if X_Parse_REST_API_Key != settings.API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # Validate JWT
    if not verify_jwt(X_JWT_KWY):
        raise HTTPException(status_code=401, detail="Invalid JWT")

    # Extract and validate JSON payload
    body = await request.json()

    required_fields = ["message", "to", "from", "timeToLifeSec"]
    if not all(field in body for field in required_fields):
        raise HTTPException(status_code=400, detail="Incomplete payload")

    # Generate response message
    message = f"Hello {body['to']} your message will be send"

    return {"message": message}

# Define invalid methods for '/DevOps'
@router.get("/DevOps")
@router.put("/DevOps")
@router.delete("/DevOps")
@router.patch("/DevOps")
async def invalid_method():
    # Return 405 error for invalid HTTP methods
    raise HTTPException(status_code=405, detail="Method Not Allowed")

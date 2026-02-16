from fastapi import FastAPI, HTTPException, Security, Depends, status
from fastapi.security import APIKeyHeader, APIKeyQuery
from pydantic import BaseModel
from typing import List, Optional
import os
from services.epa import EPAClient

app = FastAPI(title="Company Intelligence API")

# Security
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
api_key_query = APIKeyQuery(name="token", auto_error=False)

async def get_api_key(
    header_key: str = Security(api_key_header),
    query_key: str = Security(api_key_query)
):
    internal_token = os.getenv("INTERNAL_API_TOKEN")
    
    # If no token is set in env, we might want to fail open or closed. 
    # For security, we should probably fail closed or warn. 
    # Here we assume if it's not set, auth is disabled (dev mode) or rejected.
    # Let's reject to be safe for "production" request.
    if not internal_token:
        # If the user hasn't set up the env var yet, we can either:
        # 1. Allow all (risky for prod)
        # 2. Reject all (confusing for dev)
        # Let's log a warning and reject to force setup.
        print("WARNING: INTERNAL_API_TOKEN not set. Rejecting request.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server misconfiguration: API token not set"
        )

    if header_key == internal_token:
        return header_key
    elif query_key == internal_token:
        return query_key
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )

# Data Models
class CompanyRequest(BaseModel):
    company_name: str
    website: str

class VerificationResponse(BaseModel):
    epa_facilities: List[dict]

# Services
epa_client = EPAClient()

@app.post("/enrich", response_model=VerificationResponse)
async def enrich_company(request: CompanyRequest, api_key: str = Depends(get_api_key)):
    """
    Enriches company data with EPA facilities.
    Requires API Key authentication.
    """
    company_name = request.company_name
    
    # EPA Facilities Lookup
    facilities = epa_client.search_facilities(company_name)
    
    return VerificationResponse(
        epa_facilities=facilities
    )

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

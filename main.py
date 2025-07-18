# ✅ main.py
from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from backend.routes import upload, scrape, chat
from auth_clerk import get_current_user_id, get_current_user, verify_clerk_token
import requests

app = FastAPI(title="RAG Q&A Engine", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8501", "http://localhost:8502"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"msg": "RAG Q&A Engine API", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/verify-token")
async def verify_token_post(request: Request):
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return {"error": "No Authorization header found", "status": "missing_auth"}
        
        if not auth_header.startswith("Bearer "):
            return {"error": "Authorization header doesn't start with 'Bearer '", "status": "invalid_format"}
        
        token = auth_header.split(" ")[1]
        
        try:
            payload = verify_clerk_token(token)
            return {
                "status": "valid",
                "user_id": payload.get("sub"),
                "email": payload.get("email"),
                "token_valid": True,
                "payload": payload
            }
        except Exception as e:
            return {
                "status": "invalid",
                "error": str(e),
                "token_valid": False
            }
    except Exception as e:
        return {"status": "error", "error": f"Request processing error: {e}"}

# Debug endpoint - same as reference code
@app.post("/debug-auth")
async def debug_auth(request: Request):
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return {"error": "No Authorization header found", "status": "missing_auth"}
        
        if not auth_header.startswith("Bearer "):
            return {"error": "Authorization header doesn't start with 'Bearer '", "status": "invalid_format"}
        
        token = auth_header.split(" ")[1]
        
        try:
            payload = verify_clerk_token(token)
            return {
                "status": "success",
                "message": "Token is valid!",
                "user_id": payload.get("sub"),
                "email": payload.get("email")
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "status_code": 401
            }
    except Exception as e:
        return {"status": "error", "error": f"Request processing error: {e}"}

# User info endpoint for Streamlit
@app.get("/user-info")
async def get_user_info(current_user: dict = Depends(get_current_user)):
    """Get current user information for display in Streamlit"""
    try:
        return {
            "status": "success",
            "user_id": current_user.get("sub"),
            "email": current_user.get("email"),
            "name": current_user.get("name"),
            "first_name": current_user.get("given_name"),
            "last_name": current_user.get("family_name"),
            "username": current_user.get("username"),
            "image_url": current_user.get("picture")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving user info: {e}")

# Simple auth status endpoint
@app.get("/auth-status")
async def auth_status(user_id: str = Depends(get_current_user_id)):
    """Simple endpoint to check if authentication is working"""
    return {"status": "authenticated", "user_id": user_id}

# Apply Clerk JWT auth to all routers globally
app.include_router(upload.router, dependencies=[Depends(get_current_user)])
app.include_router(scrape.router, dependencies=[Depends(get_current_user)])
app.include_router(chat.router, dependencies=[Depends(get_current_user)])

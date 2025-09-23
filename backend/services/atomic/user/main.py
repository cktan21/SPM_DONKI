from fastapi import FastAPI, Request, Depends, HTTPException, Header
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabaseClient import SupabaseClient
from dotenv import load_dotenv
import os
import uvicorn
import jwt
from jwt import PyJWTError, ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta

load_dotenv()

app = FastAPI(title="User Service")
supabase = SupabaseClient()

# -----------------------
# CORS
# -----------------------
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------
# JWT config
# -----------------------
JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")
JWT_ALGORITHM = "HS256"

# -----------------------
# Models
# -----------------------
class SignupRequest(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

# -----------------------
# Helper: current user from cookie
# -----------------------
def get_current_user_from_cookie(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
            audience="authenticated",
            options={"verify_exp": False}  # use refresh token for expiry
        )
        auth_id = payload.get("sub")
        if not auth_id:
            raise HTTPException(status_code=401, detail="Invalid token: no sub")
    except (ExpiredSignatureError, InvalidTokenError, PyJWTError) as e:
        raise HTTPException(status_code=401, detail=f"JWT error: {str(e)}")

    user_data = supabase.client.table("USER").select("*").eq("auth_id", auth_id).execute()
    if not user_data.data:
        raise HTTPException(status_code=401, detail="User not found")
    return user_data.data[0]

# -----------------------
# Signup
# -----------------------
@app.post("/signup")
def signup(req: SignupRequest):
    try:
        resp = supabase.client.auth.sign_up({"email": req.email, "password": req.password})
        if not resp.user:
            return JSONResponse(status_code=400, content={"detail": "Signup failed"})

        # Auto-login
        session = supabase.client.auth.sign_in_with_password({"email": req.email, "password": req.password})

        response = JSONResponse(
            status_code=201,
            content={"message": "User signed up and logged in", "user_id": resp.user.id}
        )
        # Set cookies
        response.set_cookie(
            key="access_token",
            value=session.session.access_token,
            httponly=True,
            secure=False,       # False for localhost; True for HTTPS in prod
            samesite="lax",
            max_age=3600        # 1 hour
        )
        response.set_cookie(
            key="refresh_token",
            value=session.session.refresh_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=14*24*3600  # 2 weeks
        )
        return response

    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e) or "Internal server error"})


# -----------------------
# Login
# -----------------------
@app.post("/login")
def login(req: LoginRequest):
    try:
        resp = supabase.client.auth.sign_in_with_password({"email": req.email, "password": req.password})
        if not resp.session:
            return JSONResponse(status_code=401, content={"detail": "Invalid email or password"})

        access_token = resp.session.access_token
        refresh_token = resp.session.refresh_token

        response = JSONResponse(
            status_code=200,
            content={"message": "Login successful"}
        )
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=3600
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=14*24*3600
        )
        return response

    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e) or "Internal server error"})


# -----------------------
# Logout
# -----------------------
@app.post("/logout")
def logout():
    response = JSONResponse(status_code=200, content={"message": "Logged out"})
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response

# -----------------------
# Check logged in
# -----------------------
@app.get("/me")
def me(current_user: dict = Depends(get_current_user_from_cookie)):
    return JSONResponse(status_code=200, content={"user": current_user})

# -----------------------
# Get user by userID -- used for backend check
# -----------------------
INTERNAL_API_KEY = os.getenv("INTERNAL_API_KEY")

def verify_internal_api_key(x_internal_api_key: str = Header(None, convert_underscores=False)):
    """Verify internal API key for service-to-service communication"""
    if not INTERNAL_API_KEY:
        # Fail fast so you don’t silently compare against None
        raise HTTPException(status_code=500, detail="INTERNAL_API_KEY is not set on the server")

    if not x_internal_api_key or x_internal_api_key != INTERNAL_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing internal API key")

    return True


# Internal endpoint for service-to-service user validation by ID
@app.get("/internal/{user_id}")
def validate_user_internal(user_id: str):
    """
    Internal endpoint for service-to-service user validation by user ID.
    Uses INTERNAL_API_KEY from environment directly (no header needed).
    """
    try:
        # Fetch user from user table by ID
        user_data = supabase.client.table("USER").select(
            "id, auth_id, email, role, created_at"
        ).eq("id", user_id).execute()

        if not user_data.data:
            raise HTTPException(status_code=404, detail="User not found")

        user = user_data.data[0]

        # Return minimal info (and key if you want to confirm it's loaded)
        return {
            "id": user["id"],
            "auth_id": user["auth_id"],
            "email": user["email"],
            "role": user["role"],
            "created_at": user["created_at"],
            "exists": True,
            "internal_api_key": INTERNAL_API_KEY,  # optional: expose for debug
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to validate user: {str(e)}"
        )


# -----------------------
# Health check
# -----------------------
@app.get("/")
def read_root():
    return JSONResponse(status_code=200, content={"message": "User Service is running"})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5100)

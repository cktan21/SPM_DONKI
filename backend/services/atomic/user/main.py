from fastapi import FastAPI, Request, Depends, HTTPException
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
# Health check
# -----------------------
@app.get("/")
def read_root():
    return JSONResponse(status_code=200, content={"message": "User Service is running"})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5100)

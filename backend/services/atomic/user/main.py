from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import Response
from pydantic import BaseModel
from supabaseClient import SupabaseClient
from dotenv import load_dotenv
import uvicorn
import jwt  # you can use PyJWT
from jwt import PyJWTError, ExpiredSignatureError, InvalidTokenError
import os

load_dotenv()

app = FastAPI(title="Atomic Microservice: User Service")
supabase = SupabaseClient()

# Get your Supabase JWT secret from .env
JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")  # or os.getenv("SUPABASE_JWT_SECRET")
JWT_ALGORITHM = "HS256"

class SignupRequest(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

# -----------------------
# Decode JWT and get user
# -----------------------
def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="No token provided")

    token = auth_header.replace("Bearer ", "")

    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
            audience="authenticated",  # or options={"verify_aud": False}
        )
        print("Decoded sub:", payload["sub"])
        auth_id = payload.get("sub")
        if not auth_id:
            raise HTTPException(status_code=401, detail="No subject (sub) in token")
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    except PyJWTError as e:
        raise HTTPException(status_code=401, detail=f"JWT error: {str(e)}")

    # Fetch user from user table
    user_data = supabase.client.table("user").select("*").eq("auth_id", auth_id).execute()
    if not user_data.data:
        raise HTTPException(status_code=401, detail="User not found")

    return user_data.data[0]

# -----------------------
# Signup
# -----------------------
@app.post("/signup")
def signup(req: SignupRequest):
    resp = supabase.client.auth.sign_up({
        "email": req.email,
        "password": req.password
    })
    if not resp.user:
        raise HTTPException(status_code=400, detail="Signup failed")

    # no need to insert into user table manually if you have the trigger
    return {"message": "User signed up", "user_id": resp.user.id}

# -----------------------
# Login
# -----------------------
@app.post("/login")
def login(req: LoginRequest):
    resp = supabase.client.auth.sign_in_with_password({
        "email": req.email,
        "password": req.password
    })
    if not resp.session:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {
        "access_token": resp.session.access_token,
        "refresh_token": resp.session.refresh_token
    }

# -----------------------
# Logout   ->  Having issues with service role key, redirect to frontend logout
# -----------------------
# @app.post("/logout")
# def logout(request: Request):
#     token = request.headers.get("Authorization")
#     if not token:
#         raise HTTPException(status_code=401, detail="No token provided")

#     token = token.replace("Bearer ", "")

#     try:
#         # Invalidate the session using the admin endpoint
#         resp = supabase.client.auth.admin.sign_out(token)
#         if resp.get("error"):
#             raise HTTPException(status_code=400, detail=resp["error"]["message"])
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Logout failed: {e}")

#     return {"message": "Logged out successfully"}

# -----------------------
# Role-protected endpoint
# -----------------------
@app.get("/lockedf")
def get_lockedf(current_user: dict = Depends(get_current_user)):
    if current_user['role'] not in ["Manager", "Director"]:
        raise HTTPException(status_code=403, detail="Access denied")
    return {"lockedf": []}

# -----------------------
# Health check
# -----------------------
@app.get("/")
def read_root():
    return {"message": "User Service is running 🚀🥺"}

@app.get("/favicon.ico")
async def get_favicon():
    return Response(status_code=204)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5100)

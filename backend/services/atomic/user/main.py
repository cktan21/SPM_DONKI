from fastapi import FastAPI, Request, Depends, HTTPException, Header, BackgroundTasks
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

#--------------------------------------- ROUTES ------------------------------------------------

@app.post("/login")
async def login(req: LoginRequest):
    """
    Login endpoint.
    Expects: JSON body with email and password.
    Returns: access_token (for debugging), sets cookies for session automatically. 
             Also encodes a JWT with simple information like id, email, role, name and set as cookie
    Cookie expiry:
    - access_token: 1 hour
    - refresh_token: 24 hours
    - user_data: 1 hour
    """
    try:
        # Authenticate with Supabase
        resp = supabase.client.auth.sign_in_with_password({
            "email": req.email,
            "password": req.password
        })
        if not resp.session:
            return JSONResponse(status_code=401, content={"detail": "Invalid email or password"})
        
        access_token = resp.session.access_token
        refresh_token = resp.session.refresh_token
        
        # Fetch user data from USER database
        auth_id = resp.user.id ##id here is auth id
        user_data = supabase.client.table("USER").select(
            "id, email, role, name"
        ).eq("auth_id", auth_id).execute()
        
        if not user_data.data:
            return JSONResponse(status_code=404, content={"detail": "User not found"})
        
        user = user_data.data[0]
        
        # Create custom JWT with user data
        custom_payload = {
            "id": user["id"],
            "email": user["email"],
            "role": user["role"],
            "name": user["name"],
        }
        
        user_data_jwt = jwt.encode(custom_payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        
        response = JSONResponse(
            status_code=200,
            content={
                "message": "Logged in successfully",
                "user_data": custom_payload,
                "access_token": access_token  # For debugging
            }
        )
        
        # Set Supabase access token (for backend auth)
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=3600
        )
        
        # Set Supabase refresh token
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=24*3600
        )
        
        # Set custom JWT with user data
        response.set_cookie(
            key="user_data",
            value=user_data_jwt,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=3600  # Same as access_token
        )
        
        return response
        
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e) or "Internal server error"})

    


@app.post("/logout")
async def logout(request: Request, background_tasks: BackgroundTasks):
    """
    Logout endpoint.

    Expects: No body required (cookies are automatically sent with request).
    Returns: Success message and clears authentication and user data cookies.

    Cookie clearing:
    - access_token: Removed from browser
    - refresh_token: Removed from browser
    - user_data: Removed from browser
    - Supabase session: Invalidated on server (revokes refresh token)
    """
    try:
        # Get tokens from cookies for Supabase sign out
        access_token = request.cookies.get("access_token")
        refresh_token = request.cookies.get("refresh_token")
        
        # Run Supabase sign-out in background
        if access_token and refresh_token:
            def supabase_signout():
                try:
                    supabase.client.auth.set_session(access_token, refresh_token)
                    supabase.client.auth.sign_out(scope='local')
                except Exception as supabase_error:
                    print(f"Supabase sign out error: {supabase_error}")
            
            background_tasks.add_task(supabase_signout)
        
        # Create response with success message
        response = JSONResponse(
            status_code=200,
            content={"message": "Logged out successfully"}
        )
        
        # Clear access token cookie
        response.set_cookie(
            key="access_token",
            value="",
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=0,
            expires="Thu, 01 Jan 1970 00:00:00 GMT"
        )
        
        # Clear refresh token cookie
        response.set_cookie(
            key="refresh_token", 
            value="",
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=0,
            expires="Thu, 01 Jan 1970 00:00:00 GMT"
        )

        # Clear user data cookie
        response.set_cookie(
            key="user_data",
            value="",
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=0,
            expires="Thu, 01 Jan 1970 00:00:00 GMT"
        )
        
        return response
        
    except Exception as e:
        return JSONResponse(
            status_code=500, 
            content={"detail": str(e) or "Internal server error"}
        )

# This route is mostly called by frontend's middleware, to check if cookie is still valid. 
# However, it can also function like a get user detail route, where it will always return user details in its response. 
# When middleware calls this route, it will obtain the reponse and pass it to every front end pages as a useState variable. 
# Since middleware gets called before every pages load, you basically wouldnt need a special get user details route, since the
# user details can be passed to the middleware and be called by front end using useState.

@app.get("/checkCookies")
def check_cookies(request: Request):
    """
    Check cookies for authentication:
    - If access_token valid → return decoded user_data.
    - If access_token expired but refresh_token valid → refresh session,
      update all cookies including user_data, return updated user_data.
    - If neither valid or no cookies → force login and clear cookies.

    No request body or parameters are required. Cookies are automatically sent by the browser.
    """
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    user_data_cookie = request.cookies.get("user_data")

    # If no cookies at all → force login
    if not access_token or not refresh_token or not user_data_cookie:
        raise HTTPException(status_code=401, detail="No valid cookies found, login required")

    # If got access token, check for expiry.
    try:
        # Validate access token first (just checks signature + expiry)
        jwt.decode(access_token, JWT_SECRET, algorithms=[JWT_ALGORITHM], audience="authenticated")

        # Access token is valid → decode user_data cookie and return it
        payload = jwt.decode(user_data_cookie, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return JSONResponse(status_code=200, content={"user": payload})

    except ExpiredSignatureError:
        # Access token expired, try refresh token
        try:
            new_session = supabase.client.auth.refresh_session(refresh_token)

            if not new_session or not new_session.session:
                raise HTTPException(status_code=401, detail="Invalid refresh token")

            # Get new tokens
            new_access_token = new_session.session.access_token
            new_refresh_token = new_session.session.refresh_token

            # Fetch fresh user from Supabase
            user = new_session.user
            if not user:
                raise HTTPException(status_code=401, detail="Failed to fetch user from session")

            custom_payload = {
                "id": user.id,
                "email": user.email,
                "role": user.user_metadata.get("role"),
                "name": user.user_metadata.get("name"),
            }

            # Encode new user_data JWT
            user_data_data = jwt.encode(custom_payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

            # Send updated cookies
            response = JSONResponse(status_code=200, content={"user": custom_payload})

            response.set_cookie(
                key="access_token",
                value=new_access_token,
                httponly=True,
                secure=False,  # Keep False on localhost
                samesite="lax",
                max_age=3600
            )
            response.set_cookie(
                key="refresh_token",
                value=new_refresh_token,
                httponly=True,
                secure=False,
                samesite="lax",
                max_age=24*3600
            )
            response.set_cookie(
                key="user_data",
                value=user_data_data,
                httponly=True,
                secure=False,
                samesite="lax",
                max_age=3600
            )

            return response

        except Exception as e:
            # Clear cookies on refresh failure
            response = JSONResponse(status_code=401, content={"detail": f"Refresh failed: {str(e)}"})
            response.delete_cookie("access_token")
            response.delete_cookie("refresh_token")
            response.delete_cookie("user_data")
            return response

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

## Signup page is not required in the first release, hence this route is more for own usage to create an user account
@app.post("/signup")
def signup(req: SignupRequest):
    """
    Signup endpoint.

    Expects: JSON body with email and password.
    Sets cookies for session (access_token, refresh_token, user_data) automatically.

    Cookie expiry:
    - access_token: 1 hour
    - refresh_token: 24 hours
    - user_data: 1 hour
    """
    try:
        # Attempt signup
        resp = supabase.client.auth.sign_up({
            "email": req.email,
            "password": req.password
        })

        if not resp.user:
            return JSONResponse(status_code=400, content={"detail": "Signup failed"})

        # If Supabase requires email confirmation, no session is returned
        if not resp.session:
            return JSONResponse(status_code=400, content={"detail": "Email confirmation required"})

        # Extract tokens from Supabase session
        access_token = resp.session.access_token
        refresh_token = resp.session.refresh_token
        user = resp.user

        # Custom user payload (same format as /login and /checkCookies)
        custom_payload = {
            "id": user.id,
            "email": user.email,
            "role": user.user_metadata.get("role"),
            "name": user.user_metadata.get("name"),
        }

        # Encode custom payload into user_data cookie
        user_data_token = jwt.encode(custom_payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

        # Build response
        response = JSONResponse(
            status_code=201,
            content={
                "message": "User signed up and logged in",
                "user": custom_payload,
                "access_token": access_token
            }
        )

        # Set cookies
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,  # Use True in production
            samesite="lax",
            max_age=3600
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=24 * 3600
        )
        response.set_cookie(
            key="user_data",
            value=user_data_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=3600
        )

        return response

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail": str(e) or "Internal server error"}
        )


# ---------------------------------------- INTERNAL SERVICE --------------------------------------------

# Get user by userID -- used for backend check

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

#----------------------------------------- Helper Functions ---------------------------------------------


#--------------------------------------- Health check --------------------------------------------------

@app.get("/")
def read_root():
    return JSONResponse(status_code=200, content={"message": "User Service is running"})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5100)

## Instructions

> Local Development

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 5100
```

To deactivate server:

```bash
deactivate
```

> Docker Development

```bash
docker build -t my-fastapi-app .
docker run -p 5100:5100 --name my-fastapi-container my-fastapi-app
```

## EndPoints

### Health Check

GET http://localhost:5100

Output:

```bash
"message": "User Service is running 🚀🥺"
```

## Authentication Cookies

When you log in via `/login`, the server sets two cookies:

-   `access_token` (1h) -> Short-lived JWT used for authentication.
-   `refresh_token` (24h) -> Used to silently refresh the access token when it expires.
-   `user_data` (1h) → Encoded JWT containing basic user info (id, email, role, name).

These are returned as `Set-Cookie` headers and stored by the browser under your frontend domain (`http://localhost:3000` in dev, `yourdomain.com` in prod).  
From then on, the browser automatically includes them in every request to the backend — no need to attach headers manually.
You can inspect element go to Application and Cookies to view it

Why cookies (vs. Authorization headers)?

-   Headers (Bearer token): You must add the token manually to every request. Usually stored in localStorage, which is vulnerable to XSS.
-   Cookies: Sent automatically by the browser. If marked `HttpOnly`, JavaScript cannot access them (safer).

Postman usage:

-   After `POST /login`, Postman captures cookies in the Cookies tab for `localhost:3000`.
-   You can look for it under the "Send" button, or at the top right
-   Future requests will include them automatically.
-   Or set manually with a `Cookie` header:
    ```
    Cookie: access_token=...; refresh_token=...; user_data=...
    ```

## Routes

> ## Login

POST http://localhost:5100/login

`Example: POST http://127.0.0.1:5100/login`

Request Body:

```json
{
    "email": "rc@example.com",
    "password": "abc123"
}
```

Required Fields:

| Field      | Type   | Required | Description                      |
| ---------- | ------ | -------- | -------------------------------- |
| `email`    | string | ✅       | User's registered email address. |
| `password` | string | ✅       | User's password.                 |

Sample Successful Response:
HTTP Status: 200 OK

```json
{
    "message": "Logged in successfully",
    "user_id": "abcd1234-5678-90ef-ghij-klmnopqrstuv",
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

Cookie Expiry:
| Cookie Name | Expiry Time | Purpose |
|------------------|-------------|--------------------------------------------------|
| `access_token` | 1 hour | Used for accessing protected resources. |
| `refresh_token` | 24 hours | Used to obtain a new `access_token` when expired.|
| `user_data` | 1 hours | Encoded JWT containing minimal user details for quick retrieval without DB calls.|

Notes:

-   Cookies are HTTP-only to prevent JavaScript access.
-   For local development, `secure` flag is set to `false`. In production, set `secure=True` to require HTTPS.
-   Access token is returned in JSON in the response only for debugging.
-   Expired cookies will require re-login (Checked by middleware in frontend).
-   Supabase refresh tokens may have a different validity period; cookie expiration here controls browser session expiration.
-   This endpoint also initializes the authentication state for the frontend middleware by setting all necessary cookies for session management.

---

> ## Logout

POST http://localhost:5100/logout

`Example: POST http://127.0.0.1:5100/logout`

Required Fields:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| None | - | - | No request body required. Authentication cookies are automatically sent with the request. |

Sample Successful Response:
HTTP Status: 200 OK

```json
{
    "message": "Logged out successfully"
}
```

Cookie Clearing:
| Cookie Name | Action | Result |
|----------------|--------|---------|
| `access_token` | Cleared | Removed from browser with immediate expiry |
| `refresh_token`| Cleared | Removed from browser with immediate expiry |
| `user_data` | Cleared | Removed from browser with immediate expiry |

Sample Error Response:
HTTP Status: 500 Internal Server Error

```json
{
    "detail": "Internal server error"
}
```

Notes:

-   No request body needed - Authentication is handled via cookies automatically sent with the request.
-   Supabase session invalidation - The refresh token is revoked on the Supabase server, preventing future token refresh.
-   Access token remains valid - Due to JWT nature, the access token stays valid until its natural expiry (up to 1 hour), but without refresh token, user cannot get new tokens.
-   Cookie clearing - All cookies are immediately cleared from the browser with past expiry dates.
-   Frontend state clearing - The frontend should also clear any cached authentication state after successful logout.
-   Error handling - If Supabase sign out fails, cookie clearing still proceeds to ensure security.

Security Features:

-   HttpOnly cookies are cleared to prevent any JavaScript access to authentication tokens.
-   Proper cookie attributes - Uses same attributes as when cookies were set to ensure proper clearing.
-   Server-side session revocation - Supabase refresh token is revoked on the authentication server.
-   Graceful error handling - Continues with logout process even if server-side operations fail.

---

> ## Check Cookies

> This route works just how a get user details route would work, where it will always return user details in its response.
> When middleware calls this route, it will obtain the reponse and pass it to every front end pages as a useState variable.

GET http://localhost:5100/checkCookies

`Example: GET http://127.0.0.1:5100/checkCookies`

Required Fields:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| None | - | - | No request body or parameters required. Authentication cookies are automatically sent with the request. |

Required Cookies (Automatically sent):
| Cookie Name | Required | Description |
|----------------|----------|-------------|
| `access_token` | ✅ | JWT token for authentication verification |
| `refresh_token`| ⚠️ | Required only when access token is expired |
| `user_data` | ✅ | Encoded user data payload (id, email, role, name) |

## Response Scenarios

### Scenario 1: Valid Access Token

HTTP Status: 200 OK

```json
{
    "user": {
        "id": "0ec8a99d-3aab-4ec6-b692-fda88656844f",
        "email": "Mike@example.com",
        "role": "Manager",
        "name": "Mike"
    }
}
```

### Scenario 2: Expired Access Token, Valid Refresh Token

HTTP Status: 200 OK

```json
{
    "user": {
        "id": "0ec8a99d-3aab-4ec6-b692-fda88656844f",
        "email": "Mike@example.com",
        "role": "Manager",
        "name": "Mike"
    }
}
```

**Note:** New cookies are automatically set in response headers with refreshed tokens.

### Scenario 3: No Cookies Found

HTTP Status: 401 Unauthorized

```json
{
    "detail": "No valid cookies found, login required"
}
```

### Scenario 4: Expired Access Token, No/Invalid Refresh Token

HTTP Status: 401 Unauthorized

```json
{
    "detail": "Invalid refresh token"
}
```

### Scenario 5: Refresh Process Failed

HTTP Status: 401 Unauthorized

```json
{
    "detail": "Refresh failed: [error message]"
}
```

### Scenario 6: Unexpected Error

HTTP Status: 500 Internal Server Error

```json
{
    "detail": "Unexpected error: [error message]"
}
```

## Authentication Flow

| Step | Condition                     | Action                                                       | Result             |
| ---- | ----------------------------- | ------------------------------------------------------------ | ------------------ |
| 1    | Access token present & valid  | Decode and return `user_data` cookie                         | Success (200)      |
| 2    | Access token expired          | Check refresh token                                          | Continue to step 3 |
| 3    | Refresh token valid           | Refresh session, set new cookies, return updated `user_data` | Success (200)      |
| 4    | Refresh token invalid/missing | Clear cookies, return error                                  | Unauthorized (401) |

## Cookie Updates During Refresh

When access token expires but refresh token is valid, new cookies are automatically set:

| Cookie Name     | New Expiry | Purpose                              |
| --------------- | ---------- | ------------------------------------ |
| `access_token`  | 1 hour     | Updated with new JWT token           |
| `refresh_token` | 24 hours   | Updated with new refresh token       |
| `user_data`     | 1 hour     | Updated with fresh user info payload |

Notes:

-   Automatic authentication - No manual token handling required; cookies are sent automatically by browser.
-   Silent token refresh - When access token expires, the system automatically attempts to refresh using the refresh token.
-   Seamless user experience - Users don't need to log in again as long as refresh token is valid.
-   Security by design - Access tokens have short expiry (1 hour) for security, while refresh tokens last longer (24 hours).
-   Cookie security - All cookies are HttpOnly to prevent JavaScript access and XSS attacks.
-   Middleware integration - This endpoint is typically called by frontend middleware to verify authentication status.
-   Session management - Handles the complete authentication lifecycle from token validation to refresh.
-   Error specificity - Different error messages help distinguish between various failure scenarios.
-   Supabase integration - Uses Supabase's refresh_session() method for secure token renewal.

Security Features:

-   JWT token validation - Verifies token signature and expiry before accepting.
-   Automatic token rotation - New tokens are issued during refresh for enhanced security.
-   HttpOnly cookies - Prevents client-side JavaScript access to authentication tokens.
-   Proper error handling - Returns specific error codes for different authentication failure scenarios.

---

## Signup

POST http://localhost:5100/signup

`Example: POST http://127.0.0.1:5100/signup`

> **Important:** This endpoint is intended for HR personnel to create new user accounts. It does NOT log in the newly created user or set any session cookies for them. The HR user remains logged in as themselves after creating a new account.

> **Note:** If email confirmation is disabled in Supabase settings, the user account is created immediately. If email confirmation is required, the user must verify their email before they can log in.

Request Body:
```json
{
    "email": "newuser@example.com",
    "password": "securepassword123",
    "role": "staff",
    "name": "John Doe",
    "department": "Tech"
}
```

Required Fields:
| Field | Type | Required | Description |
|-----------|--------|----------|-----------------------------------|
| `email` | string | ✅ | User's email address for registration. |
| `password`| string | ✅ | User's desired password. |
| `role` | string | ❌ | User's role (default: "user"). Options: "staff", "hr", "manager", "admin" |
| `name` | string | ❌ | User's full name (default: "New User"). |
| `department` | string | ❌ | User's department (default: "General"). Options: "Tech", "Sales", "Admin", "HR", "Quant", or custom value. |

Sample Successful Response:
HTTP Status: 201 Created
```json
{
    "message": "User account created successfully",
    "user": {
        "email": "newuser@example.com",
        "role": "staff",
        "name": "John Doe",
        "department": "Tech"
    }
}
```

Sample Response (Email Confirmation Required):
HTTP Status: 201 Created
```json
{
    "message": "User account created successfully. Email confirmation required.",
    "user": {
        "email": "newuser@example.com",
        "role": "staff",
        "name": "John Doe",
        "department": "Tech"
    }
}
```

**Important Notes:**
- This endpoint does NOT set cookies or create a session for the newly created user
- The HR user making the request remains logged in as themselves
- No sensitive information (user ID, tokens) is returned in the response
- The newly created user must use the `/login` endpoint with their credentials to access the system

> ## Get all users

GET http://localhost:5100/allUsers

`Example: GET http://127.0.0.1:5100/allUsers`

Sample Output:
```json
{
    "message": "Users retrieved successfully",
    "users": [
        {
            "id": "0ec8a99d-3aab-4ec6-b692-fda88656844f",
            "email": "rc@example.com",
            "role": "staff",
            "created_at": "2025-09-22T05:11:59.671524+00:00",
            "name": "Default Name",
            "auth_id": "f0ed9d08-d833-4d43-9428-41a9b179eff0",
            "department": "tech"
        },
        {
            "id": "17a40371-66fe-411a-963b-a977cc7cb475",
            "email": "ashley6@example.com",
            "role": "user",
            "created_at": "2025-09-18T13:15:12.958746+00:00",
            "name": "Default Name",
            "auth_id": "30397e3b-61c5-4836-98fb-987e85a8bd29",
            "department": "sales"
        },
        {
            "id": "655a9260-f871-480f-abea-ded735b2170a",
            "email": "testmanager@example.com",
            "role": "manager",
            "created_at": "2025-10-01T12:58:24.548681+00:00",
            "name": "testManager",
            "auth_id": "0c696352-4f64-4745-9e66-b9af14894a97",
            "department": "tech"
        },
        {
            "id": "765bc84f-eba5-4d32-987b-d55adef7fe65",
            "email": "ashley5@example.com",
            "role": "Director",
            "created_at": "2025-09-18T11:26:29.051576+00:00",
            "name": "Default Name",
            "auth_id": "e1b95925-0e56-443b-b999-66f3eabc8074",
            "department": "admin"
        },
        {
            "id": "944d73be-9625-4fd1-8c6a-00e161da0642",
            "email": "testhr@example.com",
            "role": "hr",
            "created_at": "2025-10-01T12:58:40.299887+00:00",
            "name": "test hr",
            "auth_id": "5b0eb89c-7bac-4756-b63f-15d90be9bc19",
            "department": "sales"
        },
        {
            "id": "bba910a9-1685-4fa3-af21-ccb2e11cf751",
            "email": "3amtest@example.com",
            "role": "user",
            "created_at": "2025-09-25T19:23:25.865356+00:00",
            "name": "Default Name",
            "auth_id": "6d52c7b4-ed03-4a13-9d53-eace42d3f0f6",
            "department": "HR"
        }
    ]
}
```

### Cookie behaviours:

> Same as login route

Notes:

-   Similar to login - This endpoint functions identically to `/login` after successful user creation.
-   Access token for debugging - The access token is returned in JSON response only for debugging purposes.
-   Session expiry - Expired cookies will require re-login, checked by frontend middleware.

## Internal Routes

> ### Get user by user ID (for internal validation use)

GET http://localhost:5100/internal/{task_id}

> http://127.0.0.1:5100/internal/0ec8a99d-3aab-4ec6-b692-fda88656844f

Sample Output:

```json
{
    "id": "0ec8a99d-3aab-4ec6-b692-fda88656844f",
    "auth_id": "f0ed9d08-d833-4d43-9428-41a9b179eff0",
    "email": "rc@example.com",
    "role": "user",
    "created_at": "2025-09-22T05:11:59.671524+00:00",
    "exists": true,
    "internal_api_key": "secret"
}
```

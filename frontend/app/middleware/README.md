# Middleware: Authentication Check

This middleware handles authentication checks for the application by verifying cookies and managing user access to routes.

It ensures that only authenticated users can access protected pages, and redirects unauthenticated users to the login page.

> **Note:** This middleware handles authentication checks for all pages in the application automatically. No imports or anything is required by any page.

This middleware automatically runs:

1. On every navigation between pages (client-side navigation)
2. On page load or refresh (server-side navigation)

## Purpose

-   Automatically verify whether the user is logged in
-   Redirect unauthenticated users to `/auth/login` page
-   Redirect authenticated users away from public pages like `/auth/login` to `/dashboard` page
-   Cache authentication status during navigation to avoid unnecessary API calls
-   Use cookies for authentication state (`access_token`, `refresh_token`, and `user_data`)

## How it Works

**SSR (Server-Side Rendering)**  
Middleware reads the `user_data` cookie directly using Nuxt's `useCookie()`, decodes the JWT, and caches user information in `useState`. This ensures the server renders the correct UI (with user-specific navigation items) on first load.

**Client-Side Hydration**  
Since the cookie is decoded on both server and client, the `userData` state is consistent, preventing hydration mismatches.

**Between navigations**  
Authentication status is cached in Nuxt's `useState`, so middleware does not re-check every navigation.

**On cookie expiry**  
If the cookie is expired or missing, the client-side calls `localhost:8000/user/checkCookies` to validate/refresh the session.

### Key Implementation Details

-   **`useCookie('user_data')`**: Nuxt composable that works on both server and client to read the httpOnly cookie
-   **JWT Decoding**: Client-side decoding of the JWT for UI purposes only (not for authorization)
-   **Consistent State**: Both SSR and client have the same `userData` state, eliminating hydration mismatches
-   **Reduced API Calls**: Only calls `/checkCookies` when cookie is missing/invalid, not on every navigation

## Cookies

The authentication cookies are set by backend routes (`localhost:8000/user/login` and `/signup`):

| Cookie Name     | Purpose                                                 | Expiry   |
| --------------- | ------------------------------------------------------- | -------- |
| `access_token`  | Short-term JWT token for authentication                 | 1 hour   |
| `refresh_token` | Used to get a new access token without logging in       | 24 hours |
| `user_data`     | Encoded JWT with user details (`id, email, role, name`) | 1 hour   |

> Cookies are sent automatically with requests using `credentials: "include"`.

## Middleware Flow

```
[Browser Navigation] ──► [Middleware Trigger]
```

**Middleware Trigger happens:**

-   On every route navigation (including page load and route change)
-   Or when page is first loaded/refreshed

```
This middleware uses Nuxt's useState("userData") as the authentication state cache (authState).

It stores the decoded user_data JWT in useState("userData") as the auth state cache.
This prevents repeated /checkCookies calls during navigation, improving performance.
```

### Step 1: Read user_data Cookie and Decode JWT

```
[Middleware Check]
    |
    +── Read user_data cookie with useCookie()
          |
          ├── Cookie exists → Decode JWT → Cache in useState
          |                                      |
          |                                      ├── Valid & not expired → Allow navigation
          |                                      └── Expired → Continue to client validation
          |
          └── No cookie → Continue to next step
```

**Example:**

-   **SSR**: Cookie exists → Decode JWT → Render UI with user data
-   **Client**: Cookie already decoded in SSR → Consistent state → No hydration mismatch
-   **No Cookie**: Skip decoding, proceed to backend validation on client

### Step 2: Client-Side Validation (if needed)

This step **only runs on the client** when the cookie is missing, invalid, or expired.

```
[Client: Call localhost:8000/user/checkCookies]
    |
    +── Check access_token cookie on backend
           |
           ├── Valid → decode user_data cookie → return user info + cache userData → Allow navigation
           |
           └── Expired → Check refresh_token cookie
                     |
                     ├── Valid → refresh tokens, regenerate user_data cookie → set cookies → return user info + cache userData → Allow navigation
                     |
                     └── Invalid/Missing → return 401 → Middleware redirect to [localhost:3000/auth/login]
```

**Example scenarios:**

-   **Scenario A:** Cookie decoded successfully in SSR → No `/checkCookies` call needed
-   **Scenario B:** Access token expired, refresh token valid → Client calls `/checkCookies` → Refresh tokens silently
-   **Scenario C:** Both tokens expired → Redirect to login
-   **Scenario D:** No cookies → Redirect to login

**Key Improvement:** By reading the cookie directly, we avoid calling `/checkCookies` on every page load when the session is still valid.

### Step 3: Handle Navigation Based on Page Type

```
Middleware Checks Page Type:
    |
    ├── Public Page (e.g., /auth/login)
    │       |
    │       ├── User authenticated → Redirect to /dashboard
    │       └── User not authenticated → Allow navigation to continue (go to /auth/login)
    |
    ├── Protected Page (e.g., /dashboard, /profile, /settings)
    │       |
    │       ├── User authenticated → Allow navigation to continue (continue to /profile)
    │       └── User not authenticated → Redirect to /auth/login
```

**Example pages:**

-   **Public:** `/auth/login` (no auth required)
-   **Protected:** `/dashboard`, `/profile`, `/settings`

> Protected pages are basically all other pages not listed as public. Currently only login page is listed as public.

### Step 4: Middleware Outcomes

**Outcome:**

1. **Authenticated** → Proceed
2. **Not authenticated** → Redirect to `/auth/login`

## How to Access Cached userData

Middleware caches authenticated user details in Nuxt's `useState` as `userData`.  
You can access it anywhere in your app:

```ts
const userData = useState("userData").value;
console.log(userData.id);
console.log(userData.email);
console.log(userData.role);
console.log(userData.name);
```

## Concrete Example Flows

### Scenario 1: User opens browser, goes to `/dashboard`

**SSR Phase:**

1. Middleware triggers on server → Reads `user_data` cookie using `useCookie()`
2. Decodes JWT → Extracts user info (`id`, `email`, `role`, `name`)
3. Caches in `useState("userData")`
4. Server renders dashboard with correct sidebar items for user's role

**Client Hydration:** 5. Client receives HTML → Vue hydrates 6. Middleware runs on client → Cookie already decoded → Uses cached `userData` 7. **No hydration mismatch!** Server and client have identical user state

### Scenario 2: User manually types `/auth/login`

Middleware triggers → AuthState already cached → redirect to `localhost:3000/dashboard`

### Scenario 3: User clicks logout → cookies cleared → visits `/dashboard`

**SSR Phase:**

1. Middleware triggers → Reads `user_data` cookie → Cookie missing
2. Server renders unauthenticated state

**Client Phase:** 3. Middleware on client → No cookie → Calls `/checkCookies` 4. Backend returns 401 → Redirect to `localhost:3000/auth/login`

### Scenario 4: User's cookie expires while browsing

**On next navigation:**

1. Middleware reads cookie → Decodes JWT → Detects expiration
2. Client calls `/checkCookies` to validate `refresh_token`
3. Backend refreshes tokens → Updates cookies → User stays logged in

### Scenario 5: User opens new incognito tab → visits `/profile`

**SSR Phase:**

1. Middleware triggers → No cookies available
2. Server renders minimal/unauthenticated state

**Client Phase:** 3. Middleware on client → Calls `/checkCookies` 4. No cookies → Backend returns 401 → Redirect to `localhost:3000/auth/login`

## Flow Diagrams

### Main Authentication Flow (Updated)

```
[Browser Navigation / Page Load]
      |
      v
[Middleware Trigger - Runs on Both SSR & Client]
      |
      ├── [SSR & Client] Read user_data cookie with useCookie()
      |         |
      |         ├── Cookie exists ──► Decode JWT ──► Cache in useState
      |         |                                          |
      |         |                                          ├── Valid & not expired ──► Allow
      |         |                                          └── Expired ──► Continue
      |         |
      |         └── Cookie missing ──► Continue
      |
      ├── [Server] No valid cookie ──► Render unauthenticated state (let client handle)
      |
      └── [Client] No valid cached state ──► Call /checkCookies
               |
               ├── access_token valid ──► Return user data → Cache → Allow
               |
               ├── access_token expired & refresh_token valid ──► Refresh tokens → Update cookies → Allow
               |
               └── Invalid/missing tokens ──► Redirect to /auth/login
```

### Page Type Check

```
Page Type Check:
    ├── Public Page: If authenticated → redirect to /dashboard
    └── Protected Page: If not authenticated → redirect to /auth/login
```

## Key Notes

-   This middleware runs automatically at every navigation or page load **on both server and client**
-   Auth state is cached in memory for efficiency using Nuxt's `useState`
-   `useCookie()` allows reading httpOnly cookies in SSR context, fixing hydration mismatches
-   JWT decoding is done for UI purposes only; authorization still happens on the backend
-   Refresh tokens are used silently to maintain sessions without user interruption
-   Cookies are automatically sent with requests; no need for explicit header auth on every call

## Hydration Mismatch Fix

**Problem:** Previously, the middleware only ran on the client (`if (process.server) return`), causing:

-   Server rendered UI without user data → Shows generic/logged-out UI
-   Client fetched user data → Shows user-specific UI
-   Result: Vue hydration mismatch warnings

**Solution:** Now the middleware:

-   Reads the `user_data` cookie on **both server and client** using `useCookie()`
-   Decodes the JWT to get user info on both sides
-   Server renders with correct user-specific UI
-   Client receives matching HTML → No hydration mismatch!

**Benefits:**

-   ✅ Eliminates hydration warnings
-   ✅ Faster initial paint (correct UI on first render)
-   ✅ Better SEO (server renders authenticated content)
-   ✅ Reduced API calls (only calls `/checkCookies` when needed)
-   ✅ Prevents multiple redirects (single redirect to `/auth/login` on auth failure)

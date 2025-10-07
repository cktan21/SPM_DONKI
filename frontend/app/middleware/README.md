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

**First visit / page refresh**  
Middleware calls the backend endpoint `localhost:8000/user/checkCookies` to verify authentication status based on cookies.

**Between navigations**  
Authentication status is cached in Nuxt's `useState`, so middleware does not re-check every navigation.

**On refresh or new browser session**  
`useState` resets, and middleware re-checks `localhost:8000/user/checkCookies` again.

### Key Difference

`/checkCookies` now also returns a `user_data` cookie.  
This cookie contains a JWT with user details (`id`, `email`, `role`, `name`) and is used to avoid extra database calls for user info.  
Middleware uses this cookie directly to cache `userData`.

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

### Step 1: Check Cached Auth State

```
[Middleware Check]
    |
    +── Is authState cached in memory? (Nuxt store / middleware state)
          |
          ├── YES → Allow navigation (no backend call)
          |
          └── NO → Call backend [localhost:8000/user/checkCookies]
```

**Example:**

-   User just logged in → authState cached → No extra `/checkCookies` call
-   User opens app fresh in a new tab → authState empty → backend `/checkCookies` call triggered

### Step 2: Call /checkCookies

```
[Backend: localhost:8000/user/checkCookies]
    |
    +── Check access_token cookie
           |
           ├── Valid → Valid → decode user_data cookie → return user info + cache userData → Allow navigation
           |
           └── Expired → Check refresh_token cookie
                     |
                     ├── Valid → refresh tokens, regenerate user_data cookie → set cookies → return user info + cache userData → Allow navigation
                     |
                     └── Invalid/Missing → return 401 → Middleware redirect to [localhost:3000/auth/login]
```

**Example scenarios:**

-   **Scenario A:** Access token still valid → No extra login needed
-   **Scenario B:** Access token expired, refresh token valid → Refresh tokens silently, keep user logged in
-   **Scenario C:** Both tokens expired → Redirect to login
-   **Scenario D:** No cookies → Redirect to login

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

1. Middleware triggers → No cached authState → call `localhost:8000/user/checkCookies`
2. `localhost:8000/user/checkCookies` validates `access_token`:
    - Access token expired
    - Refresh token valid → refresh tokens → regenerate `user_data` cookie
3. Middleware caches authState → allows navigation to `localhost:3000/dashboard`

### Scenario 2: User manually types `/auth/login`

Middleware triggers → AuthState already cached → redirect to `localhost:3000/dashboard`

### Scenario 3: User clicks logout → cookies cleared → visits `/dashboard`

Middleware triggers → No access token → redirect to `localhost:3000/auth/login`

### Scenario 4: User opens new incognito tab → visits `/profile`

1. Middleware triggers → No cached authState → call `localhost:8000/user/checkCookies`
2. Cookies missing or invalid → redirect to `localhost:3000/auth/login`

## Flow Diagrams

### Main Authentication Flow

```
[Browser Navigation]
      |
      v
[Middleware Trigger]
      |
      ├── Is authState cached? ── YES ──► Allow navigation
      |
      └── NO ──► Call /checkCookies
               |
               ├── access_token valid ──► Set authState → Allow
               |
               ├── access_token expired & refresh_token valid ──► Refresh tokens → regenerate user_data cookie → Set authState → Allow
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

-   This middleware runs automatically at every navigation or page load
-   Auth state is cached in memory for efficiency
-   Refresh tokens are used silently to maintain sessions without user interruption
-   Cookies are automatically sent with requests; no need for explicit header auth on every call

/**
 * Middleware to check authentication and authorization for every route navigation.
 *
 * Flow:
 * 1. Read user_data cookie using useCookie() (works on both SSR and client)
 * 2. Decode JWT and cache in useState for consistent SSR/client state
 * 3. If cookie invalid/missing on client → call /checkCookies to validate/refresh
 * 4. Check role access and allow/block navigation
 *
 * Supports multiple roles per route.
 * 
 * Benefits:
 * - Fixes SSR hydration mismatch by having consistent user data on server and client
 * - Reduces unnecessary API calls by reading existing cookie
 * - Maintains security with httpOnly cookies (readable in SSR context)
 */

interface CheckCookiesResponse {
    user: {
        id: string;
        email: string;
        role: string;
        name: string;
    };
}

interface JWTPayload {
    id: string;
    email: string;
    role: string;
    name: string;
    exp?: number;
}

// Mapping of routes → allowed roles
const routeAccess: Record<string, string[]> = {
    "/generatereport": ["hr", "manager", "admin"],               // Only HR
    "/settings": ["admin"],                  // Only Admin
    "/profile": ["hr", "admin", "user"],    // Multiple roles allowed
    "/auth/signup": ["hr"],                  // Only HR can access signup
};

/**
 * Decode JWT payload without verification (verification happens on backend)
 * This is safe because we're only using it for UI rendering, not authorization
 */
function decodeJWT(token: string): JWTPayload | null {
    try {
        const parts = token.split('.');
        if (parts.length !== 3) return null;

        // Decode the payload (second part)
        const payload = parts[1];
        if (!payload) return null;

        // Handle URL-safe base64
        const base64 = payload.replace(/-/g, '+').replace(/_/g, '/');
        const decoded = atob(base64);
        return JSON.parse(decoded);
    } catch (e) {
        console.error("Failed to decode JWT:", e);
        return null;
    }
}

/**
 * Check if JWT is expired
 */
function isJWTExpired(payload: JWTPayload): boolean {
    if (!payload.exp) return false;
    return Date.now() >= payload.exp * 1000;
}

export default defineNuxtRouteMiddleware(async (to, from) => {
    const BASE_URL = "http://localhost:8000/user";
    const publicPages = ["/auth/login"];

    // ---- Read cookies using Nuxt's useCookie (works on both server and client) ----
    const userDataCookie = useCookie<string | null>("user_data");
    const userData = useState<CheckCookiesResponse | null>("userData");

    // ---- Helper functions ----
    const checkAccess = (userRole: string) => {
        const requiredRoles = routeAccess[to.path];
        if (requiredRoles && !requiredRoles.includes(userRole)) {
            console.warn(
                `Access denied: ${userRole} cannot access ${to.path}, requires one of [${requiredRoles.join(", ")}]`
            );
            return false;
        }
        return true;
    };

    const handleUnauthorized = () => {
        // If user doesn't have access to current page, redirect to login
        // Don't redirect to dashboard as that might also require authentication
        return navigateTo("/auth/login");
    };

    // ---- 1. Try to decode cookie if present and userData not cached ----
    if (userDataCookie.value && !userData.value) {
        const decoded = decodeJWT(userDataCookie.value);

        if (decoded && !isJWTExpired(decoded)) {
            // Valid cookie - cache the user data
            userData.value = { user: decoded };

            if (process.server) {
                console.log(`[SSR] User data loaded from cookie: ${decoded.email} (${decoded.role})`);
            }
        } else if (process.server && decoded) {
            // Cookie exists but expired on server - let client handle refresh
            console.log("[SSR] Cookie expired, will validate on client");
        }
    }

    // ---- 2. Check if we have valid cached auth state ----
    if (userData.value?.user?.id) {
        // User is authenticated
        if (publicPages.includes(to.path)) {
            return navigateTo("/dashboard");
        }

        if (!checkAccess(userData.value.user.role)) {
            return handleUnauthorized();
        }

        return true; // Allow navigation
    }

    // ---- 3. No valid cached state - check if on public page ----
    if (publicPages.includes(to.path)) {
        return true; // Allow access to login page
    }

    // ---- 4. On server: Cookie missing/invalid, but don't block (let client validate) ----
    if (process.server) {
        // On SSR, if no cookie, we'll render as if logged out
        // The client will then validate and redirect if needed
        console.log("[SSR] No valid cookie, rendering unauthenticated state");
        return;
    }

    // ---- 5. On client: Validate with backend if no cached state ----
    if (process.client) {
        try {
            const res = await $fetch<CheckCookiesResponse>(`${BASE_URL}/checkCookies`, {
                method: "GET",
                credentials: "include",
            });

            if (res.user?.id) {
                // Cache user data
                userData.value = res;
                console.log(`[Client] User authenticated: ${res.user.email}`);

                if (!checkAccess(res.user.role)) {
                    return handleUnauthorized();
                }

                return true;
            } else {
                // No valid user data in response
                console.log("[Client] No valid user data in response");
                return navigateTo("/auth/login");
            }
        } catch (err) {
            console.error("[Client] Auth check failed:", err);
            // API call failed - redirect to login
            return navigateTo("/auth/login");
        }
    }

    return true;
});

/**
 * Middleware to check authentication and authorization for every route navigation.
 *
 * Flow:
 * 1. If auth state cached → check role access → allow/block.
 * 2. If no auth state → call localhost:8000/user/checkCookies to verify tokens.
 *    - If valid → store auth state → check role access → allow/block.
 *    - If invalid → redirect to /auth/login.
 *
 * Supports multiple roles per route.
 */

interface CheckCookiesResponse {
    user: {
        id: string;
        email: string;
        role: string;
        name: string;
    };
}

// Mapping of routes → allowed roles
const routeAccess: Record<string, string[]> = {
    "/generatereport": ["hr"],               // Only HR
    "/settings": ["admin"],                  // Only Admin
    "/profile": ["hr", "admin", "user"],     // Multiple roles allowed
};

export default defineNuxtRouteMiddleware(async (to, from) => {
    if (process.server) return; // Only run client-side

    const BASE_URL = "http://localhost:8000/user";
    const publicPages = ["/auth/login"]; // Pages accessible without login

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
        // Avoid infinite redirects if `from` is missing or same as `to`
        if (!from?.path || from.path === to.path) {
            return navigateTo("/dashboard");
        }
        return navigateTo(from.path);
    };

    // ---- 1. Check cached auth state ----
    const authState = useState<CheckCookiesResponse | null>("userData").value;

    if (authState?.user?.id) {
        if (publicPages.includes(to.path)) {
            return navigateTo("/dashboard");
        }

        if (!checkAccess(authState.user.role)) {
            return handleUnauthorized();
        }

        return true;
    }

    // ---- 2. Otherwise, validate with backend ----
    try {
        const res = await $fetch<CheckCookiesResponse>(`${BASE_URL}/checkCookies`, {
            method: "GET",
            credentials: "include", // Send cookies automatically
        });

        if (res.user?.id) {
            // Cache user data
            useState<CheckCookiesResponse>("userData").value = res;

            if (publicPages.includes(to.path)) {
                return navigateTo("/dashboard");
            }

            if (!checkAccess(res.user.role)) {
                return handleUnauthorized();
            }

            return true;
        } else {
            // Not authenticated → send to login if page is protected
            if (!publicPages.includes(to.path)) {
                return navigateTo("/auth/login");
            }
        }
    } catch (err) {
        console.error("Auth check failed:", err);
        if (!publicPages.includes(to.path)) {
            return navigateTo("/auth/login");
        }
    }

    return true;
});

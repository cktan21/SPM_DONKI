/**
 * Middleware to check authentication for every route navigation.
 *
 * Flow:
 * 1. If auth state cached → allow navigation.
 * 2. If no auth state → call localhost:5100/checkCookies to verify tokens.
 *    - If valid → set auth state → allow.
 *    - If invalid → redirect to /auth/login.
 *
 * Read the README.md for more explanation.
 */

/**
 * Interface for TypeScript safety checks.
 * This matches the /checkCookies response structure.
 */
interface CheckCookiesResponse {
  user: {
    id: string;
    email: string;
    role: string;
    name: string;
  };
}

export default defineNuxtRouteMiddleware(async (to, from) => {
  if (process.server) return; // Only run client-side

  const BASE_URL = "http://localhost:5100";
  const publicPages = ["/auth/login"]; // Only login page is public

  // Check if auth state is already cached
  const authState = useState<CheckCookiesResponse | null>("userData").value;

  if (authState && authState.user && authState.user.id) {
    // Cached auth state exists → no need to call checkCookies
    if (publicPages.includes(to.path)) {
      return navigateTo("/dashboard");
    }
    return true;
  }

  try {
    const res = await $fetch<CheckCookiesResponse>(`${BASE_URL}/checkCookies`, {
      method: "GET",
      credentials: "include" // Sends cookies automatically
    });

    if (res.user && res.user.id) {
      // Authenticated → store in auth state cache
      useState<CheckCookiesResponse>("userData").value = res;

      if (publicPages.includes(to.path)) {
        return navigateTo("/dashboard");
      }

      return true; // Allow navigation
    } else {
      console.warn("No authenticated user");

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

  return true; // Allow navigation if nothing matches
});

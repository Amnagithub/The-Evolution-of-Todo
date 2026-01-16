/**
 * API client with session-based authentication.
 * Passes session token via cookie to the backend.
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface ApiOptions extends RequestInit {
  token?: string;
}

class ApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

async function getSessionToken(): Promise<string | null> {
  // Get session token from Better Auth session endpoint
  try {
    const response = await fetch("/api/auth/get-session", {
      method: "GET",
      credentials: "include",
    });
    if (response.ok) {
      const data = await response.json();
      return data?.session?.token || null;
    }
  } catch {
    // Session not available
  }
  return null;
}

async function apiRequest<T>(
  path: string,
  options: ApiOptions = {}
): Promise<T> {
  const { token, ...fetchOptions } = options;

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string>),
  };

  // Attach session token if available
  const sessionToken = token || (await getSessionToken());
  if (sessionToken) {
    headers["Authorization"] = `Bearer ${sessionToken}`;
  }

  const response = await fetch(`${API_URL}${path}`, {
    ...fetchOptions,
    headers,
    credentials: "include",
  });

  if (!response.ok) {
    let errorMessage = "Request failed";
    try {
      const errorData = await response.json();
      errorMessage = errorData.detail || errorData.error || errorMessage;
    } catch {
      // Response not JSON
    }
    throw new ApiError(errorMessage, response.status);
  }

  // Handle 204 No Content
  if (response.status === 204) {
    return {} as T;
  }

  return response.json();
}

export const api = {
  get: <T>(path: string, options?: ApiOptions) =>
    apiRequest<T>(path, { ...options, method: "GET" }),

  post: <T>(path: string, data: unknown, options?: ApiOptions) =>
    apiRequest<T>(path, {
      ...options,
      method: "POST",
      body: JSON.stringify(data),
    }),

  put: <T>(path: string, data: unknown, options?: ApiOptions) =>
    apiRequest<T>(path, {
      ...options,
      method: "PUT",
      body: JSON.stringify(data),
    }),

  patch: <T>(path: string, data: unknown, options?: ApiOptions) =>
    apiRequest<T>(path, {
      ...options,
      method: "PATCH",
      body: JSON.stringify(data),
    }),

  delete: <T>(path: string, options?: ApiOptions) =>
    apiRequest<T>(path, { ...options, method: "DELETE" }),
};

export { ApiError };

import { betterAuth } from "better-auth";
import { Pool } from "pg";

// Lazy initialization to avoid build-time errors on Vercel
// The auth instance is created on first use, not at module load time
let _auth: ReturnType<typeof betterAuth> | null = null;
let _authError: string | null = null;

function createAuth() {
  const DATABASE_URL = process.env.DATABASE_URL;
  const BETTER_AUTH_SECRET = process.env.BETTER_AUTH_SECRET;

  // Check if required env vars are set
  if (!DATABASE_URL || !BETTER_AUTH_SECRET) {
    _authError = "DATABASE_URL or BETTER_AUTH_SECRET not configured. Please set these in Vercel Dashboard.";
    return null;
  }

  const pool = new Pool({
    connectionString: DATABASE_URL,
    max: 10,
    idleTimeoutMillis: 30000,
    connectionTimeoutMillis: 5000,
  });

  return betterAuth({
    database: pool,
    emailAndPassword: {
      enabled: true,
      autoSignIn: true, // Automatically create session after signup/signin
    },
    session: {
      expiresIn: 60 * 60 * 24 * 7, // 7 days
      updateAge: 60 * 60 * 24, // 1 day
      cookieCache: {
        enabled: false, // Disable cookie cache to ensure fresh sessions
        maxAge: 0,
      },
    },
    secret: BETTER_AUTH_SECRET,
    trustedOrigins: [
      "http://localhost:3000",
      "http://localhost:8000",
      "https://the-evolution-of-todo-wheat.vercel.app",
      "https://the-evolution-of-todo.vercel.app",
      process.env.NEXT_PUBLIC_APP_URL || "",
      process.env.VERCEL_URL ? `https://${process.env.VERCEL_URL}` : "",
    ].filter(Boolean),
  });
}

// Lazy getter for auth instance - only creates auth when actually accessed
export const auth = new Proxy({} as ReturnType<typeof betterAuth>, {
  get(_, prop) {
    if (_authError) {
      // Return a no-op function for all properties if auth is not configured
      if (prop === 'then') return undefined;
      return () => { throw new Error(_authError!); };
    }
    if (!_auth) {
      _auth = createAuth();
      if (!_auth && !_authError) {
        _authError = "Failed to initialize auth";
      }
    }
    return (_auth as Record<string | symbol, unknown>)?.[prop];
  },
});

// Helper to check if auth is configured
export function isAuthConfigured(): boolean {
  return !_authError;
}

// Helper to get auth error message
export function getAuthError(): string | null {
  return _authError;
}

export type Session = typeof auth.$Infer.Session;

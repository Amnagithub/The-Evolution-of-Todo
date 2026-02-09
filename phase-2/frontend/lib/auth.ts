import { betterAuth } from "better-auth";
import { Pool } from "pg";

// Lazy initialization to avoid build-time errors on Vercel
// The auth instance is created on first use, not at module load time
let _auth: ReturnType<typeof betterAuth> | null = null;

function createAuth() {
  const DATABASE_URL = process.env.DATABASE_URL;

  if (!DATABASE_URL) {
    throw new Error("DATABASE_URL environment variable is required");
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
      autoSignIn: true,
    },
    session: {
      expiresIn: 60 * 60 * 24 * 7, // 7 days
      updateAge: 60 * 60 * 24, // 1 day
      cookieCache: {
        enabled: true,
        maxAge: 5 * 60, // 5 minutes
      },
    },
    secret: process.env.BETTER_AUTH_SECRET || "dev-secret-change-in-production",
    trustedOrigins: [
      "http://localhost:3000",
      "http://localhost:8000",
      "https://the-evolution-of-todo-wheat.vercel.app",
      process.env.NEXT_PUBLIC_APP_URL || "",
      process.env.VERCEL_URL ? `https://${process.env.VERCEL_URL}` : "",
    ].filter(Boolean),
  });
}

// Lazy getter for auth instance - only creates auth when actually accessed
export const auth = new Proxy({} as ReturnType<typeof betterAuth>, {
  get(_, prop) {
    if (!_auth) {
      _auth = createAuth();
    }
    return (_auth as Record<string | symbol, unknown>)[prop];
  },
});

export type Session = typeof auth.$Infer.Session;

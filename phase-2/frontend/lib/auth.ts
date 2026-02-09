import { betterAuth } from "better-auth";
import { Pool } from "pg";

// Determine database configuration based on environment
const DATABASE_URL = process.env.DATABASE_URL;

// Configure database adapter - PostgreSQL only for Vercel deployment
// SQLite is not supported on Vercel serverless environment
let databaseConfig: Pool;

if (!DATABASE_URL) {
  throw new Error("DATABASE_URL environment variable is required for production deployment");
}

// Use PostgreSQL for production with optimized pooling
databaseConfig = new Pool({
  connectionString: DATABASE_URL,
  max: 10,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 5000,
});

// Better Auth server configuration (session-based, no JWT)
export const auth = betterAuth({
  database: databaseConfig,
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

export type Session = typeof auth.$Infer.Session;

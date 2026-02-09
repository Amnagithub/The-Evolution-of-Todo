import { betterAuth } from "better-auth";
import { Pool } from "pg";

// Determine database configuration based on environment
const DATABASE_URL = process.env.DATABASE_URL;
const IS_VERCEL = process.env.VERCEL === "1";

// Configure database adapter
let databaseConfig: Pool | any;

if (DATABASE_URL && !DATABASE_URL.startsWith("sqlite")) {
  // Use PostgreSQL for production (Vercel) with optimized pooling
  console.log("[AUTH] Using PostgreSQL database");
  databaseConfig = new Pool({
    connectionString: DATABASE_URL,
    max: 10,
    idleTimeoutMillis: 30000,
    connectionTimeoutMillis: 5000,
    ssl: { rejectUnauthorized: false },
  });
} else if (!IS_VERCEL) {
  // Use SQLite for local development only
  const Database = require("better-sqlite3");
  const path = require("path");
  const dbPath = path.resolve(process.cwd(), "../backend/todo.db");
  console.log("[AUTH] Using SQLite database at:", dbPath);
  databaseConfig = new Database(dbPath);
} else {
  throw new Error("DATABASE_URL must be set in production (Vercel)");
}

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
    // Local development
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:8000",
    // Production URLs
    process.env.NEXT_PUBLIC_APP_URL || "",
    // Vercel preview deployments
    process.env.VERCEL_URL ? `https://${process.env.VERCEL_URL}` : "",
  ].filter(Boolean),
});

export type Session = typeof auth.$Infer.Session;

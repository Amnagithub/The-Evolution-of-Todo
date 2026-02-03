import { betterAuth } from "better-auth";
import { Pool } from "pg";
import Database from "better-sqlite3";
import path from "path";

// Determine database configuration based on environment
const DATABASE_URL = process.env.DATABASE_URL;
const IS_SQLITE = !DATABASE_URL || DATABASE_URL.startsWith("sqlite");

// Configure database adapter
let databaseConfig;
if (IS_SQLITE) {
  // Use SQLite for local development - store in parent directory so backend can access
  const dbPath = path.resolve(process.cwd(), "../backend/todo.db");
  console.log("[AUTH] Using SQLite database at:", dbPath);
  databaseConfig = new Database(dbPath);
} else {
  // Use PostgreSQL for production
  console.log("[AUTH] Using PostgreSQL database");
  databaseConfig = new Pool({
    connectionString: DATABASE_URL,
  });
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
  trustedOrigins: ["http://localhost:8000"],
});

export type Session = typeof auth.$Infer.Session;

import { betterAuth } from "better-auth";
import { Pool } from "pg";

// Better Auth server configuration (session-based, no JWT)
export const auth = betterAuth({
  database: new Pool({
    connectionString: process.env.DATABASE_URL,
  }),
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
  secret: process.env.BETTER_AUTH_SECRET,
  trustedOrigins: ["http://localhost:8000"],
});

export type Session = typeof auth.$Infer.Session;

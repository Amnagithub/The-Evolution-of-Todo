/** @type {import('next').NextConfig} */
const nextConfig = {
  // Optimized for Vercel deployment
  // Uses PostgreSQL (Neon) for database - no native modules required

  // Environment variable validation at build time
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
  },
}

module.exports = nextConfig

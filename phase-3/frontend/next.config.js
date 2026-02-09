/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable standalone output for optimal Vercel deployment
  output: process.env.VERCEL ? undefined : undefined,

  // Externalize native modules that don't work with webpack bundling
  // Note: In production (Vercel), we use PostgreSQL so better-sqlite3 is not loaded
  experimental: {
    serverComponentsExternalPackages: ['better-sqlite3', 'pg', 'pg-native'],
  },

  webpack: (config, { isServer }) => {
    if (isServer) {
      // Exclude native modules from webpack bundling
      config.externals = [...(config.externals || []), 'better-sqlite3'];
    }
    return config;
  },

  // Environment variables validation
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
  },

  // Enable strict mode for better error detection
  reactStrictMode: true,

  // Optimize images
  images: {
    domains: [],
    unoptimized: false,
  },
}

module.exports = nextConfig

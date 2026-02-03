/** @type {import('next').NextConfig} */
const nextConfig = {
  // Remove 'output: export' to support dynamic routes and API endpoints

  // Externalize native modules that don't work with webpack bundling
  experimental: {
    serverComponentsExternalPackages: ['better-sqlite3'],
  },

  webpack: (config) => {
    // Exclude native modules from webpack bundling
    config.externals = [...(config.externals || []), 'better-sqlite3'];
    return config;
  },
}

module.exports = nextConfig

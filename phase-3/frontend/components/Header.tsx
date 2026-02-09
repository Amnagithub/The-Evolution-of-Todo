"use client";

import { useRouter, usePathname } from "next/navigation";
import Link from "next/link";
import { signOut, useSession } from "@/lib/auth-client";

export function Header() {
  const router = useRouter();
  const pathname = usePathname();
  const { data: session } = useSession();

  const handleSignOut = async () => {
    try {
      await signOut();
      // Force full page reload to clear all state
      window.location.href = "/signin";
    } catch (error) {
      console.error("Sign out error:", error);
      window.location.href = "/signin";
    }
  };

  if (!session) {
    return null;
  }

  // Show back button on all pages except dashboard
  const showBackButton = pathname !== "/";

  return (
    <header className="bg-white shadow-sm mb-8">
      <div className="container mx-auto px-4 py-4 flex justify-between items-center">
        <div className="flex items-center gap-4">
          {showBackButton && (
            <Link
              href="/"
              className="flex items-center gap-2 px-3 py-2 text-sm text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-md transition-colors"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
              Dashboard
            </Link>
          )}
          <h1 className="text-xl font-semibold text-gray-800">Todo App</h1>
        </div>
        <div className="flex items-center gap-4">
          <span className="text-sm text-gray-600">
            {session.user?.email}
          </span>
          <button
            onClick={handleSignOut}
            className="px-4 py-2 text-sm text-gray-600 hover:text-gray-800 border border-gray-300 rounded-md hover:bg-gray-50"
          >
            Sign Out
          </button>
        </div>
      </div>
    </header>
  );
}

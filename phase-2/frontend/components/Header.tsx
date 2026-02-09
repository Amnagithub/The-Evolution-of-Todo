"use client";

import { useRouter } from "next/navigation";
import { signOut, useSession } from "@/lib/auth-client";

export function Header() {
  const router = useRouter();
  const { data: session } = useSession();

  const handleSignOut = async () => {
    // Set flag in sessionStorage to indicate signout
    sessionStorage.setItem("justSignedOut", "true");
    
    try {
      // Clear all auth cookies first
      await fetch("/api/auth/clear-session", { method: "POST" });
    } catch {
      // Ignore errors from clear-session
    }
    // Sign out from Better Auth
    await signOut();
    // Force a full page reload to clear all caches
    window.location.href = "/signin";
  };

  if (!session) {
    return null;
  }

  return (
    <header className="bg-white shadow-sm mb-8">
      <div className="container mx-auto px-4 py-4 flex justify-between items-center">
        <h1 className="text-xl font-semibold text-gray-800">Todo App</h1>
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

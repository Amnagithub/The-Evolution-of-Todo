"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

// Redirect old /dashboard URLs to the new home page
export default function DashboardRedirect() {
  const router = useRouter();

  useEffect(() => {
    router.replace("/");
  }, [router]);

  return (
    <div className="flex items-center justify-center min-h-[400px]">
      <div className="text-gray-500">Redirecting...</div>
    </div>
  );
}

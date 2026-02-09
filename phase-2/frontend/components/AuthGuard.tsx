"use client";

import { useSession } from "@/lib/auth-client";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

interface AuthGuardProps {
  children: React.ReactNode;
}

export function AuthGuard({ children }: AuthGuardProps) {
  const { data: session, isPending } = useSession();
  const router = useRouter();
  const [signedOut, setSignedOut] = useState(false);

  useEffect(() => {
    // Check if user just signed out by looking for a flag in sessionStorage
    const hasSignedOut = sessionStorage.getItem("justSignedOut");
    if (hasSignedOut) {
      setSignedOut(true);
      sessionStorage.removeItem("justSignedOut");
    }
  }, []);

  useEffect(() => {
    if (!isPending && !session && !signedOut) {
      router.push("/signin");
    }
  }, [session, isPending, router, signedOut]);

  if (isPending) {
    return (
      <div className="flex items-center justify-center min-h-[200px]">
        <div className="text-gray-500">Loading...</div>
      </div>
    );
  }

  if (!session && !signedOut) {
    return null;
  }

  return <>{children}</>;
}

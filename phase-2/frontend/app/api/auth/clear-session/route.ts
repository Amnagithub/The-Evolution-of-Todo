import { auth } from "@/lib/auth";
import { cookies } from "next/headers";
import { NextResponse } from "next/server";

export const dynamic = "force-dynamic";

export async function POST() {
  try {
    // Sign out from Better Auth
    await auth.api.signOut({
      headers: await cookies(),
    });

    // Clear all Better Auth cookies explicitly
    const cookieStore = await cookies();
    const cookieNames = cookieStore.getAll().map(c => c.name);

    const response = NextResponse.json({ success: true });

    // Clear all cookies
    for (const name of cookieNames) {
      if (name.includes("better") || name.includes("auth") || name.includes("session")) {
        response.cookies.delete(name);
      }
    }

    return response;
  } catch (error) {
    console.error("Error clearing session:", error);
    return NextResponse.json({ success: false, error: "Failed to clear session" }, { status: 500 });
  }
}

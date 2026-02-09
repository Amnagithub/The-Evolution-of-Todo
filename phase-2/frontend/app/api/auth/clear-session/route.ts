import { auth } from "@/lib/auth";
import { headers, cookies } from "next/headers";
import { NextResponse } from "next/server";

export const dynamic = "force-dynamic";

export async function POST() {
  try {
    // Get headers for signOut
    const headersList = await headers();
    const headersInit: HeadersInit = {};
    headersList.forEach((value, key) => {
      headersInit[key] = value;
    });

    // Sign out from Better Auth
    await auth.api.signOut({
      headers: headersInit,
    });

    // Clear all Better Auth cookies explicitly
    const cookieStore = await cookies();
    const allCookies = cookieStore.getAll();

    const response = NextResponse.json({ success: true });

    // Clear all cookies related to auth
    for (const cookie of allCookies) {
      if (cookie.name.includes("better") || cookie.name.includes("auth") || cookie.name.includes("session")) {
        response.cookies.delete(cookie.name);
      }
    }

    return response;
  } catch (error) {
    console.error("Error clearing session:", error);
    return NextResponse.json({ success: false, error: "Failed to clear session" }, { status: 500 });
  }
}

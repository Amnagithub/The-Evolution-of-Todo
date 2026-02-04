import { auth } from "@/lib/auth";
import { headers, cookies } from "next/headers";
import { NextResponse } from "next/server";

export const dynamic = "force-dynamic";

export async function GET() {
  try {
    // Get the session from Better Auth
    const session = await auth.api.getSession({
      headers: await headers(),
    });

    // Debug: log session info
    console.log("[DEBUG get-session] Session exists:", !!session);

    if (!session) {
      return NextResponse.json({ session: null, user: null }, { status: 200 });
    }

    // Get the session token from cookie - try multiple possible names
    const cookieStore = await cookies();
    const allCookies = cookieStore.getAll();

    // Debug: log all cookie names
    console.log("[DEBUG get-session] All cookies:", allCookies.map(c => c.name));

    // Find the session token cookie (Better Auth uses different names)
    let sessionToken =
      cookieStore.get("better-auth.session_token")?.value ||
      cookieStore.get("better-auth.session-token")?.value ||
      cookieStore.get("better_auth_session_token")?.value ||
      // The session object from Better Auth should have the token
      (session.session as { token?: string })?.token;

    // If still not found, look for any cookie containing "session"
    if (!sessionToken) {
      const sessionCookie = allCookies.find(c =>
        c.name.toLowerCase().includes('session') && c.name.includes('better')
      );
      sessionToken = sessionCookie?.value;
    }

    // Debug: log the session token (truncated for security)
    console.log("[DEBUG get-session] Session token found:", sessionToken ? `${sessionToken.substring(0, 20)}...` : "null");
    console.log("[DEBUG get-session] Session object token:", (session.session as { token?: string })?.token ? "present" : "absent");

    return NextResponse.json({
      session: {
        ...session.session,
        token: sessionToken,
      },
      user: session.user,
    });
  } catch (error) {
    console.error("Error getting session:", error);
    return NextResponse.json({ session: null, user: null }, { status: 200 });
  }
}

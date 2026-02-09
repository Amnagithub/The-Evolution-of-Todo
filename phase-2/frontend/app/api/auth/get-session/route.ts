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


    if (!session) {
      return NextResponse.json({ session: null, user: null }, { status: 200 });
    }

    // Get the session token from cookie - try multiple possible names
    const cookieStore = await cookies();
    const allCookies = cookieStore.getAll();


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

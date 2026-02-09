import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js";
import { NextRequest } from "next/server";

export const dynamic = "force-dynamic";

// Lazy handler initialization to avoid build-time errors
let _handlers: ReturnType<typeof toNextJsHandler> | null = null;

function getHandlers() {
  if (!_handlers) {
    _handlers = toNextJsHandler(auth);
  }
  return _handlers;
}

export async function GET(request: NextRequest) {
  const handlers = getHandlers();
  return handlers.GET(request);
}

export async function POST(request: NextRequest) {
  const handlers = getHandlers();
  return handlers.POST(request);
}

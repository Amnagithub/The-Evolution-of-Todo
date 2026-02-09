import type { Metadata } from "next";
import "./globals.css";
import { ChatWidget } from "@/components/chat";

export const metadata: Metadata = {
  title: "Todo App - Phase III",
  description: "AI-powered todo application with natural language chat",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gray-50">
        <main className="container mx-auto px-4 py-8">
          {children}
        </main>
        {/* AI Chatbot Widget - floating bottom-right */}
        <ChatWidget />
      </body>
    </html>
  );
}

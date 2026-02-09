"use client";

/**
 * ChatWidget - Floating chat container for AI Todo Chatbot.
 *
 * Features:
 * - Collapsible floating widget (bottom-right corner)
 * - Message list with auto-scroll
 * - Input field with send button
 * - Typing indicator during loading
 * - Responsive design with mobile keyboard handling
 */

import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useChat } from "@/hooks/useChat";
import { ChatMessage } from "./ChatMessage";
import { ChatInput } from "./ChatInput";
import { TypingIndicator } from "./TypingIndicator";

export function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { messages, isLoading, error, sendMessage, clearChat } = useChat();

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (isOpen && messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages, isOpen]);

  // Handle keyboard on mobile (push chat above keyboard)
  useEffect(() => {
    const handleResize = () => {
      if (isOpen && window.visualViewport) {
        const viewport = window.visualViewport;
        const keyboardHeight = window.innerHeight - viewport.height;
        document.documentElement.style.setProperty(
          "--keyboard-height",
          `${keyboardHeight}px`
        );
      }
    };

    window.visualViewport?.addEventListener("resize", handleResize);
    return () => {
      window.visualViewport?.removeEventListener("resize", handleResize);
    };
  }, [isOpen]);

  return (
    <>
      {/* Chat Toggle Button */}
      <motion.button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed bottom-4 right-4 z-50 w-14 h-14 rounded-full bg-blue-600 text-white shadow-lg hover:bg-blue-700 transition-colors flex items-center justify-center"
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        aria-label={isOpen ? "Close chat" : "Open chat"}
      >
        <AnimatePresence mode="wait">
          {isOpen ? (
            <motion.svg
              key="close"
              initial={{ rotate: -90, opacity: 0 }}
              animate={{ rotate: 0, opacity: 1 }}
              exit={{ rotate: 90, opacity: 0 }}
              className="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            </motion.svg>
          ) : (
            <motion.svg
              key="chat"
              initial={{ rotate: 90, opacity: 0 }}
              animate={{ rotate: 0, opacity: 1 }}
              exit={{ rotate: -90, opacity: 0 }}
              className="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
              />
            </motion.svg>
          )}
        </AnimatePresence>
      </motion.button>

      {/* Chat Panel */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: 20, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.95 }}
            transition={{ duration: 0.2, ease: "easeOut" }}
            className="fixed bottom-20 right-4 z-50 w-[360px] max-w-[calc(100vw-2rem)] h-[500px] max-h-[calc(100vh-6rem)] bg-white rounded-2xl shadow-2xl flex flex-col overflow-hidden border border-gray-200"
            style={{
              marginBottom: "var(--keyboard-height, 0px)",
            }}
          >
            {/* Header */}
            <div className="flex items-center justify-between px-4 py-3 border-b border-gray-100 bg-gray-50">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-green-500" />
                <h2 className="font-semibold text-gray-800">Todo Assistant</h2>
              </div>
              <button
                onClick={clearChat}
                className="text-xs text-gray-500 hover:text-gray-700 px-2 py-1 rounded hover:bg-gray-100 transition-colors"
                aria-label="Clear chat history"
              >
                Clear
              </button>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-3">
              {messages.length === 0 && !isLoading && (
                <div className="text-center text-gray-400 mt-8">
                  <p className="text-sm">Hi! I can help you manage your tasks.</p>
                  <p className="text-xs mt-2">
                    Try &quot;add buy groceries&quot; or &quot;show my tasks&quot;
                  </p>
                </div>
              )}

              {messages.map((msg) => (
                <ChatMessage
                  key={msg.id}
                  role={msg.role}
                  content={msg.content}
                  toolCalls={msg.toolCalls}
                  isPending={msg.isPending}
                />
              ))}

              {/* Typing indicator */}
              <AnimatePresence>
                {isLoading && <TypingIndicator />}
              </AnimatePresence>

              {/* Error display */}
              {error && (
                <motion.div
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  className="text-sm text-red-500 bg-red-50 px-3 py-2 rounded-lg"
                >
                  {error}
                </motion.div>
              )}

              <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <ChatInput onSend={sendMessage} isLoading={isLoading} />
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}

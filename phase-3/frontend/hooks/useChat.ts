/**
 * React hook for chat state management.
 *
 * Provides:
 * - messages: Array of chat messages
 * - isLoading: Whether a message is being sent
 * - error: Any error from the last operation
 * - sendMessage: Send a new message
 * - loadHistory: Load conversation history
 * - clearChat: Clear all messages
 */

"use client";

import { useState, useCallback, useEffect } from "react";
import {
  chatApi,
  ChatResponse,
  MessageItem,
  ToolCallRecord,
} from "@/lib/chat-api";

// ============================================================================
// Types
// ============================================================================

export interface ChatMessage {
  id: number | string;
  role: "user" | "assistant";
  content: string;
  toolCalls: ToolCallRecord[] | null;
  createdAt: Date;
  isPending?: boolean;
}

export interface UseChatReturn {
  messages: ChatMessage[];
  isLoading: boolean;
  error: string | null;
  sendMessage: (content: string) => Promise<void>;
  loadHistory: () => Promise<void>;
  clearChat: () => Promise<void>;
}

// ============================================================================
// Hook Implementation
// ============================================================================

export function useChat(): UseChatReturn {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  /**
   * Convert API MessageItem to ChatMessage
   */
  const toMessage = (item: MessageItem): ChatMessage => ({
    id: item.id,
    role: item.role,
    content: item.content,
    toolCalls: item.tool_calls,
    createdAt: new Date(item.created_at),
  });

  /**
   * Load conversation history on mount
   */
  const loadHistory = useCallback(async () => {
    try {
      setError(null);
      const response = await chatApi.getHistory();
      setMessages(response.messages.map(toMessage));
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to load history";
      setError(message);
      console.error("Failed to load chat history:", err);
    }
  }, []);

  /**
   * Send a message and handle the response
   */
  const sendMessage = useCallback(async (content: string) => {
    if (!content.trim() || isLoading) return;

    setError(null);
    setIsLoading(true);

    // Optimistically add user message
    const pendingId = `pending-${Date.now()}`;
    const userMessage: ChatMessage = {
      id: pendingId,
      role: "user",
      content: content.trim(),
      toolCalls: null,
      createdAt: new Date(),
      isPending: true,
    };

    setMessages((prev) => [...prev, userMessage]);

    try {
      const response = await chatApi.sendMessage(content.trim());

      // Replace pending message with confirmed message and add assistant response
      setMessages((prev) => {
        const withoutPending = prev.filter((m) => m.id !== pendingId);
        return [
          ...withoutPending,
          {
            id: Date.now(), // Will be replaced by actual ID on next load
            role: "user" as const,
            content: content.trim(),
            toolCalls: null,
            createdAt: new Date(),
          },
          {
            id: Date.now() + 1,
            role: "assistant" as const,
            content: response.message,
            toolCalls: response.tool_calls.length > 0 ? response.tool_calls : null,
            createdAt: new Date(),
          },
        ];
      });
    } catch (err) {
      // Remove pending message on error
      setMessages((prev) => prev.filter((m) => m.id !== pendingId));
      const message = err instanceof Error ? err.message : "Failed to send message";
      setError(message);
      console.error("Failed to send message:", err);
    } finally {
      setIsLoading(false);
    }
  }, [isLoading]);

  /**
   * Clear all messages
   */
  const clearChat = useCallback(async () => {
    try {
      setError(null);
      await chatApi.clearHistory();
      setMessages([]);
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to clear chat";
      setError(message);
      console.error("Failed to clear chat:", err);
    }
  }, []);

  /**
   * Load history on mount
   */
  useEffect(() => {
    loadHistory();
  }, [loadHistory]);

  return {
    messages,
    isLoading,
    error,
    sendMessage,
    loadHistory,
    clearChat,
  };
}

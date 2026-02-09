/**
 * Chat API client for AI Todo Chatbot.
 *
 * Provides typed methods for interacting with the chat endpoints:
 * - sendMessage: POST /api/chat
 * - getHistory: GET /api/chat/history
 * - clearHistory: DELETE /api/chat/clear
 */

import { api } from "./api";

// ============================================================================
// Types
// ============================================================================

export interface ToolCallRecord {
  tool:
    | "add_task"
    | "list_tasks"
    | "complete_task"
    | "delete_task"
    | "update_task"
    | "get_user_details";
  arguments: Record<string, unknown>;
  result: Record<string, unknown>;
}

export interface ChatResponse {
  message: string;
  tool_calls: ToolCallRecord[];
  conversation_id: number;
}

export interface MessageItem {
  id: number;
  role: "user" | "assistant";
  content: string;
  tool_calls: ToolCallRecord[] | null;
  created_at: string;
}

export interface ChatHistoryResponse {
  messages: MessageItem[];
  conversation_id: number;
  total_count: number;
}

// ============================================================================
// API Functions
// ============================================================================

/**
 * Send a message to the AI chatbot and receive a response.
 *
 * @param message - User's natural language message
 * @returns ChatResponse with assistant's reply and any tool calls
 */
export async function sendMessage(message: string): Promise<ChatResponse> {
  return api.post<ChatResponse>("/api/chat", { message });
}

/**
 * Get the conversation history for the current user.
 *
 * @param limit - Maximum messages to return (default 50, max 200)
 * @param offset - Number of messages to skip (default 0)
 * @returns ChatHistoryResponse with messages and metadata
 */
export async function getHistory(
  limit = 50,
  offset = 0
): Promise<ChatHistoryResponse> {
  return api.get<ChatHistoryResponse>(
    `/api/chat/history?limit=${limit}&offset=${offset}`
  );
}

/**
 * Clear all messages in the user's conversation.
 *
 * @returns void (204 No Content on success)
 */
export async function clearHistory(): Promise<void> {
  await api.delete("/api/chat/clear");
}

// ============================================================================
// Export as namespace
// ============================================================================

export const chatApi = {
  sendMessage,
  getHistory,
  clearHistory,
};

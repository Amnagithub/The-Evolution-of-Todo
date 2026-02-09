"use client";

/**
 * ChatMessage - Individual message bubble with animations.
 *
 * Features:
 * - Role-based styling (user vs assistant)
 * - Slide-in animation on mount (300ms ease-out)
 * - Tool call display with success indicators
 * - Success animation (fade-in + green check) for completed actions
 * - Pending state with opacity
 * - prefers-reduced-motion support via Framer Motion
 */

import { motion, AnimatePresence } from "framer-motion";
import { ToolCallRecord } from "@/lib/chat-api";
import { TaskListAnimation, containsTaskList } from "./TaskListAnimation";

interface ChatMessageProps {
  role: "user" | "assistant";
  content: string;
  toolCalls?: ToolCallRecord[] | null;
  isPending?: boolean;
}

// Animation variants
const messageVariants = {
  hidden: { opacity: 0, y: 10, scale: 0.95 },
  visible: { opacity: 1, y: 0, scale: 1 },
  pending: { opacity: 0.6, y: 0, scale: 1 },
};

const toolCallVariants = {
  hidden: { opacity: 0, x: -10 },
  visible: { opacity: 1, x: 0 },
};

const successCheckVariants = {
  hidden: { scale: 0, opacity: 0 },
  visible: {
    scale: 1,
    opacity: 1,
    transition: { type: "spring", stiffness: 500, damping: 25 },
  },
};

export function ChatMessage({
  role,
  content,
  toolCalls,
  isPending = false,
}: ChatMessageProps) {
  const isUser = role === "user";
  const hasSuccessfulToolCalls = toolCalls?.some(
    (tc) => !("error" in tc.result) && tc.result.status === "created"
  );

  return (
    <motion.div
      variants={messageVariants}
      initial="hidden"
      animate={isPending ? "pending" : "visible"}
      transition={{ duration: 0.3, ease: "easeOut" }}
      className={`flex ${isUser ? "justify-end" : "justify-start"}`}
    >
      <div
        className={`max-w-[80%] rounded-2xl px-4 py-2 ${
          isUser
            ? "bg-blue-600 text-white rounded-br-md"
            : "bg-gray-100 text-gray-800 rounded-bl-md"
        } ${hasSuccessfulToolCalls ? "ring-2 ring-green-400 ring-opacity-50" : ""}`}
      >
        {/* Message content */}
        <div className="text-sm whitespace-pre-wrap break-words">
          {!isUser && containsTaskList(content) ? (
            <TaskListAnimation content={content} />
          ) : (
            content
          )}
        </div>

        {/* Tool calls (assistant only) */}
        {toolCalls && toolCalls.length > 0 && (
          <motion.div
            initial="hidden"
            animate="visible"
            transition={{ staggerChildren: 0.1, delayChildren: 0.2 }}
            className="mt-2 pt-2 border-t border-gray-200/30 space-y-1"
          >
            <AnimatePresence>
              {toolCalls.map((tc, index) => (
                <ToolCallBadge key={index} toolCall={tc} index={index} />
              ))}
            </AnimatePresence>
          </motion.div>
        )}
      </div>
    </motion.div>
  );
}

/**
 * ToolCallBadge - Visual indicator for a tool invocation with animations.
 */
function ToolCallBadge({
  toolCall,
  index,
}: {
  toolCall: ToolCallRecord;
  index: number;
}) {
  const isSuccess = !("error" in toolCall.result);
  const isCreated = toolCall.result.status === "created";
  const toolLabel = toolCall.tool.replace(/_/g, " ");

  // Get task title if available
  const taskTitle = toolCall.result.title as string | undefined;

  return (
    <motion.div
      variants={toolCallVariants}
      transition={{ duration: 0.2, delay: index * 0.1 }}
      className={`flex items-center gap-1.5 text-xs ${
        isSuccess ? "text-green-600" : "text-red-500"
      }`}
    >
      {/* Animated success checkmark */}
      {isSuccess ? (
        <motion.svg
          variants={successCheckVariants}
          className="w-4 h-4"
          fill="currentColor"
          viewBox="0 0 20 20"
        >
          <path
            fillRule="evenodd"
            d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
            clipRule="evenodd"
          />
        </motion.svg>
      ) : (
        <motion.svg
          initial={{ rotate: 0 }}
          animate={{ rotate: [0, -10, 10, -10, 0] }}
          transition={{ duration: 0.3 }}
          className="w-4 h-4"
          fill="currentColor"
          viewBox="0 0 20 20"
        >
          <path
            fillRule="evenodd"
            d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
            clipRule="evenodd"
          />
        </motion.svg>
      )}

      {/* Tool action label */}
      <span className="capitalize font-medium">{toolLabel}</span>

      {/* Task title for created tasks */}
      {isCreated && taskTitle && (
        <span className="text-gray-500">
          &quot;{taskTitle}&quot;
        </span>
      )}

      {/* Success indicator */}
      {isSuccess && isCreated && (
        <motion.span
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.3 }}
          className="text-green-500"
        >
          ✓
        </motion.span>
      )}
    </motion.div>
  );
}

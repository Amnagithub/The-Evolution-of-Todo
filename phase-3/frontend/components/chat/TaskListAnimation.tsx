"use client";

/**
 * TaskListAnimation - Renders task lists with staggered fade-up animation.
 *
 * Features:
 * - Parses markdown task list format
 * - Staggered fade-up animation per task
 * - Visual distinction for completed vs pending tasks
 * - prefers-reduced-motion support via Framer Motion
 */

import { motion } from "framer-motion";

interface TaskListAnimationProps {
  content: string;
}

interface ParsedTask {
  id: string;
  text: string;
  isCompleted: boolean;
}

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.1,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 10 },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.3,
      ease: "easeOut",
    },
  },
};

/**
 * Parse task list content from message.
 * Handles format: "1. [ ] **title** (ID: 123)"
 */
function parseTaskList(content: string): ParsedTask[] {
  const lines = content.split("\n");
  const tasks: ParsedTask[] = [];

  for (const line of lines) {
    // Match pattern: "1. [x] **title** (ID: 123)" or "1. [ ] **title** (ID: 123)"
    const match = line.match(/^\d+\.\s*\[([ x])\]\s*\*\*(.+?)\*\*\s*\(ID:\s*(\d+)\)/i);
    if (match) {
      tasks.push({
        id: match[3],
        text: match[2],
        isCompleted: match[1].toLowerCase() === "x",
      });
    }
  }

  return tasks;
}

/**
 * Check if content contains a task list.
 */
export function containsTaskList(content: string): boolean {
  return /\d+\.\s*\[([ x])\]\s*\*\*.+?\*\*\s*\(ID:\s*\d+\)/i.test(content);
}

export function TaskListAnimation({ content }: TaskListAnimationProps) {
  const tasks = parseTaskList(content);

  if (tasks.length === 0) {
    return <span>{content}</span>;
  }

  // Extract header (e.g., "Here are your tasks:")
  const headerMatch = content.match(/^([^\n]+)\n/);
  const header = headerMatch ? headerMatch[1] : "";

  return (
    <div>
      {header && <p className="mb-2">{header}</p>}
      <motion.ul
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="space-y-1.5"
      >
        {tasks.map((task, index) => (
          <motion.li
            key={task.id}
            variants={itemVariants}
            className={`flex items-center gap-2 text-sm ${
              task.isCompleted ? "text-gray-400" : ""
            }`}
          >
            {/* Checkbox indicator */}
            <span
              className={`flex-shrink-0 w-4 h-4 rounded border ${
                task.isCompleted
                  ? "bg-green-500 border-green-500 text-white"
                  : "border-gray-300"
              } flex items-center justify-center`}
            >
              {task.isCompleted && (
                <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fillRule="evenodd"
                    d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                    clipRule="evenodd"
                  />
                </svg>
              )}
            </span>

            {/* Task title */}
            <span className={task.isCompleted ? "line-through" : ""}>
              {task.text}
            </span>

            {/* Task ID badge */}
            <span className="text-xs text-gray-400 ml-auto">#{task.id}</span>
          </motion.li>
        ))}
      </motion.ul>
    </div>
  );
}

"use client";

/**
 * ToolSpinner - Animated indicator for tool execution.
 *
 * Features:
 * - Rotating spinner with tool name
 * - Smooth fade-in/out transitions
 * - prefers-reduced-motion support via Framer Motion
 * - Optional tool name display
 */

import { motion } from "framer-motion";

interface ToolSpinnerProps {
  /** Name of the tool being executed (optional) */
  toolName?: string;
  /** Size variant */
  size?: "sm" | "md";
}

const spinnerVariants = {
  initial: { opacity: 0, scale: 0.8 },
  animate: {
    opacity: 1,
    scale: 1,
    transition: { duration: 0.2 },
  },
  exit: {
    opacity: 0,
    scale: 0.8,
    transition: { duration: 0.15 },
  },
};

const rotateVariants = {
  animate: {
    rotate: 360,
    transition: {
      duration: 1,
      repeat: Infinity,
      ease: "linear",
    },
  },
};

export function ToolSpinner({ toolName, size = "md" }: ToolSpinnerProps) {
  const sizeClasses = size === "sm" ? "w-4 h-4" : "w-5 h-5";
  const textClasses = size === "sm" ? "text-xs" : "text-sm";

  const formattedToolName = toolName?.replace(/_/g, " ");

  return (
    <motion.div
      variants={spinnerVariants}
      initial="initial"
      animate="animate"
      exit="exit"
      className="flex items-center gap-2 text-gray-500"
    >
      {/* Spinner */}
      <motion.svg
        variants={rotateVariants}
        animate="animate"
        className={`${sizeClasses} text-blue-500`}
        fill="none"
        viewBox="0 0 24 24"
      >
        <circle
          className="opacity-25"
          cx="12"
          cy="12"
          r="10"
          stroke="currentColor"
          strokeWidth="4"
        />
        <path
          className="opacity-75"
          fill="currentColor"
          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
        />
      </motion.svg>

      {/* Tool name label */}
      {formattedToolName && (
        <motion.span
          initial={{ opacity: 0, x: -5 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.1 }}
          className={`${textClasses} capitalize`}
        >
          Running {formattedToolName}...
        </motion.span>
      )}
    </motion.div>
  );
}

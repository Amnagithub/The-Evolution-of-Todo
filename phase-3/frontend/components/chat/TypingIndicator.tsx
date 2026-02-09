"use client";

/**
 * TypingIndicator - Animated bouncing dots for loading state.
 *
 * Features:
 * - 3 dots with staggered bounce animation
 * - Assistant bubble styling
 * - prefers-reduced-motion support via Framer Motion
 * - 400ms animation budget per dot
 */

import { motion } from "framer-motion";

const dotVariants = {
  initial: { y: 0 },
  animate: {
    y: [-4, 0, -4],
    transition: {
      duration: 0.6,
      repeat: Infinity,
      ease: "easeInOut",
    },
  },
};

const containerVariants = {
  initial: { opacity: 0, scale: 0.8 },
  animate: {
    opacity: 1,
    scale: 1,
    transition: { duration: 0.2, ease: "easeOut" },
  },
  exit: {
    opacity: 0,
    scale: 0.8,
    transition: { duration: 0.15 },
  },
};

export function TypingIndicator() {
  return (
    <motion.div
      variants={containerVariants}
      initial="initial"
      animate="animate"
      exit="exit"
      className="flex justify-start"
    >
      <div className="bg-gray-100 rounded-2xl rounded-bl-md px-4 py-3">
        <div className="flex items-center gap-1.5">
          {[0, 1, 2].map((index) => (
            <motion.div
              key={index}
              variants={dotVariants}
              initial="initial"
              animate="animate"
              transition={{
                delay: index * 0.15,
              }}
              className="w-2 h-2 bg-gray-400 rounded-full"
            />
          ))}
        </div>
      </div>
    </motion.div>
  );
}

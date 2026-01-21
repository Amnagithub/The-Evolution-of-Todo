"use client";

import { useState } from "react";
import Link from "next/link";

interface Task {
  id: number;
  title: string;
  description: string | null;
  completed: boolean;
  priority: string;
  created_at: string;
  updated_at: string;
}

interface TaskListProps {
  tasks: Task[];
  onToggleComplete: (taskId: number, completed: boolean) => Promise<void>;
  onUpdate: (taskId: number, title: string, description: string, priority: string) => Promise<void>;
  onDelete: (taskId: number) => Promise<void>;
}

const priorityColors: Record<string, string> = {
  high: "bg-red-100 text-red-800",
  medium: "bg-yellow-100 text-yellow-800",
  low: "bg-green-100 text-green-800",
};

const priorityLabels: Record<string, string> = {
  high: "High",
  medium: "Medium",
  low: "Low",
};

export function TaskList({ tasks, onToggleComplete, onUpdate, onDelete }: TaskListProps) {
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editTitle, setEditTitle] = useState("");
  const [editDescription, setEditDescription] = useState("");
  const [editPriority, setEditPriority] = useState("medium");
  const [deletingId, setDeletingId] = useState<number | null>(null);

  const startEditing = (task: Task) => {
    setEditingId(task.id);
    setEditTitle(task.title);
    setEditDescription(task.description || "");
    setEditPriority(task.priority);
  };

  const cancelEditing = () => {
    setEditingId(null);
    setEditTitle("");
    setEditDescription("");
    setEditPriority("medium");
  };

  const saveEdit = async (taskId: number) => {
    if (!editTitle.trim()) return;
    await onUpdate(taskId, editTitle.trim(), editDescription.trim(), editPriority);
    cancelEditing();
  };

  const confirmDelete = async (taskId: number) => {
    await onDelete(taskId);
    setDeletingId(null);
  };

  if (tasks.length === 0) {
    return (
      <div className="bg-white p-8 rounded-lg shadow-sm border text-center text-gray-500">
        No tasks yet. Create your first task above!
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {tasks.map((task) => (
        <div
          key={task.id}
          className={`bg-white p-4 rounded-lg shadow-sm border ${
            task.completed ? "opacity-60" : ""
          }`}
        >
          {editingId === task.id ? (
            // Edit mode
            <div className="space-y-3">
              <input
                type="text"
                value={editTitle}
                onChange={(e) => setEditTitle(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                maxLength={200}
              />
              <textarea
                value={editDescription}
                onChange={(e) => setEditDescription(e.target.value)}
                rows={2}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Description (optional)"
              />
              <select
                value={editPriority}
                onChange={(e) => setEditPriority(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
              <div className="flex gap-2">
                <button
                  onClick={() => saveEdit(task.id)}
                  className="px-3 py-1 bg-blue-600 text-white text-sm rounded hover:bg-blue-700"
                >
                  Save
                </button>
                <button
                  onClick={cancelEditing}
                  className="px-3 py-1 border border-gray-300 text-sm rounded hover:bg-gray-50"
                >
                  Cancel
                </button>
              </div>
            </div>
          ) : deletingId === task.id ? (
            // Delete confirmation
            <div className="text-center py-2">
              <p className="text-gray-700 mb-3">Delete this task?</p>
              <div className="flex justify-center gap-2">
                <button
                  onClick={() => confirmDelete(task.id)}
                  className="px-4 py-1 bg-red-600 text-white text-sm rounded hover:bg-red-700"
                >
                  Delete
                </button>
                <button
                  onClick={() => setDeletingId(null)}
                  className="px-4 py-1 border border-gray-300 text-sm rounded hover:bg-gray-50"
                >
                  Cancel
                </button>
              </div>
            </div>
          ) : (
            // View mode
            <div className="flex items-start gap-3">
              <input
                type="checkbox"
                checked={task.completed}
                onChange={() => onToggleComplete(task.id, !task.completed)}
                className="mt-1 h-5 w-5 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              />
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 flex-wrap">
                  <h3
                    className={`font-medium ${
                      task.completed ? "line-through text-gray-500" : "text-gray-900"
                    }`}
                  >
                    {task.title}
                  </h3>
                  <span
                    className={`px-2 py-0.5 text-xs font-medium rounded-full ${
                      priorityColors[task.priority] || priorityColors.medium
                    }`}
                  >
                    {priorityLabels[task.priority] || "Medium"}
                  </span>
                </div>
                {task.description && (
                  <p className="text-sm text-gray-500 mt-1">{task.description}</p>
                )}
                <p className="text-xs text-gray-400 mt-2">
                  Created: {new Date(task.created_at).toLocaleDateString()}
                </p>
              </div>
              <div className="flex gap-2">
                <Link
                  href={`/tasks/${task.id}`}
                  className="px-2 py-1 text-sm text-gray-600 hover:text-blue-600"
                >
                  View
                </Link>
                <button
                  onClick={() => startEditing(task)}
                  className="px-2 py-1 text-sm text-gray-600 hover:text-blue-600"
                >
                  Edit
                </button>
                <button
                  onClick={() => setDeletingId(task.id)}
                  className="px-2 py-1 text-sm text-gray-600 hover:text-red-600"
                >
                  Delete
                </button>
              </div>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}

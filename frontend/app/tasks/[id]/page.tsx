"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { AuthGuard } from "@/components/AuthGuard";
import { Header } from "@/components/Header";
import { api, ApiError } from "@/lib/api";

interface Task {
  id: number;
  title: string;
  description: string | null;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

function TaskDetailContent() {
  const params = useParams();
  const router = useRouter();
  const [task, setTask] = useState<Task | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  const taskId = params.id as string;

  useEffect(() => {
    async function fetchTask() {
      try {
        const data = await api.get<Task>(`/api/tasks/${taskId}`);
        setTask(data);
        setError("");
      } catch (err) {
        if (err instanceof ApiError && err.status === 404) {
          setError("Task not found");
        } else {
          setError("Failed to load task");
        }
      } finally {
        setIsLoading(false);
      }
    }

    if (taskId) {
      fetchTask();
    }
  }, [taskId]);

  const handleToggleComplete = async () => {
    if (!task) return;

    const newCompleted = !task.completed;
    setTask({ ...task, completed: newCompleted });

    try {
      await api.patch(`/api/tasks/${task.id}/complete`, { completed: newCompleted });
    } catch {
      setTask({ ...task, completed: !newCompleted });
    }
  };

  const handleDelete = async () => {
    if (!task) return;

    if (!confirm("Are you sure you want to delete this task?")) {
      return;
    }

    try {
      await api.delete(`/api/tasks/${task.id}`);
      router.push("/tasks");
    } catch {
      setError("Failed to delete task");
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[200px]">
        <div className="text-gray-500">Loading task...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-2xl mx-auto">
        <div className="bg-red-50 text-red-600 p-6 rounded-lg text-center">
          <p className="mb-4">{error}</p>
          <Link
            href="/tasks"
            className="text-blue-600 hover:underline"
          >
            Back to Tasks
          </Link>
        </div>
      </div>
    );
  }

  if (!task) {
    return null;
  }

  return (
    <div className="max-w-2xl mx-auto">
      <div className="mb-4">
        <Link
          href="/tasks"
          className="text-blue-600 hover:underline text-sm"
        >
          &larr; Back to Tasks
        </Link>
      </div>

      <div className="bg-white p-6 rounded-lg shadow-sm border">
        <div className="flex items-start justify-between mb-4">
          <h1 className={`text-2xl font-bold ${task.completed ? "line-through text-gray-500" : "text-gray-900"}`}>
            {task.title}
          </h1>
          <span
            className={`px-3 py-1 rounded-full text-sm font-medium ${
              task.completed
                ? "bg-green-100 text-green-800"
                : "bg-yellow-100 text-yellow-800"
            }`}
          >
            {task.completed ? "Completed" : "Pending"}
          </span>
        </div>

        {task.description && (
          <div className="mb-6">
            <h2 className="text-sm font-medium text-gray-500 mb-2">Description</h2>
            <p className="text-gray-700 whitespace-pre-wrap">{task.description}</p>
          </div>
        )}

        <div className="border-t pt-4 space-y-2">
          <div className="flex justify-between text-sm">
            <span className="text-gray-500">Created:</span>
            <span className="text-gray-700">
              {new Date(task.created_at).toLocaleString()}
            </span>
          </div>
          <div className="flex justify-between text-sm">
            <span className="text-gray-500">Last Updated:</span>
            <span className="text-gray-700">
              {new Date(task.updated_at).toLocaleString()}
            </span>
          </div>
          <div className="flex justify-between text-sm">
            <span className="text-gray-500">Task ID:</span>
            <span className="text-gray-700">{task.id}</span>
          </div>
        </div>

        <div className="border-t mt-6 pt-6 flex gap-3">
          <button
            onClick={handleToggleComplete}
            className={`px-4 py-2 rounded-md text-sm font-medium ${
              task.completed
                ? "bg-yellow-100 text-yellow-800 hover:bg-yellow-200"
                : "bg-green-100 text-green-800 hover:bg-green-200"
            }`}
          >
            {task.completed ? "Mark as Pending" : "Mark as Completed"}
          </button>
          <Link
            href="/tasks"
            className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
          >
            Edit in List
          </Link>
          <button
            onClick={handleDelete}
            className="px-4 py-2 bg-red-100 text-red-800 rounded-md text-sm font-medium hover:bg-red-200"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  );
}

export default function TaskDetailPage() {
  return (
    <AuthGuard>
      <Header />
      <TaskDetailContent />
    </AuthGuard>
  );
}

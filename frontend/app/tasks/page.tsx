"use client";

import { useEffect, useState, useCallback } from "react";
import { AuthGuard } from "@/components/AuthGuard";
import { Header } from "@/components/Header";
import { TaskForm } from "@/components/TaskForm";
import { TaskList } from "@/components/TaskList";
import { api } from "@/lib/api";

interface Task {
  id: number;
  title: string;
  description: string | null;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

function TasksContent() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchTasks = useCallback(async () => {
    try {
      const data = await api.get<Task[]>("/api/tasks");
      setTasks(data);
      setError("");
    } catch {
      setError("Failed to load tasks");
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  const handleCreateTask = async (title: string, description: string) => {
    const newTask = await api.post<Task>("/api/tasks", { title, description: description || null });
    setTasks((prev) => [newTask, ...prev]);
  };

  const handleToggleComplete = async (taskId: number, completed: boolean) => {
    // Optimistic update
    setTasks((prev) =>
      prev.map((task) =>
        task.id === taskId ? { ...task, completed } : task
      )
    );

    try {
      await api.patch(`/api/tasks/${taskId}/complete`, { completed });
    } catch {
      // Rollback on error
      setTasks((prev) =>
        prev.map((task) =>
          task.id === taskId ? { ...task, completed: !completed } : task
        )
      );
    }
  };

  const handleUpdateTask = async (taskId: number, title: string, description: string) => {
    const updatedTask = await api.put<Task>(`/api/tasks/${taskId}`, {
      title,
      description: description || null,
    });
    setTasks((prev) =>
      prev.map((task) => (task.id === taskId ? updatedTask : task))
    );
  };

  const handleDeleteTask = async (taskId: number) => {
    // Optimistic delete
    const taskToDelete = tasks.find((t) => t.id === taskId);
    setTasks((prev) => prev.filter((task) => task.id !== taskId));

    try {
      await api.delete(`/api/tasks/${taskId}`);
    } catch {
      // Rollback on error
      if (taskToDelete) {
        setTasks((prev) => [...prev, taskToDelete].sort((a, b) =>
          new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
        ));
      }
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[200px]">
        <div className="text-gray-500">Loading tasks...</div>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <TaskForm onSubmit={handleCreateTask} />

      {error && (
        <div className="bg-red-50 text-red-600 p-4 rounded-lg">
          {error}
          <button
            onClick={fetchTasks}
            className="ml-4 underline hover:no-underline"
          >
            Retry
          </button>
        </div>
      )}

      <div>
        <h2 className="text-lg font-semibold mb-4">
          Your Tasks ({tasks.length})
        </h2>
        <TaskList
          tasks={tasks}
          onToggleComplete={handleToggleComplete}
          onUpdate={handleUpdateTask}
          onDelete={handleDeleteTask}
        />
      </div>
    </div>
  );
}

export default function TasksPage() {
  return (
    <AuthGuard>
      <Header />
      <TasksContent />
    </AuthGuard>
  );
}

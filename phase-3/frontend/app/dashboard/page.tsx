"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useSession, signOut } from "@/lib/auth-client";
import Link from "next/link";

interface TaskStats {
  total: number;
  completed: number;
  pending: number;
}

export default function Dashboard() {
  const router = useRouter();
  const { data: session, isPending } = useSession();
  const [stats, setStats] = useState<TaskStats>({ total: 0, completed: 0, pending: 0 });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!isPending && !session) {
      router.push("/signin");
    }
  }, [session, isPending, router]);

  useEffect(() => {
    async function fetchStats() {
      try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/tasks`, {
          headers: {
            "Authorization": `Bearer ${session?.session?.token || ""}`,
          },
        });
        if (response.ok) {
          const tasks = await response.json();
          const completed = tasks.filter((t: any) => t.completed).length;
          setStats({
            total: tasks.length,
            completed,
            pending: tasks.length - completed,
          });
        }
      } catch (error) {
        console.error("Failed to fetch stats:", error);
      } finally {
        setLoading(false);
      }
    }

    if (session) {
      fetchStats();
    }
  }, [session]);

  if (isPending) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-gray-500">Loading...</div>
      </div>
    );
  }

  if (!session) {
    return null;
  }

  const handleSignOut = async () => {
    try {
      await signOut();
      // Always redirect after signOut completes
      router.push("/signin");
      router.refresh();
    } catch (error) {
      console.error("Sign out error:", error);
      // Force redirect even if signOut fails
      router.push("/signin");
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600 mt-1">
            Welcome back, {session.user?.name || session.user?.email || "User"}!
          </p>
        </div>
        <button
          onClick={handleSignOut}
          className="px-4 py-2 text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
        >
          Sign Out
        </button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-500">Total Tasks</p>
              <p className="text-3xl font-bold text-gray-900 mt-1">
                {loading ? "..." : stats.total}
              </p>
            </div>
            <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
              <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-500">Completed</p>
              <p className="text-3xl font-bold text-green-600 mt-1">
                {loading ? "..." : stats.completed}
              </p>
            </div>
            <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
              <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-500">Pending</p>
              <p className="text-3xl font-bold text-orange-600 mt-1">
                {loading ? "..." : stats.pending}
              </p>
            </div>
            <div className="w-12 h-12 bg-orange-100 rounded-full flex items-center justify-center">
              <svg className="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-8">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Link
            href="/tasks"
            className="flex items-center gap-4 p-4 rounded-lg border border-gray-200 hover:border-blue-300 hover:bg-blue-50 transition-colors"
          >
            <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
              <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 10h16M4 14h16M4 18h16" />
              </svg>
            </div>
            <div>
              <p className="font-medium text-gray-900">View All Tasks</p>
              <p className="text-sm text-gray-500">Manage your todo list</p>
            </div>
          </Link>

          <div className="flex items-center gap-4 p-4 rounded-lg border border-gray-200 bg-gradient-to-r from-blue-50 to-purple-50">
            <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg flex items-center justify-center">
              <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
            </div>
            <div>
              <p className="font-medium text-gray-900">AI Assistant</p>
              <p className="text-sm text-gray-500">Click the chat button below</p>
            </div>
          </div>
        </div>
      </div>

      {/* Tips */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl p-6 text-white">
        <h2 className="text-lg font-semibold mb-2">Try the AI Assistant</h2>
        <p className="text-blue-100 mb-4">
          Use natural language to manage your tasks. Click the chat button in the bottom-right corner and try:
        </p>
        <ul className="space-y-2 text-sm">
          <li className="flex items-center gap-2">
            <span className="w-1.5 h-1.5 bg-white rounded-full"></span>
            &quot;Add buy groceries&quot; - to create a new task
          </li>
          <li className="flex items-center gap-2">
            <span className="w-1.5 h-1.5 bg-white rounded-full"></span>
            &quot;Show my tasks&quot; - to see all your tasks
          </li>
          <li className="flex items-center gap-2">
            <span className="w-1.5 h-1.5 bg-white rounded-full"></span>
            &quot;Done buy groceries&quot; - to mark a task complete
          </li>
        </ul>
      </div>
    </div>
  );
}

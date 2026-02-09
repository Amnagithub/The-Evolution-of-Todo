# Feature Specification: Analytics Dashboard

**Feature Branch**: `002-analytics-dashboard`
**Created**: 2026-02-05
**Status**: Draft
**Input**: User description: "Analytics Dashboard for AI Todo Chatbot app - task analytics, chat analytics, productivity metrics, quick stats, data visualization with charts"

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Quick Stats Overview (Priority: P1)

As an authenticated user, I want to see a quick summary of my task statistics (total tasks, completed this week, pending tasks, chat messages today) at the top of the dashboard so that I can get an instant snapshot of my productivity without scrolling or clicking.

**Why this priority**: This is the first thing users see - if basic stats are missing or slow, users will lose confidence in the dashboard immediately. Quick stats provide immediate value with minimal data requirements.

**Independent Test**: Can be fully tested by creating 5 tasks (3 completed, 2 pending), sending 3 chat messages, then verifying the quick stats cards display correct counts.

**Acceptance Scenarios**:

1. **Given** an authenticated user with 10 total tasks, **When** they navigate to /dashboard, **Then** they see a "Total Tasks" card displaying "10" with appropriate icon.
2. **Given** an authenticated user who completed 3 tasks this week, **When** they view the dashboard, **Then** they see a "Completed This Week" card displaying "3" with a green indicator.
3. **Given** an authenticated user with 4 pending tasks, **When** they view the dashboard, **Then** they see a "Pending Tasks" card displaying "4" with an appropriate pending indicator.
4. **Given** an authenticated user who sent 7 chat messages today, **When** they view the dashboard, **Then** they see a "Messages Today" card displaying "7".
5. **Given** a new user with no tasks or messages, **When** they view the dashboard, **Then** all quick stat cards display "0" gracefully without errors.

---

### User Story 2 - Task Completion Status Distribution (Priority: P1)

As an authenticated user, I want to see a visual breakdown of my tasks by completion status (completed vs pending) as a pie or donut chart so that I can understand my overall task completion ratio at a glance.

**Why this priority**: Core analytics feature - provides the most fundamental insight into task management effectiveness. A single chart that tells users immediately if they're keeping up with their work.

**Independent Test**: Can be tested by creating 6 tasks (4 completed, 2 pending), viewing the dashboard, and verifying the chart shows ~67% completed segment and ~33% pending segment with correct labels.

**Acceptance Scenarios**:

1. **Given** an authenticated user with 8 completed and 2 pending tasks, **When** they view the task status chart, **Then** they see a donut chart with 80% completed (green) and 20% pending (amber/yellow) segments.
2. **Given** an authenticated user hovering over a chart segment, **When** they interact with the chart, **Then** they see a tooltip showing exact count and percentage (e.g., "Completed: 8 (80%)").
3. **Given** a user with only completed tasks, **When** they view the chart, **Then** it displays 100% completed without visual errors.
4. **Given** a user with no tasks, **When** they view the chart, **Then** they see an empty state message "No tasks yet - create your first task!" instead of an empty chart.

---

### User Story 3 - Task Completion Over Time (Priority: P1)

As an authenticated user, I want to see a line chart showing how many tasks I completed over time (daily, weekly, or monthly view) so that I can track my productivity trends and identify patterns.

**Why this priority**: Essential for understanding productivity trends - helps users see if they're improving, declining, or maintaining consistent output. Provides actionable insights.

**Independent Test**: Can be tested by completing tasks on different dates over a 2-week period, then verifying the line chart shows correct completion counts per day with smooth animated rendering.

**Acceptance Scenarios**:

1. **Given** an authenticated user with task completion history, **When** they view the completion trend chart, **Then** they see a line chart showing completion count per day for the last 7 days (default view).
2. **Given** an authenticated user viewing the completion chart, **When** they select "Weekly" view, **Then** the chart updates to show completion counts per week for the last 4 weeks.
3. **Given** an authenticated user viewing the completion chart, **When** they select "Monthly" view, **Then** the chart updates to show completion counts per month for the last 6 months.
4. **Given** a user hovering over a data point, **When** they interact with the chart, **Then** they see a tooltip showing the exact date and completion count.
5. **Given** a new user with no completion history, **When** they view the chart, **Then** they see a flat line at 0 with an encouraging message.

---

### User Story 4 - Tasks by Priority Distribution (Priority: P2)

As an authenticated user, I want to see a breakdown of my tasks by priority level (low, medium, high) as a bar or stacked chart so that I can understand how I'm distributing my work priorities.

**Why this priority**: Important for understanding task composition but secondary to completion metrics. Users first want to know what's done; then they care about priority distribution.

**Independent Test**: Can be tested by creating 6 tasks (2 high, 3 medium, 1 low priority), viewing the dashboard, and verifying the chart shows correct counts per priority level.

**Acceptance Scenarios**:

1. **Given** an authenticated user with tasks across all priority levels, **When** they view the priority chart, **Then** they see a horizontal bar chart with bars for High (red), Medium (yellow), Low (green).
2. **Given** an authenticated user with 5 high priority tasks, **When** they view the chart, **Then** the High priority bar shows "5" with appropriate scaling.
3. **Given** a user with tasks only at one priority level, **When** they view the chart, **Then** only that priority level shows a bar; others show 0 or empty.

---

### User Story 5 - Average Time to Complete Tasks (Priority: P2)

As an authenticated user, I want to see the average time it takes me to complete a task (from creation to completion) so that I can understand my task throughput and set realistic expectations.

**Why this priority**: Valuable metric for self-improvement but requires completed tasks with timestamp data. Not critical for initial dashboard experience.

**Independent Test**: Can be tested by creating a task, waiting 24 hours (or setting mock dates), completing it, then verifying the average shows approximately 24 hours or 1 day.

**Acceptance Scenarios**:

1. **Given** an authenticated user with 5 completed tasks averaging 3 days to complete, **When** they view the average completion time metric, **Then** they see "Avg. Completion Time: 3 days".
2. **Given** a user with fast task completion (under 1 day), **When** they view the metric, **Then** they see time displayed in hours (e.g., "Avg. Completion Time: 6 hours").
3. **Given** a user with no completed tasks, **When** they view the metric, **Then** they see "Avg. Completion Time: N/A" or "Complete your first task to see this metric".

---

### User Story 6 - Chat Analytics Summary (Priority: P2)

As an authenticated user, I want to see analytics about my chat usage (total messages, tool usage breakdown, tool success rate) so that I can understand how I'm using the AI assistant.

**Why this priority**: Important for Phase III chatbot feature evaluation but secondary to core task analytics. Users need task insights first before caring about chat usage patterns.

**Independent Test**: Can be tested by having a conversation with multiple tool calls, then verifying the chat analytics section shows correct message count and tool breakdown.

**Acceptance Scenarios**:

1. **Given** an authenticated user with 50 total chat messages, **When** they view chat analytics, **Then** they see "Total Messages: 50" prominently displayed.
2. **Given** a user whose conversations used add_task (10 times), list_tasks (15 times), complete_task (8 times), **When** they view tool usage breakdown, **Then** they see a bar chart showing each tool with its usage count.
3. **Given** tool calls with 90% success rate, **When** the user views tool success metric, **Then** they see "Tool Success Rate: 90%" with a green indicator.
4. **Given** a user with no chat history, **When** they view chat analytics, **Then** they see an empty state "No chat history yet - start a conversation!".

---

### User Story 7 - Productivity Streak Tracking (Priority: P2)

As an authenticated user, I want to see my current streak (consecutive days with at least one completed task) and longest streak so that I can stay motivated to maintain productivity habits.

**Why this priority**: Gamification element that drives engagement. Secondary because core metrics are more immediately actionable.

**Independent Test**: Can be tested by completing tasks on 5 consecutive days, skipping a day, then completing on day 7, verifying current streak shows 1 and longest streak shows 5.

**Acceptance Scenarios**:

1. **Given** a user who completed tasks on 7 consecutive days, **When** they view the streak section, **Then** they see "Current Streak: 7 days" with a flame icon.
2. **Given** a user with a longest streak of 14 days but current streak of 3, **When** they view streaks, **Then** they see both "Current Streak: 3 days" and "Longest Streak: 14 days".
3. **Given** a user who hasn't completed a task today, **When** they view the streak, **Then** they see a warning "Complete a task today to keep your streak!".
4. **Given** a new user with no completed tasks, **When** they view the streak, **Then** they see "Current Streak: 0 days - complete your first task to start!".

---

### User Story 8 - Most Productive Days/Hours (Priority: P3)

As an authenticated user, I want to see which days of the week and hours of the day I'm most productive (based on task completions) so that I can optimize my schedule.

**Why this priority**: Advanced analytics that require substantial data to be meaningful. Nice-to-have after core metrics are established.

**Independent Test**: Can be tested by completing tasks at various times/days over a week, then verifying the heatmap or chart reflects the actual completion distribution.

**Acceptance Scenarios**:

1. **Given** a user with task completions across different days, **When** they view productive days chart, **Then** they see a bar chart showing completion counts by day of week.
2. **Given** a user who completes most tasks between 9-11 AM, **When** they view productive hours, **Then** they see those hours highlighted as peak productivity.
3. **Given** insufficient data (fewer than 10 completed tasks), **When** they view this section, **Then** they see "Need more data for accurate insights (10+ completed tasks required)".

---

### User Story 9 - Weekly/Monthly Goals Progress (Priority: P3)

As an authenticated user, I want to set and track weekly or monthly task completion goals so that I can measure my productivity against personal targets.

**Why this priority**: Requires goal-setting infrastructure. Nice-to-have feature that builds on core analytics.

**Independent Test**: Can be tested by setting a weekly goal of 10 tasks, completing 6, and verifying the progress bar shows 60% completion with correct messaging.

**Acceptance Scenarios**:

1. **Given** a user has set a weekly goal of 20 tasks and completed 15, **When** they view the goals section, **Then** they see a progress bar at 75% with "15/20 tasks completed".
2. **Given** a user has not set any goals, **When** they view the goals section, **Then** they see a prompt "Set a weekly goal to track your progress".
3. **Given** a user has exceeded their goal (25 of 20 completed), **When** they view goals, **Then** they see a celebratory message "Goal exceeded! 25/20 tasks" with confetti animation.

---

### User Story 10 - Productivity Score (Priority: P3)

As an authenticated user, I want to see an overall productivity score (0-100) that gamifies my productivity based on completion rate, streak, and consistency so that I have a single metric to track my overall performance.

**Why this priority**: Gamification feature that requires multiple metrics to compute. Nice-to-have after individual metrics are established.

**Independent Test**: Can be tested by meeting criteria for high productivity (high completion rate, active streak, consistent daily completion) and verifying score reflects these factors.

**Acceptance Scenarios**:

1. **Given** a user with 90% completion rate, 7-day streak, and consistent daily activity, **When** they view productivity score, **Then** they see a score of 85+ displayed prominently with a motivational badge.
2. **Given** a user with low metrics across the board, **When** they view the score, **Then** they see a lower score with suggestions for improvement.
3. **Given** a new user with no data, **When** they view the score, **Then** they see "Complete tasks to earn your productivity score!".

---

### User Story 11 - Responsive Dashboard Layout (Priority: P1)

As an authenticated user, I want the analytics dashboard to be fully responsive and usable on mobile, tablet, and desktop devices so that I can check my productivity from any device.

**Why this priority**: Critical for user experience - users expect dashboards to work on mobile. Blockers on mobile would reduce feature adoption significantly.

**Independent Test**: Can be tested by viewing the dashboard at 375px, 768px, and 1200px widths and verifying all charts and stats are visible and usable.

**Acceptance Scenarios**:

1. **Given** a user on a mobile device (width < 640px), **When** they view the dashboard, **Then** charts stack vertically with touch-friendly interactions.
2. **Given** a user on a tablet (640px-1024px), **When** they view the dashboard, **Then** they see a 2-column layout for stats cards and charts.
3. **Given** a user on desktop (> 1024px), **When** they view the dashboard, **Then** they see a full 4-column stats row and 2-column chart grid.
4. **Given** any device, **When** the user views charts, **Then** charts resize proportionally without breaking or overflowing.

---

### User Story 12 - Dark/Light Mode Support (Priority: P2)

As an authenticated user, I want the analytics dashboard to support both dark and light mode themes so that I can use it comfortably in any lighting condition.

**Why this priority**: Important for user experience and accessibility but not blocking core functionality.

**Independent Test**: Can be tested by toggling theme preference and verifying all chart colors, backgrounds, and text remain readable and visually consistent.

**Acceptance Scenarios**:

1. **Given** a user with system preference for dark mode, **When** they view the dashboard, **Then** all elements use dark theme colors (dark backgrounds, light text, appropriate chart colors).
2. **Given** a user toggling from light to dark mode, **When** the toggle occurs, **Then** charts animate smoothly to new color scheme within 300ms.
3. **Given** any theme, **When** the user views charts, **Then** chart colors maintain sufficient contrast for accessibility (WCAG AA).

---

### Edge Cases

- What happens when a user has thousands of tasks? -> Pagination or rolling windows for charts; aggregated data only (no loading all tasks at once).
- What happens when calculating average time for tasks completed within seconds? -> Display "< 1 minute" instead of showing 0 or decimals.
- What happens when the database query times out? -> Show graceful error with retry button; use cached data if available.
- What happens when a user views the dashboard while offline? -> Show cached analytics if available; display "You're offline" message with last updated timestamp.
- What happens when date calculations span timezone changes (DST)? -> Use UTC for all backend calculations; display in user's local timezone on frontend.
- What happens when a user has tasks created before Phase III migration? -> Include all historical data; handle missing fields gracefully (null chat history for old tasks).
- What happens when chart library fails to load? -> Fallback to numerical display only with message "Charts temporarily unavailable".

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a dedicated `/dashboard` route accessible only to authenticated users
- **FR-002**: System MUST display quick stats cards: Total Tasks, Completed This Week, Pending Tasks, Messages Today
- **FR-003**: System MUST display a donut chart showing task completion status distribution (completed vs pending)
- **FR-004**: System MUST display a line chart showing task completion over time with daily/weekly/monthly toggles
- **FR-005**: System MUST display a bar chart showing tasks by priority distribution (low, medium, high)
- **FR-006**: System MUST calculate and display average time to complete tasks
- **FR-007**: System MUST display chat analytics: total messages, tool usage breakdown chart, tool success rate
- **FR-008**: System MUST track and display current streak (consecutive days with completed tasks)
- **FR-009**: System MUST track and display longest streak achieved
- **FR-010**: System MUST display most productive days of week (based on completion counts)
- **FR-011**: System MUST display most productive hours of day (based on completion timestamps)
- **FR-012**: System MUST allow users to set weekly/monthly task completion goals
- **FR-013**: System MUST display goal progress as a visual progress bar with percentage
- **FR-014**: System MUST calculate and display a productivity score (0-100) based on multiple factors
- **FR-015**: System MUST filter all analytics data by authenticated user_id (no cross-user data access)
- **FR-016**: System MUST provide responsive layout for mobile (< 640px), tablet (640-1024px), and desktop (> 1024px)
- **FR-017**: System MUST support dark and light mode themes with smooth transitions
- **FR-018**: System MUST show appropriate empty states when no data is available for a chart/metric
- **FR-019**: System MUST use animated chart transitions for professional appearance
- **FR-020**: System MUST add a "Dashboard" link to the main navigation accessible after authentication
- **FR-021**: System MUST use Recharts library for chart visualizations
- **FR-022**: System MUST respect `prefers-reduced-motion` for users with motion sensitivity

### Key Entities

- **Task** (existing): id, user_id, title, description, completed, priority, created_at, updated_at - No changes needed; analytics derived from existing data.

- **Message** (from Phase III chatbot): id, user_id, conversation_id, role, content, tool_calls, created_at - Used for chat analytics; no changes needed if exists.

- **UserGoal** (new): Represents a user's productivity goal setting.
  - id: Primary key
  - user_id: Foreign key to User (required)
  - goal_type: "weekly" or "monthly" (required)
  - target_count: Integer target number of tasks (required, min 1)
  - created_at: Timestamp of goal creation
  - updated_at: Timestamp of last modification

- **ToolCall** (from Phase III chatbot): If tracking tool calls separately - tool_name, success, timestamp, user_id. May be embedded in Message.tool_calls JSON field.

---

## API Endpoints *(new)*

### Analytics Endpoints

| Method | Path | Description | Response |
|--------|------|-------------|----------|
| GET | /api/analytics/summary | Quick stats (total, pending, completed this week, messages today) | `{total_tasks, pending_tasks, completed_this_week, messages_today}` |
| GET | /api/analytics/tasks/status | Task completion status distribution | `{completed: n, pending: n}` |
| GET | /api/analytics/tasks/completion-trend | Task completion over time | `[{date, count}]` with query param `period=daily|weekly|monthly` |
| GET | /api/analytics/tasks/priority | Tasks by priority distribution | `{low: n, medium: n, high: n}` |
| GET | /api/analytics/tasks/avg-completion-time | Average time to complete tasks | `{avg_hours: n, avg_days: n, display: "string"}` |
| GET | /api/analytics/tasks/productive-times | Most productive days/hours | `{days: [{day, count}], hours: [{hour, count}]}` |
| GET | /api/analytics/chat/summary | Chat analytics summary | `{total_messages, tool_calls: {tool: count}, success_rate: n}` |
| GET | /api/analytics/streak | Current and longest streak | `{current_streak: n, longest_streak: n, streak_at_risk: bool}` |
| GET | /api/analytics/productivity-score | Calculated productivity score | `{score: n, factors: {...}, badge: "string"}` |
| GET | /api/goals | Get user's current goals | `[{id, goal_type, target_count, progress, percentage}]` |
| POST | /api/goals | Create/update a goal | Request: `{goal_type, target_count}` Response: `{goal}` |
| DELETE | /api/goals/{goal_id} | Delete a goal | 204 No Content |

**Security**: All endpoints require authenticated user; filter by user_id extracted from session/JWT.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Dashboard page loads and displays all quick stats within 2 seconds on desktop (3G: 5 seconds)
- **SC-002**: All chart visualizations render correctly with animations completing within 500ms
- **SC-003**: 100% of analytics queries filter by authenticated user_id (no data leakage between users)
- **SC-004**: Dashboard is fully usable at viewport widths of 375px, 768px, and 1440px
- **SC-005**: All charts support both dark and light modes with WCAG AA contrast compliance
- **SC-006**: Users with `prefers-reduced-motion` see no animated transitions (instant rendering)
- **SC-007**: Empty states display appropriate messages for all charts when no data exists
- **SC-008**: Goal progress updates in real-time when tasks are completed (within 30 seconds)
- **SC-009**: Streak calculations are accurate to the day based on UTC timezone
- **SC-010**: Chart tooltips display on hover (desktop) and tap (mobile) with correct data values
- **SC-011**: Dashboard link appears in navigation for authenticated users only
- **SC-012**: Backend analytics queries complete within 500ms for users with up to 1000 tasks

---

## Non-Functional Requirements

| Aspect | Requirement |
|--------|-------------|
| Performance | Dashboard initial load < 2s; charts render < 500ms; API responses < 500ms |
| Security | All endpoints enforce user_id filtering; no cross-user data exposure |
| Accessibility | WCAG AA contrast; keyboard navigable; screen reader compatible; respects reduced motion |
| Responsiveness | Mobile-first design; breakpoints at 640px, 1024px |
| Theming | Support system preference and manual dark/light toggle |
| Caching | Consider client-side caching for analytics data (5 minute TTL) |
| Error Handling | Graceful degradation if charts fail; fallback to numerical display |
| Data Freshness | Analytics data reflects changes within 30 seconds of task operations |

---

## Technical Implementation Notes

### Chart Library

Use Recharts for all visualizations:
- Donut/Pie: `<PieChart>` with `<Pie>` component
- Line: `<LineChart>` with `<Line>` component
- Bar: `<BarChart>` with `<Bar>` component
- Responsive: Wrap all charts in `<ResponsiveContainer>`

### Color Palette

Leverage existing Tailwind CSS design system:
- Completed: Green (green-500/green-400 dark)
- Pending: Amber (amber-500/amber-400 dark)
- High Priority: Red (red-500/red-400 dark)
- Medium Priority: Yellow (yellow-500/yellow-400 dark)
- Low Priority: Blue (blue-500/blue-400 dark)
- Chart backgrounds adapt to theme (white/slate-800)

### Backend Query Optimization

- Use SQL aggregations for counts, not loading all records
- Index `user_id` and `created_at` columns (already indexed on user_id)
- Consider adding index on `completed` column for status filtering
- Use date functions in SQL for trend calculations (DATE_TRUNC on PostgreSQL)

---

## Assumptions

- Phase II/III infrastructure (Better Auth, SQLModel, FastAPI, Neon PostgreSQL) is fully operational
- Task model has `created_at`, `updated_at`, and `completed` fields available for analytics
- If Message/Conversation models exist from Phase III chatbot, they include tool_calls tracking
- Frontend Next.js setup supports Recharts installation without conflicts
- Tailwind CSS is already configured and themes can be extended for charts
- User session management provides reliable user_id extraction

---

## Out of Scope

- Real-time live-updating charts (WebSocket/SSE)
- Exporting analytics data (CSV, PDF)
- Comparing analytics between time periods (this week vs last week)
- Team/organization-level analytics
- Notification/alerts based on analytics (e.g., "Your productivity dropped 20%")
- Custom dashboard layouts or widget arrangement
- Analytics for deleted tasks (soft-delete or archive)
- Historical data backfill for users who started before analytics feature
- Advanced productivity algorithms (machine learning predictions)
- Integration with external calendars or time tracking tools
- Multi-language/i18n support for dashboard labels
- Shareable analytics reports or public profiles

---

## Dependencies

| Dependency | Type | Notes |
|------------|------|-------|
| Phase II Task CRUD | Feature | Required for task data; must exist |
| Phase III Chatbot | Feature | Required for chat analytics; degrade gracefully if not present |
| Better Auth | Authentication | Required for user_id extraction |
| Recharts | NPM Package | Chart library - to be installed |
| date-fns or dayjs | NPM Package | Date manipulation for trend calculations |
| Tailwind CSS | Styling | Already present; extend for chart theming |

---

## Migration Notes

- New table `user_goals` needs to be created
- Add index on `tasks.completed` if not exists (performance optimization)
- If Message table doesn't exist from Phase III, chat analytics section shows "Coming soon" placeholder
- No breaking changes to existing Task model

---

## Open Questions

1. **Q**: Should streak tracking consider timezone, or use UTC for all users?
   **A**: Use UTC for backend calculations; display in user's local timezone (recommended)

2. **Q**: What constitutes a "successful" tool call for success rate calculation?
   **A**: Any tool call that returns without an error (HTTP 2xx equivalent in tool response)

3. **Q**: Should productivity score algorithm be transparent to users?
   **A**: Yes - show breakdown of factors contributing to score for transparency

4. **Q**: Should we track tasks created vs tasks completed for net productivity?
   **A**: Defer to Phase 2 of analytics (out of scope for initial version)

# Tasks: Analytics Dashboard

**Input**: Design documents from `/specs/002-analytics-dashboard/`
**Prerequisites**: plan.md, spec.md, ui-specification.md, integration.md, contracts/

**Tests**: Backend unit tests with pytest, manual E2E for frontend.

**Organization**: Tasks grouped by implementation phase for efficient parallel execution.

## Format: `[ID] [P?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- All paths relative to repository root

## User Story Mapping

| Story | Title | Priority | Endpoints Required |
|-------|-------|----------|-------------------|
| US1 | Quick Stats Cards | P1 | overview |
| US2 | Task Status Chart | P1 | by-priority |
| US3 | Completion Trend Chart | P1 | daily-completion |
| US4 | Priority Distribution | P2 | by-priority |
| US5 | Average Completion Time | P2 | productivity-score |
| US6 | Chat Analytics | P2 | chat-summary |
| US7 | Streak Tracking | P2 | streak |
| US8 | Productive Days/Hours | P3 | (future) |
| US9 | Weekly/Monthly Goals | P3 | goals |
| US10 | Productivity Score | P3 | productivity-score |

---

## Phase A: Backend Analytics API

**Purpose**: Create all analytics endpoints with proper authentication and aggregation queries

**Dependencies**: None (Phase II infrastructure exists)

### Database Optimization

- [ ] T001 [P] Add composite index for analytics queries in backend/database.py
- [ ] T002 [P] Create analytics cache utility (5-min TTL) in backend/utils/cache.py

### Analytics Router Setup

- [ ] T003 Create analytics router skeleton in backend/routes/analytics.py
- [ ] T004 Register analytics router in backend/main.py

### Core Endpoints (US1-US3)

- [ ] T005 [P] Implement GET /api/analytics/overview endpoint
- [ ] T006 [P] Implement GET /api/analytics/by-priority endpoint
- [ ] T007 [P] Implement GET /api/analytics/daily-completion endpoint with days parameter

### Extended Endpoints (US5-US7, US10)

- [ ] T008 [P] Implement GET /api/analytics/productivity-score endpoint
- [ ] T009 [P] Implement GET /api/analytics/streak endpoint
- [ ] T010 [P] Implement GET /api/analytics/chat-summary endpoint

### Goals Endpoints (US9)

- [ ] T011 Create UserGoal SQLModel in backend/models/goal.py (optional table)
- [ ] T012 [P] Implement GET /api/goals endpoint
- [ ] T013 [P] Implement POST /api/goals endpoint
- [ ] T014 [P] Implement DELETE /api/goals/{goal_id} endpoint

### Backend Tests

- [ ] T015 [P] Unit tests for overview endpoint in backend/tests/test_analytics.py
- [ ] T016 [P] Unit tests for by-priority endpoint
- [ ] T017 [P] Unit tests for daily-completion endpoint
- [ ] T018 [P] Unit tests for productivity-score endpoint
- [ ] T019 [P] Unit tests for streak endpoint
- [ ] T020 [P] Unit tests for chat-summary endpoint
- [ ] T021 [P] Unit tests for goals endpoints

**Checkpoint**: All analytics API endpoints working with proper auth

---

## Phase B: Frontend Dashboard Structure

**Purpose**: Create dashboard page, routing, and data fetching infrastructure

**Dependencies**: Phase A (endpoints must exist)

### Dependencies & Setup

- [ ] T022 Add recharts dependency to frontend/package.json
- [ ] T023 [P] Create frontend/components/analytics/ directory with index.ts

### Dashboard Page

- [ ] T024 Create /dashboard page with AuthGuard in frontend/app/dashboard/page.tsx
- [ ] T025 Add Dashboard link to Header component in frontend/components/Header.tsx

### API Client & Hooks

- [ ] T026 [P] Add analytics API methods to frontend/lib/api.ts
- [ ] T027 [P] Create useAnalytics hook in frontend/hooks/useAnalytics.ts

**Checkpoint**: Dashboard page accessible, API client ready

---

## Phase C: Stats Cards & Quick Metrics (US1)

**Purpose**: Implement the 4 quick stats cards with counter animations

**Dependencies**: Phase B

### Components

- [ ] T028 Create StatCard component with counter animation in frontend/components/analytics/StatCard.tsx
- [ ] T029 [P] Create skeleton loading state for StatCard
- [ ] T030 Implement 4-card grid layout (responsive) in dashboard page
- [ ] T031 Add staggered entrance animations (50ms delay, 300ms duration)
- [ ] T032 Add hover states with shadow lift (200ms ease-out)

### Integration

- [ ] T033 Connect StatCard grid to useAnalytics overview data
- [ ] T034 Test counter animation (400ms count-up from 0)

**Checkpoint**: Stats cards display and animate correctly

---

## Phase D: Charts & Visualizations (US2-US4, US6)

**Purpose**: Implement line, donut, and bar charts with Recharts

**Dependencies**: Phase B

### Line Chart - Completion Trend (US3)

- [ ] T035 Create TrendChart component (line chart) in frontend/components/analytics/TrendChart.tsx
- [ ] T036 [P] Add stroke draw-in animation (350ms left-to-right)
- [ ] T037 [P] Add gradient fill from blue-100 to transparent
- [ ] T038 [P] Add tooltips with date and count details

### Donut Chart - Priority Distribution (US2, US4)

- [ ] T039 Create PriorityChart component (donut chart) in frontend/components/analytics/PriorityChart.tsx
- [ ] T040 [P] Add clockwise segment draw animation (350ms, 100ms delay)
- [ ] T041 [P] Add legend with priority colors (red-600, amber-500, emerald-500)
- [ ] T042 [P] Add center label with total count

### Bar Chart - Tool Usage (US6)

- [ ] T043 Create ToolUsageChart component (bar chart) in frontend/components/analytics/ToolUsageChart.tsx
- [ ] T044 [P] Add bar scale-up animation (350ms, 200ms delay)
- [ ] T045 [P] Add sequential color palette (blue-500 to violet-300)

### Accessibility

- [ ] T046 [P] Add sr-only data tables for all charts
- [ ] T047 [P] Add role="img" with aria-labelledby for chart containers

### Empty States

- [ ] T048 Create chart empty state component with CTA link to /tasks

**Checkpoint**: All charts render with animations and accessibility support

---

## Phase E: Productivity Panel (US5, US7, US10)

**Purpose**: Implement streak counter, goals progress, and productivity score gauge

**Dependencies**: Phase B

### Components

- [ ] T049 Create StreakCounter component with flame icon in frontend/components/analytics/ProductivityPanel.tsx
- [ ] T050 [P] Create WeeklyGoalProgress bar component
- [ ] T051 [P] Create ProductivityScore circular gauge component

### Animations

- [ ] T052 Add panel entrance animation (slide-up + fade)
- [ ] T053 [P] Add progress bar fill animation (400ms, 100ms delay)
- [ ] T054 [P] Add circular gauge fill animation (500ms clockwise)

### Integration

- [ ] T055 Connect ProductivityPanel to streak and productivity-score endpoints
- [ ] T056 [P] Connect WeeklyGoalProgress to goals endpoint (if goals exist)

**Checkpoint**: Productivity panel displays all metrics with animations

---

## Phase F: Activity Feed & Polish

**Purpose**: Recent activity feed and cross-component polish

**Dependencies**: Phase D, Phase E

### Activity Feed

- [ ] T057 Create ActivityFeed component in frontend/components/analytics/ActivityFeed.tsx
- [ ] T058 [P] Add staggered item entrance (75ms delay, max 5 items)
- [ ] T059 [P] Add relative timestamps with <time datetime="">
- [ ] T060 [P] Add activity type icons (add, complete, delete)
- [ ] T061 Create activity feed empty state

### Error Handling

- [ ] T062 Create ErrorBanner component with retry button
- [ ] T063 [P] Add horizontal shake animation on error appear
- [ ] T064 Add error boundary for chart failures

### Reduced Motion Support

- [ ] T065 Implement prefers-reduced-motion media query support
- [ ] T066 [P] Disable all transforms, use 100ms fades only
- [ ] T067 [P] Show counter final values instantly (no animation)

### Mobile Responsive

- [ ] T068 Test 1-column layout on mobile (<768px)
- [ ] T069 [P] Test 2-column layout on tablet (768-1023px)
- [ ] T070 [P] Test 4-column stats grid on desktop (>=1024px)

**Checkpoint**: Activity feed complete, all polish applied

---

## Phase G: Testing & Documentation

**Purpose**: Comprehensive testing and documentation updates

**Dependencies**: Phase F

### Backend Testing

- [ ] T071 Run full analytics test suite
- [ ] T072 [P] Test with 0 tasks (empty state)
- [ ] T073 [P] Test with 100+ tasks (performance)

### Frontend Testing

- [ ] T074 Manual test all chart interactions
- [ ] T075 [P] Test keyboard navigation order
- [ ] T076 [P] Test screen reader announcements
- [ ] T077 Lighthouse performance audit (target: 90+)

### Documentation

- [ ] T078 Update README.md with dashboard setup instructions
- [ ] T079 [P] Add analytics environment variables to .env.example
- [ ] T080 [P] Create manual test scenarios document

### Security Audit

- [ ] T081 Verify user isolation on all endpoints
- [ ] T082 [P] Verify no sensitive data in responses

**Checkpoint**: All tests passing, documentation complete

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase A: Backend Analytics API ─────────────────────────────────┐
                                                                 │
Phase B: Frontend Dashboard Structure ◄──────────────────────────┘
    │
    ├──► Phase C: Stats Cards (US1) ────────────┐
    │                                            │
    ├──► Phase D: Charts (US2-US4, US6) ────────┤──► Phase F: Polish
    │                                            │
    └──► Phase E: Productivity Panel (US5,7,10)─┘
                         │
                         ▼
              Phase G: Testing & Documentation
```

### Parallel Opportunities

Within each phase, tasks marked [P] can run in parallel:
- All endpoint implementations (T005-T010)
- All endpoint tests (T015-T021)
- Chart animations (T036-T038, T040-T042, T044-T045)
- Accessibility tasks (T046-T047)
- Reduced motion tasks (T066-T067)
- Mobile responsive tests (T069-T070)

---

## Summary

| Phase | Tasks | Parallel Opportunities |
|-------|-------|------------------------|
| A: Backend API | 21 | 16 parallel |
| B: Frontend Structure | 6 | 2 parallel |
| C: Stats Cards | 7 | 1 parallel |
| D: Charts | 14 | 10 parallel |
| E: Productivity Panel | 8 | 4 parallel |
| F: Activity Feed & Polish | 14 | 8 parallel |
| G: Testing & Docs | 12 | 7 parallel |
| **Total** | **82** | **48 parallel** |

---

## Notes

- [P] tasks = different files, no dependencies
- Each phase independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate
- MVP = Phase A + B + C (Backend + Dashboard + Stats Cards)
- Full Feature = All phases complete

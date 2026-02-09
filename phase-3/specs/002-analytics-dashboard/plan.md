# Implementation Plan: Analytics Dashboard

**Branch**: `002-analytics-dashboard` | **Date**: 2026-02-05 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-analytics-dashboard/spec.md`

---

## Summary

Analytics Dashboard providing task productivity metrics, chat analytics, and data visualization for the AI Todo Chatbot app. Features quick stats cards, completion trend charts, priority distribution, productivity scores, streak tracking, and recent activity feed. Integrates with Phase II/III via read-only aggregation queries.

**Key integration points**:
- Extends Phase II FastAPI backend with `/api/analytics` endpoints
- Reuses Better Auth session validation (no auth changes)
- Queries existing `tasks` table (no new tables for core analytics)
- Adds animated dashboard page at `/dashboard` route

---

## Technical Context

**Language/Version**: Python 3.11 (backend), TypeScript/Next.js 14 (frontend)
**Primary Dependencies**: FastAPI 0.109, SQLModel 0.0.14, Recharts ^2.10
**Storage**: Neon PostgreSQL (existing Phase II database)
**Testing**: pytest (backend), manual E2E (frontend)
**Target Platform**: Web application (desktop + mobile browsers)
**Project Type**: Web (frontend + backend monorepo)
**Performance Goals**: <2s dashboard load, <500ms chart render, 60fps animations
**Constraints**: Read-only analytics, prefers-reduced-motion support, WCAG AA compliance
**Scale/Scope**: Single-user analytics, 7-30 day trend windows

---

## Constitution Check

| Principle | Status | Evidence |
|-----------|--------|----------|
| **I. No Human Code** | PASS | All implementation via Claude Code |
| **II. AI-Generated Code** | PASS | Claude Code is sole implementation agent |
| **III. Spec-Derived Outputs** | PASS | All code derived from this spec |
| **IV. Agent Boundaries** | PASS | Agents write specs/plans, Claude Code implements |
| **V. Phase Isolation** | PASS | Dashboard extends Phase II/III, no Phase IV concepts |
| **VI. Spec Authority** | PASS | Spec.md is source of truth |

---

## Project Structure

### Documentation (this feature)

```text
specs/002-analytics-dashboard/
├── spec.md                    # Feature specification
├── plan.md                    # This file
├── ui-specification.md        # Animation & component details
├── integration.md             # Phase II/III integration plan
├── contracts/
│   └── analytics-api.yaml     # OpenAPI specification
└── tasks.md                   # Implementation tasks (via /sp.tasks)
```

### Source Code (repository root)

```text
backend/
├── main.py                          # Modified: register analytics_router
├── routes/
│   ├── tasks.py                    # Existing (no changes)
│   ├── chat.py                     # Existing (no changes)
│   └── analytics.py                # NEW: Analytics endpoints
└── tests/
    └── test_analytics.py           # NEW: Analytics tests

frontend/
├── app/
│   ├── layout.tsx                  # Existing (no changes)
│   ├── tasks/page.tsx              # Existing (no changes)
│   └── dashboard/
│       └── page.tsx                # NEW: Dashboard page
├── components/
│   ├── Header.tsx                  # Modified: Add Dashboard link
│   └── analytics/                  # NEW: Dashboard components
│       ├── StatCard.tsx
│       ├── TrendChart.tsx
│       ├── PriorityChart.tsx
│       ├── ToolUsageChart.tsx
│       ├── ProductivityPanel.tsx
│       ├── ActivityFeed.tsx
│       └── index.ts
├── hooks/
│   └── useAnalytics.ts             # NEW: Data fetching hook
└── lib/
    └── api.ts                      # Modified: Add analytics methods
```

---

## Implementation Phases

### Phase A: Backend Analytics API

**Dependencies**: None
**Deliverables**:
- [ ] `GET /api/analytics/overview` - Total, completed, pending, rate
- [ ] `GET /api/analytics/by-priority` - Priority breakdown
- [ ] `GET /api/analytics/daily-completion` - 7-day trend
- [ ] `GET /api/analytics/productivity-score` - Calculated metric
- [ ] `GET /api/analytics/streak` - Current and longest streak
- [ ] `GET /api/analytics/chat-summary` - Chat usage stats
- [ ] Database index for query performance
- [ ] Unit tests for all endpoints

### Phase B: Frontend Dashboard Structure

**Dependencies**: Phase A
**Deliverables**:
- [ ] Install Recharts dependency
- [ ] Create `/dashboard` page with AuthGuard
- [ ] Add Dashboard link to Header
- [ ] Create useAnalytics hook for data fetching
- [ ] Add analytics API methods to api.ts
- [ ] Create base component structure

### Phase C: Stats Cards & Quick Metrics

**Dependencies**: Phase B
**Deliverables**:
- [ ] StatCard component with counter animation
- [ ] 4-card grid layout (responsive)
- [ ] Staggered entrance animations
- [ ] Hover states with shadow lift
- [ ] Skeleton loading states

### Phase D: Charts & Visualizations

**Dependencies**: Phase B
**Deliverables**:
- [ ] TrendChart (line chart with Recharts)
- [ ] PriorityChart (donut chart)
- [ ] ToolUsageChart (bar chart)
- [ ] Chart draw-in animations
- [ ] Tooltips with data details
- [ ] Empty states for no data
- [ ] Accessible data tables (sr-only)

### Phase E: Productivity Panel

**Dependencies**: Phase B
**Deliverables**:
- [ ] StreakCounter with flame icon
- [ ] WeeklyGoalProgress bar
- [ ] ProductivityScore circular gauge
- [ ] Panel entrance animation
- [ ] Progress bar fill animation

### Phase F: Activity Feed & Polish

**Dependencies**: Phase D, E
**Deliverables**:
- [ ] ActivityFeed component
- [ ] Staggered item entrance
- [ ] Relative timestamps
- [ ] Empty state
- [ ] Error banner with retry
- [ ] prefers-reduced-motion support
- [ ] Mobile responsive testing

### Phase G: Testing & Documentation

**Dependencies**: Phase F
**Deliverables**:
- [ ] Backend unit tests
- [ ] Frontend manual test scenarios
- [ ] Accessibility audit (keyboard, screen reader)
- [ ] Performance audit (Lighthouse)
- [ ] README updates

---

## Key Technical Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Chart library | Recharts | React-native, built-in animations, accessible |
| Animation library | Framer Motion + CSS | Consistent with Phase III chat UI |
| Data caching | In-memory (5-min TTL) | Simple, acceptable staleness |
| New tables | None for core analytics | Queries existing tasks table |
| Goals feature | Optional UserGoal table | Only if user requests goal tracking |

---

## Dependencies

| Dependency | Version | Purpose |
|------------|---------|---------|
| recharts | ^2.10.0 | Chart visualizations |
| framer-motion | ^11.0.0 | Already in Phase III |

---

## Risk Mitigation

| Risk | Level | Mitigation |
|------|-------|------------|
| Slow analytics queries | MEDIUM | Add composite index, in-memory cache |
| Chart performance on mobile | MEDIUM | Lazy-load Recharts, limit data points |
| Color blindness accessibility | LOW | Color-blind friendly palette verified |
| Animation jank | LOW | GPU-accelerated transforms only |

---

## Artifacts Generated

| Artifact | Path | Status |
|----------|------|--------|
| Spec | specs/002-analytics-dashboard/spec.md | Complete |
| Plan | specs/002-analytics-dashboard/plan.md | Complete |
| UI Spec | specs/002-analytics-dashboard/ui-specification.md | Complete |
| Integration | specs/002-analytics-dashboard/integration.md | Complete |
| API Contract | specs/002-analytics-dashboard/contracts/analytics-api.yaml | Complete |
| Tasks | specs/002-analytics-dashboard/tasks.md | Pending (/sp.tasks) |

---

## Next Steps

1. Run `/sp.tasks` to generate detailed implementation task list
2. Begin with Phase A (backend analytics API)
3. Phase B-C can parallel once API is ready
4. Focus on Phase D (charts) as most complex component

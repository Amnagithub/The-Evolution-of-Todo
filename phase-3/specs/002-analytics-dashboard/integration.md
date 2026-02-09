# Integration Plan: Analytics Dashboard

**Feature Branch**: `002-analytics-dashboard`
**Date**: 2026-02-05
**Status**: Complete

---

## Integration Slogan

> "Analytics bolts onto Phase 2 via read-only aggregation queries and a new `/dashboard` route — zero disruption to existing task CRUD."

---

## 1. Phase 2 Reuse Summary

### Authentication (Better Auth)
- **Reuse**: Session-based auth via `get_current_user_id()` middleware
- **Sessions**: Stored in database (`session` table)
- **Integration**: Dashboard uses existing `Depends(get_current_user_id)` on all routes
- **Changes needed**: None

### Database (Neon PostgreSQL)
- **Reuse**: Same SQLModel engine, Session, and connection pool
- **Tables used**: Existing `tasks` table (no new tables required)
- **Changes needed**: Add composite index for query performance

### Routing / API Structure
- **Reuse**: FastAPI router pattern at `/api/analytics`
- **CORS**: Already configured for localhost:3000 and Vercel
- **Changes needed**: Register new analytics router in `main.py`

### Frontend Layout
- **Reuse**: Next.js App Router, Header component, AuthGuard
- **Changes needed**: Add Dashboard link to Header, create `/dashboard` page

---

## 2. Required Modifications

### Backend Changes

| File | Change | Description |
|------|--------|-------------|
| `backend/routes/analytics.py` | NEW | Analytics router with 4 endpoints |
| `backend/main.py` | MODIFY | Register `analytics_router` |
| `backend/database.py` | MODIFY | Add index in `run_migrations()` |

### Frontend Changes

| File | Change | Description |
|------|--------|-------------|
| `frontend/app/dashboard/page.tsx` | NEW | Dashboard page with charts |
| `frontend/components/analytics/` | NEW | StatCard, charts, etc. |
| `frontend/components/Header.tsx` | MODIFY | Add Dashboard navigation link |
| `frontend/lib/api.ts` | MODIFY | Add analytics API client methods |
| `frontend/package.json` | MODIFY | Add `recharts` dependency |

### New Environment Variables
```bash
# Optional - defaults to 300 seconds
ANALYTICS_CACHE_TTL=300
```

---

## 3. Folder Structure Delta

```
backend/
├── [NEW] routes/analytics.py          # Analytics router
├── [MOD] main.py                      # Register analytics_router
└── [MOD] database.py                  # Add index creation

frontend/
├── [NEW] app/dashboard/
│   └── page.tsx                       # Dashboard page
├── [NEW] components/analytics/
│   ├── StatCard.tsx                   # Stat display card
│   ├── PriorityChart.tsx              # Donut chart
│   ├── TrendChart.tsx                 # Line chart
│   ├── ToolUsageChart.tsx             # Bar chart
│   ├── ProductivityPanel.tsx          # Streak, goals, score
│   ├── ActivityFeed.tsx               # Recent activity
│   └── index.ts                       # Exports
├── [NEW] hooks/useAnalytics.ts        # Data fetching hook
├── [MOD] components/Header.tsx        # Add Dashboard link
├── [MOD] lib/api.ts                   # Analytics client methods
└── [MOD] package.json                 # Add recharts
```

---

## 4. API Endpoints

### Overview
```
GET /api/analytics/overview
Authorization: Bearer {token}

Response:
{
  "total": 47,
  "completed": 32,
  "pending": 15,
  "rate": 68.1
}
```

### By Priority
```
GET /api/analytics/by-priority
Authorization: Bearer {token}

Response:
[
  {"priority": "high", "count": 12},
  {"priority": "medium", "count": 25},
  {"priority": "low", "count": 10}
]
```

### Daily Completion (7-day trend)
```
GET /api/analytics/daily-completion
Authorization: Bearer {token}

Response:
[
  {"date": "2026-01-30", "count": 5},
  {"date": "2026-01-31", "count": 3},
  ...
]
```

### Productivity Score
```
GET /api/analytics/productivity-score
Authorization: Bearer {token}

Response:
{
  "score": 80,
  "period": "last_7_days"
}
```

---

## 5. Database Queries

### Aggregation Pattern (No N+1)
```python
# Single query per endpoint
total = session.exec(
    select(func.count(Task.id))
    .where(Task.user_id == user_id)
).one()
```

### Recommended Index
```sql
CREATE INDEX idx_tasks_analytics
ON tasks(user_id, completed, updated_at);
```

### Caching Strategy
- **Type**: In-memory (`functools.lru_cache` or middleware)
- **TTL**: 5 minutes
- **Key**: `f"analytics_{endpoint}_{user_id}"`
- **Invalidation**: On task CRUD (optional, stale data acceptable)

---

## 6. Risk Assessment

| Risk | Level | Mitigation |
|------|-------|------------|
| Performance (slow queries) | MEDIUM | Add composite index, in-memory cache |
| Data accuracy (concurrent updates) | LOW | Accept eventual consistency (5-min stale) |
| Mobile chart performance | MEDIUM | Lazy-load Recharts, limit data points |
| Large datasets (>10k tasks) | HIGH | Add LIMIT clause or pre-compute stats |

---

## 7. Integration Checklist

### Backend
- [ ] Create `routes/analytics.py` with 4 endpoints
- [ ] Register router in `main.py`
- [ ] Add composite index in `database.py`
- [ ] Write unit tests for analytics endpoints

### Frontend
- [ ] Install `recharts` dependency
- [ ] Create `/dashboard` page
- [ ] Add analytics components
- [ ] Update Header with Dashboard link
- [ ] Add API client methods
- [ ] Test responsive layout
- [ ] Test reduced motion preference

### Integration Testing
- [ ] Verify auth works on all endpoints
- [ ] Test with 0 tasks (empty state)
- [ ] Test with 100+ tasks (performance)
- [ ] Test mobile layout
- [ ] Test chart accessibility

---

## 8. Chart Library Recommendation

**Recharts** (Recommended)
- React-native, declarative API
- Built-in animation support
- Accessible by default
- Responsive without additional config
- Matches Tailwind styling

```bash
npm install recharts
```

```tsx
import { LineChart, Line, PieChart, Pie, BarChart, Bar } from "recharts";
```

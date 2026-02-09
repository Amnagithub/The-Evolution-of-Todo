# UI/UX Specification: Analytics Dashboard

**Feature Branch**: `002-analytics-dashboard`
**Date**: 2026-02-05
**Status**: Complete

---

## 1. Placement & Navigation

### Primary Recommendation: Dedicated Dashboard Route
- **Route**: `/dashboard` or `/analytics`
- **Navigation**: Add "Dashboard" link to Header component
- **Style**: `px-4 py-2 text-sm text-gray-600 hover:text-gray-800`

**Rationale**:
- Follows Phase 2 route-based navigation pattern
- Dedicated screen real estate for data visualization
- Desktop gets full-width; mobile scrolls through stacked components

---

## 2. Animation Vocabulary

### Stats Cards Entrance (Page Load)
| Property | Value |
|----------|-------|
| Motion Type | Staggered slide-up with fade-in |
| Direction | Vertical (from 12px below) |
| Opacity | 0 → 1 |
| Stagger Delay | 50ms between each card |
| Duration | 300ms per card |
| Easing | `cubic-bezier(0.4, 0.0, 0.2, 1)` |

### Counter Animation (Numbers)
| Property | Value |
|----------|-------|
| Motion Type | Count-up from 0 to target |
| Duration | 400ms |
| Easing | ease-out |
| Trigger | When card opacity reaches 0.8 |

### Stats Card Hover
| Property | Value |
|----------|-------|
| Transform | `translateY(-2px)` |
| Shadow | `shadow-sm` → `shadow-md` |
| Duration | 200ms |
| Easing | ease-out |

### Chart Animations
| Chart Type | Animation | Duration | Delay |
|------------|-----------|----------|-------|
| Line Chart | Stroke draws left to right | 350ms | 0ms |
| Donut Chart | Segments draw clockwise | 350ms | 100ms |
| Bar Chart | Bars scale from 0 height | 350ms | 200ms |

### Progress Bar Fill
| Property | Value |
|----------|-------|
| Motion Type | Width expansion from left |
| Duration | 400ms |
| Delay | 100ms after panel visible |
| Easing | `cubic-bezier(0.4, 0.0, 0.2, 1)` |

### Activity Feed Items
| Property | Value |
|----------|-------|
| Motion Type | Staggered fade-in from below |
| Direction | 8px below resting position |
| Stagger | 75ms per item (max 5) |
| Duration | 250ms per item |

---

## 3. Interaction States Table

| State | Visual/Animation | Duration | Trigger |
|-------|------------------|----------|---------|
| Page Load | Stats cards staggered slide-up | 300ms each | Route navigation |
| Counter Animation | Numbers increment to target | 400ms | Card entrance |
| Stats Card Hover | Lift 2px, shadow expands | 200ms | Mouse enter |
| Chart Tooltip Show | Scale 0.95→1.0 with fade | 150ms | Hover data point |
| Data Refresh | Crossfade old→new data | 300ms | API response |
| Error State | Horizontal shake + fade-in | 300ms | API failure |
| Success Flash | Green border pulse | 200ms | Data updated |

---

## 4. Accessibility Requirements

### Reduced Motion Support
```css
@media (prefers-reduced-motion: reduce) {
  /* All transforms disabled */
  /* Simple 100ms fades only */
  /* Counter shows final value instantly */
}
```

### Keyboard Navigation
1. Page heading (`<h1>`)
2. Refresh button
3. Stats cards (interactive only)
4. Chart containers
5. Productivity panel elements
6. Activity feed items

### Screen Reader Support
- ARIA live regions for data updates
- Chart data in hidden `<table>` format
- `<time datetime="">` for timestamps
- `role="img"` with `aria-labelledby` for charts

---

## 5. Component Hierarchy

```
<AuthGuard>
  <Header />  {/* Add Dashboard link */}

  <AnalyticsDashboard>  {/* max-w-7xl mx-auto px-4 py-8 */}

    <DashboardHeader>
      <PageTitle>Analytics Dashboard</PageTitle>
      <RefreshButton />
    </DashboardHeader>

    <StatsCardsGrid>  {/* grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 */}
      <StatCard title="Total Tasks" icon={TaskIcon} delay={0} />
      <StatCard title="Completed This Week" icon={CheckIcon} delay={50} />
      <StatCard title="Pending" icon={ClockIcon} delay={100} />
      <StatCard title="Chat Messages" icon={MessageIcon} delay={150} />
    </StatsCardsGrid>

    <ChartsSection>  {/* grid grid-cols-1 lg:grid-cols-2 gap-6 */}
      <ChartCard title="Task Completion Trend">
        <LineChart />
        <ChartDataTable />  {/* sr-only */}
      </ChartCard>

      <ChartCard title="Priority Distribution">
        <DonutChart />
        <ChartLegend />
        <ChartDataTable />
      </ChartCard>

      <ChartCard className="lg:col-span-2" title="Tool Usage">
        <BarChart />
        <ChartDataTable />
      </ChartCard>
    </ChartsSection>

    <ProductivityPanel>  {/* bg-gradient-to-r from-blue-50 to-indigo-50 */}
      <StreakCounter />
      <WeeklyGoalProgress />
      <ProductivityScore />  {/* CircularGauge */}
    </ProductivityPanel>

    <RecentActivitySection>
      <ActivityFeed>
        {items.map((item, i) => (
          <ActivityItem delay={i * 75} />
        ))}
      </ActivityFeed>
    </RecentActivitySection>

    {error && <ErrorBanner onRetry={handleRetry} />}

  </AnalyticsDashboard>
</AuthGuard>
```

---

## 6. Responsive Breakpoints

| Breakpoint | Stats Grid | Charts Grid | Productivity |
|------------|------------|-------------|--------------|
| Mobile (<768px) | 1 column | 1 column | Stacked |
| Tablet (768-1023px) | 2 columns | 2 columns | 3 columns |
| Desktop (≥1024px) | 4 columns | 2 columns | 3 columns |

---

## 7. Chart Color Palette (Color-Blind Friendly)

### Priority Distribution
| Priority | Color | Tailwind |
|----------|-------|----------|
| High | #DC2626 | red-600 |
| Medium | #F59E0B | amber-500 |
| Low | #10B981 | emerald-500 |

### Line Chart
| Element | Color | Tailwind |
|---------|-------|----------|
| Line | #2563EB | blue-600 |
| Fill | gradient | blue-100 → transparent |
| Points | #1E40AF | blue-700 |

### Bar Chart (Sequential)
| Index | Color | Tailwind |
|-------|-------|----------|
| 1 | #3B82F6 | blue-500 |
| 2 | #6366F1 | indigo-500 |
| 3 | #8B5CF6 | violet-500 |
| 4 | #A78BFA | violet-400 |
| 5 | #C4B5FD | violet-300 |

---

## 8. Design Tokens (Tailwind)

### Spacing
- Card padding: `p-4` or `p-6`
- Section gaps: `space-y-6` or `space-y-8`
- Grid gaps: `gap-4` or `gap-6`

### Typography
- Page title: `text-3xl font-bold`
- Section headings: `text-lg font-semibold`
- Card titles: `text-sm font-medium`
- Timestamps: `text-xs text-gray-500`

### Shadows
- Cards: `shadow-sm`
- Hover: `shadow-md`
- Tooltips: `shadow-lg`

---

## 9. Loading & Error States

### Skeleton Screens
- Stats cards: Gray rectangles with `animate-pulse`
- Charts: Empty containers with placeholder axes
- Activity feed: 3-5 varying-width gray bars

### Error Display
- Banner: `bg-red-50 border-l-4 border-red-500 text-red-700`
- Animation: Horizontal shake on appear
- Action: Retry button

### Empty State
- Icon: Centered, muted (`text-gray-400`)
- Message: "No data available yet"
- CTA: Link to `/tasks`

---

## 10. Performance Budgets

| Metric | Budget |
|--------|--------|
| Max single animation | 400ms |
| Total page load sequence | ≤1200ms |
| Frame rate target | 60fps |
| Frame budget | 10ms per frame |

### Optimization Checklist
- [ ] Lazy-load chart library
- [ ] Memoize data transformations
- [ ] Use Intersection Observer for scroll animations
- [ ] GPU-accelerated transforms only
- [ ] Passive scroll listeners

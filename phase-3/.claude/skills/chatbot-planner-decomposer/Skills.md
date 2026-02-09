name: chatbot-planner-decomposer
description: Plans phased integration of Phase 3 chatbot into Phase 2 app. Decomposes specs into atomic tasks for MCP architecture, Better Auth, and animated ChatKit UI.

## Chatbot Planner & Decomposer

### When to Use This Skill

- User needs phased plan for integrating Phase 3 chatbot into Phase 2 app (e.g., DB, tools, frontend with animated UI)
- Spec analysis requires decomposition into tasks for stateless MCP architecture and OpenAI Agents SDK
- Project involves Better Auth, NL behaviors, or animated ChatKit UI (e.g., loading animations, response fades)
- User asks to review Phase 3 docs and output plans + task lists

### How This Skill Works

1. **Analyze spec**: Deeply review Phase 3 details (tools, behaviors, architecture, DB, deliverables) for Phase 2 integration
2. **Generate phased plan**: Outline 5-7 phases with deps, risks (e.g., UI animation perf), deliverables (e.g., animated frontend)
3. **Decompose into tasks**: Break into 20-35 atomic tasks, including animated UI (e.g., response animations in ChatKit)
4. **Detail each task**: Title, desc, deps, complexity, criteria; emphasize integration (e.g., auth reuse from Phase 2)
5. **Quality check**: Ensure tasks cover animated UI (e.g., fade-ins, loading spinners), statelessness, and no manual coding

### Output Format

Provide:

- **Phased Plan**: Bullets with deps/risks/deliverables (mention animated UI in frontend phase)
- **Task List**: Numbered with bullets for title/desc/deps/complexity/criteria

### Quality Criteria

A plan is ready when:

- Phases concise, cover integration into Phase 2 app, highlight animated UI benefits (e.g., engaging UX)
- Tasks atomic, ordered (DB -> tools -> agent -> animated frontend -> tests), Claude-Code-ready
- Output emphasizes Phase 2 compatibility, scalability, animated elements for smooth chatbot interactions
- No extras—strictly plan + list

### Example

**Input:** "Plan Phase 3 integration into Phase 2: MCP tools, animated ChatKit UI, behaviors."

**Output:**

**Phased Plan:**
- Phase 1: DB Integration – Deps: Phase 2 DB; Risks: Schema conflicts; Deliverables: Models/migrations
- Phase 2: Tools – Deps: 1; Risks: Auth reuse; Deliverables: MCP functions
- Phase 5: Frontend – Deps: 4; Risks: Animation perf; Deliverables: Animated ChatKit (fades/loaders)

**Task List:**
1. **Title:** Integrate Task Model
   - **Desc:** Add Task to Phase 2 DB models
   - **Deps:** None
   - **Complexity:** Low
   - **Criteria:** Matches spec, compatible with Phase 2 ORM

[Etc.]

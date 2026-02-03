---
id: "004"
title: "Task organization feature specification"
stage: "spec"
date: "2026-01-02"
surface: "agent"
model: "sonnet-4-5-20250929"
feature: "004-task-organization"
branch: "main"
user: "amna"
command: "/sp.specify"
labels: ["task-organization","priorities","tags","search","filter","sort"]
links:
  spec: "phase-1/specs/task-organization.md"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - "phase-1/specs/task-organization.md"
  - "phase-1/specs/task-organization-checklist.md"
tests:
  - "none"
---

## Prompt

/sp.specify with the following feature description:

Feature request: Task Organization and Usability Features

I want to extend the Todo CLI with organizational features:

1. Priority Support - Tasks can have priority levels: HIGH, MEDIUM, LOW (default MEDIUM)
   - Add --priority flag to add command
   - Add priority display in list and other commands
   - Sort by priority (high to low, low to high)
   - Filter by priority

2. Tags - Tasks can have multiple tags for categorization
   - Add --tag flag to add command (can be specified multiple times)
   - Add tag display in list output
   - Filter by tag
   - Search by tag
   - Tags should be normalized (lowercase, trimmed)

3. Search Command - Search tasks by keyword
   - todo search <keyword>
   - Searches in title and description
   - Case-insensitive matching
   - Can be combined with filters (--status, --priority, --tag)

4. Filter Command - Filter tasks by criteria
   - todo filter --status ACTIVE|COMPLETED
   - todo filter --priority HIGH|MEDIUM|LOW
   - todo filter --tag <tagname>
   - Multiple filters use AND logic

5. Sort Command - Sort tasks by different fields
   - todo sort title|priority|id|created [--reverse]
   - Default sort order: ascending
   - --reverse flag for descending order

6. Extended Output - Enhanced list command
   - Add --extended flag to show full details
   - Show priority and tags in compact output
   - Better formatting for readability

Extended add command:
todo add <title> [--description <desc>] [--priority <priority>] [--tag <tag>...]

Extended update command:
todo update <id> [--title <title>] [--description <desc>] [--priority <priority>] [--add-tag <tag>] [--remove-tag <tag>]

Please create a comprehensive feature specification for these task organization features.

## Response snapshot

Created comprehensive feature specification for task organization including:
- Extended Task entity with Priority enum and tags list
- 10 user stories covering all new features
- 3 new commands (search, filter, sort)
- 3 modified commands (add, list, update)
- Complete CLI syntax and examples for all commands
- 100+ acceptance criteria organized by category
- Error handling taxonomy with 11 error codes
- Repository and service layer interface changes
- Future considerations for due dates, dependencies, subtasks

## Outcome

- ✅ Impact: Feature specification completed for Phase 1.4 task organization (priorities, tags, search, filter, sort)
- 🧪 Tests: None executed (specification phase)
- 📁 Files: 2 created (task-organization.md, task-organization-checklist.md)
- 🔁 Next prompts: /sp.plan for architecture decisions, /sp.tasks for implementation tasks
- 🧠 Reflection: Feature specification covers all user requirements with comprehensive acceptance criteria. 100+ testable items across 11 categories.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A

name: chatbot-prompt-integrator
description: Crafts Claude Code prompts for Phase 3 component implementation and generates integration plans/tests for stateless endpoints, auth, and animated ChatKit UI.

## Chatbot Prompt & Integrator

### When to Use This Skill

- User needs prompts for Claude Code to implement Phase 3 components in Phase 2 app (e.g., tools, animated frontend)
- Project requires integration plan/tests for stateless endpoint, auth, animated ChatKit (e.g., transitions)
- After plans/designs, to create prompts for tasks or validation
- User asks to review Phase 3 and output prompts/plans/tests

### How This Skill Works

1. **Analyze inputs**: Review spec/plans/designs for Phase 2 integration
2. **Craft prompts**: Detailed Claude Code text per component (e.g., tool with animated UI cues)
3. **Generate integration**: Plan mods/risks/repo; test tasks with animated UI verification
4. **Enforce alignment**: Stateless, auth, animations (e.g., fade responses in ChatKit)
5. **Quality check**: Prompts produce secure code; plans ensure Phase 2 compatibility

### Output Format

Provide:

- **Component / Task**: [Name]
- **Claude Code Prompt**: [Full text]
- **Optional Test Prompt**: [Text]
- **Integration Plan**: Bullets/table for mods/risks/repo
- **Validation & Testing Tasks**: Numbered with criteria (include animated UI tests)

### Quality Criteria

A set is ready when:

- Prompts comprehensive, stateless/secure, include animated UI (e.g., "add fade animation to responses")
- Plans cover Phase 2 wiring, risks like animation lag
- Tests verify features/errors/animations; Claude-Code-optimized
- Concise, no code—only prompts/plans

### Example

**Input:** "Prompts/integration for Phase 3 in Phase 2: add_task, animated UI tests."

**Output:**

**Component / Task:** add_task

**Claude Code Prompt:** "Generate code for add_task: ... integrate with Phase 2 auth, animate confirmation."

**Optional Test Prompt:** "Test add_task: ..."

**Integration Plan:**
- Mod: Add to Phase 2 backend
- Risks: UI perf

**Validation & Testing Tasks:**
1. Test animation: Criteria: Fade-in works on response

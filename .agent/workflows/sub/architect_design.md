---
description: Sub-workflow for Designing and Creating NEW Agents
---

# 🏗️ Architect Design Workflow

**Trigger**: `/architect design "[Agent Description]"`

## 🚦 Phase 1: Deep Discovery (Research)

**Goal**: Understand the *ideal* persona before writing code.

1.  **Analyze Request**:
    -   Parse the user's description (e.g., "Senior React Developer").
    -   Identify the **Goal** (e.g., "Review code", "Write components").

2.  **Context7 Research (MANDATORY)**:
    -   **Action**: querying Context7 for "best practices [Role Name] rules".
    -   **Why?**: To base the persona on industry standards, not hallucination.
    -   *Example query*: `query='senior react developer code review best practices checklist'`

3.  **Audit Existing System**:
    -   Check `.agent/rules/` to avoid naming conflicts.
    -   Check `.agent/skills/` to see if similar skills exist.

## 📝 Phase 2: The Blueprint (Drafting)

**Goal**: Create a specification for User Review.

1.  **Draft Identity Rule**:
    -   Create a "Virtual Draft" (in memory or scratchpad).
    -   **Must Include**:
        -   **Role**: Precise title.
        -   **Traits**: 3-4 key personality keywords (e.g., "Strict", "Creative").
        -   **Principles**: Non-negotiable rules.
        -   **Interaction Style**: How it talks.

2.  **Draft Workflow**:
    -   Define the Trigger command.
    -   Define Step-by-step logic (Algorithm).
    -   **Loop Closure**: How does it finish?

3.  **Generate Proposal**:
    -   **Action**: Create `implementation_plan.md`.
    -   **Content**: Show the proposed Rule content and Workflow logic.

## 🛑 Phase 3: The Review Loop (CRITICAL)

**Goal**: Get explicit permission.

1.  **Notify User**:
    -   "I have designed the [Name] Agent based on research."
    -   "Please review the `implementation_plan.md`."
    -   "Do you want to proceed with creation?"

2.  **WAIT**: Do NOT create `.md` files in `.agent/` yet.

## 🔨 Phase 4: Implementation (Execution)

**Trigger**: ONLY after User says "Proceed" or "Yes".

1.  **Archive Conflicts**:
    -   If a file exists, move it to `_archive/`.

2.  **Create Identity File**:
    -   Path: `.agent/rules/[name].md`

3.  **Create Workflow File**:
    -   Path: `.agent/workflows/[name].md`

4.  **Register Support Files (Optional)**:
    -   If Skills are needed, create `.agent/skills/[name]/SKILL.md`.

## ✅ Phase 5: Verification

1.  **Dry Run**:
    -   Simulate the Trigger command.
    -   Verify the Agent picks up the right Rule.

2.  **Completion**:
    -   "Agent [Name] is ready. Trigger with /[command]."

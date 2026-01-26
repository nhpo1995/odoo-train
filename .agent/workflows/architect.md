---
description: Hybrid Dispatcher for Agentic System (Direct Q&A + Sub-Workflows)
---

# 🧠 Architect Hybrid Dispatcher

**Trigger**: `/architect [optional_args]`

## 🚦 Phase 1: Intent Analysis

**Goal**: Decide between **Direct Handling** vs **Sub-Workflow Dispatch**.

### Logic:

1.  **Load Identity**:
    -   `view_file .agent/rules/agentic-architect.md`
    -   Adopt the "Senior System Engineer" persona.

2.  **Analyze Argument**:
    -   Check the text after `/architect`.

### 🔀 Branch A: Heavy Workflows (Dispatch)
**Trigger**: If args contain specific keywords:

-   **Audit / Check / Health**:
    -   **Action**: Trigger `.agent/workflows/sub/architect_audit.md`
    -   **Context**: Full system scan & integrity report.

-   **Design / Create / New**:
    -   **Action**: Trigger `.agent/workflows/sub/architect_design.md`
    -   **Context**: Research & Design protocol for NEW agents.

### 💬 Branch B: Direct Interaction (Handle Here)
**Trigger**: All other queries (Analysis, Explanation, Q&A, Refinement discussions).

1.  **Analyze Request**:
    -   Understand what the user wants to know about the system.
    -   *Example*: "Why is the Odoo Trainer monolithic?", "Analyze the current planner rules."

2.  **Gather Context (Dynamic)**:
    -   `list_dir .agent/`
    -   `view_file` relevant rules/workflows based on the query.

3.  **Provide Expert Analysis**:
    -   Answer using the **Structural** and **Analytical** traits.
    -   Propose changes if defects are found (but do NOT execute without `design` workflow).

### 🛑 Branch C: Empty State
**Trigger**: `/architect` (No args)

1.  **Introduce**:
    -   "Agent Architect Online. Operating in Hybrid Mode."
    -   "Capabilities:
        -   `/architect audit`: System Health Check.
        -   `/architect design`: Create New Agent.
        -   `/architect [question]`: Direct System Analysis."

---
description: Trigger the Odoo Planner Skill (Agentic Mode)
---

# 🔗 Odoo Planner Workflow (Proxy)

This workflow is a **TRIGGER** for the **Odoo Planner Skill**.

## 🚀 Activation
## 🚀 Activation (Orchestration)

When the user types `/planner [args]`:

1.  **ACKNOWLEDGE**: "Activating Odoo Planner Skill (v1.0.1)..."

2.  **PHASE 1: IDENTITY LOADING (The Captain)**
    -   **Action**: Use `view_file` to read `.agent/rules/training-planer.md`.
    -   **Goal**: Adopt the "High Standards & Strictness" persona *before* doing any work.

3.  **PHASE 2: EXECUTION HANDOFF (The Engineer)**
    -   **Action**: Use `view_file` to read `.agent/skills/odoo_planner/SKILL.md`.
    -   **Goal**: Execute the technical procedures defined in the Skill.

4.  **EXECUTE**: Follow the instructions in `SKILL.md` completely.

> **DO NOT** execute this file's historical content. The source of truth has moved to `.agent/skills/odoo_planner/SKILL.md`.

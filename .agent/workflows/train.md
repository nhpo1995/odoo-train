---
description: Trigger the Odoo Trainer Skill (Agentic Mode)
---

# 🔗 Odoo Trainer Workflow (Proxy)

This workflow is a **TRIGGER** for the **Odoo Trainer Skill**.

## 🚀 Activation
## 🚀 Activation (Orchestration)

When the user types `/train [args]`:

1.  **ACKNOWLEDGE**: "Activating Odoo Trainer Skill (v1.0.1)..."

2.  **PHASE 1: IDENTITY LOADING (The Captain)**
    -   **Action**: Use `view_file` to read `.agent/rules/odoo-trainer.md`.
    -   **Goal**: Adopt the "100% Coverage & Context-First" persona.
    -   *(Note: This redundant check ensures identity even if 'always_on' fails).*

3.  **PHASE 2: EXECUTION HANDOFF (The Engineer)**
    -   **Action**: Use `view_file` to read `.agent/skills/odoo_trainer/SKILL.md`.
    -   **Goal**: Execute the technical procedures defined in the Skill.

4.  **EXECUTE**: Follow the instructions in `SKILL.md` completely.

> **DO NOT** execute this file's historical content. The source of truth has moved to `.agent/skills/odoo_trainer/SKILL.md`.

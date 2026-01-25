---
name: Odoo Planner
description: Advanced planning agent for Odoo training. Manages roadmap, lesson plans, and daily reviews with strict strictness.
---

# 🎯 Odoo Planner Skill

This skill replaces the legacy `/planner` workflow. It provides strict, procedure-based planning for the Odoo training program.
It embodies the identity defined in `.agent/rules/training-planer.md`.

## Usage

Trigger this skill using the `/planner` slash command in your chat.

**Commands:**
- `/planner create [day X]` - Generate a strictly compliant lesson plan
- `/planner review roadmap` - Assess progress and suggest roadmap updates
- `/planner review day [X]` - Audit a specific lesson plan
- `/planner verify spec` - Run automated specification check

## Core Procedures

When executing these commands, you MUST follow the linked procedures STRICTLY.

### 1. Create Lesson Plan
**Trigger:** `/planner create [day X]`
**Procedure:**
1.  **Research Phase**: Execute `procedures/research.md` to gather context.
    -   *System enforces*: Reading `module_spec.md`, `actual_module.md`, and querying Context7.
2.  **Design Phase**: Execute `procedures/design.md` to draft the plan.
    -   *System enforces*: 90% topic coverage, strictly complex exercises.
3.  **Finalize**: Save the file to `.agent/learning/daily_notes/`.

### 2. Verify Specification
**Trigger:** `/planner verify spec`
**Action:**
-   Run script: `scripts/validate_spec.py`
-   Report discrepancies between `module_spec.md` and the actual codebase.

### 3. Review Roadmap
**Trigger:** `/planner review roadmap`
**Procedure:**
-   Load `procedures/review_roadmap.md` (to be created)
-   Analyze gap between current progress and job requirements.

## Golden Rules
1.  **No Delegation**: You (the Planner) do the updates. Do not ask the user or trainer to do it.
2.  **Strict Strictness**: If a step in the procedure says "MANDATORY", you cannot skip it.
3.  **Evidence-Based**: Every plan must be backed by actual source code lines (checked via `view_file`).

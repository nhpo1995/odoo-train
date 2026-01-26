---
description: Sub-workflow for System Health Audit (Orphans, Integrity, Compliance)
---

# 🕵️ Architect Audit Workflow

**Trigger**: `/architect audit`

## 🚦 Phase 1: Structure Mapping

**Goal**: Get a complete picture of the "Brain".

1.  **Scan Directories**:
    -   `list_dir .agent/rules/`
    -   `list_dir .agent/skills/`
    -   `list_dir .agent/workflows/`
    -   `list_dir .agent/workflows/sub/`

2.  **Inventory Check**:
    -   Identify all Rules.
    -   Identify all Skills.
    -   Identify all Workflows.

## 🔍 Phase 2: Integrity & Compliance Check

**Goal**: Detect "Rot" and "Drift".

1.  **Orphan Detection**:
    -   Are there Rules that no Skill/Workflow uses?
    -   Are there Skills that are never triggered?

2.  **Odoo System Validation (Critical)**:
    -   **Target**: `odoo-trainer` (Skill) and `planner` (Workflow).
    -   **Check**:
        -   Are they **Monolithic**? (Single file prefers over many small ones).
        -   Do they have **Strict Identity**?
        -   Do they have **Legacy Protocol** (Step 0 -> Step N)?

3.  **Archival Check**:
    -   Ensure `_archive/` exists and contains previous versions.

## 📝 Phase 3: The Report

**Goal**: Transparent communication.

1.  **Draft Report**:
    -   **Status**: Healthy / Degraded / Critical.
    -   **Issues**: List specific violations.
    -   **Recommendations**: Actionable fixes.

2.  **Notify User**:
    -   Present the findings.
    -   Ask for permission to fix (if needed).

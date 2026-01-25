# Changelog

All notable changes to the Agentic Odoo Learning System (`.agent/`) will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2026-01-25

### Changed
- **Workflow Architecture**: Refactored `workflows/*.md` to be "True Orchestrators" instead of passive proxies.
    - Workflows now explicitly load **Rules** (Persona) first.
    - Then Workflows hand off to **Skills** (Execution).
- **Skill Cleanup**: Removed "Step 0: Load Persona" from `SKILL.md` as checking identity is now the Captain's (Workflow) job.

## [1.0.0] - 2026-01-25

### Added
- **Hybrid Architecture**: Split monolithic workflows into modular **Skills** (`odoo_planner`, `odoo_trainer`) and **Rules** (Identity).
- **Planner Skill**:
    - `procedures/research.md`: Strict Spec validation and Context7 lookup.
    - `procedures/design.md`: Automated lesson planning standard.
    - `scripts/validate_spec.py`: Python script to detect Spec vs Code drift.
    - `scripts/validate_lesson.py`: Python script to enforce 10-15 concepts/lesson (QA).
    - **Interactive Deviation Check**: Planner halts and asks "Keep or Trash?" when un-specced features are found.
- **Trainer Skill**:
    - `procedures/prep_checklist.md`: Enforces `view_file` on source code before teaching.
    - `procedures/teaching_cycle.md`: Strict "Read -> Explain -> Practice" loop.
    - **Knowledge Base Caching**: Check `references/` -> Query Context7 -> Save to `references/`.
    - `scripts/verify_progress.py`: Validates session completion based on logs.
- **Version Control**: Added `.agent/VERSION` and `CHANGELOG.md`.

### Deprecated
- **Workflows**: Moved old `.agent/workflows/*.md` to `_archive/`. The system now runs entirely on Skills.

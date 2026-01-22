---
name: odoo-planner
description: Create, review, and improve Odoo training lesson plans and roadmaps. Use when the user runs /planner ... or asks to plan lessons, review the roadmap, or improve a day plan. Do not use for teaching sessions.
---

# Odoo Planner

## Overview
Design and update Odoo training plans with strict workflow adherence and direct file edits in this repo.

## Trigger and routing
- If the user message starts with `/planner`, run this skill.
- If the user message starts with `/train` or the request is teaching, do not use this skill; use the trainer skill.

## Required sources
- Read `.agent/rules/training-planer.md` for role rules.
- Read `.agent/workflows/planner.md` for the exact workflow.

## Execution
- Follow the workflow steps verbatim; treat those files as source of truth.
- Edit files directly when required; do not only recommend changes.
- Use Context7 only when required by the workflow and persist references as instructed.
- Keep context small and summarize long inputs as required by the workflow.

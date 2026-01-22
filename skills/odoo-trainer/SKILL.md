---
name: odoo-trainer
description: Teach Odoo lesson plans and run training sessions. Use when the user runs /train day X, asks to teach or mentor, or does not use /planner. Follow the training workflow and fill evaluations.
---

# Odoo Trainer

## Overview
Deliver Odoo lessons from daily plans with full coverage and interactive practice.

## Trigger and routing
- If the user message starts with `/planner`, do not use this skill; use the planner skill.
- If the user message starts with `/train day X`, start that day.
- Otherwise, default to this skill for teaching and mentoring requests.

## Required sources
- Read `.agent/rules/odoo-trainer.md` for role rules.
- Read `.agent/workflows/train.md` for the exact workflow.

## Execution
- Follow the workflow steps verbatim and in order.
- Read source files before guiding the learner, as required.
- Update evaluation sections and tracking files exactly as specified.

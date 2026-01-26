# Antigravity Agentic System

**Version**: 1.0.2
**Status**: Hybrid Monolith

## 🧠 Core Agents

### 1. Architect (`/architect`)
The meta-agent responsible for designing, auditing, and refining the system itself.
- **Identity**: Strict, Analytical, Polymath.
- **Capabilities**:
    - **Direct**: System Analysis, Explanations.
    - **Sub-workflows**: Audit (`/architect audit`), Design (`/architect design`).

### 2. Odoo Trainer (`/train`)
Specialized mentor for Odoo development.
- **Style**: Strict 100% coverage, step-by-step.
- **Architecture**: Monolithic (Rule + Workflow). Refactored to eliminate "Split Brain".

### 3. Planner (`/planner`)
Strategic planner for learning roadmaps.
- **Capabilities**: Create Lesson Plans, Review Progress.
- **Architecture**: Monolithic.

## 📂 Structure

### Core
- `.agent/rules/`: Agent Identities (The "Soul").
- `.agent/workflows/`: Main Dispatchers (The "Process").
- `.agent/learning/`: User's learning progress and artifacts.

### Advanced
- `.agent/workflows/sub/`: specialized interactions (e.g., `architect_audit.md`).
- `.agent/workflows/_archive/`: Backup of previous versions (Legacy Protection).

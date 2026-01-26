# 🧠 Agentic Odoo Learning System

> **A self-improving, rigorous AI mentorship program for mastering Odoo Framework.**
> Built on a **Hybrid Monolith Architecture** of Rules (Identity) and Workflows (Process).

![Architecture](https://img.shields.io/badge/Architecture-Hybrid%20Monolith-blue)
![Strictness](https://img.shields.io/badge/Strictness-High-red)
![Agent Version](https://img.shields.io/badge/Agent_System-v1.0.2-blue)
![Odoo Version](https://img.shields.io/badge/Odoo-14.0-purple)

## 📖 Overview

This repository is not just a collection of Odoo code. It is the workspace for an advanced **AI Agent System** designed to teach Odoo development with Senior-level strictness.

It replaces traditional "Chatbot Tutorials" with a structured, rigorous workflow:
1.  **Architect Agent**: Designs, audits, and maintains the system integrity (`/architect`).
2.  **Planner Agent**: Researchs specs, validates code, and designs high-fidelity lesson plans (`/planner`).
3.  **Trainer Agent**: Teaches strict source-code reading, context-first concepts, and enforces "100% Coverage" (`/train`).

## 🏗 System Architecture

The system operates on a **Hybrid Monolith** model:

```mermaid
graph TD
    User([User]) -->|/architect| Arch[Architect Dispatcher]
    User -->|/planner| Planner[Planner Workflow]
    User -->|/train| Trainer[Trainer Workflow]

    subgraph "Meta-Cognition Layer"
        Arch -->|Direct Analysis| Self[Hybrid Polymath]
        Arch -->|/architect design| Design[Design Protocol]
        Arch -->|/architect audit| Audit[Health Check]
    end

    subgraph "Execution Layer"
        Planner -->|Load Persona| R1[Rule: Planner]
        Trainer -->|Load Persona| R2[Rule: Trainer]
        Trainer -->|Read| Src[Odoo Source Code]
    end
```

## 🚀 Usage

### 1. The Architect (`/architect`)
*The System Engineer.*
- **Commands**: 
    - `/architect analyze [question]` (Direct Q&A)
    - `/architect audit` (System Health Check)
    - `/architect design` (Create New Agent)

### 2. The Planner (`/planner`)
*The Strategist.*
- **Command**: `/planner create day [X]`
- **Goal**: Generates production-ready lesson plans.

### 3. The Trainer (`/train`)
*The Mentor.*
- **Command**: `/train day [X]`
- **Goal**: Teaches strict source-code reading and enforces 100% coverage.

## 📂 Repository Structure

```
.
├── .agent/                 # The Brain 🧠
│   ├── rules/              # Agent Personas (Identity)
│   ├── workflows/          # Process Definitions (The Work)
│   │   ├── sub/            # Specialized Protocols (Audit, Design)
│   │   └── _archive/       # Legacy Protection
│   └── learning/           # Curriculum & Knowledge Base
├── custom_addons/          # The Odoo Code being built
└── README.md               # You are here
```

## 🛡️ "Zero Hallucination" Mechanisms

How we prevent the AI from lying:
1.  **Strict Identity**: Agents must read their Rule file before acting (Single Source of Truth).
2.  **Protocol Enforcement**: Steps are hardcoded in Workflows.
3.  **Context7 Integration**: Mandatory external verification for best practices.

## 🤝 Contribution

This is a personal learning workspace, but the **Agent Architecture** is reusable.
Feel free to copy `.agent/` folder to your own projects to enable this AI workflow.

---
*Created by NHPDev with Agentic AI Engineering*

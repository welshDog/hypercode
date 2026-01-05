# 🧠 HyperCode AI Context & Builder Brief

This file defines the project vision, structure, and operational rules for AI agents (Broski, Architect, Code, etc.) working on HyperCode. **READ THIS FIRST.**

---

## 1. 🌍 Project Vision (The "Why")

**HyperCode** is a **neurodivergent-first**, multi-paradigm programming language (classical, quantum, molecular) designed to lower the barrier to complex systems engineering.

-   **Core Philosophy:** Neurodivergent-first. Minimize cognitive load. Visuals over walls of text. Clear spatial layouts.
-   **Paradigms:**
    -   **Classical:** Python-like logic.
    -   **Quantum:** Qiskit-backed circuit design.
    -   **Molecular:** DNA assembly (Golden Gate), PCR, CRISPR simulation.
-   **Architecture:** Monorepo with a shared core (Python) and a visual frontend (React/TypeScript).

---

## 2. 📂 Core Context & File Structure

### 📜 Primary Context (Read these to understand "The Rules")
-   **[`README.md`](../README.md)**: High-level overview, monorepo layout, run instructions.
-   **[`ROADMAP.md`](../ROADMAP.md)**: Project phases, priorities, future Bio-Logic/DNA work.
-   **[`DEVELOPMENT.md`](../DEVELOPMENT.md)**: Development phases and workflow organization.
-   **[`docs/CONTRIBUTING.md`](../docs/CONTRIBUTING.md)**: How to contribute, style guides.
-   **[`.github/SUGGESTED_ISSUES.md`](../.github/SUGGESTED_ISSUES.md)**: "Good First Issues" and entry points.

### ⚙️ The "Engine Room" (Where Real Work Happens)
-   **Language Core (`hypercode-core/`)**:
    -   Parser, AST, IR, Simulator.
    -   Backends: `quantum/`, `molecular/`.
-   **Interpreter (`interpreter/` + `syntax/`)**:
    -   Execution logic and syntax definitions.
-   **Visual Editor (`hyperflow-editor/`)**:
    -   **React + Vite + React Flow**.
    -   Key Components: `CompilerPanel`, `GoldenGateNode`, Custom Nodes.
-   **Tests (`tests/`)**:
    -   `pytest` for backend, `vitest` for frontend.
    -   **Golden Rule:** If you change logic, you MUST update/run tests.

### 🧠 Planning & Spec Layer
-   **`HyperCode Mega TO-DO List/`**: Big-picture backlog.
-   **`hyperflow-issues.csv`**: Granular editor tasks.
-   **Specs**:
    -   `visual_editor_spec.md` (Editor behavior)
    -   `VIS4-Playbook.md`, `VIS5-Playbook.md` (Visual design systems)

---

## 3. 🤖 How to Work (Agent Protocol)

### Phrasing Asks (Prompt Structure)
When communicating or planning, use this structure:
1.  **Context**: "You are working in HyperCode, a neurodivergent-first language..."
2.  **Scope**: "Modify ONLY `hyperflow-editor/src/components/CompilerPanel.tsx`..."
3.  **Goal**: "Implement [feature] matching [spec]..."
4.  **Checks**: "Run `pytest` and verify [X]..."

### Operational Rules
1.  **Neurodivergent-First**: Prioritize clarity. Use bullet points. Avoid walls of text.
2.  **Filesystem Hygiene**:
    -   **NEVER** create files unless necessary.
    -   **ALWAYS** prefer editing existing files.
    -   **NEVER** create proactive docs (READMEs) unless asked.
3.  **Verification**: Always verify changes with tests or build checks before finishing.

---

## 4. 🚀 Current Status (Phase 2 -> Phase 3)
-   **Current Focus**: Phase 2 (Implementation) & Phase 3 (Bio-Logic/DNA).
-   **Key Active Areas**:
    -   Golden Gate Assembly Simulator (Backend).
    -   Plasmid Map Visualization (Frontend).
    -   Compiler integration (Flow -> HyperCode -> Simulation).

---

*This file is the source of truth for AI agent context. Update it as the project evolves.*

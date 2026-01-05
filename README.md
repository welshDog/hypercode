# THE HYPERCODE Monorepo

Welcome to the HyperCode project monorepo.

## Structure

> **Legend**:
> - ✅ **STABLE**: Active development, core components.
> - 🚧 **WIP**: In progress, expect changes.
> - 🗑️ **DEPRECATED**: Legacy code, moved to archive.

- **[hypercode-core](./hypercode-core/)** ✅: The Core Language Backend (Python). Contains the Parser, AST, IR, Simulator, and Compiler. **(Heart of the Backend)**
- **[hyperflow-editor](./hyperflow-editor/)** ✅: The Visual Editor (React + Vite). The primary UI for HyperCode. **(Heart of the Frontend)**
- **[ai-agents](./ai-agents/)** 🚧: Configuration and prompts for AI assistants.
- **[planning](./planning/)** 🚧: Project roadmaps, specs, and issue tracking.
- **[website](./website/)** 🚧: The HyperCode marketing homepage.
- **[archive](./archive/)** 🗑️: Legacy code (`hypercode/`, `interpreter/`, `tests/` root folders) and backups.

## FAQ & Architecture

### Active vs Legacy
- **Active**: `hypercode-core/` (Backend) and `hyperflow-editor/` (Frontend).
- **Legacy**: Anything in `archive/`. The root-level `hypercode/` and `interpreter/` folders were duplicates and have been archived.

### Core vs Interpreter
- The **Interpreter** is a module *within* `hypercode-core`. It is not a separate repo.

### Project Management
- We are consolidating planning into the `planning/` directory. The "Mega TO-DO" is a backlog, but GitHub Issues are preferred for active tasks.

### Next Milestone
- **Alpha Testing**: Release v0.2-alpha to early testers.
- **Feedback Loop**: Gathering input on accessibility features.

### Neurodivergent Features
- **Implemented**: High-contrast maps, spatial node layouts, clear tooltips.
- **Implemented**: Dyslexia Mode (Shift + D), Reduced Visual Noise (Zen Mode).

## Getting Started

### HyperFlow Editor
```bash
cd hyperflow-editor
npm install
npm run dev
```

### HyperCode Core
```bash
cd hypercode-core
# Setup virtual environment if needed
pip install -e .
```

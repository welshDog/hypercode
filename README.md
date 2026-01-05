# THE HYPERCODE Monorepo

Welcome to the HyperCode project monorepo.

## Structure

- **[hyperflow-editor](./hyperflow-editor/)**: The Visual Editor (React + Vite + React Flow). This is the primary UI for HyperCode.
- **[hypercode-core](./hypercode-core/)**: The Core Language Backend (Python). Contains the Parser, AST, IR, and Quantum/Molecular Backends.
- **[website](./website/)**: The HyperCode marketing homepage.
- **[ai-agents](./ai-agents/)**: Configuration and prompts for AI assistants.
- **[planning](./planning/)**: Project roadmaps, specs, and issue tracking.
- **[archive](./archive/)**: Legacy code and backups.

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

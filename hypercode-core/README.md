# 🧠 HyperCode

**Programming Language for Neurodivergent Brains**

> A multi-paradigm, neurodivergent-first programming language with textual + visual syntax, targeting classical, quantum, and molecular computing.

[![License: CC-BY 4.0](https://img.shields.io/badge/License-CC--BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Status: Phase 2 - Implementation](https://img.shields.io/badge/Status-Phase%202%20--%20Implementation-blue)]()
[![Built for](https://img.shields.io/badge/Built%20for-ADHD%20%7C%20Dyslexia%20%7C%20Autism-ff69b4)](#neurodivergent-first-design)
[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

## 🎯 The Vision

Programming languages are more than syntax. **They are an expression of how minds think.**

For neurodivergent coders, typical languages often don't fit brain patterns. HyperCode is built FROM THE GROUND UP for:

- **ADHD brains:** Visual-spatial thinking, expandable complexity, immediate feedback
- **Dyslexic brains:** Minimal symbols, consistent patterns, high contrast, dyslexia-friendly fonts
- **Autistic brains:** Explicit rules, no hidden behavior, domain-specific precision

---

## 🚀 Installation

HyperCode requires Python 3.10 or higher. We recommend using a virtual environment.

### Using pip

```bash
# Create and activate a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install core HyperCode
pip install hypercode

# Install optional dependencies
pip install "hypercode[quantum]"  # For quantum computing support
# pip install "hypercode[molecular]"  # For molecular computing (coming soon)
```

### Development Installation

For development, clone the repository and install in editable mode:

```bash
git clone https://github.com/welshDog/hypercode.git
cd hypercode

# Install with development dependencies
pip install -e ".[dev]"

# Install optional dependencies for development
pip install -e ".[quantum,dev]"

# Run tests
pytest
```

## ✨ Features

### Multi-Paradigm
- **Classical Computing** → Traditional imperative code (compiles to LLVM → CPU)
- **Quantum Computing** → Circuit-based operations (compiles to Qiskit, Cirq, etc.)
- **Molecular Computing** → DNA strand displacement (compiles to DSD simulator)

### Dual Syntax
- **Textual:** `@`-prefixed keywords, consistent structure, LLM-friendly
- **Visual:** Node-based canvas with semantic color coding, spatial relationships
- **Bidirectional:** Switch between text ↔ visual without data loss

### AI Co-Development
- Language Server Protocol (LSP) for real-time feedback
- Domain hints for LLM context
- Curated example patterns for fine-tuning Claude/GPT-4
- Feedback loop system (error → LLM → correction)

### Accessibility-First
- Designed with neurodivergent users from day 1
- Multiple representation modes (text, visual, auditory future)
- Clear semantics, no implicit behavior
- Dyslexia-friendly typography + color schemes

---

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/welshDog/THE-HYPERCODE
cd THE-HYPERCODE
pip install -e ".[qiskit]"
```

### First Program (Quantum Bell Pair)

Create a file named `bell_pair.hc`:

```hypercode
@quantum BellState qubits 2
    H q0
    CX q0 q1
    MEASURE q0 -> c0
    MEASURE q1 -> c1
@end
```

Run it:

```bash
hypercode quantum run bell_pair.hc --shots 1000
```

Output:
```
QuantumCircuit BellState: 2 qubits, 4 ops
Results (BellState): {'00': 502, '11': 498}
```

---

## 📚 Documentation

### Phase 1: Complete Design Specification

- **[HyperCode Research Report 2025](./docs/HyperCode_Research_Report_2025.md)** — Landscape analysis, trends, vision
- **[Design Sprint 1: Textual Syntax](./docs/Phase1_Design_Sprint_1_Textual_Syntax.md)** — Grammar, type system, examples
- **[Design Sprint 2: Visual Syntax](./docs/Phase1_Design_Sprint_2_Visual_Syntax.md)** — Node library, interactions, patterns
- **[Design Sprint 3: Intermediate Representation](./docs/Phase1_Design_Sprint_3_Intermediate_Representation.md)** — MLIR-style IR, optimization, code gen
- **[Phase 1 Summary](./docs/Phase1_Complete_Summary.md)** — Overview, decisions, next steps

### Phase 2: Implementation (In Progress)

- [Parser Implementation](./DEVELOPMENT.md#parser)
- [IR Builder](./DEVELOPMENT.md#ir-builder)
- [Backends](./DEVELOPMENT.md#backends)
- [Visual Editor](./DEVELOPMENT.md#visual-editor)

---

## 🧠 Neurodivergent-First Design

### For ADHD Brains
✅ Visual-spatial representation (nodes + wires, not text walls)  
✅ Expandable complexity (collapse/expand subgraphs)  
✅ Immediate feedback (run button, see data flow animate)  
✅ Chunked syntax (one concept per line)  
✅ Consistent patterns (predictable structure)

### For Dyslexic Brains
✅ Sans-serif fonts (OpenDyslexic, Comic Sans, Verdana options)  
✅ Minimal symbols (only `@`, `:`, `<>`)  
✅ Color + shape semantics (don't rely on text alone)  
✅ Generous spacing (not cramped)  
✅ High contrast color schemes (red-green friendly)

### For Autistic Brains
✅ Explicit everything (no hidden behavior)  
✅ Clear, unambiguous rules (grammar is deterministic)  
✅ Predictable structure (same across all contexts)  
✅ Loud, informative errors (fail fast, fail clear)  
✅ Domain-specific tools (quantum, molecular built-in)

---

## 📊 Current Status (v0.1.0) ✅

| Phase | Status | What's Real |
|-------|--------|-------------|
| Phase 1 — Design Spec | ✅ Complete | Vision docs + architecture diagram |
| Phase 2 — Implementation | 🟡 In Progress | v0.1.0 Released (Parser + Quantum Backend) |
| Phase 3 — Optimization | ⏳ Planned | Optimization passes |

## What Works Today ✅

- **Parser** — Custom recursive descent parser for HyperCode syntax.
- **HyperFlow Editor** — React-based visual IDE with Bio-Logic and Focus Mode.
- **Quantum Backend** — Execution via Qiskit (Aer Simulator priority).
- **CLI** — `hypercode` command line interface for running and debugging.
- **Repo structure** — `hypercode/`, `examples/`, `tests/` folders scaffolded.

---

## 🎨 HyperFlow: The Visual Cockpit

> **"The cockpit for your neurodivergent brain."**

HyperFlow is the visual IDE for HyperCode, designed to reduce cognitive load and prevent "wall-of-text" overwhelm. It is **not** just a prototype—it is a production-ready React Flow environment.

### Core Features (v0.1.0)

#### 🧬 Bio-Logic Engine (`VIS1`)
- **Real Science**: Built-in `BioLogic.ts` engine handles DNA sticky ends, restriction sites, and ligation rules.
- **Nodes**: `Sequence`, `Enzyme` (EcoRI, BamHI, etc.), `Ligase`.
- **Validation**: Visual feedback prevents invalid biological connections.

#### 👁️ Focus Mode (`VIS2`)
- **Hyperfocus Toggle**: One click dims the entire world to 15% opacity, leaving only your active node and its neighbors.
- **Semantic LOD**: Zoom out to see the "big picture" (blocks), zoom in to see the details (sequences/params).
- **Benefit**: Eliminates visual noise and supports ADHD single-tasking.

#### 🐍 Hybrid Export (`VIS3`)
- **Code Generation**: Instantly converts your visual flow into executable Python code.
- **Bio**: Generates `BioPython` scripts using `Bio.Restriction`.
- **Quantum**: Generates `Qiskit` circuits for quantum nodes.

### Try It Out
Run the editor locally:
```bash
cd hyperflow-editor
npm install
npm run dev
```

---

## 🛠️ Architecture

```
HyperCode Code (Text or Visual)
        ↓
    [Parser/Lexer]
        ↓
   [AST Builder]
        ↓
[Semantic Analyzer]
        ↓
   ╔════════════════╗
   ║  HyperCode IR  ║  (MLIR-style, multi-domain)
   ║   (SSA Form)   ║
   ╚════════════════╝
        ↓
    [Optimizers]
        ↓
  ┌─────┬─────┬─────┐
  ↓     ↓     ↓     ↓
LLVM  Qiskit DSD  [Future]
  ↓     ↓     ↓
CPU   Quantum Molecular
```

---

## 🤝 Contributing

We're **recruiting neurodivergent co-designers and developers**.

### Ways to Help

1. **Design Feedback** — Does the syntax make sense to YOUR brain?
2. **Parser Implementation** — Help build the textual frontend
3. **Visual Editor** — Build the node-based interface
4. **Quantum Backend** — Connect to Qiskit, Cirq
5. **Testing** — Test with real quantum hardware (IBM, Google, IonQ)
6. **Documentation** — Make it clearer, better organized
7. **Community** — Spread the word, recruit co-builders

**See [CONTRIBUTING.md](./CONTRIBUTING.md) for details.**

---

## 📖 Examples

See the `examples/` directory for more.

### Quantum Bell Pair
```hypercode
@quantum BellState qubits 2
    H q0
    CX q0 q1
    MEASURE q0 -> c0
    MEASURE q1 -> c1
@end
```

### Classical Logic
```hypercode
@data x: 10
@check (x > 5) -> {
    @print(x)
}
```

---

## 📜 License

HyperCode is open-source and distributed under the **CC-BY 4.0 License**.

---

## 🙏 Acknowledgments

HyperCode synthesizes insights from:

- **MLIR** (Google's multi-level IR compiler)
- **Qiskit + Qutes** (quantum computing accessibility)
- **DSD Visual** (molecular strand displacement)
- **Eclipse Langium** (DSL best practices)
- **Fuser** (node-based visual programming)
- **Neurodiversity Research** (HCI, accessibility, cognitive science)
- **LLM Code Generation** (feedback loops, DSL + AI synergy)

---

## 🚀 The Moment

> *Programming languages express how minds think. For decades, they've expressed only neurotypical minds.*
>
> *HyperCode flips that.*
>
> *We're building a language for neurodivergent brains, AI systems, and the quantum/molecular computing frontier.*
>
> *The future is calling. Join us or watch it get built without you.* 🔥

---

**Made with ♾️ by [Lyndz Williams](https://github.com/welshDog) and the HyperCode community.**

**Last Updated:** December 30, 2025

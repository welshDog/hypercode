# 🏗️ HyperCode System Architecture

**HyperCode** is designed as a modular, neurodivergent-first compiler ecosystem. It separates the **Visual Interface** (HyperFlow) from the **Language Core** (HyperCode), connected by a robust compilation pipeline.

## 🧩 High-Level Overview

```mermaid
graph TD
    User[User] -->|Drag & Drop| Editor[HyperFlow Editor (React)]
    Editor -->|JSON Graph| Compiler[HyperCode Compiler]
    Compiler -->|V3 Source Code| Parser[V3 Parser]
    Parser -->|AST| Evaluator[Evaluator]
    Evaluator -->|QIR| Backend[Quantum/Bio Backend]
    Backend -->|Results| Editor
```

---

## 🔌 Core Components

### 1. HyperFlow Editor (`/hyperflow-editor`)
- **Tech**: React, React Flow, Vite, TypeScript.
- **Role**: The visual IDE. Users manipulate nodes (Hadamard, CRISPR, etc.) on a 2D canvas.
- **Output**: A JSON representation of the graph (`nodes` + `edges`).

### 2. The Compiler (`hypercode.compiler`)
- **Role**: Translates the React Flow JSON graph into **HyperCode V3 Source Code**.
- **Domain Detection**: Automatically detects if a program is `#:domain quantum` or `#:domain molecular` based on the nodes used.
- **Optimization**: Performs basic topological sorting to ensure operations happen in the correct order.

### 3. The Parser (`hypercode.parser`)
- **Tech**: Recursive Descent Parser (Python).
- **Role**: Reads HyperCode V3 source text and builds a strict **Abstract Syntax Tree (AST)**.
- **Key Features**:
  - **Strict Typing**: No fuzzy parsing; enforces `@init`, `@circuit`, and `@gate` structure.
  - **Error Reporting**: Provides line/column location for syntax errors.

### 4. The Evaluator (`hypercode.interpreter`)
- **Role**: Orchestrates the execution of the AST.
- **Lowering**: Converts high-level AST nodes (e.g., `QGate`) into an Intermediate Representation (QIR).
- **Execution**:
  - **Quantum**: Dispatches to Qiskit (or internal simulator).
  - **Molecular**: Runs biological simulation logic (Restriction digests, PCR amplification).

### 5. Intermediate Representation (IR)
- **Quantum**: Uses a **QIR (Quantum Intermediate Representation)**-like structure to map logical qubits to physical indices.
- **Bio**: Uses `BioPython` sequence objects and simulated laboratory states.

---

## 🧬 Domain Specifics

### Quantum Pipeline
1. **Source**: `@hadamard: q[0]`
2. **AST**: `QGate(name='hadamard', qubits=[QubitRef('q', 0)])`
3. **IR**: `QInstr(op='H', target=0)`
4. **Backend**: `qc.h(0)` (Qiskit)

### Molecular Pipeline
1. **Source**: `@let: seq = pcr(source, fwd="ATG...", rev="TAG...")`
2. **AST**: `Assign(target='seq', value=Call(func='pcr', args=[...]))`
3. **Backend**: Simulates primer annealing and amplification cycles.

---

## 📂 Directory Structure

- `hypercode-core/`: The Python backend.
  - `ast/`: Node definitions.
  - `parser/`: Lexer and Parser logic.
  - `compiler/`: HyperFlow -> HyperCode converter.
  - `interpreter/`: Runtime logic.
  - `backends/`: Qiskit and Bio execution engines.
- `hyperflow-editor/`: The React frontend.
- `docs/`: Documentation and Specifications.

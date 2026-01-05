# HyperCode Development Report (December 2025)

## 1. Executive Summary
HyperCode is a **neurodivergent-first quantum programming language** designed to reduce cognitive load through a clean, line-based syntax and explicit state management.

As of December 2025, the project has achieved a **working Vertical Slice (v0.1.0)**. The core pipeline—Parsing → AST → IR → Backend (Stub)—is functional for both classical logic and basic quantum circuits.

## 2. Architecture & Components

### 2.1 Core Language (Frontend)
- **Parser**: A custom **Recursive Descent Parser** (`hypercode/parser/parser.py`) was implemented to bypass complex tooling dependencies (ANTLR) and ensure maintainability. It supports:
  - `@data` for constants
  - `@check` for conditionals
  - `@print` for output
  - `@quantum` for circuit definitions
- **AST**: A strongly-typed Python dataclass structure (`hypercode/ast/nodes.py`) representing the program tree.

### 2.2 Quantum Intermediate Representation (IR)
- **Design**: A linear, assembly-like IR (`hypercode/ir/qir_nodes.py`) that abstracts away surface syntax.
- **Components**: `QModule`, `QAlloc`, `QGate`, `QMeasure`.
- **Lowering**: The `QuantumLowerer` (`hypercode/ir/lower_quantum.py`) converts AST `QuantumCircuitDecl` nodes into linear IR, performing constant folding for gate parameters (e.g., resolving `RZ(PI/2)`).

### 2.3 Backends
- **Qiskit Backend**: A functional stub (`hypercode/backends/qiskit_backend.py`) that translates HyperCode IR into `qiskit.QuantumCircuit` objects.
  - *Status*: Operational (requires `qiskit` installed).
- **Molecular Backend**: Planned for future chemical simulation integration.

### 2.4 CLI Tooling
- **Command**: `hypercode`
- **Subcommands**:
  - `parse <file>`: Inspect AST.
  - `qir <file>`: Generate and view Quantum IR.
  - `run <file>`: Execute program (Classical logic + Quantum stubs).

## 3. Current Status & Achievements

| Component | Status | Notes |
|-----------|--------|-------|
| **Parser** | ✅ Complete | Handles full v0 syntax including Quantum blocks. |
| **AST** | ✅ Complete | Fully typed dataclasses. |
| **Evaluator** | ⚠️ Partial | Classical logic works; Quantum executes as print-stubs (execution pending backend wiring). |
| **Quantum IR** | ✅ Complete | Linear IR + Lowering implemented. |
| **Qiskit Bridge**| ✅ Alpha | Can compile IR to Qiskit objects. |
| **Tests** | ✅ Passing | 100% pass rate on `test_v0.py` and `test_ir_quantum.py`. |

### Recent Milestones
1.  **Quantum Syntax Added**: Support for `H`, `CX`, `RZ(theta)`, and `MEASURE` operations.
2.  **IR Layer Built**: Decoupled the frontend from the backend execution.
3.  **CLI Integration**: Added `qir` command for inspecting compilation results.

## 4. Code Structure
```text
hypercode/
├── ast/
│   └── nodes.py          # AST Definitions
├── parser/
│   └── parser.py         # Recursive Descent Parser
├── ir/
│   ├── qir_nodes.py      # Quantum IR Definitions
│   └── lower_quantum.py  # AST -> IR Lowering Logic
├── backends/
│   └── qiskit_backend.py # IR -> Qiskit Compiler
├── interpreter/
│   └── evaluator.py      # Classical Interpreter
└── cli.py                # Command Line Interface
```

## 5. Recommendations & Roadmap

### Immediate Next Steps (v0.2)
1.  **Connect Evaluator to Backend**: Modify `Evaluator` to call `to_qiskit()` and actually run circuits when encountering `@quantum` blocks (if a simulator is available).
2.  **Classical IR**: Implement a similar IR layer for classical logic (SSA form) to enable optimization.
3.  **Hybrid Flow**: Allow classical variables to control quantum gates (e.g., `RZ(angle_var)`).

### Long-Term Goals (v1.0)
- **Visual IDE**: A block-based or graph-based editor that maps 1:1 to the text syntax.
- **Molecular DSL**: specialized syntax for `@molecule` definitions.
- **Error Messages**: Improve "friendly" error reporting for neurodivergent users.

## 6. Conclusion
The foundation is solid. The decision to write a custom parser paid off in flexibility, allowing rapid addition of Quantum features. The IR layer ensures we can swap backends (Qiskit, Cirq, Molecular) without rewriting the parser.

**Ready for: Hybrid Classical-Quantum Execution.**

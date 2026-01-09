# 📘 HyperCode DEEP DIVE: The Complete Specification

> **Version:** 1.0.0-alpha
> **Status:** Phase 2 Implementation
> **Target Audience:** Core Architects, Compiler Engineers, Advanced Users

---

## 📑 Table of Contents

1.  [Language Architecture](#1-language-architecture)
2.  [The Type System](#2-the-type-system)
3.  [Syntax Specification (Textual)](#3-syntax-specification-textual)
4.  [Syntax Specification (Visual)](#4-syntax-specification-visual)
5.  [Compiler Pipeline](#5-compiler-pipeline)
6.  [Memory Management](#6-memory-management)
7.  [Error Handling & Diagnostics](#7-error-handling--diagnostics)

---

## 1. Language Architecture

HyperCode is a **multi-backend** language. It does not compile to a single machine code but rather transforms into domain-specific instructions.

### 1.1 The Domain Directive
Every HyperCode file begins with a `#:` directive that sets the execution context.

```python
#:domain classical  # Standard CPU execution
#:domain quantum    # Quantum Circuit execution
#:domain molecular  # DNA Strand Displacement
```

### 1.2 The Execution Model
*   **Classical**: Sequential execution, stack-based memory, standard control flow.
*   **Quantum**: Circuit construction -> Transpilation -> Shot-based execution -> Measurement aggregation.
*   **Molecular**: Reaction network compilation -> Kinetic simulation (ODE/Stochastic).

---

## 2. The Type System

HyperCode uses a **Strong, Static Type System** with type inference where possible.

### 2.1 Primitive Types
*   `Int`: 64-bit signed integer.
*   `Float`: 64-bit IEEE floating point.
*   `Bool`: True/False.
*   `String`: UTF-8 immutable string.
*   `Void`: No return value.

### 2.2 Quantum Types (`#:domain quantum`)
*   `Qubit`: A handle to a quantum bit. Cannot be copied (No-Cloning Theorem).
*   `QReg`: A register of `n` qubits.
*   `Bit`: A classical bit resulting from measurement.
*   `CReg`: A register of `n` classical bits.

### 2.3 Molecular Types (`#:domain molecular`)
*   `Strand`: A DNA sequence (e.g., "ATCG").
*   `Complex`: A bound structure of strands.
*   `Concentration`: Float representing Molar (M) or count.

---

## 3. Syntax Specification (Textual)

HyperCode uses `@` decorators (at-signs) for keywords to assist dyslexic parsing by creating visual anchors.

### 3.1 Functions
```python
@function: calculate_sum (a: Int, b: Int) -> Int
  @return: a + b
```

### 3.2 Variables (`@let`)
Variables are immutable by default unless marked mutable (future feature).
```python
@let: x = 10
@let: name = "HyperCode"
```

### 3.3 Control Flow
```python
@if: x > 5
  @print: "Big"
@else:
  @print: "Small"

@for: i in range(10)
  @print: i
```

### 3.4 Quantum Circuits
```python
@circuit: bell_state
  @init: q = Qubit(2)
  @init: c = Bit(2)
  
  @hadamard: q[0]
  @cnot: q[0], q[1]
  
  @measure: q -> c
```

---

## 4. Syntax Specification (Visual)

The Visual Editor (HyperFlow) maps 1:1 to the Textual AST.

*   **Nodes**: Functions, Variables, Gates.
*   **Edges**: Data flow (Classical), Wire connections (Quantum).
*   **Shapes**:
    *   *Hexagon*: Logic/Control Flow.
    *   *Circle*: Qubits/Atoms.
    *   *Rectangle*: Functions/Transformations.
*   **Colors**:
    *   `#FF6B6B` (Red): Classical Logic.
    *   `#4ECDC4` (Teal): Quantum Operations.
    *   `#FFE66D` (Yellow): Molecular/Data.

---

## 5. Compiler Pipeline

The HyperCode compiler (`hc`) follows a modern multi-pass architecture:

1.  **Lexing (ANTLR4)**: Converts `.hc` text into tokens.
2.  **Parsing (ANTLR4)**: Generates a Concrete Syntax Tree (CST).
3.  **AST Generation**: Transforms CST into a typed Abstract Syntax Tree.
4.  **Semantic Analysis**:
    *   Type Checking.
    *   Borrow Checking (for Qubits).
    *   Domain Verification.
5.  **IR Generation (HIR)**: "HyperCode Intermediate Representation".
6.  **Backend Codegen**:
    *   `classical` -> Python AST / LLVM IR.
    *   `quantum` -> Qiskit DAG / OpenQASM 3.0.
    *   `molecular` -> Visual DSD / CRN (Chemical Reaction Network).

---

## 6. Memory Management

*   **Classical**: Reference counting (via Python backend) or GC.
*   **Quantum**:
    *   Qubits are allocated at the start of a `@circuit`.
    *   Qubits are automatically deallocated (reset) at the end of scope unless returned.
    *   **Linear Types**: A Qubit cannot be used twice in a way that violates quantum laws (e.g., passed to two gates simultaneously).

---

## 7. Error Handling & Diagnostics

HyperCode prioritizes **Actionable Error Messages**.

*   **Bad**: `SyntaxError: Unexpected token '@'`
*   **Good**: 
    ```
    Error at line 10: Missing type annotation.
    
    @let: x = calculate(y)
             ^
    Did you mean to specify the type of 'x'? 
    HyperCode requires explicit types in this context.
    ```

---

## 8. Future Roadmap (Phase 3+)

*   **Hybrid Runtime**: Real-time interaction between Classical and Quantum execution (e.g., using measurement results to decide next quantum gate in real-time).
*   **3D Visualization**: VR/AR interface for circuit design.
*   **Direct FPGA Backend**: Synthesizing quantum control logic directly to hardware.

---

*End of Deep Dive Specification*

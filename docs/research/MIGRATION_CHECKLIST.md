# 🚧 HyperCode V3 Migration Checklist

> **Goal:** Ensure all code adheres to the "Neurodivergent-First" V3 Standard.
> **Date:** 2026-01-09
> **Status:** ACTIVE

## 🛑 1. Critical Syntax Shifts

- [ ] **Domain Headers**: Does every file start with `#:domain`?
    - *Why*: Sets context immediately. Prevents "What language is this?" confusion.
- [ ] **Explicit Decorators**: Are all keywords prefixed with `@`?
    - *Bad*: `function`, `if`, `quantum`
    - *Good*: `@function`, `@if`, `@circuit`
    - *Why*: Visual anchoring for dyslexic reading flow.
- [ ] **No Implicit Blocks**: Are quantum circuits named and explicit?
    - *Bad*: `@quantum ... @end`
    - *Good*: `@circuit: my_circuit` (Indentation defines block)
    - *Why*: Reduces vertical noise and nesting.

## ⚛️ 2. Quantum Specifics

- [ ] **Register Types**: Are you using `QReg` and `CReg`?
    - *Bad*: `qubits 2` (Implicit) or `QuantumRegister(2)` (Verbose)
    - *Good*: `@init: q = QReg(2)`
- [ ] **Gate Syntax**: Are gates lower-case decorators?
    - *Bad*: `H q0`, `CX q0 q1`
    - *Good*: `@hadamard: q[0]`, `@cnot: q[0], q[1]`
- [ ] **Measurement**: Is the arrow syntax used?
    - *Style*: `@measure: q -> c`

## 🧩 3. Classical Logic

- [ ] **Type Annotations**: Are functions typed?
    - *Style*: `(n: Int) -> Void`
- [ ] **Control Flow**: Are `@if`, `@else`, `@for` used?
- [ ] **Entry Point**: Is there a `@function: main()`?

## 🧹 4. Clean Code & Accessibility

- [ ] **Docstrings**: Do complex functions have `@doc`?
- [ ] **Variable Naming**: Are variables semantic? (e.g., `threshold` vs `t`)
- [ ] **Visual Spacing**: Is there a blank line between logical blocks?

---

## 🔍 Self-Audit Log

| File | Status | Notes |
| :--- | :--- | :--- |
| `examples/bell_pair.hc` | ✅ FIXED | Converted to V3 |
| `examples/grover.hc` | ✅ FIXED | Updated QReg syntax |
| `examples/hybrid_logic.hc` | ✅ FIXED | Removed legacy `@data` |
| `examples/parameterized_gate.hc` | ✅ FIXED | Added `@circuit` block |
| `examples/classical/fizzbuzz.hc` | ✅ FIXED | Standardized decorators |

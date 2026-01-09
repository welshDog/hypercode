# ⚡ QUANTUM QUICK REFERENCE

## 🔑 Key Directives

| Directive | Description | Example |
| :--- | :--- | :--- |
| `#:domain quantum` | Enables quantum mode | Top of file |
| `#:backend qiskit` | Sets target backend | `#:backend qiskit` |
| `@circuit:` | Defines a quantum circuit | `@circuit: my_circ` |
| `@quantum_function:` | Function with quantum logic | `@quantum_function: run()` |

## 🚪 Quantum Gates Cheat Sheet

| Gate | Syntax | Effect |
| :--- | :--- | :--- |
| **H** | `@hadamard: q` | Superposition |
| **X** | `@x: q` | NOT (0->1) |
| **Y** | `@y: q` | Phase+Bit Flip |
| **Z** | `@z: q` | Phase Flip |
| **CX** | `@cnot: c, t` | Entanglement |
| **CCX** | `@ccnot: c1, c2, t` | Toffoli (AND) |
| **S** | `@s: q` | sqrt(Z) phase |
| **T** | `@t: q` | sqrt(S) phase |
| **M** | `@measure: q -> c` | Readout |

## 📦 Types

*   `Qubit`: Single qubit.
*   `QReg(n)`: Register of `n` qubits. `q[0]`, `q[1]`.
*   `Bit`: Single classical bit.
*   `CReg(n)`: Register of `n` bits.

## 📝 Common Patterns

**Bell Pair (Entanglement)**
```python
@init: q = QReg(2)
@hadamard: q[0]
@cnot: q[0], q[1]
```

**Superposition Array**
```python
@for: i in range(n)
  @hadamard: q[i]
```

**Teleportation Protocol**
1. Bell Pair
2. CNOT(msg, alice)
3. H(msg)
4. Measure
5. Correct

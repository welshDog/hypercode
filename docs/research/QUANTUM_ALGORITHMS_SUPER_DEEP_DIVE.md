# ⚛️ QUANTUM ALGORITHMS: SUPER DEEP DIVE

> **Domain:** `#:domain quantum`
> **Backend:** Qiskit / OpenQASM
> **Focus:** Algorithms, Gates, and Implementation

---

## 1. The Quantum Primitive

In HyperCode, Quantum Computing is not a library; it is a **mode of thought**.

### 1.1 The Qubit
The fundamental unit. Unlike a bit (0 or 1), a Qubit exists in a state:
`|ψ⟩ = α|0⟩ + β|1⟩`
Where `|α|² + |β|² = 1`.

In HyperCode:
```python
@init: q = Qubit()  # Initialized to |0⟩
```

### 1.2 Superposition
Creating a state where the qubit is both 0 and 1 with equal probability.
```python
@hadamard: q
```

### 1.3 Entanglement
Linking two qubits so the state of one instantly determines the state of the other.
```python
@cnot: control, target
```

---

## 2. Standard Gate Library

HyperCode supports the universal gate set.

| Gate | Syntax | Description | Matrix |
| :--- | :--- | :--- | :--- |
| **Pauli-X** | `@x: q` | Bit Flip (NOT) | `[[0, 1], [1, 0]]` |
| **Pauli-Y** | `@y: q` | Bit + Phase Flip | `[[0, -i], [i, 0]]` |
| **Pauli-Z** | `@z: q` | Phase Flip | `[[1, 0], [0, -1]]` |
| **Hadamard** | `@hadamard: q` | Superposition | `1/√2 [[1, 1], [1, -1]]` |
| **CNOT** | `@cnot: c, t` | Controlled-NOT | 4x4 Identity/Swap |
| **Toffoli** | `@ccnot: c1, c2, t` | Controlled-Controlled-NOT | 8x8 |
| **Phase** | `@phase(theta): q` | Rotation around Z | `[[1, 0], [0, e^iθ]]` |
| **Measure** | `@measure: q -> c` | Collapse wavefunction | N/A |

---

## 3. Algorithm: Grover's Search

Grover's algorithm provides a quadratic speedup for searching unstructured databases.
`O(N)` -> `O(√N)`

### 3.1 Implementation in HyperCode

```python
#:domain quantum

@circuit: grover_oracle(qubits: QReg, target_state: Int)
    # Flips the phase of the target state
    @comment: "Phase Oracle implementation would go here"
    # (Simplified for documentation)
    @cz: qubits[0], qubits[1] 

@circuit: diffusion_operator(qubits: QReg)
    # Inversion about the mean
    @for: q in qubits
        @hadamard: q
        @x: q
    
    @h: qubits[-1]
    @mcx: qubits[:-1], qubits[-1]  # Multi-controlled X
    @h: qubits[-1]
    
    @for: q in qubits
        @x: q
        @hadamard: q

@function: run_grover(n_qubits: Int, target: Int) -> Int
    @init: q = QReg(n_qubits)
    @init: c = CReg(n_qubits)
    
    # 1. Initialization
    @for: i in range(n_qubits)
        @hadamard: q[i]
        
    # 2. Iteration (approx sqrt(N))
    @let: iterations = floor(sqrt(2^n_qubits))
    @for: _ in range(iterations)
        @apply: grover_oracle(q, target)
        @apply: diffusion_operator(q)
        
    # 3. Measurement
    @measure: q -> c
    @return: c
```

---

## 4. Algorithm: Quantum Teleportation

Transmitting a quantum state using two classical bits and entanglement.

```python
@circuit: teleport(msg: Qubit, alice: Qubit, bob: Qubit)
    # 1. Create Bell Pair between Alice and Bob
    @hadamard: alice
    @cnot: alice, bob
    
    # 2. Alice prepares to send 'msg'
    @cnot: msg, alice
    @hadamard: msg
    
    # 3. Alice measures
    @init: c1 = Bit()
    @init: c2 = Bit()
    @measure: msg -> c1
    @measure: alice -> c2
    
    # 4. Bob applies corrections based on classical bits
    # Note: This requires dynamic circuits (Phase 3)
    @if: c2 == 1
        @x: bob
    @if: c1 == 1
        @z: bob
        
    # 'bob' now holds the state of 'msg'
```

---

## 5. Quantum Error Correction (QEC)

HyperCode plans to support QEC codes (Surface Code, Shor Code) via high-level abstractions.

```python
# Future Syntax
@qec: surface_code(distance=3)
    @circuit: my_logical_circuit
        # Operations on logical qubits
```

---

## 6. Hardware Backends

HyperCode bridges to:
1.  **IBM Quantum** (via Qiskit)
2.  **Google Sycamore** (via Cirq - planned)
3.  **Rigetti** (via Quil - planned)
4.  **IonQ** (via Azure Quantum - planned)

The compiler optimizes the circuit for the specific topology of the target hardware (mapping virtual qubits to physical qubits).

---
*End of Quantum Super Deep Dive*

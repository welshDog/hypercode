# ⚙️ **PHASE 1 DESIGN SPRINT 3: INTERMEDIATE REPRESENTATION (IR) DESIGN**
## *The Bridge Between Human Code & Machine Execution*

**Status:** 🟢 ACTIVE SPRINT  
**Duration:** Week 3-4 (Jan 2025)  
**Goal:** Design IR that targets classical, quantum, and molecular backends  

---

## 📋 WHAT IS AN INTERMEDIATE REPRESENTATION?

An **IR** is the internal format a compiler uses to:

1. **Unify different syntax** (textual, visual) → single canonical form
2. **Optimize code** (reorder operations, eliminate redundancy)
3. **Target multiple backends** (classical, quantum, molecular)
4. **Enable analysis** (type checking, resource estimation)

**Example:**

```
Input (textual or visual)
    ↓
[Lexer/Parser] → Parse Tree
    ↓
[Semantic Analysis] → **INTERMEDIATE REPRESENTATION** ← We design this
    ↓
[Backend Code Generator] → LLVM IR, Qiskit, DNA Simulator
    ↓
[Compiler] → Machine Code, Quantum Circuit, Reactions
```

---

## 🎯 HyperCode IR Design Principles

### **1. Multi-Level Abstraction** [1]

Unlike traditional IRs (one level), HyperCode IR supports **multiple abstraction levels**:

- **High-Level IR (HIR)** → What user wrote (close to textual/visual syntax)
- **Mid-Level IR (MIR)** → Domain-specific optimizations (quantum, molecular)
- **Low-Level IR (LIR)** → Near-hardware (register allocation, scheduling)

**Why?** Each backend needs different information.

### **2. Domain-Aware** [1]

IR must handle **three different semantic models**:

- **Classical:** Imperative, state-based, deterministic
- **Quantum:** Unitary, superposition-aware, probabilistic
- **Molecular:** Reaction-rate-based, time-aware, stochastic

### **3. Extensible** [1]

New domains/backends should be **plug-and-play:**

```
HyperCode IR ──┌─> ClassicalBackend (→ LLVM → CPU code)
               ├─> QuantumBackend (→ Qiskit → Quantum circuit)
               ├─> MolecularBackend (→ DSD → Reactions)
               └─> [Future Backend] (extensible)
```

---

## 🧪 SPRINT 3 DELIVERABLE: THE IR SPECIFICATION

### **Part A: Core IR Data Structures (MLIR-Inspired)**

We use **MLIR-style** IR design (Google's approach, proven for ML/quantum/hardware):

```python
# Pseudo-Python IR representation

class IRModule:
    """Top-level HyperCode IR container"""
    name: str
    domain: str  # "classical", "quantum", "molecular"
    imports: List[str]  # imported modules
    functions: List[IRFunction]
    types: List[IRType]

class IRFunction:
    """A HyperCode function"""
    name: str
    signature: IRFunctionType
    args: List[IRArgument]
    return_type: IRType
    blocks: List[IRBlock]  # blocks of operations
    attributes: Dict[str, Any]  # metadata

class IRBlock:
    """A basic block (straight-line code, no branches)"""
    label: str
    operations: List[IROp]
    terminator: IRTerminator  # branch, return, etc.

class IROp:
    """A single operation"""
    opcode: str  # "load", "add", "hadamard", etc.
    operands: List[IRValue]  # inputs
    result: IRValue  # output
    attributes: Dict[str, Any]  # parameters

class IRValue:
    """A value (result of operation)"""
    name: str
    type: IRType

class IRType:
    """Type information"""
    kind: str  # "int", "float", "qubit", "dna_strand"
    element_type: Optional[IRType]  # for List<T>, Option<T>
    attributes: Dict[str, Any]  # metadata
```

---

### **Part B: Classical Domain IR**

#### **Example: Classical Data Pipeline**

**Input Code:**
```hypercode
@function: filter_positive (data: List<Int>) -> List<Int>
  @let: result = []
  @for: x in data
    @when: x > 0
      @push: result, x
  @return: result
```

**IR Representation:**

```mlir
hc.function @filter_positive(
    %data: !hc.list<i32>
) -> !hc.list<i32> {
  %result = hc.alloc: !hc.list<i32>
  %zero = hc.const 0: i32
  
  hc.for %x in %data {
    %cond = hc.gt %x, %zero: i32
    hc.cond_br %cond, ^bb_push, ^bb_skip
    
  ^bb_push:
    hc.list_push %result, %x: !hc.list<i32>
    hc.br ^bb_iter_next
    
  ^bb_skip:
    hc.br ^bb_iter_next
    
  ^bb_iter_next:
    hc.yield  # Next iteration
  }
  
  hc.return %result: !hc.list<i32>
}
```

---

### **Part C: Quantum Domain IR**

#### **Example: Grover's Algorithm**

**IR Representation:**

```mlir
hc.quantum_function @grover_search(
    %n: i32,
    %marked: i32
) -> i32 {
  %qubits = hc.quantum_alloc %n: !hc.quantum<qubit>
  %result = hc.quantum_alloc %n: !hc.quantum<qubit>
  
  # Initial superposition
  hc.for %i in range(%n) {
    %q_i = hc.quantum_index %qubits, %i: !hc.quantum<qubit>
    hc.hadamard %q_i: !hc.quantum<qubit>
  }
  
  # Grover iterations
  %sqrt_n = hc.int_sqrt %n: i32
  hc.for %iter in range(%sqrt_n) {
    # Oracle application
    hc.quantum_apply @oracle(%qubits, %marked): !hc.quantum<qubit>
    
    # Diffusion operator
    hc.quantum_apply @diffusion(%qubits): !hc.quantum<qubit>
  }
  
  # Measurement
  %bits = hc.quantum_measure %qubits: !hc.quantum<bit>
  %answer = hc.bits_to_int %bits: i32
  
  hc.return %answer: i32
}
```

---

### **Part D: Molecular Domain IR**

#### **Example: Gene Detection Circuit**

```mlir
hc.molecular_circuit @gene_detector(
    %sample: !hc.dna.solution
) -> f64 {
  %probe = hc.dna_strand "ATCGATCG": !hc.dna.strand
  
  # Stage 1: Binding
  %stage1 = hc.molecular_stage "binding" {
    time: !hc.time<minutes, 5>
    temperature: 37.0
  } {
    %complex = hc.dna_reaction(
        %probe, 
        %sample
    ) {
      forward_rate: 1.0e6,
      reverse_rate: 1.0e-3,
      binding_energy: -8.5
    }: !hc.dna.complex
    
    hc.yield %complex: !hc.dna.complex
  }
  
  %result = hc.molecular_stage_output %stage1: f64
  hc.return %result: f64
}
```

---

## ✅ IR VALIDATION

### **Correctness Properties:**
- [ ] **Type safety** ✓ (all values have explicit types)
- [ ] **SSA property** ✓ (each value assigned once)
- [ ] **Block termination** ✓ (every block ends with terminator)
- [ ] **Use-def chains** ✓ (easy to analyze dataflow)

### **Optimization-Friendly:**
- [ ] **Easy constant folding** ✓
- [ ] **Dead code elimination** ✓
- [ ] **Dataflow analysis** ✓ (value dependencies clear)
- [ ] **Resource estimation** ✓ (metadata available)

### **Multi-Backend Support:**
- [ ] **Classical compatible** ✓ (→ LLVM)
- [ ] **Quantum compatible** ✓ (→ Qiskit)
- [ ] **Molecular compatible** ✓ (→ DSD)
- [ ] **Extensible** ✓ (custom operations per backend)

---

**SPRINT 3 STATUS: 🟢 IR SPECIFICATION COMPLETE**

# 🛠️ HYPERCODE DEVELOPMENT GUIDE

## 📂 Code Surfaces & Architecture

When working on HyperCode, understand where your task fits:

1.  **Language Core (`hypercode-core/`)**:
    -   The brain. Parser, AST, IR, Simulator.
    -   *Key Files*: `simulator.py`, `parser.py`, `backends/`.
2.  **Visual Editor (`hyperflow-editor/`)**:
    -   The face. React, Vite, React Flow.
    -   *Key Files*: `CompilerPanel.tsx`, `App.tsx`, `components/nodes/`.
3.  **Interpreter (`interpreter/` + `syntax/`)**:
    -   The nervous system. Execution logic.
4.  **Tests (`tests/`)**:
    -   The immune system. `pytest` for backend, `vitest` for frontend.

---

## Phase 2 Implementation Roadmap

### Setup

```bash
git clone https://github.com/welshDog/hypercode
cd hypercode
poetry install  # or pip install -r requirements.txt
```

---

## Phase 2.1: Parser & AST (Jan 2025)

### Minimal MVP Slice: "Hello Quantum"

**Goal:** Parse + compile a simple quantum program to Qiskit.

### Grammar (ANTLR `.g4`)

Start with:
- `@quantum_function`
- `@circuit`
- `@init`, `@hadamard`, `@cnot`, `@measure`
- `@return`

### AST Data Structures

```python
@dataclass
class QuantumFunction:
    name: str
    circuit: QuantumCircuit
    return_type: str

@dataclass
class QuantumCircuit:
    instructions: List[Instruction]

@dataclass
class Instruction:
    opcode: str  # "init", "hadamard", "cnot", "measure"
    args: Dict[str, Any]
```

### Tests

```bash
pytest tests/parser/test_quantum_parse.py
```

---

## Phase 2.2: IR Builder (Feb 2025)

Map AST → IR (SSA form).

```python
def ast_to_ir(ast: QuantumFunction) -> IRFunction:
    """Convert AST to HyperCode IR"""
    pass
```

---

## Phase 2.3: Quantum Backend (Feb 2025)

IR → Qiskit code.

```bash
hypercode run examples/bell_pair.hc --backend qiskit
```

---

## Phase 2.4: CLI (Feb 2025)

```bash
hypercode parse examples/bell_pair.hc          # Show AST
hypercode ir examples/bell_pair.hc             # Show IR
hypercode run examples/bell_pair.hc            # Execute
```

---

## Phase 2.5: Visual Editor (Mar 2025)

Web-based node editor using React + React Flow.

```bash
cd editor
npm install
npm run dev
```

---

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/parser/ -k "test_hadamard"

# With coverage
pytest tests/ --cov=hypercode --cov-report=html
```

---

## Deployment

TBD: Once CLI is ready, package as:
- PyPI (`pip install hypercode`)
- Conda
- Docker image

---

## Contributing

See CONTRIBUTING.md

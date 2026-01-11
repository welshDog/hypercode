# 🚀 Getting Started with HyperCode

Welcome to **HyperCode**, the neurodivergent-first quantum and biological programming language. This guide will get you set up and running your first V3 circuit in minutes.

## 📦 Installation

### Prerequisites
- **Python 3.9+**
- **Node.js 16+** (for the Editor)
- **Git**

### 1. Clone the Repo
```bash
git clone https://github.com/welshDog/THE-HYPERCODE.git
cd THE-HYPERCODE
```

### 2. Install Core (Backend)
The core language engine (Parser, Compiler, Evaluator).

```bash
cd hypercode-core
pip install -e .
```
*Note: This installs HyperCode in editable mode, so your changes take effect immediately.*

### 3. Install Editor (Frontend)
The visual flow-based IDE.

```bash
cd ../hyperflow-editor
npm install
```

---

## ⚡ Quick Start: CLI

You can run HyperCode programs directly from the terminal.

### 1. Create a File (`hello.hc`)
Create a file named `hello.hc` with the following **V3 Syntax**:

```hypercode
#:domain quantum

@circuit: main
    # 1. Initialize 2 Qubits and 2 Classical Bits
    @init: q = QReg(2)
    @init: c = CReg(2)

    # 2. Create Entanglement (Bell Pair)
    @hadamard: q[0]
    @cnot: q[0], q[1]

    # 3. Measure
    @measure: q[0] -> c[0]
    @measure: q[1] -> c[1]
```

### 2. Run It
```bash
hypercode run hello.hc
```

**Expected Output:**
```text
Running Quantum Circuit: main
Results: {'00': 512, '11': 512}
```

---

## 🎨 Quick Start: Visual Editor

Prefer a visual approach? Use HyperFlow.

### 1. Start the Dev Server
```bash
cd hyperflow-editor
npm run dev
```
Open [http://localhost:5173](http://localhost:5173) in your browser.

### 2. Build Your Flow
1. Drag a **Hadamard** node onto the canvas.
2. Drag a **CNOT** node.
3. Connect them.
4. Click **Compile** to see the generated V3 code!

---

## 🛠️ Troubleshooting

**"Command not found: hypercode"**
- Ensure you ran `pip install -e .` inside `hypercode-core`.
- Check your PATH.

**"ImportError: No module named qiskit"**
- HyperCode defaults to the internal simulator if Qiskit is missing, but for full features:
- `pip install qiskit`

**"SyntaxError: Expected AT_CMD"**
- Ensure you are using the new **V3 Syntax** (`@init`, `@gate`). Old V1/V2 syntax is deprecated.

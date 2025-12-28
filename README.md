# 🧠 HyperCode

**Programming Language for Neurodivergent Brains**

> A multi-paradigm, neurodivergent-first programming language with textual + visual syntax, targeting classical, quantum, and molecular computing.

[![License: CC-BY 4.0](https://img.shields.io/badge/License-CC--BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Status: Phase 2 - Implementation](https://img.shields.io/badge/Status-Phase%202%20--%20Implementation-blue)]()
[![Built for](https://img.shields.io/badge/Built%20for-ADHD%20%7C%20Dyslexia%20%7C%20Autism-ff69b4)](#neurodivergent-first-design)

---

## 🎯 The Vision

Programming languages are more than syntax. **They are an expression of how minds think.**

For neurodivergent coders, typical languages often don't fit brain patterns. HyperCode is built FROM THE GROUND UP for:

- **ADHD brains:** Visual-spatial thinking, expandable complexity, immediate feedback
- **Dyslexic brains:** Minimal symbols, consistent patterns, high contrast, dyslexia-friendly fonts
- **Autistic brains:** Explicit rules, no hidden behavior, domain-specific precision

---

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

### Installation (Coming Soon)

```bash
git clone https://github.com/welshDog/hypercode
cd hypercode
poetry install  # or pip install -r requirements.txt
```

### First Program (Quantum Example)

```hypercode
#:domain quantum
#:backend qiskit

@quantum_function: bell_pair () -> Bits
  @doc: "Create a Bell pair (maximally entangled state)"
  
  @circuit: c
    @init: qubits = QuantumRegister(2)
    @hadamard: qubits[0]
    @cnot: control=qubits[0], target=qubits[1]
    @measure: qubits -> result
  
  @return: result

@function: main ()
  @let: result = bell_pair()
  @print: result
```

Run it:
```bash
hypercode run examples/bell_pair.hc --backend qiskit
```

---

## 📚 Documentation

### Phase 1: Complete Design Specification

- **[HyperCode Research Report 2025](./docs/HyperCode_Research_Report_2025.md)** — Landscape analysis, trends, vision (521 lines)
- **[Design Sprint 1: Textual Syntax](./docs/Phase1_Design_Sprint_1_Textual_Syntax.md)** — Grammar, type system, examples (435 lines)
- **[Design Sprint 2: Visual Syntax](./docs/Phase1_Design_Sprint_2_Visual_Syntax.md)** — Node library, interactions, patterns (616 lines)
- **[Design Sprint 3: Intermediate Representation](./docs/Phase1_Design_Sprint_3_Intermediate_Representation.md)** — MLIR-style IR, optimization, code gen (769 lines)
- **[Phase 1 Summary](./docs/Phase1_Complete_Summary.md)** — Overview, decisions, next steps (433 lines)

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

## 📊 Current Status

| Phase | Status | Timeline |
|-------|--------|----------|
| **Phase 1:** Design Specification | ✅ **COMPLETE** | Done (Dec 2025) |
| **Phase 2:** Implementation | 🟡 **STARTING** | Jan-May 2025 |
| **2.1:** Parser + AST | 🟢 **Ready to start** | Jan 2025 |
| **2.2:** IR Builder | 🟡 **Planned** | Feb 2025 |
| **2.3:** Quantum Backend | 🟡 **Planned** | Feb-Mar 2025 |
| **2.4:** Classical + Molecular | 🟡 **Planned** | Mar-Apr 2025 |
| **2.5:** Visual Editor | 🟡 **Planned** | Feb-Apr 2025 |
| **Phase 3:** Optimization & Reliability | 🟡 **Planned** | Apr-Jun 2025 |

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

### Classical (Imperative)

```hypercode
@function: filter_positive (data: List<Int>) -> List<Int>
  @let: result = []
  @for: x in data
    @when: x > 0
      @push: result, x
  @return: result

@function: main ()
  @let: input = [1, -2, 3, -4, 5]
  @let: output = filter_positive(input)
  @print: output  # → [1, 3, 5]
```

### Quantum (Circuit-Based)

```hypercode
#:domain quantum

@quantum_function: grover_search (n: Int, marked: Int) -> Int
  @doc: "Quantum search: find marked element in n items"
  
  @circuit: c
    @init: qubits = QuantumRegister(n)
    
    @for: i in range(n)
      @hadamard: qubits[i]
    
    @let: iterations = int(sqrt(n))
    @for: _ in range(iterations)
      @apply: oracle(qubits, marked)
      @apply: diffusion(qubits)
    
    @measure: qubits -> result
  
  @return: result
```

### Molecular (Reaction-Based)

```hypercode
#:domain molecular

@molecular_circuit: gene_detector (sample: DNASolution) -> Float
  @stages
    @stage: "binding"
      @reaction: probe + target -> complex
      @time: 5 minutes
    
    @stage: "amplification"
      @cascade: signal_amplification
        @trigger: complex
        @output: fluorescence
    
    @measure: output
  
  @return: fluorescence_intensity
```

---

## 🎯 Roadmap (2025)

### Q1 2025: Parser & First Backend
- ✅ Textual syntax parser (ANTLR or langcc)
- ✅ AST builder
- ✅ Basic IR infrastructure
- ✅ Quantum backend (→ Qiskit)
- ✅ CLI tool (`hypercode run`)

### Q2 2025: Multi-Backend
- Classical backend (→ LLVM)
- Molecular backend (→ DSD)
- Visual editor (React + node library)
- Language Server Protocol (LSP) support

### Q3 2025: Optimization & AI
- Optimization passes (constant folding, gate fusion, etc.)
- LLM integration (Claude/GPT fine-tuned for HyperCode)
- Resource estimation
- Hardware deployment guides

### Q4 2025: Community & Hardening
- Open-source community building
- Industry partnerships (IBM, Google, Microsoft)
- Educational materials
- Production-ready reliability

---

## 📞 Get Involved

- **GitHub Issues:** [Report bugs, suggest features](https://github.com/welshDog/hypercode/issues)
- **Discussions:** [Chat about design, ask questions](https://github.com/welshDog/hypercode/discussions)
- **Twitter:** [@HyperCodeLang](https://twitter.com) (coming soon)
- **Discord:** [Community server](https://discord.gg) (coming soon)

---

## 📜 License

HyperCode is open-source and distributed under the **CC-BY 4.0 License** (documentation) + **[TBD: Choose Compiler License]** (implementation).

This means:
✅ Use it freely (personal, research, commercial)  
✅ Modify it (fork, adapt, extend)  
✅ Share it (redistribute with attribution)  
✅ Attribution required (mention HyperCode)

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

**Last Updated:** December 28, 2025

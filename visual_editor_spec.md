# 🎨 HyperCode Visual Node Graph Editor Specification

**Version:** 1.1.0-DRAFT  
**Date:** January 4, 2026  
**Status:** Living Document (Auto-updates with research)  
**Authors:** HyperCode Community (Lyndz Williams lead)

---

## 📋 TABLE OF CONTENTS

1. [Executive Summary](#-executive-summary)
2. [Design Philosophy](#-design-philosophy)
3. [Architecture](#-architecture)
4. [Visual Language: The HyperGraph](#-visual-language-the-hypergraph)
5. [Accessibility First](#-accessibility-first)
6. [Component Taxonomy](#-component-taxonomy)
7. [Keyboard & Input](#-keyboard--input)
8. [Microinteractions](#-microinteractions)
9. [Code Generation](#-code-generation)
10. [Roadmap & Milestones](#-roadmap--milestones)

---

## 🎯 EXECUTIVE SUMMARY

HyperCode's **Visual Node Graph Editor** (codenamed **"HyperFlow"**) is a neurodivergent-first, accessibility-focused, hybrid visual programming environment that bridges classical computation, quantum circuits, and molecular pathways in a unified spatial canvas.

### Key Principles:

✅ **Neurodivergent-First Design:** Minimal visual noise, spatial logic, high contrast, chunking-friendly  
✅ **Hybrid Architecture:** React Flow (frontend) + Rete.js (computation engine)  
✅ **WCAG 2.1 AA Compliant:** Keyboard navigation, screen reader support, ADHD-specific UX  
✅ **Extensible Nodes:** Classical, Quantum, DNA, Custom (plugin system ready)  
✅ **Live Feedback:** Real-time execution, statevector visualization, molecular simulations  
✅ **Quantum Native:** First-class support for Qiskit export and quantum circuit visualization

### Target Users:

- **Primary:** Neurodivergent (ADHD, Dyslexic, Autistic) programmers
- **Secondary:** Quantum researchers, Synthetic biologists, Students
- **Accessibility:** Everyone (low-barrier entry point)

---

## 🧠 DESIGN PHILOSOPHY

### Why Visual Programming?

Traditional text-based languages prioritize sequential, left-to-right cognitive processing. **Neurodivergent brains often excel at spatial reasoning, pattern recognition, and parallel thinking.**

HyperFlow leverages:
- **2D Spatial Layout:** Logic flows as circuits, not sequences
- **Visual Chunking:** Zones and scopes prevent cognitive overload
- **Biomimetic Shapes:** Hexagons (nature-inspired, efficient packing)
- **Color-Coded Semantics:** Edge types = data flow types (instant recognition)
- **Tactile/Kinesthetic Feedback:** Node placement, connecting wires, snapping

### Design Axioms:

1. **Less is More:** Every pixel earns its place. No decorative complexity.
2. **Bandwidth = Choice:** Users control verbosity (tooltip level, auto-layout, dark mode)
3. **Errors are Teachers:** Failed connections highlight logic errors visually (not cryptic text)
4. **Flow Over Form:** Process clarity > aesthetic perfection
5. **Hands-On Agency:** Dragging, connecting, arranging = understanding

---

## 🏗️ ARCHITECTURE

### System Diagram:

```
┌─────────────────────────────────────────────────────┐
│ HYPERFLOW (User-Facing Visual Editor)               │
│ ┌──────────────────────────────────────────────────┐│
│ │ React Flow Canvas                                 ││
│ │ - Node Rendering (Hexagon shapes)                 ││
│ │ - Edge Visualization (Solid/Wavy/Dashed)          ││
│ │ - Mini-map + Controls                             ││
│ │ - Keyboard navigation (Tab, Arrow keys, Enter)    ││
│ └──────────────────────────────────────────────────┘│
├─────────────────────────────────────────────────────┤
│ ADAPTER LAYER (React Flow ↔ Rete.js)               │
│ - Node serialization/deserialization                │
│ - Event bridging                                    │
│ - Scope management                                  │
└─────────────────────────────────────────────────────┘
├─────────────────────────────────────────────────────┤
│ RETE.JS COMPUTATION ENGINE (Behind the scenes)      │
│ ┌──────────────────────────────────────────────────┐│
│ │ DataflowEngine: Process inputs → outputs          ││
│ │ ControlFlowEngine: Sequential execution           ││
│ │ Node Library: Classical, Quantum, DNA plugins     ││
│ └──────────────────────────────────────────────────┘│
├─────────────────────────────────────────────────────┤
│ EXECUTION TARGETS (Code Generation)                 │
│ - HyperCode Intermediate Representation (HIR)       │
│ - Python (Classical + Quantum via Qiskit)           │
│ - OpenQASM (Quantum circuits)                       │
│ - DNA Design Language (Molecular pathways)          │
│ - LLVM (Future: Hardware compilation)               │
└─────────────────────────────────────────────────────┘
```

### Why Hybrid?

| Aspect | React Flow | Rete.js | Decision |
|--------|-----------|---------|----------|
| **Visual Rendering** | ✅ Battle-tested | ⚠️ Needs plugin | Use React Flow |
| **Accessibility** | ✅ WCAG 2.1 AA | ⚠️ Build custom | Use React Flow |
| **Computation Logic** | ❌ Not designed | ✅ Powerful | Use Rete.js |
| **Quantum Support** | ❌ Need plugin | ✅ Plugin-ready | Use Rete.js |
| **Speed to MVP** | ✅ Fast | ⚠️ Moderate | Use React Flow |

**Result:** React Flow handles what it's BEST at (rendering + a11y), Rete.js handles what IT'S best at (processing + extensibility). Adapter bridges them seamlessly.

---

## 🎨 VISUAL LANGUAGE: THE HYPERGRAPH

### Node Design: Hexagons

**Why Hexagons?**
- Biomimetic (honeycombs, natural structures)
- Efficient packing (3 rotations instead of 4 for squares)
- 6 connection points naturally (vs. 4 on squares = more flexible)
- Aesthetically distinctive (not generic rounded squares)

### Hexagon Anatomy:

```
         ▲
        / \
       /   \
      |  ⚙  |   ← Node label (icon + text)
       \   /
        \ /
         ▼
```

**Specifications:**

- **Size:** 80px (standard), 120px (expanded), 60px (compact)
- **Corner Radius:** 12px (slight bevel, not rounded)
- **Connection Points:** 6 positions around perimeter (N, NE, SE, S, SW, NW)
- **Fill Color:** By node type (see Component Taxonomy)
- **Border:** 2px, dynamic color (normal/focused/error)
- **Shadow:** var(--shadow-md) (depth perception)

### Node States:

| State | Border | Glow | Opacity |
|-------|--------|------|---------|
| **Normal** | var(--color-border) | None | 1.0 |
| **Focused** | var(--color-primary) | var(--focus-ring) | 1.0 |
| **Selected** | var(--color-primary) | 0 0 0 4px var(--color-primary) | 1.0 |
| **Executing** | var(--color-primary) | Pulse animation | 1.0 |
| **Error** | var(--color-error) | var(--color-error) glow | 0.8 |
| **Disabled** | var(--color-border) | None | 0.5 |

### Edge Design: Three Types

Visual distinction through **line style**, not just color (accessible for colorblind users).

#### **Type 1: Solid Line (Data Flow)**
```
Sender ◄────────────► Receiver
```
- **Purpose:** Classical data (numbers, strings, booleans)
- **Color:** var(--color-info) (default: slate blue)
- **Thickness:** 2px
- **Animation:** None (static)
- **Example:** Integer value flowing from generator to processor

#### **Type 2: Wavy Line (Quantum State)**
```
Qubit ◄∿∿∿∿∿∿∿∿∿∿◄ Quantum Gate
```
- **Purpose:** Quantum information (superposition, entanglement)
- **Color:** var(--color-success) (default: teal)
- **Thickness:** 3px
- **SVG Path:** Wave amplitude = importance/fidelity
- **Animation:** Gentle wave pulse (subtle, not distracting)
- **Example:** Qubit superposition flowing from H gate to measurement

#### **Type 3: Dashed Line (Control Flow)**
```
Condition ◄- - - - - - - - ◄ If/Then
```
- **Purpose:** Execution control (conditional branches, loops)
- **Color:** var(--color-warning) (default: orange)
- **Thickness:** 2px
- **Dash Pattern:** 5px dash, 5px gap
- **Animation:** None (clarity over motion)
- **Example:** Boolean result routing to conditional execution

### Edge Labels (Optional):

When hovering over an edge, show:
- Data type (e.g., "uint32", "Qubit[2]", "DNA[AGTC]")
- Current value (if executing)
- Error message (if invalid)

---

## ♿ ACCESSIBILITY FIRST

### WCAG 2.1 AA Compliance

HyperFlow is designed to meet or exceed **WCAG 2.1 Level AA** standards:

#### Perceivable (Can users see/hear content?)

✅ **Color:** Edge types distinguished by line style, not color alone  
✅ **Contrast:** var(--color-text) on var(--color-surface) ≥ 4.5:1  
✅ **Text:** All nodes have text labels (not icon-only)  
✅ **Resize:** Canvas zooms (0.25x to 4x) without losing functionality  

#### Operable (Can users interact?)

✅ **Keyboard Navigation:** Full operation without mouse (Tab, Arrow, Enter, Space)  
✅ **Timing:** No time limits (no auto-save pressure)  
✅ **Seizure Safety:** No flashing (≥3 Hz rule), animations are gentle  
✅ **Navigability:** Focus order logical, visible focus indicators  

#### Understandable (Can users understand?)

✅ **Predictability:** Consistent interaction patterns  
✅ **Error Prevention:** Type checking before connection  
✅ **Error Recovery:** Undo/Redo (Cmd+Z / Cmd+Shift+Z)  
✅ **Help:** Tooltips + contextual hints on hover  

#### Robust (Works with assistive tech?)

✅ **ARIA:** Proper roles, labels, descriptions  
✅ **Screen Readers:** Tested with NVDA, JAWS, VoiceOver  
✅ **Keyboard:** All interactions keyboard-accessible  

### Neurodivergent-Specific Customizations

#### ADHD Patterns:

| Challenge | Solution | Setting |
|-----------|----------|---------|
| **Visual Clutter** | Toggle edge labels, collapse zones | Preferences: Verbosity |
| **Distraction** | Disable animations, dim inactive areas | Preferences: Focus Mode |
| **Decision Paralysis** | Show suggested next steps, quick templates | Toolbar: Smart Suggestions |
| **Executive Dysfunction** | Auto-save every 30s, session recovery | Preferences: Auto-save |
| **Time Blindness** | Timer widget, execution timeline | Sidebar: Execution Timeline |

#### Dyslexia Patterns:

| Challenge | Solution | Setting |
|-----------|----------|---------|
| **Font Legibility** | OpenDyslexic font option, increased letter spacing | Preferences: Font Family |
| **Color Sensitivity** | Custom color schemes, mono mode | Preferences: Color Mode |
| **Text Load** | Icons + labels (never text-only), short labels | All UI elements |
| **Spatial Reasoning Support** | Grid/snap-to-grid, alignment guides | Toolbar: Snap Options |

#### Autism Patterns:

| Challenge | Solution | Setting |
|-----------|----------|---------|
| **Sensory Overload** | Disable animations, high contrast mode, sound toggle | Preferences: Sensory |
| **Pattern Recognition** | Show node groups, color-code by category | Toolbar: Group Display |
| **Literal Communication** | Explicit error messages, no humor in help text | Error Handling |

---

## 🔧 COMPONENT TAXONOMY

### Node Types: Classical

#### **Input Nodes**
- **Constant:** Fixed values (42, "hello", true)
- **Variable:** Reference to state (x, data, config)
- **Sensor:** External input (time, mouse, network)

**Example Node:**
```
┌────────────────┐
│ 📊 Constant    │
│    Value: 42   │
└────────────────┘
      │
      ▼ (uint32)
```

#### **Processing Nodes**
- **Arithmetic:** +, -, *, /, %, **
- **Logic:** AND, OR, NOT, XOR
- **String:** concat, split, replace, length
- **Array:** map, filter, reduce, sort

**Example Node:**
```
┌────────────────┐
│  ➕ Add        │
│ A: ▢  B: ▢   │
└────────────────┘
   ▲    ▲
   │    └── B: int32
   └────── A: int32
```

#### **Output Nodes**
- **Display:** Console.log, debug print
- **Write:** Save to file, database, network
- **Export:** Code generation, visualization

---

### Node Types: Quantum

#### **State Preparation**
- **|0⟩ State:** Initialize qubit to ground
- **|1⟩ State:** Initialize qubit to excited
- **|+⟩ State:** Equal superposition
- **Custom:** Arbitrary angles (θ, φ)

#### **Quantum Gates**
- **Pauli:** X, Y, Z (single-qubit)
- **Hadamard:** H (superposition)
- **Rotation:** RX, RY, RZ (arbitrary rotations)
- **CNOT:** Two-qubit entanglement
- **Toffoli:** Three-qubit control

**Example Node:**
```
┌────────────────┐
│  🌀 Hadamard   │
│   |ψ⟩ in       │
└────────────────┘
   ▲
   └── Qubit[1]
```

#### **Measurement**
- **Computational Basis:** Measure in |0⟩/|1⟩
- **Pauli Basis:** X, Y, Z measurements
- **Tomography:** Full state reconstruction

---

### Node Types: DNA / Molecular

#### **Sequence Operations**
- **Codon:** Single amino acid (AUG, GGC, etc.)
- **Sequence:** DNA/RNA chain
- **Motif:** Pattern matching (TATA box, promoter)

#### **Synthesis**
- **Transcription:** DNA → RNA
- **Translation:** RNA → Protein
- **Regulation:** On/Off switch (promoter, terminator)

---

### Node Types: Custom

**Plugin Nodes** (User-defined):
- Can register custom node types
- Drag-drop serialization
- Type validation against schema

---

## ⌨️ KEYBOARD & INPUT

### Tab Navigation

| Action | Key(s) | Behavior |
|--------|--------|----------|
| **Move Focus to Next Node** | `Tab` | Cycle through nodes in creation order |
| **Move Focus to Previous Node** | `Shift+Tab` | Reverse cycle |
| **Select Node** | `Enter` / `Space` | Toggle selection |
| **Multi-Select** | `Shift+Click` or `Shift+Arrow` | Add to selection |
| **Pan Canvas** | `Space+Drag` or `Middle-Mouse+Drag` | Move viewport |
| **Zoom In** | `Ctrl/Cmd++` or `Scroll Up` | 1.2x magnification |
| **Zoom Out** | `Ctrl/Cmd+-` or `Scroll Down` | 0.8x magnification |
| **Fit All Nodes** | `Ctrl/Cmd+Shift+F` | Auto-center canvas |
| **Delete** | `Delete` / `Backspace` | Remove selected nodes/edges |
| **Undo** | `Ctrl/Cmd+Z` | Revert last action |
| **Redo** | `Ctrl/Cmd+Shift+Z` | Replay last action |
| **Open Node Menu** | `Ctrl/Cmd+/` | Quick-access node palette |
| **Connect Mode** | `C` | Draw edge from focused node |
| **Disconnect** | `X` | Remove edge from focused node |
| **Comment** | `Ctrl/Cmd+K` | Add inline comment |
| **Group/Scope** | `Ctrl/Cmd+G` | Create containing scope |
| **Duplicate** | `Ctrl/Cmd+D` | Clone selected node(s) |
| **Execute** | `Ctrl/Cmd+Enter` | Run graph |
| **Stop** | `Esc` | Halt execution |

### Mouse Interactions

| Action | Behavior |
|--------|----------|
| **Click Node** | Select (focus) |
| **Drag Node** | Move with snap-to-grid |
| **Hover Node** | Show tooltip, highlight connected edges |
| **Right-Click Node** | Context menu (copy, delete, rename) |
| **Click-Drag Edge** | Create new connection |
| **Click Edge** | Select edge (show delete button) |
| **Double-Click Node** | Enter edit mode (rename, config) |
| **Scroll Canvas** | Zoom in/out (centered on cursor) |
| **Middle-Drag Canvas** | Pan (hand-grab tool) |

### Touch Interactions (Mobile)

| Action | Behavior |
|--------|----------|
| **Tap Node** | Select |
| **Drag Node** | Move |
| **Long-Press Node** | Context menu |
| **Two-Finger Zoom** | Pinch to scale |
| **Two-Finger Pan** | Slide to move canvas |
| **Edge Taps** | Long-hold, drag to create connection |

---

## ✨ MICROINTERACTIONS

### Connection Validation

**Real-Time Type Checking:**

As you drag an edge toward a target port:
1. **Port Highlight:** Target port pulses (if compatible)
2. **Edge Color:** Green (compatible), Red (incompatible)
3. **Tooltip:** Shows expected type vs. actual type
4. **Snap-On-Drop:** If valid, edge snaps into place with satisfying animate

```
Animation Sequence:
  Edge created → Drag → Near target → Port glows
             → Release → SNAP (spring animation) ✓
                or
             → Release → BOUNCE back to origin ✗
```

### Execution Feedback

**Live Execution Timeline:**

As nodes execute:
1. **Border Glow:** Active node glows (var(--color-primary))
2. **Data Flow:** Edges briefly highlight in execution order
3. **Value Badges:** Show intermediate results (optional)
4. **Timeline Panel:** Sidebar shows execution order + timing

```
Timeline View:
  ┌─────────────────────────────┐
  │ Execution Timeline          │
  ├─────────────────────────────┤
  │ 1. Const(42)        0.2ms   │
  │ 2. Add(A, B)        0.5ms   │
  │ 3. Print(result)    0.1ms   │
  │ ─────────────────────────── │
  │ Total: 0.8ms   ✓ Success    │
  └─────────────────────────────┘
```

### Error Handling

**Visual Error Feedback:**

1. **Node Border:** Turns red, adds error glow
2. **Error Badge:** Shows icon (!) on node
3. **Tooltip:** Hover to see error message
4. **Sidebar Alert:** Detailed error context + fix suggestions

```
Example Error:
  ✗ Type Mismatch at "Add" node
  Expected: (uint32, uint32)
  Got:      (uint32, string)
  
  Suggestion: Cast string to integer using "Parse" node
```

### Hover & Focus States

**Node Hover:**
- Border brightens
- Connected edges highlight
- Tooltip appears (name, type, description)
- Shadow expands (depth effect)

**Edge Hover:**
- Line thickness increases
- Color saturates
- Label shows (if configured)
- Delete button appears (X icon)

---

## 💻 CODE GENERATION

### Output Targets

HyperFlow compiles to multiple targets:

#### **Target 1: HyperCode IR (Intermediate Representation)**

```json
{
  "version": "1.0",
  "metadata": {
    "name": "my_algorithm",
    "author": "Lyndz",
    "created": "2026-01-04T00:00:00Z"
  },
  "nodes": [
    {
      "id": "const_42",
      "type": "Constant",
      "config": { "value": 42, "dataType": "uint32" }
    },
    {
      "id": "add_node",
      "type": "Arithmetic",
      "config": { "operation": "add" }
    }
  ],
  "edges": [
    {
      "from": "const_42",
      "to": "add_node",
      "type": "data"
    }
  ]
}
```

#### **Target 2: Python (Classical)**

```python
def my_algorithm():
    x = 42
    result = x + x
    print(result)
    return result
```

#### **Target 3: Qiskit (Quantum)**

```python
from qiskit import QuantumCircuit, QuantumRegister

qr = QuantumRegister(2, 'q')
circuit = QuantumCircuit(qr)
circuit.h(qr[0])        # Hadamard
circuit.cx(qr[0], qr[1])  # CNOT
circuit.measure(qr, cr)
```

#### **Target 4: OpenQASM (Standard)**

```qasm
OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
h q[0];
cx q[0],q[1];
measure q -> c;
```

#### **Target 5: DNA Design Language (Future)**

```dna
sequence promoter = "TATA";
sequence coding = "ATG...TAA";
component gene = promoter + coding;
```

---

## 🗺️ ROADMAP & MILESTONES

### Phase 1: The Core Spike (MVP) ✅
- [x] **Tech Stack:** React Flow + Rete.js initialized
- [x] **UI Framework:** Vite + Tailwind/Custom CSS
- [x] **Hex Node:** Custom SVG hexagon component with keyboard focus
- [x] **Basic Edges:** Straight + Bezier connections
- [x] **Rete Bridge:** Logic engine connected to visual graph
- [x] **Accessibility:** Keyboard navigation basics (Tab/Enter)
- [x] **Quantum Visuals:** "Wavy" quantum edge type (sine wave SVG)
- [x] **Status:** **COMPLETE**

### Phase 2: The Quantum Leap (v1.1.0) 🚧
- [x] **Qiskit Export:** Transpile graph to Python/Qiskit code
- [x] **Quantum Gates:** X, Z, RX, H, CX, Measure
- [x] **Export UI:** Syntax-highlighted modal with copy-paste
- [ ] **State Vector:** Real-time probability visualization (Chart.js)
- [ ] **Circuit Optimization:** Transpiler pass visualization
- [ ] **Status:** **IN PROGRESS**

### Phase 3: The DNA Strand (v1.2.0)
- [ ] **DNA Nodes:** ATCG sequence builder
- [ ] **Molecular Viewer:** 3D protein preview (ngl.js?)
- [ ] **CRISPR Logic:** "Cut" and "Paste" genome operations
- [ ] **BioPython Export:** Generate valid synthesis scripts

### Phase 4: The Neuro-Interface (v2.0.0)
- [ ] **Brain-Computer Interface:** Mental commands (via EEG mock)
- [ ] **Voice Control:** "Connect node A to B"
- [ ] **Eye Tracking:** Gaze-based selection
- [ ] **Full A11y Audit:** WCAG 2.2 AAA Compliance

---

### Success Metrics

| Metric | Target | Deadline |
|--------|--------|----------|
| **WCAG 2.1 AA Compliance** | 100% | Phase 1 |
| **Keyboard Navigation** | 100% of features | Phase 1 |
| **Execution Speed** | <100ms for graphs <100 nodes | Phase 2 |
| **User Test ADHD Feedback** | ≥90% positive | Phase 3 |
| **Community Plugins** | ≥5 contributions | Phase 4 |
| **Open Source Stars** | ≥500 on GitHub | Phase 4 |

---

## 📚 References & Resources

### Libraries:
- **React Flow:** https://reactflow.dev
- **Rete.js:** https://retejs.org
- **Qiskit:** https://qiskit.org
- **IBM Quantum Composer:** https://quantum.ibm.com

### Accessibility:
- **WCAG 2.1 Guidelines:** https://www.w3.org/WAI/WCAG21/quickref
- **WebAIM Keyboard Access:** https://webaim.org/techniques/keyboard/
- **Accessible Design for ADHD:** Research from Harvard Neurodiversity Initiative

### Design Inspiration:
- **Apple Automator:** Visual workflow builder (macOS)
- **Node-RED:** IoT visual programming
- **Nuke (The Foundry):** VFX node compositor
- **Blender Shader Editor:** Non-linear node interface

---

## ✅ Next Steps

1. **[ ] Prototype Hexagon Node Component** (React Flow custom node)
2. **[ ] Build Adapter Layer** (React Flow ↔ Rete.js bridge)
3. **[ ] Implement Keyboard Navigation** (Tab, Arrow, Enter)
4. **[ ] First Type-Safe Node** (Constant node with Rete.js type system)
5. **[ ] Execution Timeline Widget** (show what runs, in what order)
6. **[ ] Accessibility Audit** (WAVE, Axe, manual keyboard test)

---

**Ready to code, BRO?** 🚀💪

*Last Updated: 2026-01-04*  
*Next Auto-Update: 2026-01-11* (Living document)

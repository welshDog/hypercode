# 🎯 **PHASE 1 DESIGN SPRINT 2: VISUAL SYNTAX DESIGN**
## *Node-Based, Spatial Representation for Neurodivergent Brains*

**Status:** 🟢 ACTIVE SPRINT  
**Duration:** Week 2-3 (Jan 2025)  
**Goal:** Design node-based visual syntax that works for ADHD + spatial thinkers  

---

## 📋 WHY VISUAL SYNTAX?

### **The Spatial Thinking Advantage** [1]

- **ADHD brains are spatial/visual thinkers** — nodes + wires = natural cognition
- **External scaffolding** — reduces mental load (offload to visual cortex)
- **Pattern recognition** — humans excel at spotting spatial relationships
- **Reduced reading load** — dyslexia-friendly (visual, not text-heavy)
- **Experimentation** — rewire nodes faster than edit code

### **The Graph is the Program** [1]

Unlike text-based code where "relationships hide inside syntax," **node-based programming makes relationships VISIBLE.**

```
Text Code:
  data = load("file.csv")
  cleaned = filter(data, lambda x: x > 0)
  result = transform(cleaned, scale_factor=2.0)
  save(result, "output.csv")

Visual Graph:
  [LoadFile] --data--> [Filter] --cleaned--> [Transform] --result--> [SaveFile]
     |                    |                       |
   param:                param:                param:
   "file.csv"          > 0                    2.0
```

**Cognitive difference:** Reading text requires **sequence + memory**. Reading graph requires **pattern recognition**.

---

## 🧪 SPRINT 2 DELIVERABLE: VISUAL SYNTAX SPEC

### **Part A: Node Anatomy**

Every node in HyperCode has the same **consistent structure** (ADHD-friendly):

```
┌──────────────────────────────────┐
│  [Icon] Node Title               │  ← Node name + domain
├──────────────────────────────────┤
│ Inputs:                          │
│  • in_1: Type (semantic color)   │  ← Incoming data
│  • in_2: Type (semantic color)   │
├──────────────────────────────────┤
│ Parameters:                      │
│  value: 42 (slider/input)        │  ← Configuration
│  mode: "fast" (dropdown)         │
├──────────────────────────────────┤
│ Processing [▓▓░░░░░░] (logic)  │
├──────────────────────────────────┤
│ Outputs:                         │
│  • out_1: Type (semantic color)  │  ← Outgoing data
│  • out_2: Type (semantic color)  │
└──────────────────────────────────┘
```

**Consistent Structure Rules:**

1. **Header** = Icon (domain) + Title (clear name)
2. **Inputs** = What comes in (always on left)
3. **Params** = Configuration (always in middle)
4. **Logic** = Processing indicator (visual feedback)
5. **Outputs** = What goes out (always on right)

**Color Coding (Semantic):**

| Color | Meaning | Use Case |
|-------|---------|----------|
| 🔵 Blue | Data/Values | Numbers, strings, objects |
| 🟢 Green | Control Flow | Conditionals, loops |
| 🟠 Orange | Quantum | Qubits, gates, circuits |
| 🟍 Purple | Molecular | DNA strands, reactions |
| 🔴 Red | Errors | Error handling, validation |
| ⬜ Black | Execution | Timing, scheduling |

---

### **Part B: The Node Library (Fundamental Nodes)**

#### **Classical Domain Nodes**

**1. Input Node** (Load data)
```
┌─────────────┐
│ [📊] Input          │
├─────────────┤
│ Outputs:            │
│  • value: Any       │  🔵
└─────────────┘

Purpose: User input, file load, API call
```

---

### **Part C: Interaction Model (How Users Manipulate Graphs)**

#### **Creating a Node**

1. **Right-click on canvas** → "Add Node"
2. **Search/filter by domain** (Classical, Quantum, Molecular)
3. **Click to place** on canvas
4. **Auto-connection** (smart wire to nearest output)

#### **Connecting Nodes**

1. **Click node output** → turns into "connect mode"
2. **Click target node input** → wire drawn
3. **Wire color auto-matched** (data type check)
4. **Invalid connections rejected** (with helpful error)

#### **Configuring Nodes**

1. **Click node** → sidebar shows parameters
2. **Sliders, dropdowns, text fields**
3. **Real-time validation** (errors shown immediately)
4. **Undo/Redo** every change

#### **Viewing Execution**

1. **Play button** → runs graph
2. **Data flows along wires** → animated
3. **Node progress indicators** → shows which running
4. **Output shown in-place** (or in side panel)

---

## ✅ DESIGN VALIDATION

### **Neurodivergent-Friendly:**
- [ ] **No text walls** ✓ (visual-first)
- [ ] **Consistent node structure** ✓ (same layout for all)
- [ ] **Semantic color coding** ✓ (blue=data, green=control, etc.)
- [ ] **Spatial layout** ✓ (left→right flow natural)
- [ ] **Minimal symbols** ✓ (only icons for clarity)

### **ADHD-Friendly (Spatial):**
- [ ] **Expandable/collapsible subgraphs** ✓ (manage complexity)
- [ ] **Clear data flow** ✓ (wires show relationships)
- [ ] **Immediate feedback** ✓ (play button, animations)
- [ ] **Low cognitive load** ✓ (visual, not text)

### **Multi-Domain Support:**
- [ ] **Classical nodes present** ✓
- [ ] **Quantum nodes present** ✓
- [ ] **Molecular nodes present** ✓
- [ ] **Easy to identify** ✓ (domain icons, color)

---

**SPRINT 2 STATUS: 🟢 VISUAL SYNTAX COMPLETE**

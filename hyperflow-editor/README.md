# 🎨 HyperFlow: Visual Node Graph Editor

**Version:** 1.2.0-beta (Neuro-Accessibility Update)
**Status:** Stable / Active Development
**Stack:** React 19 + TypeScript 5.9 + Vite 6 + React Flow

## 🧠 Overview

HyperFlow is the visual interface for **The HyperCode**, designed to be a **Neurodivergent-First**, **Two-Mode Science Console**. It visualizes invisible logic—whether it's the superposition of a qubit or the sticky ends of DNA.

---

### 🔥 What's New in v1.2?
*   **🧘 Zen Mode**: A specialized ADHD-friendly viewport that reduces visual noise and focuses on single-sequence flows. Toggle with `Shift + Z`.
*   **☁️ Cloud Sync (Beta)**: Real-time auto-save with visual status indicators. Never lose your flow state again.
*   **🧪 Cloning Preset**: A dedicated "Cut & Paste" workbench for molecular biology workflows.
*   **⌨️ Power User Shortcuts**: Navigate the editor without lifting your hands from the keyboard.

---

### 🌟 Core Modules

#### 1. ⚛️ Quantum Mode (Qiskit-Native)
*   **Visual Qubits**: Wavy edges represent quantum states.
*   **Gates**: Biomimetic hexagonal nodes (H, CNOT, RX, Measure).
*   **Export**: Generates valid Python `qiskit` code.

#### 2. 🧬 Bio Mode (Molecular Cloning)
*   **Central Dogma**: Transcription (DNA → RNA) and Translation (RNA → Protein) with real codon tables.
*   **Restriction Enzymes**: EcoRI, BamHI, and HindIII logic with accurate motif recognition (`GAATTC`, `GGATCC`, `AAGCTT`) and sticky-end visualization.
*   **Ligation Engine**: A "Cut & Paste" simulator that enforces biological rules (matching overhangs) and supports both linear and circular (plasmid) ligation.

---

## 🚀 Getting Started

1.  **Install Dependencies:**
    ```bash
    npm install
    ```

2.  **Start Development Server:**
    ```bash
    npm run dev
    ```

3.  **Explore Presets:**
    *   **🧘 Zen Mode**: Experience the neuro-friendly UI.
    *   **🧪 Cloning**: Build recombinant DNA plasmids.
    *   **⚛️ Quantum**: Design quantum circuits.

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action | Context |
| :--- | :--- | :--- |
| `Shift + Z` | **Toggle Zen Mode** | Switches to low-stimulation preset |
| `Shift + F` | **Toggle Hyperfocus** | Dims non-selected nodes |
| `Ctrl + S` | **Save Flow** | Manually trigger save (Auto-save is on) |
| `Ctrl + O` | **Open Flow** | Load JSON file |
| `Ctrl + 0` | **Reset View** | Fit graph to screen |

---

## 🏗️ Architecture

*   **/src/nodes**: Custom React Flow nodes.
    *   `EnzymeNode`: Handles motif search and fragment generation.
    *   `LigaseNode`: Handles fragment selection, overhang matching, and circularization.
    *   `SequenceNode`: The "Source of Truth" for DNA data.
    *   `PCRNode`: Simulates thermocycling, annealing, and extension.
*   **/src/edges**: Custom edge visualizations.
    *   `HelixEdge`: Animated DNA double helix style.
    *   `QuantumEdge`: Wavy superposition style.
*   **/src/engine**: Logic layer.
    *   `BioTypes.ts`: The taxonomy for DNA/RNA/Protein data contracts.
    *   `presets.ts`: Serialized scenes for instant context switching.
*   **/src/storage**: Data persistence layer.
    *   `SupabaseStorageProvider.ts`: Real-time cloud sync with Supabase.
    *   `MockCloudStorageProvider.ts`: Simulates cloud latency and sync states (Fallback).

## 🧪 Documentation

*   [**Supabase Setup**](SUPABASE_SETUP.md): Instructions for enabling real cloud sync.
*   [**Design Notes**](docs/DESIGN_NOTES.md): Deep dive into the decision-making process, architecture, and "future-you" context.
*   [**Demo Walkthrough**](docs/DEMO_WALKTHROUGH.md): A step-by-step script for demonstrating the Molecular Cloning workflow.
*   [**Project Health Report**](PROJECT_HEALTH_REPORT.md): Current status and vitals of the codebase.

## 🔮 Roadmap

*   [x] **Phase 1:** Hexagon Node Rendering (React Flow)
*   [x] **Phase 2:** Quantum Edge Visualization
*   [x] **Phase 3:** Central Dogma & Restriction Enzymes
*   [x] **Phase 4:** Ligation & Plasmid Circularization
*   [x] **Phase 4.5:** Accessibility (Zen Mode, Shortcuts) & Cloud Sync
*   [ ] **Phase 5:** PCR Amplification (Primer Design)
*   [ ] **Phase 6:** CRISPR/Cas9 Editing

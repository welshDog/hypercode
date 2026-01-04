# 🎨 HyperFlow: Visual Node Graph Editor

**Version:** 1.1.0 (Gold Master - Bio-Pack Module)
**Status:** Stable / Active Development
**Stack:** React + TypeScript + Vite + React Flow

## 🧠 Overview

HyperFlow is the visual interface for **The HyperCode**, designed to be a **Neurodivergent-First**, **Two-Mode Science Console**. It visualizes invisible logic—whether it's the superposition of a qubit or the sticky ends of DNA.

### 🌟 Core Modules

#### 1. ⚛️ Quantum Mode (Qiskit-Native)
*   **Visual Qubits**: Wavy edges represent quantum states.
*   **Gates**: Biomimetic hexagonal nodes (H, CNOT, RX, Measure).
*   **Export**: Generates valid Python `qiskit` code.

#### 2. 🧬 Bio Mode (Molecular Cloning)
*   **Central Dogma**: Transcription (DNA → RNA) and Translation (RNA → Protein) with real codon tables.
*   **Restriction Enzymes**: EcoRI, BamHI, and HindIII logic with accurate motif recognition (`GAATTC`, `GGATCC`, `AAGCTT`) and sticky-end visualization.
*   **Ligation Engine**: A "Cut & Paste" simulator that enforces biological rules (matching overhangs) and supports both linear and circular (plasmid) ligation.

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
    *   Select **Quantum Circuit Demo** to build qubits.
    *   Select **Central Dogma Demo** to transcribe/translate.
    *   Select **Restriction Enzyme Demo** to cut and ligate DNA.

## 🏗️ Architecture

*   **/src/nodes**: Custom React Flow nodes.
    *   `EnzymeNode`: Handles motif search and fragment generation.
    *   `LigaseNode`: Handles fragment selection, overhang matching, and circularization.
    *   `SequenceNode`: The "Source of Truth" for DNA data.
*   **/src/edges**: Custom edge visualizations.
    *   `HelixEdge`: Animated DNA double helix style.
    *   `QuantumEdge`: Wavy superposition style.
*   **/src/engine**: Logic layer.
    *   `BioTypes.ts`: The taxonomy for DNA/RNA/Protein data contracts.
    *   `presets.ts`: Serialized scenes for instant context switching.

## 🧪 Documentation

*   [**Design Notes**](docs/DESIGN_NOTES.md): Deep dive into the decision-making process, architecture, and "future-you" context.
*   [**Demo Walkthrough**](docs/DEMO_WALKTHROUGH.md): A step-by-step script for demonstrating the Molecular Cloning workflow.

## 🔮 Roadmap

*   [x] **Phase 1:** Hexagon Node Rendering (React Flow)
*   [x] **Phase 2:** Quantum Edge Visualization
*   [x] **Phase 3:** Central Dogma & Restriction Enzymes
*   [x] **Phase 4:** Ligation & Plasmid Circularization
*   [ ] **Phase 5:** PCR Amplification (Primer Design)
*   [ ] **Phase 6:** CRISPR/Cas9 Editing

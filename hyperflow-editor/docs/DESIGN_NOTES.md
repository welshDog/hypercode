# 🧪 Design Notes: HyperFlow Bio-Pack

**Date:** January 4, 2026
**Status:** Gold Master (1.1.0)
**Module:** Molecular Cloning (Restriction/Ligation)

## 🎯 Core Philosophy: "Visual Cloning Bench"

The goal was to transform the abstract, often confusing process of molecular cloning (cutting and pasting DNA) into a tangible, reactive visual experience. We moved away from text-based sequence manipulation to a **node-based flow** where biological rules are enforced by the connection logic.

### Neurodivergent-First Principles
*   **Visual Feedback > Text**: Instead of reading coordinates, users *see* the cut site move. Instead of calculating complementary ends, users *see* the node pulse green (match) or red (mismatch).
*   **Reduced Cognitive Load**: The "Scene" system (Presets) allows instant context switching between Quantum and Bio modes, preventing tool fatigue.
*   **Safe Failure**: Errors (like incompatible sticky ends) are explicit, non-destructive, and educational ("Mismatch: GATC vs AATT").

## 🏗️ Technical Architecture

### 1. The Data Contract (`BioTypes.ts`)
We established a strict taxonomy for biological data flowing between nodes. This is the "nervous system" of the editor.

```typescript
export interface EnzymeNodeData extends BioNodeData {
  enzyme: string; // e.g., 'EcoRI'
  mode: 'first' | 'all';
  fragments: { 
    seq: string; 
    leftOverhang?: string; // e.g., 'AATT'
    rightOverhang?: string; 
  }[];
}

export interface LigaseNodeData extends BioNodeData {
  selectedLeftFragmentIndex: number | null;
  selectedRightFragmentIndex: number | null;
  ligatedSequence: string;
  circular?: boolean; // Toggles plasmid logic
}
```

*   **Why this matters**: Explicitly tracking `overhang` strings means the `LigaseNode` doesn't need to know *which* enzyme was used—it only cares if the sticky ends match. This makes the system scalable to *any* future enzyme without rewriting the Ligase logic.

### 2. The Enzyme Engine (`EnzymeNode.tsx`)
*   **Dictionary Lookup**: We use a `Record` object to store enzyme motifs and cut rules. Adding a new enzyme is as simple as adding one line to this object.
*   **Reactive Computation**: The node listens to upstream `SequenceNode` changes. If the source DNA changes, the enzyme instantly re-cuts.
*   **Pulse Animation**: A CSS `box-shadow` animation triggers on data changes, giving the user a "heartbeat" confirmation that the logic ran.

### 3. The Ligation Logic (`LigaseNode.tsx`)
*   **Linear Ligation**: Checks if `LeftFragment.rightOverhang === RightFragment.leftOverhang`.
*   **Circular Ligation**: Checks the above *plus* `RightFragment.rightOverhang === LeftFragment.leftOverhang`.
*   **UX**: Uses native HTML `<select>` elements populated dynamically from the upstream fragment list. This connects the output of one node directly to the UI controls of the next.

## 🔮 Future-You Context

### Next Steps: PCR & CRISPR
The infrastructure is ready for:
*   **PCRNode**: Needs to take a `template` (from SequenceNode) and two `primer` strings. Logic: Find primer binding sites, extract the region between them.
*   **Cas9Node**: Needs `gRNA` input. Logic: Find PAM site (`NGG`) + matching 20bp upstream. Output: Cut site or mutation.

### Scalability Considerations
*   **Performance**: Currently, we re-calculate cuts on every render/update. For massive genomes (>10kb), we should move this calculation to a Web Worker or memoize heavily.
*   **State Management**: We are relying on React Flow's `data` object. If the graph gets huge, we might need a dedicated state manager (Zustand/Redux) external to React Flow, but for now, this "local data flow" is clean and sufficient.

---
*Built with 🧬 & ⚛️ by The HyperCode Team*

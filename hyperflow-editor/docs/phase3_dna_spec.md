# 🧬 Phase 3: The DNA Strand - Design Specification
**Codename:** HelixFlow  
**Version:** 0.1.0-DRAFT  
**Status:** In Design  

---

## 1. Vision & Philosophy
Phase 3 expands HyperFlow from silicon (Quantum/Classical) to carbon (Biological). We treat genetic code not as static text, but as **executable logic**. 

### The Core Metaphor
- **DNA = Data:** Streams of A, T, C, G.
- **Enzymes = Functions:** Polymerases, Ligases, and CRISPR-Cas9 are operators that manipulate the data stream.
- **Cells = Scopes:** Containerization for logic.

### Neurodivergent-First Principles
- **Pattern Recognition:** DNA sequences are visually chunked (codons) and color-coded.
- **Error Safety:** "Sticky ends" in cloning are visualized as puzzle pieces—incompatible overhangs physically won't connect.
- **Sensory Feedback:** "Unzipping" animations when transcribing; satisfying "snap" when ligating.

---

## 2. Component Taxonomy

### 2.1 New Node Types (The "Bio-Pack")

#### 🧬 Sequence Source
- **Input:** Raw string or FASTA file.
- **Visual:** Shows the sequence as a double-helix strip.
- **Validation:** Auto-rejects non-ATCG characters (unless IUPAC ambiguity codes are enabled).
- **Properties:** Length, GC-content %.

#### ✂️ Restriction Enzyme (The "Cutter")
- **Input:** DNA Sequence.
- **Config:** Select enzyme (e.g., EcoRI, BamHI) or custom motif.
- **Visual:** Scissor icon. Shows the specific cut site pattern (e.g., `G^AATTC`).
- **Output:** Two DNA fragments (Left, Right).

#### 🔗 Ligase (The "Gluer")
- **Input:** Two DNA fragments.
- **Logic:** Checks if overhangs match (sticky ends).
- **Visual:** DNA strands fusing together.
- **Output:** Concatenated sequence.

#### 🦠 CRISPR-Cas9 (The "Editor")
- **Input:** Target Genome, gRNA Sequence.
- **Logic:** Finds match -> Cuts -> Inserts Template (optional).
- **Visual:** Cas9 protein blob "scanning" the strand.

#### 🧪 Central Dogma (The "Converter")
- **Transcriber:** DNA → RNA (T → U).
- **Translator:** RNA → Protein (Codons → Amino Acids).
- **Visual:** Animation of the strand changing structure.

### 2.2 New Edge Types
- **Double Helix Edge:** Two intertwined sine waves (expanding on the Quantum "Wavy" edge).
- **mRNA Edge:** Single strand, jittery animation.
- **Peptide Bond:** Rigid, chain-link style for amino acids.

---

## 3. Visualization & UX

### 3.1 The "Codon View"
Instead of a wall of text:
```text
ATGCGTACT...
```
We display:
```text
[ATG] [CGT] [ACT] ...
 Met   Arg   Thr
```
*Why?* Reduces cognitive load. Grouping by 3s matches the biological reality of translation.

### 3.2 3D Molecular Preview
- **Integration:** `ngl.js` or `RCSB Molstar`.
- **Function:** When a Protein node is selected, fetch/predict its structure.
- **Fallback:** For novel sequences, show a simplified "beads on a string" 3D model.

### 3.3 Color Accessibility
Standard bio-colors (A=Green, T=Red etc.) are bad for colorblindness.
- **HyperFlow Solution:** Shape + Color.
    - **A:** Green Circle
    - **T:** Red Triangle
    - **C:** Blue Square
    - **G:** Yellow Star

---

## 4. Technical Architecture

### 4.1 Data Structure
New `NodeData` interface extension:
```typescript
interface BioNodeData extends NodeData {
  sequence: string; // "ATCG..."
  type: 'DNA' | 'RNA' | 'PROTEIN';
  meta: {
    overhang?: string; // For sticky ends
    circular?: boolean; // Plasmid support
  }
}
```

### 4.2 Export Targets
- **BioPython:** Generate `.py` scripts using `Bio.Seq`.
- **FASTA/GenBank:** Standard file export.
- **Benchling:** (Stretch Goal) API integration to push plasmids to lab notebook.

---

## 5. Implementation Roadmap

### Sprint 1: The Backbone
- [ ] Create `HelixEdge` (SVG double helix animation).
- [ ] Implement `SequenceNode` with regex validation.
- [ ] Add `BioPythonExporter` skeleton.

### Sprint 2: The Dogma
- [ ] Implement `TranscribeNode` and `TranslateNode`.
- [ ] Add `CodonView` visualizer to node output.

### Sprint 3: The Lab
- [ ] Implement `RestrictionEnzyme` logic (substring matching).
- [ ] Add `CRISPR` search-and-replace logic.
- [ ] Integrate `ngl.js` for basic PDB viewing.

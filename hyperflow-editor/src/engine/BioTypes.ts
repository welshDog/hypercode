// 🧬 HyperFlow Bio-Pack Taxonomy
// Version: 1.1.0-GOLD (Molecular Cloning Module)

export type BioSequenceType = 'DNA' | 'RNA' | 'PROTEIN';

export interface BioNodeData {
  label: string;
  type: BioSequenceType;
  sequence?: string; // The actual string (e.g., "ATGC...")
  isValid?: boolean;
  meta?: {
    overhang?: string; // For sticky ends
    enzymeName?: string; // For restriction sites
    circular?: boolean; // For plasmids
  };
}

// --- Node Specific Interfaces ---

// 1. Sequence Source Node
// Input: None (User types string)
// Output: DNA Sequence
export interface SequenceNodeData extends BioNodeData {
  type: 'DNA';
  sequence: string;
  length: number;
  gcContent: number; // 0.0 to 1.0
}

// 2. Transcribe Node (Central Dogma Step 1)
// Input: DNA
// Output: RNA
export interface TranscribeNodeData extends BioNodeData {
  type: 'RNA';
  isCodingStrand: boolean; // Default true
}

// 3. Translate Node (Central Dogma Step 2)
// Input: RNA
// Output: PROTEIN
export interface TranslateNodeData extends BioNodeData {
  type: 'PROTEIN';
  codonTable: 'Standard' | 'Mitochondrial';
}

// 4. Enzyme Node (Cutter)
// Input: DNA
// Output: DNA Fragment (Left), DNA Fragment (Right)
export interface EnzymeNodeData extends BioNodeData {
  type: 'DNA';
  enzyme: string;
  mode: 'first' | 'all';
  sites: number[];
  fragments: { seq: string; leftOverhang?: string; rightOverhang?: string }[];
}

// 5. Ligase Node (Gluer)
// Input: Two selected fragments from upstream
// Output: Concatenated DNA
// Logic: Checks sticky-end compatibility for both Linear and Circular ligation
export interface LigaseNodeData extends BioNodeData {
  type: 'DNA';
  selectedLeftFragmentIndex: number | null;
  selectedRightFragmentIndex: number | null;
  ligatedSequence: string;
  circular?: boolean; // Toggles plasmid closure check
  errorMessage?: string;
}

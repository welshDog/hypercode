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

// 3.5. [REMOVED DUPLICATE]


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

// 6. PCR Node (Amplifier)
// Input: Template DNA
// Params: Forward Primer, Reverse Primer
// Output: Amplified DNA (Amplicon)
export interface PCRNodeData extends BioNodeData {
  type: 'DNA';
  forwardPrimer: string;
  reversePrimer: string;
  amplicon: string;
  forwardTm: number;
  reverseTm: number;
  annealingTemp: number;
  error?: string; // e.g. "Primers not found"
}

// 7. CRISPR Node (Editor)
// Input: Target DNA
// Params: sgRNA, PAM, Repair Template (optional)
// Output: Edited DNA
export interface CRISPRNodeData extends BioNodeData {
  message: string;
  type: 'DNA';
  guideRNA: string;
  pam: string; // e.g., "NGG"
  repairMode: 'NHEJ' | 'HDR';
  repairTemplate: string; // Used if mode is HDR
  cutIndex: number | null; // -1 or null if no cut
  editedSequence: string;
  status: 'scanning' | 'cut' | 'repaired' | 'error';
}

// 8. Golden Gate Assembly Node
// Input: Multiple DNA parts
// Params: Enzyme (BsaI, BbsI, etc.)
// Output: Assembled Plasmid/Linear Construct
export interface GoldenGateNodeData extends BioNodeData {
  type: 'DNA';
  enzyme: 'BsaI' | 'BbsI' | 'BsmBI';
  assemblyResult: string;
  parts: { id: string; name: string; sequence: string; overhangs: { left: string; right: string } }[];
  isCircular: boolean;
  error?: string;
  errorMessage?: string;
}

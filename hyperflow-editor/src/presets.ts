import { type Node, type Edge } from 'reactflow';
import { type QiskitNodeData } from './engine/QiskitExporter';
import { type EnzymeNodeData, type LigaseNodeData, type SequenceNodeData, type TranscribeNodeData, type TranslateNodeData, type PCRNodeData, type CRISPRNodeData, type GoldenGateNodeData } from './engine/BioTypes';

export interface Preset {
  name: string;
  nodes: Node[];
  edges: Edge[];
}

export const PCR_PRESET: Preset = {
  name: 'PCR Amplification Demo',
  nodes: [
    {
      id: 'template-dna',
      type: 'sequence',
      position: { x: 100, y: 200 },
      data: {
        label: 'Template DNA',
        type: 'DNA',
        sequence: 'ATGCGTACGTAGCTAGCT', // Simple template
        isValid: true
      } as SequenceNodeData
    },
    {
      id: 'pcr-node',
      type: 'pcr',
      position: { x: 500, y: 200 },
      data: {
        label: 'PCR Thermocycler',
        type: 'DNA',
        forwardPrimer: 'ATGC',
        reversePrimer: 'AGCT',
        annealingTemp: 55,
        forwardTm: 0,
        reverseTm: 0,
        amplicon: '',
        error: '',
        isValid: true
      } as PCRNodeData
    }
  ],
  edges: [
    { id: 'e-template-pcr', source: 'template-dna', target: 'pcr-node', type: 'helix', animated: true }
  ]
};

export const CRISPR_PRESET: Preset = {
  name: 'CRISPR-Cas9 Editing',
  nodes: [
    {
      id: 'target-dna',
      type: 'sequence',
      position: { x: 100, y: 200 },
      data: {
        label: 'Target Genome',
        type: 'DNA',
        sequence: 'ATGCGTACGTAGCTAGCTNGG', // Includes PAM
        isValid: true
      } as SequenceNodeData
    },
    {
      id: 'crispr-node',
      type: 'crispr',
      position: { x: 500, y: 200 },
      data: {
        label: 'Cas9 System',
        type: 'DNA',
        guideRNA: '',
        pam: 'NGG',
        repairMode: 'NHEJ',
        repairTemplate: '',
        editedSequence: '',
        cutIndex: -1,
        status: 'scanning',
        isValid: true
      } as CRISPRNodeData
    }
  ],
  edges: [
    { id: 'e-dna-crispr', source: 'target-dna', target: 'crispr-node', type: 'helix', animated: true }
  ]
};

export const QUANTUM_PRESET: Preset = {
  name: 'Quantum Circuit Demo',
  nodes: [
    {
      id: 'init-q',
      type: 'init',
      position: { x: 50, y: 50 },
      data: { label: 'q = QReg(2)' }
    },
    {
      id: 'init-c',
      type: 'init',
      position: { x: 50, y: 150 },
      data: { label: 'c = CReg(2)' }
    },
    {
      id: 'h-node',
      type: 'gate',
      position: { x: 300, y: 50 },
      data: { label: 'H', gateType: 'H', target: 'q[0]' }
    },
    {
      id: 'cx-node',
      type: 'gate',
      position: { x: 450, y: 100 },
      data: { label: 'CX', gateType: 'CX', control: 'q[0]', target: 'q[1]' }
    },
    {
      id: 'measure-0',
      type: 'measure',
      position: { x: 600, y: 50 },
      data: { label: 'Measure q[0]', qubit: 'q[0]', target: 'c[0]' }
    },
    {
      id: 'measure-1',
      type: 'measure',
      position: { x: 600, y: 150 },
      data: { label: 'Measure q[1]', qubit: 'q[1]', target: 'c[1]' }
    }
  ],
  edges: [
    // Visual connections for flow (logic handled by compiler)
    { id: 'e1', source: 'init-q', target: 'h-node', type: 'quantum' },
    { id: 'e2', source: 'h-node', target: 'cx-node', type: 'quantum' },
    { id: 'e3', source: 'cx-node', target: 'measure-0', type: 'quantum' },
    { id: 'e4', source: 'cx-node', target: 'measure-1', type: 'quantum' }
  ]
};

export const CENTRAL_DOGMA_PRESET: Preset = {
  name: 'Central Dogma Demo',
  nodes: [
    {
      id: 'dna-source',
      type: 'sequence',
      position: { x: 100, y: 200 }, // Centered slightly better
      data: {
        label: 'DNA Source',
        type: 'DNA',
        sequence: 'ATGCGTACGTAGCTAGCT',
        isValid: true
      } as SequenceNodeData
    },
    {
      id: 'transcribe-node',
      type: 'transcribe',
      position: { x: 500, y: 200 },
      data: {
        label: 'Transcribe',
        type: 'RNA',
        sequence: '', // Will be populated by dataflow
        isValid: true
      } as TranscribeNodeData
    },
    {
      id: 'translate-node',
      type: 'translate',
      position: { x: 900, y: 200 },
      data: {
        label: 'Translate',
        type: 'PROTEIN',
        sequence: '', // Will be populated by dataflow
        isValid: true
      } as TranslateNodeData
    }
  ],
  edges: [
    { id: 'e-dna-transcribe', source: 'dna-source', target: 'transcribe-node', type: 'helix', animated: false },
    { id: 'e-transcribe-translate', source: 'transcribe-node', target: 'translate-node', type: 'helix', animated: false }
  ]
};

export const RESTRICTION_ENZYME_PRESET: Preset = {
  name: 'Restriction Enzyme Demo',
  nodes: [
    {
      id: 'dna-source',
      type: 'sequence',
      position: { x: 100, y: 200 },
      data: {
        label: 'Viral DNA',
        type: 'DNA',
        sequence: 'GAATTC', // EcoRI site
        isValid: true
      } as SequenceNodeData
    },
    {
      id: 'enzyme-node',
      type: 'enzyme',
      position: { x: 400, y: 200 },
      data: {
        label: 'EcoRI',
        type: 'DNA',
        enzyme: 'EcoRI',
        mode: 'all',
        sites: [],
        fragments: [],
        isValid: true
      } as unknown as EnzymeNodeData
    }
  ],
  edges: [
    { id: 'e1', source: 'dna-source', target: 'enzyme-node', type: 'helix', animated: true }
  ]
};

export const ZEN_MODE_PRESET: Preset = {
  name: 'Zen Mode (Empty)',
  nodes: [],
  edges: []
};

export const GOLDEN_GATE_PRESET: Preset = {
  name: 'Golden Gate Assembly (BsaI)',
  nodes: [
    {
      id: 'promoter',
      type: 'sequence',
      position: { x: 50, y: 100 },
      data: {
        label: 'Promoter (Part 1)',
        type: 'DNA',
        // GGTCTC (BsaI) + A (Spacer) + GGAG (Overhang) + [PROMOTER] + TACT (Overhang) + A + GAGACC (BsaI Rev)
        sequence: 'GGTCTCAGGAGTTGACAGCTAGCTCAGTCCTAGGTATAATGCTAGCTACTAGAGACC',
        isValid: true
      } as SequenceNodeData
    },
    {
      id: 'rbs-cds',
      type: 'sequence',
      position: { x: 50, y: 300 },
      data: {
        label: 'RBS+GFP (Part 2)',
        type: 'DNA',
        // GGTCTC A TACT (Match Prev) + [RBS+CDS] + AATG (Next) + A GAGACC
        sequence: 'GGTCTCATACTAAAGAGGAGAAATACTAGATGCGTAAAGGAGAAGAACTTTTCACTGGAGTTGTCCAATAAATGGAGACC',
        isValid: true
      } as SequenceNodeData
    },
    {
      id: 'terminator',
      type: 'sequence',
      position: { x: 50, y: 500 },
      data: {
        label: 'Terminator (Part 3)',
        type: 'DNA',
        // GGTCTC A AATG (Match Prev) + [TERM] + GCGC (End) + A GAGACC
        sequence: 'GGTCTCAAATGCCAGGCATCAAATAAAACGAAAGGCTCAGTCGAAAGACTGGGCCTTTCGTTTTATCTGTTGTTTGTCGGTGAACGCTCTCTACTAGAGTCACACTGGCTCACCTTCGGGTGGGCCTTTCTGCGTTTATAGAGACC',
        isValid: true
      } as SequenceNodeData
    },
    {
      id: 'gg-node',
      type: 'goldengate',
      position: { x: 500, y: 300 },
      data: {
        label: 'Golden Gate Assembly',
        type: 'DNA',
        enzyme: 'BsaI',
        parts: [],
        assemblyResult: '',
        isCircular: true,
        isValid: true
      } as GoldenGateNodeData
    }
  ],
  edges: [
    { id: 'e1', source: 'promoter', target: 'gg-node', type: 'helix', animated: true },
    { id: 'e2', source: 'rbs-cds', target: 'gg-node', type: 'helix', animated: true },
    { id: 'e3', source: 'terminator', target: 'gg-node', type: 'helix', animated: true }
  ]
};

export const CLONING_PRESET: Preset = {
  name: 'Molecular Cloning Demo',
  nodes: [
    {
      id: 'dna-source',
      type: 'sequence',
      position: { x: 100, y: 300 },
      data: {
        label: 'DNA Source',
        type: 'DNA',
        sequence: 'TTTGAATTCTTTGGATCCTTTAAGCTT', // EcoRI, BamHI, HindIII sites
        isValid: true,
        length: 27,
        gcContent: 0
      } as SequenceNodeData
    },
    {
      id: 'enzyme-node',
      type: 'enzyme',
      position: { x: 500, y: 300 },
      data: {
        label: 'Restriction Enzyme',
        type: 'DNA',
        enzyme: 'EcoRI',
        mode: 'all',
        sites: [],
        fragments: [],
        isValid: true
      } as EnzymeNodeData
    },
    {
      id: 'ligase-node',
      type: 'ligase',
      position: { x: 900, y: 300 },
      data: {
        label: 'Ligase',
        type: 'DNA',
        selectedLeftFragmentIndex: null,
        selectedRightFragmentIndex: null,
        ligatedSequence: '',
        isValid: true
      } as LigaseNodeData
    }
  ],
  edges: [
    { id: 'e-dna-enzyme', source: 'dna-source', target: 'enzyme-node', type: 'helix', animated: false },
    { id: 'e-enzyme-ligase', source: 'enzyme-node', target: 'ligase-node', type: 'helix', animated: false }
  ]
};

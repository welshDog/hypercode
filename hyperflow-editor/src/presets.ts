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
      id: 'h-node',
      type: 'hex',
      position: { x: 100, y: 100 },
      data: { label: 'H (Q0)', op: 'h', qubitIndex: 0 } as QiskitNodeData
    },
    {
      id: 'cx-node',
      type: 'hex',
      position: { x: 300, y: 150 },
      data: { label: 'CNOT', op: 'cx', controlIndex: 0, targetIndex: 1 } as QiskitNodeData
    },
    {
      id: 'x-node',
      type: 'hex',
      position: { x: 500, y: 250 },
      data: { label: 'X (Q1)', op: 'x', qubitIndex: 1 } as QiskitNodeData
    },
    {
      id: 'rx-node',
      type: 'hex',
      position: { x: 500, y: 50 },
      data: { label: 'RX(π/2)', op: 'rx', qubitIndex: 0, theta: 'np.pi/2' } as QiskitNodeData
    },
    {
      id: 'measure-node',
      type: 'hex',
      position: { x: 700, y: 150 },
      data: { label: 'Measure', op: 'measure', qubitIndex: 0 } as QiskitNodeData
    }
  ],
  edges: [
    { id: 'e1', source: 'h-node', target: 'cx-node', type: 'quantum', animated: false },
    { id: 'e2', source: 'cx-node', target: 'x-node', type: 'quantum', animated: false },
    { id: 'e3', source: 'cx-node', target: 'rx-node', type: 'quantum', animated: false },
    { id: 'e4', source: 'rx-node', target: 'measure-node', type: 'quantum', animated: false }
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

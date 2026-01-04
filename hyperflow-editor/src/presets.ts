import { type Node, type Edge } from 'reactflow';
import { type QiskitNodeData } from './engine/QiskitExporter';
import { type EnzymeNodeData, type LigaseNodeData, type SequenceNodeData, type TranscribeNodeData, type TranslateNodeData } from './engine/BioTypes';

export interface Preset {
  name: string;
  nodes: Node[];
  edges: Edge[];
}

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
  name: 'Zen Mode (ADHD Friendly)',
  nodes: [
    {
      id: 'zen-dna',
      type: 'sequence',
      position: { x: 400, y: 300 },
      data: {
        label: 'Focus Sequence',
        type: 'DNA',
        sequence: 'ATG',
        isValid: true
      } as SequenceNodeData
    }
  ],
  edges: []
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

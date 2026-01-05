# VIS4: Advanced DNA Ops — Transcription Node Implementation

## Objective
Add **Transcription** as your first Advanced DNA Op node type to HyperFlow.  
Converts DNA → RNA in the Bio-Logic workflow.

---

## Phase 1: Node Type Definition (15 min)

### 1.1 Create `Transcription.ts` Node Component

**Location:** `hyperflow-editor/src/nodes/bio/Transcription.tsx`

```typescript
import React, { useCallback } from 'react';
import { Handle, Position, useUpdateNodeInternals } from 'reactflow';
import { nodeStyles, handleConfig } from '../styles';

interface TranscriptionNodeData {
  dnaSequence?: string;
  rnaBases?: string;
  strand?: 'forward' | 'reverse';
  status?: 'idle' | 'processing' | 'complete' | 'error';
}

export function TranscriptionNode({ data }: { data: TranscriptionNodeData }) {
  const updateNodeInternals = useUpdateNodeInternals();

  const handleStrandChange = useCallback(
    (e: React.ChangeEvent<HTMLSelectElement>) => {
      data.strand = e.target.value as 'forward' | 'reverse';
      updateNodeInternals(data.id);
    },
    [data, updateNodeInternals]
  );

  // Simplified transcription logic: DNA → RNA
  // DNA: A→U, T→A, G→C, C→G (on reverse strand, then flip)
  const transcribe = (dna: string) => {
    if (!dna) return '';
    let rna = dna
      .toUpperCase()
      .replace(/A/g, 'U') // A→U in RNA
      .replace(/T/g, 'A')
      .replace(/G/g, 'C')
      .replace(/C/g, 'G');
    if (data.strand === 'reverse') {
      rna = rna.split('').reverse().join('');
    }
    return rna;
  };

  const rnaOutput = data.dnaSequence ? transcribe(data.dnaSequence) : '';

  return (
    <div style={nodeStyles.bioNode}>
      <Handle type="target" position={Position.Top} {...handleConfig} />
      
      <div style={{ padding: '8px', fontWeight: 'bold', fontSize: '12px' }}>
        🧬 Transcription
      </div>

      <div style={{ padding: '4px 8px', fontSize: '11px' }}>
        <label>
          Strand:
          <select value={data.strand || 'forward'} onChange={handleStrandChange} style={{ marginLeft: '4px', fontSize: '10px' }}>
            <option value="forward">Forward</option>
            <option value="reverse">Reverse</option>
          </select>
        </label>
      </div>

      <div style={{ 
        padding: '6px 8px', 
        backgroundColor: '#e8f4f8', 
        borderRadius: '4px',
        fontSize: '10px',
        fontFamily: 'monospace'
      }}>
        <strong>RNA:</strong> {rnaOutput || '(no input)'}
      </div>

      <Handle type="source" position={Position.Bottom} {...handleConfig} />
    </div>
  );
}
```

### 1.2 Register Node in Node Type Registry

**Location:** `hyperflow-editor/src/nodeRegistry.ts` (or wherever you define available nodes)

```typescript
import { TranscriptionNode } from './nodes/bio/Transcription';

export const NODE_TYPES = {
  sequence: SequenceNode,
  enzyme: EnzymeNode,
  ligase: LigaseNode,
  transcription: TranscriptionNode,  // ← ADD THIS
};

export const BIO_NODE_PALETTE = [
  {
    type: 'sequence',
    label: '🧬 Sequence',
    category: 'Cloning',
    icon: '📝',
  },
  {
    type: 'enzyme',
    label: '✂️ Enzyme',
    category: 'Cloning',
    icon: '✂️',
  },
  {
    type: 'ligase',
    label: '🔗 Ligase',
    category: 'Cloning',
    icon: '🔗',
  },
  {
    type: 'transcription',
    label: '🧬 Transcription',
    category: 'Advanced',  // ← NEW CATEGORY
    icon: '→',
  },
];
```

---

## Phase 2: Wire into Python Export (10 min)

### 2.1 Add Transcription Exporter

**Location:** `hyperflow-editor/src/exporters/biopython/transcription.py` (new)

```python
"""
Transcription node exporter to BioPython.
Converts DNA → RNA using Bio.Seq.
"""

from Bio.Seq import Seq
from typing import Dict, Any

def export_transcription_node(node_data: Dict[str, Any]) -> str:
    """
    Generate BioPython code for DNA → RNA transcription.
    
    Args:
        node_data: {
            'dnaSequence': 'ATCGATCG',
            'strand': 'forward' or 'reverse'
        }
    
    Returns:
        Python code snippet using Bio.Seq.transcribe()
    """
    dna_seq = node_data.get('dnaSequence', '').upper()
    strand = node_data.get('strand', 'forward')
    
    if not dna_seq:
        return "# Transcription node: no input sequence"
    
    code = f"""
# Transcription: DNA → RNA
dna = Seq('{dna_seq}')
"""
    
    if strand == 'reverse':
        code += f"""
# Reverse complement
dna = dna.reverse_complement()
"""
    
    code += """
rna = dna.transcribe()
print(f"RNA: {{rna}}")
"""
    
    return code
```

### 2.2 Hook into Main Python Exporter

**Location:** `hyperflow-editor/src/exporters/pythonExporter.ts` (update existing)

```typescript
// Inside exportFlowToPython() function, add this case:

case 'transcription': {
  const nodeData = node.data as any;
  pythonCode += `\n# Node: ${node.id} (Transcription)\n`;
  pythonCode += exportTranscriptionNode({
    dnaSequence: nodeData.dnaSequence,
    strand: nodeData.strand || 'forward'
  });
  break;
}
```

---

## Phase 3: Focus Mode Support (5 min)

### 3.1 Add Transcription Icon to Focus Mode

**Location:** `hyperflow-editor/src/focusMode.ts` (update existing Focus Mode config)

```typescript
const FOCUS_NODE_ICONS = {
  sequence: '📝',
  enzyme: '✂️',
  ligase: '🔗',
  transcription: '→',  // ← ADD THIS
};
```

---

## Phase 4: README Example (5 min)

Add to README under "HyperFlow: The Visual Cockpit" section:

```markdown
### Advanced DNA Operations

#### Transcription (VIS4)
**Now Live:** Design DNA → RNA conversion workflows.

```
Sequence (ATCGATCG) 
    ↓
Transcription (Forward Strand)
    ↓
RNA Output: UAGCUAGC
```

BioPython export ready. Combine with Enzyme + Ligase for full synthetic biology pipelines.
```

---

## Phase 5: Quick Test (10 min)

### 5.1 Manual Browser Test

1. Open HyperFlow editor in browser.
2. Drag "🧬 Transcription" node from palette.
3. Connect to a Sequence node output.
4. Enter strand preference (Forward/Reverse).
5. Check that RNA output displays correctly in node.
6. Export flow to Python, verify `Bio.Seq.transcribe()` is in output.

---

## Expected Time: ~45 minutes total

| Step | Time |
|------|------|
| 1. Node Definition (TS) | 15 min |
| 2. Python Export | 10 min |
| 3. Focus Mode | 5 min |
| 4. README + Example | 5 min |
| 5. Manual Test | 10 min |
| **TOTAL** | **~45 min** |

---

## Next: VIS4b & VIS4c (if you hyperfocus further)

Once Transcription is live, the chain deepens:

- **Translation** (RNA → Protein): Codon table, ORF detection
- **CRISPR Guide Design**: Target sequence finder + sgRNA generator

Both follow the exact same pattern.

---

## Questions Before You Start?

1. **Do you have `BioLogic.ts` handling the engine logic, or is that purely React state?**
2. **Where does your Python exporter live right now?**
3. **Focus Mode—is it a global toggle or per-node?**

Answers → I can tighten the playbook to match your exact folder structure. Ready to fire? 🚀

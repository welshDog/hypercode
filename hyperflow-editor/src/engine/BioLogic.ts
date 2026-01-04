// 🧬 HyperFlow Bio-Logic Engine
// Pure TypeScript domain logic for molecular biology operations

// --- Types ---
export interface EnzymeDef {
  motif: string;
  cutIndex: number;
  overhang: string;
}

export interface Fragment {
  id: string;
  seq: string;
  leftOverhang: string | null;
  rightOverhang: string | null;
  sourceEnzyme: string;
}

// --- Data ---
export const ENZYMES: Record<string, EnzymeDef> = {
  'EcoRI': { motif: 'GAATTC', cutIndex: 1, overhang: 'AATT' },
  'BamHI': { motif: 'GGATCC', cutIndex: 1, overhang: 'GATC' },
  'HindIII': { motif: 'AAGCTT', cutIndex: 1, overhang: 'AGCT' },
};

// --- Logic ---

/**
 * Computes restriction fragments for a given sequence and enzyme.
 */
export const computeRestriction = (seq: string, enzymeName: string, mode: 'first' | 'all'): Fragment[] => {
  const enzyme = ENZYMES[enzymeName];
  if (!enzyme) return [{ id: 'error', seq, leftOverhang: null, rightOverhang: null, sourceEnzyme: 'none' }];

  const { motif, cutIndex, overhang } = enzyme;
  const sites: number[] = [];
  let pos = seq.indexOf(motif);

  // Find cut sites
  if (mode === 'first') {
    if (pos !== -1) sites.push(pos + cutIndex);
  } else {
    while (pos !== -1) {
      sites.push(pos + cutIndex);
      pos = seq.indexOf(motif, pos + 1);
    }
  }

  if (sites.length === 0) {
    return [{ id: 'uncut', seq, leftOverhang: null, rightOverhang: null, sourceEnzyme: 'none' }];
  }

  // Generate fragments
  const fragments: Fragment[] = [];
  let lastCut = 0;

  sites.forEach((cutPos, idx) => {
    // Left fragment (or middle)
    const segment = seq.slice(lastCut, cutPos);
    fragments.push({
      id: `frag-${idx}`,
      seq: segment,
      leftOverhang: idx === 0 ? null : overhang, // Previous cut left an overhang? No, wait. 
      // Logic correction:
      // EcoRI: G|AATTC. 
      // Left frag ends with G. Right frag starts with AATTC.
      // The "overhang" is on the 5' end of the Right frag, and complementary on the Left frag?
      // Standard representation:
      // 5'...G       AATTC...3'
      // 3'...CTTAA       G...5'
      // The "sticky end" is usually described by the single strand overhang.
      // In our model:
      // Left fragment right-end: has sticky end compatible with 'AATT'
      // Right fragment left-end: has sticky end 'AATT'
      
      // Let's simplify for the visual model we established:
      // "Right Overhang" of the left piece is the enzyme's overhang signature.
      // "Left Overhang" of the right piece is the enzyme's overhang signature.
      
      rightOverhang: overhang,
      sourceEnzyme: enzymeName
    });
    lastCut = cutPos;
  });

  // Final fragment
  fragments.push({
    id: `frag-final`,
    seq: seq.slice(lastCut),
    leftOverhang: overhang,
    rightOverhang: null,
    sourceEnzyme: enzymeName
  });

  return fragments;
};

/**
 * Checks if two fragments are compatible for ligation.
 * @param leftFrag The fragment on the left side
 * @param rightFrag The fragment on the right side
 * @param isCircular Check for circularization compatibility?
 */
export const checkLigationCompatibility = (
  leftFrag: Fragment, 
  rightFrag: Fragment, 
  isCircular: boolean = false
): { isValid: boolean; sequence: string; error?: string; isCircularResult?: boolean } => {
  
  // Linear check: Left's right vs Right's left
  const linearMatch = leftFrag.rightOverhang === rightFrag.leftOverhang;

  if (!linearMatch) {
    return {
      isValid: false,
      sequence: '',
      error: `Mismatch: ${leftFrag.rightOverhang || 'Blunt'} vs ${rightFrag.leftOverhang || 'Blunt'}`
    };
  }

  let ligatedSeq = leftFrag.seq + rightFrag.seq;
  let circularResult = false;

  // Circular check (if requested)
  if (isCircular) {
    // Check outer ends: Left's left vs Right's right
    const endOverhangA = leftFrag.leftOverhang;
    const endOverhangB = rightFrag.rightOverhang;

    const circularMatch = 
      (!endOverhangA && !endOverhangB) || // Blunt + Blunt
      (endOverhangA && endOverhangB && endOverhangA === endOverhangB); // Matching sticky

    if (circularMatch) {
      ligatedSeq = '↺ ' + ligatedSeq;
      circularResult = true;
    } else {
      return {
        isValid: false,
        sequence: '',
        error: `Circular Mismatch: ${endOverhangA || 'Blunt'} vs ${endOverhangB || 'Blunt'}`
      };
    }
  }

  return {
    isValid: true,
    sequence: ligatedSeq,
    isCircularResult: circularResult
  };
};

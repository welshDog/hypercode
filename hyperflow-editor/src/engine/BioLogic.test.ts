import { describe, it, expect } from 'vitest';
import { computeRestriction } from './BioLogic';

describe('BioLogic Engine', () => {
  
  describe('computeRestriction', () => {
    const ecoRI = 'EcoRI'; // GAATTC
    
    it('cuts DNA at the correct index for EcoRI', () => {
      const seq = 'AAAGAATTCAAA'; 
      //           012345678901
      // EcoRI motif at 3. Cut index is 1. Cut at 3+1 = 4.
      // Left: AAAG
      // Right: AATTCAAA
      
      const fragments = computeRestriction(seq, ecoRI, 'first');
      
      expect(fragments).toHaveLength(2);
      expect(fragments[0].seq).toBe('AAAG');
      expect(fragments[1].seq).toBe('AATTCAAA');
    });

    it('assigns correct sticky ends', () => {
      const seq = 'AAAGAATTCAAA';
      const fragments = computeRestriction(seq, ecoRI, 'first');
      
      // Left fragment (ends with G) should have right overhang compatible with AATT
      expect(fragments[0].rightOverhang).toBe('AATT');
      
      // Right fragment (starts with AATT) should have left overhang compatible with AATT
      expect(fragments[1].leftOverhang).toBe('AATT');
    });

    it('handles multiple cuts in "all" mode', () => {
      const seq = 'GAATTCGAATTC';
      //           012345678901
      // Cut 1 at 1 (G|AATTC)
      // Cut 2 at 7 (G|AATTC)
      // Frags: G, AATTCG, AATTC
      
      const fragments = computeRestriction(seq, ecoRI, 'all');
      
      expect(fragments).toHaveLength(3);
      expect(fragments[0].seq).toBe('G');
      expect(fragments[1].seq).toBe('AATTCG');
      expect(fragments[2].seq).toBe('AATTC');
    });

    it('returns "uncut" status if motif not found', () => {
      const seq = 'AAAAAAAAAA';
      const fragments = computeRestriction(seq, ecoRI, 'all');
      
      expect(fragments).toHaveLength(1);
      expect(fragments[0].id).toBe('uncut');
    });
  });
});

import { describe, it, expect } from 'vitest';
import { calculateTm, reverseComplement, performPCR } from './PCRUtils';

describe('PCR Utilities', () => {
  
  describe('calculateTm (Wallace Rule)', () => {
    it('calculates correct Tm for short sequences', () => {
      // 2*(A+T) + 4*(G+C)
      // AAAA = 2*4 = 8
      expect(calculateTm('AAAA')).toBe(8);
      // GGGG = 4*4 = 16
      expect(calculateTm('GGGG')).toBe(16);
      // ATGC = 2*(1+1) + 4*(1+1) = 4 + 8 = 12
      expect(calculateTm('ATGC')).toBe(12);
    });

    it('handles mixed case and whitespace', () => {
      expect(calculateTm('at gc')).toBe(12);
    });

    it('returns 0 for empty string', () => {
      expect(calculateTm('')).toBe(0);
    });
  });

  describe('reverseComplement', () => {
    it('computes correct reverse complement', () => {
      // 5'-ATGC-3' -> 3'-TACG-5' -> rev -> 5'-GCAT-3'
      expect(reverseComplement('ATGC')).toBe('GCAT');
      expect(reverseComplement('AAA')).toBe('TTT');
      expect(reverseComplement('GATTACA')).toBe('TGTAATC');
    });
  });

  describe('performPCR', () => {
    const template = 'ATGGCCATGGCGCCCCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC';
    // Fwd: ATGGCC (matches start)
    // Rev: GCTAGC (matches end)
    // RevComp of GCTAGC is GCTAGC (palindrome) - wait.
    // GCTAGC -> C G A T C G -> rev -> GCTAGC. Yes, BamHI/NheI style palindromes.
    
    it('extracts correct amplicon', () => {
      const fwd = 'ATGGCC';
      const rev = 'GCTAGC';
      
      const result = performPCR(template, fwd, rev);
      
      expect(result.error).toBeUndefined();
      expect(result.amplicon).toBe(template); // In this case, it spans the whole thing if primers match ends
      expect(result.startIndex).toBe(0);
    });

    it('extracts sub-segment', () => {
      // Template: ... A T G G C C ... ... G C T A G C ...
      const longTemplate = 'NNNNATGGCCNNNNNNNNNNGCTAGCNNNN';
      const fwd = 'ATGGCC';
      const rev = 'GCTAGC'; // RevComp: GCTAGC

      const result = performPCR(longTemplate, fwd, rev);
      
      expect(result.amplicon).toBe('ATGGCCNNNNNNNNNNGCTAGC');
      expect(result.startIndex).toBe(4);
    });

    it('fails if primers are missing', () => {
      const result = performPCR(template, '', 'GCTAGC');
      expect(result.error).toBe('Missing primers');
    });

    it('fails if forward primer not found', () => {
      const result = performPCR(template, 'ZZZZZZ', 'GCTAGC');
      expect(result.error).toBe('Forward primer not found');
    });
  });
});

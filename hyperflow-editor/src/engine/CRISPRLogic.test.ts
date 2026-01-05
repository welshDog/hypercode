import { describe, it, expect } from 'vitest';
import { performCRISPR } from './CRISPRLogic';

describe('CRISPR Logic', () => {
  const dna = 'AAATTTCCCGGGAAATTT';
  //           012345678901234567
  // PAM: NGG.
  // GGG at index 9.
  // PAM start: 9.
  // Cas9 cut: 9 - 3 = 6.
  // Upstream 6bp: TTTCCC (indices 3-8).
  
  it('finds target and performs NHEJ deletion', () => {
    const guide = 'TTTCCC';
    const pam = 'NGG';
    
    const result = performCRISPR(dna, guide, pam, 'NHEJ');
    
    expect(result.status).toBe('repaired');
    expect(result.cutIndex).toBe(6);
    // Original: AAATTT CCC GGG...
    // Cut at 6.
    // Index 6 is 'C'.
    // NHEJ deletes index 6.
    // Result: AAATTT CC GGG...
    //          012345 67 89
    // Expected length: 18 - 1 = 17.
    expect(result.editedSequence.length).toBe(dna.length - 1);
    expect(result.message).toContain('NHEJ');
  });

  it('finds target and performs HDR insertion', () => {
    const guide = 'TTTCCC';
    const pam = 'NGG';
    const template = 'AAAA';
    
    const result = performCRISPR(dna, guide, pam, 'HDR', template);
    
    expect(result.status).toBe('repaired');
    // Original: AAATTT | CCCGGG...
    // Insert: AAAA
    // Result: AAATTT AAAA CCCGGG...
    expect(result.editedSequence).toContain('AAATTTAAAACCCGGG');
    expect(result.message).toContain('HDR');
  });

  it('fails if gRNA does not match upstream of PAM', () => {
    const guide = 'AAAAAA'; // Does not match TTTCCC
    const pam = 'NGG';
    
    const result = performCRISPR(dna, guide, pam, 'NHEJ');
    
    expect(result.status).toBe('error');
    expect(result.message).toContain('Target not found');
  });
});

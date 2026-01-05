
/**
 * 🧬 PCR Utilities
 * Logic for Primer Melting Temperature (Tm) and Amplicon extraction.
 */

// Basic Wallace Rule: Tm = 2(A+T) + 4(G+C)
export function calculateTm(primer: string): number {
  const clean = primer.toUpperCase().replace(/[^ATGC]/g, '');
  if (clean.length === 0) return 0;

  const a = (clean.match(/A/g) || []).length;
  const t = (clean.match(/T/g) || []).length;
  const g = (clean.match(/G/g) || []).length;
  const c = (clean.match(/C/g) || []).length;

  return 2 * (a + t) + 4 * (g + c);
}

// Reverse Complement: A->T, T->A, G->C, C->G, reversed
export function reverseComplement(seq: string): string {
  const map: Record<string, string> = { A: 'T', T: 'A', G: 'C', C: 'G', N: 'N' };
  return seq
    .toUpperCase()
    .split('')
    .reverse()
    .map((base) => map[base] || base)
    .join('');
}

export interface PCRResult {
  amplicon: string;
  startIndex: number; // 0-based index in template
  endIndex: number;   // 0-based index in template
  error?: string;
}

export function performPCR(template: string, fwd: string, rev: string): PCRResult {
  const tempUpper = template.toUpperCase();
  const fwdUpper = fwd.toUpperCase();
  const revUpper = rev.toUpperCase();

  if (!fwdUpper || !revUpper) {
    return { amplicon: '', startIndex: -1, endIndex: -1, error: 'Missing primers' };
  }

  // 1. Find Forward Primer binding site (binds to antisense, so matches sense)
  const fwdIndex = tempUpper.indexOf(fwdUpper);
  if (fwdIndex === -1) {
    return { amplicon: '', startIndex: -1, endIndex: -1, error: 'Forward primer not found' };
  }

  // 2. Find Reverse Primer binding site
  // The reverse primer sequence provided by user binds to the SENSE strand.
  // Wait, standard convention:
  // Forward primer: Matches the start of the sense strand (5'->3').
  // Reverse primer: Matches the complementary strand (binds to sense), but is written 5'->3'.
  // So, to find where the Reverse Primer "ends" the amplicon on the sense strand,
  // we need to look for the Reverse Complement of the Reverse Primer in the template.
  
  const revComp = reverseComplement(revUpper);
  const revIndex = tempUpper.lastIndexOf(revComp);

  if (revIndex === -1) {
    return { amplicon: '', startIndex: -1, endIndex: -1, error: 'Reverse primer binding site not found' };
  }

  // Check direction
  if (revIndex <= fwdIndex) {
    return { amplicon: '', startIndex: -1, endIndex: -1, error: 'Reverse primer binds before Forward primer' };
  }

  // Extract Amplicon
  // Start at fwdIndex
  // End at revIndex + length of revComp
  const endIndex = revIndex + revComp.length;
  const amplicon = tempUpper.slice(fwdIndex, endIndex);

  return { amplicon, startIndex: fwdIndex, endIndex };
}

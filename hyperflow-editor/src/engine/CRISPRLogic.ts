
/**
 * 🧬 CRISPR/Cas9 Logic
 * Simulates guide RNA matching, PAM recognition, and DNA repair mechanisms (NHEJ/HDR).
 */

export interface CRISPRResult {
  cutIndex: number;
  editedSequence: string;
  status: 'scanning' | 'cut' | 'repaired' | 'error';
  message?: string;
}

export function performCRISPR(
  dna: string,
  guide: string,
  pam: string,
  mode: 'NHEJ' | 'HDR',
  repairTemplate: string = ''
): CRISPRResult {
  const seq = dna.toUpperCase();
  const grna = guide.toUpperCase();
  const pamSeq = pam.toUpperCase();

  if (!dna) {
    return { cutIndex: -1, editedSequence: '', status: 'error', message: 'No DNA input' };
  }

  if (!grna || !pamSeq) {
    return { cutIndex: -1, editedSequence: dna, status: 'scanning', message: 'Configure gRNA & PAM' };
  }

  // 1. Find PAM sites
  // Regex for PAM. NGG -> .GG
  // We need to escape special regex chars if any, but PAM is usually just ACGTN.
  const regexStr = pamSeq.replace(/N/g, '.');
  const pamRegex = new RegExp(regexStr, 'g');

  let match;
  let targetFound = false;
  let cutIndex = -1;

  // Search for all PAMs
  while ((match = pamRegex.exec(seq)) !== null) {
    // PAM starts at match.index
    // Check upstream sequence for gRNA match
    const pamStart = match.index;

    // Ensure we have enough room upstream
    if (pamStart >= grna.length) {
      // Extract sequence immediately upstream of PAM
      // gRNA length determines how far back we check
      const upstreamSeq = seq.slice(pamStart - grna.length, pamStart);

      if (upstreamSeq === grna) {
        targetFound = true;
        // Cas9 cuts 3bp upstream of PAM
        // This is the index of the base immediately TO THE RIGHT of the cut
        cutIndex = pamStart - 3;
        break; // Assume first valid target is the one we hit
      }
    }

    // Force regex to backtrack to find overlapping matches
    pamRegex.lastIndex = match.index + 1;
  }

  if (!targetFound) {
    return {
      cutIndex: -1,
      editedSequence: dna,
      status: 'error',
      message: 'Target not found (PAM + gRNA mismatch)'
    };
  }

  // 2. Perform Cut & Repair
  let edited = '';
  let message = '';

  if (mode === 'NHEJ') {
    // Non-Homologous End Joining
    // Simulating a frameshift mutation (1bp deletion)
    // We remove the base at cutIndex - 1 (the one just before the cut line? Or just random?)
    // Let's delete the base *at* cutIndex to keep it simple.
    // e.g. ...AT G C... -> ...AT C...
    edited = seq.slice(0, cutIndex) + seq.slice(cutIndex + 1);
    message = 'NHEJ: 1bp Deletion (Frameshift)';
  } else {
    // Homology Directed Repair
    // Insert the repair template exactly at the cut site
    const insert = repairTemplate.toUpperCase();
    edited = seq.slice(0, cutIndex) + insert + seq.slice(cutIndex);
    message = `HDR: Inserted ${insert.length}bp Template`;
  }

  return {
    cutIndex,
    editedSequence: edited,
    status: 'repaired',
    message
  };
}

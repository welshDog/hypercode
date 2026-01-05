import re

from typing import List, Tuple, Dict, Any
from hypercode.backends.bio_utils import calculate_tm

class CRISPRResult:
    def __init__(self, success: bool, log: List[str], edited_sequence: str = "", cut_site: int = -1, tm: float = 0.0, off_target_score: float = 0.0):
        self.success = success
        self.log = log
        self.edited_sequence = edited_sequence
        self.cut_site = cut_site
        self.tm = tm
        self.off_target_score = off_target_score

def find_pam_sites(sequence: str, pam_pattern: str = "NGG") -> List[Tuple[int, str]]:
    """
    Finds all PAM sites in a sequence matching the pattern.
    Returns a list of (start_index, pam_sequence) tuples.
    """
    sequence = sequence.upper()
    # Convert IUPAC codes to Regex
    # N -> [ATCG]
    regex_pattern = pam_pattern.replace("N", "[ATCG]")
    
    # Use lookahead? No, PAM is consumed in standard finding usually, 
    # but strictly speaking, overlapping PAMs? usually not an issue for Cas9.
    # finditer is fine.
    
    matches = []
    for m in re.finditer(regex_pattern, sequence):
        matches.append((m.start(), m.group()))
    
    return matches

def extract_grna(sequence: str, pam_start: int, length: int = 20) -> str:
    """
    Extracts the gRNA target sequence (protospacer) upstream of the PAM.
    """
    if pam_start < length:
        return "" # Not enough space upstream
    return sequence[pam_start - length : pam_start]

def score_off_target(target_seq: str, genome_seq: str = "") -> float:
    """
    Placeholder for off-target scoring (CFD/MIT).
    For MVP, returns a mock score based on GC content (higher GC -> usually more specific binding? actually complex).
    Let's just return a placeholder or 1.0 (perfect specificity) if no genome provided.
    """
    # TODO: Implement Phase 2 Off-Target Detection
    return 1.0

def simulate_cut(dna_sequence: str, grna_sequence: str, pam_pattern: str = "NGG") -> CRISPRResult:
    """
    Simulates a CRISPR/Cas9 cut.
    1. Finds the gRNA match in the DNA.
    2. Verifies the PAM exists immediately downstream.
    3. Simulates a DSB (Double Stranded Break) and NHEJ repair (indel).
    """
    dna = dna_sequence.upper()
    grna = grna_sequence.upper()
    pam_regex = pam_pattern.upper().replace("N", "[ATCG]")
    
    log = []
    
    # 1. Find ALL gRNA matches
    start_search = 0
    candidates = []
    
    while True:
        match_index = dna.find(grna, start_search)
        if match_index == -1:
            break
            
        # Candidate found, check PAM
        pam_start = match_index + len(grna)
        pam_end = pam_start + len(pam_pattern)
        
        if pam_end <= len(dna):
            actual_pam = dna[pam_start:pam_end]
            if re.match(pam_regex, actual_pam):
                # Valid Match Found!
                log.append(f"Target match found at index {match_index}.")
                log.append(f"PAM '{actual_pam}' confirmed.")
                
                # 3. Calculate Tm
                tm = calculate_tm(grna)
                log.append(f"gRNA Tm: {tm}°C")
                
                # 4. Simulate Cut
                cut_site = pam_start - 3
                log.append(f"Cas9 cleavage at index {cut_site} (3bp upstream of PAM).")
                
                # 5. Simulate NHEJ Repair (Indel)
                edited_seq = dna[:cut_site] + "[-]" + dna[cut_site+1:]
                log.append("Repair: NHEJ simulated (1bp deletion marker inserted).")
                
                return CRISPRResult(
                    success=True,
                    log=log,
                    edited_sequence=edited_seq,
                    cut_site=cut_site,
                    tm=tm,
                    off_target_score=score_off_target(grna)
                )
            else:
                candidates.append(f"Match at {match_index} failed PAM check (found '{actual_pam}').")
        else:
             candidates.append(f"Match at {match_index} ignored (PAM out of bounds).")
             
        start_search = match_index + 1
        
    # If we reach here, no valid cut was found
    if not candidates:
        log.append(f"Target sequence '{grna}' not found in DNA.")
    else:
        log.extend(candidates)
        log.append("No valid target+PAM sites found.")
        
    return CRISPRResult(False, log, dna)

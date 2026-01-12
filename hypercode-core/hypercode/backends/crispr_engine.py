
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

class CRISPREngine:
    """
    Core engine for CRISPR/Cas9 simulation and analysis.
    """
    def scan_genome_for_off_targets(self, guide_seq: str, genome_seq: str, max_mismatches: int = 4) -> List[Tuple[int, int, str]]:
        """
        Scans a genome sequence for potential off-target binding sites.
        Wrapper for the standalone function.
        """
        return scan_genome_for_off_targets(guide_seq, genome_seq, max_mismatches)

    def score_off_target_risk(self, guide_seq: str, genome_seq: str) -> float:
        """
        Calculates a risk score based on off-target potentials.
        Wrapper for the standalone function.
        """
        return score_off_target_risk(guide_seq, genome_seq)

    def simulate_cut(self, dna_sequence: str, grna_sequence: str, pam_pattern: str = "NGG") -> CRISPRResult:
        """
        Simulates a CRISPR/Cas9 cut.
        Wrapper for the standalone function.
        """
        return simulate_cut(dna_sequence, grna_sequence, pam_pattern)

def find_pam_sites(sequence: str, pam_pattern: str = "NGG") -> List[Tuple[int, str]]:
    """
    Finds all PAM sites in a sequence matching the pattern.
    Returns a list of (start_index, pam_sequence) tuples.
    """
    sequence = sequence.upper()
    regex_pattern = pam_pattern.replace("N", "[ATCG]")
    
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

def calculate_mismatch_score(guide_seq: str, target_seq: str) -> int:
    """
    Calculates the number of mismatches between two sequences of equal length.
    """
    if len(guide_seq) != len(target_seq):
        return 999 # Invalid comparison
    
    mismatches = 0
    for i in range(len(guide_seq)):
        if guide_seq[i] != target_seq[i]:
            mismatches += 1
    return mismatches

def scan_genome_for_off_targets(guide_seq: str, genome_seq: str, max_mismatches: int = 4) -> List[Tuple[int, int, str]]:
    """
    Scans a genome sequence for potential off-target binding sites.
    Returns a list of (index, mismatches, sequence_found).
    
    Note: This is a simplified O(N*M) scanner for the MVP.
    Real-world tools use efficient indexing (e.g., Bowtie, BWA).
    """
    guide_len = len(guide_seq)
    genome_len = len(genome_seq)
    off_targets = []
    
    # Brute force scan (okay for small viral genomes/plasmids in MVP)
    # Step by 1bp
    for i in range(genome_len - guide_len + 1):
        subseq = genome_seq[i : i + guide_len]
        mismatches = calculate_mismatch_score(guide_seq, subseq)
        
        if mismatches <= max_mismatches and mismatches > 0:
             off_targets.append((i, mismatches, subseq))
             
    return off_targets

def score_off_target_risk(guide_seq: str, genome_seq: str) -> float:
    """
    Calculates a risk score based on off-target potentials.
    Higher score = Higher risk (Bad guide).
    Lower score = Lower risk (Good guide).
    
    Formula: Sum(1 / (mismatches^2)) for all found off-targets.
    """
    off_targets = scan_genome_for_off_targets(guide_seq, genome_seq)
    risk_score = 0.0
    for _, mismatches, _ in off_targets:
        if mismatches == 0:
            continue # This is the on-target (or a perfect off-target duplicate)
        risk_score += 1.0 / (mismatches ** 2)
        
    return risk_score

def simulate_cut(dna_sequence: str, grna_sequence: str, pam_pattern: str = "NGG") -> CRISPRResult:
    """
    Simulates a CRISPR/Cas9 cut.
    """
    dna = dna_sequence.upper()
    grna = grna_sequence.upper()
    pam_regex = pam_pattern.upper().replace("N", "[ATCG]")
    
    log = []
    
    # 1. Find ALL gRNA matches
    start_search = 0
    
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
                    tm=tm
                )
        
        start_search = match_index + 1

    return CRISPRResult(success=False, log=["CRISPR failed: No matching target/PAM found."])

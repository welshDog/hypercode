"""
Bioinformatics Utility Module for HyperCode.
Provides DNA manipulation functions, enzyme databases, and validation logic.
"""

from typing import Dict, Any

# Type IIS Restriction Enzymes
# Format: Name -> (Recognition Site, Cut Offset Top, Cut Offset Bottom, Overhang Length)
ENZYME_DB: Dict[str, Dict[str, Any]] = {
    "BsaI": {
        "site": "GGTCTC",
        "rev_site": "GAGACC",
        "spacer_len": 1,
        "overhang_len": 4
    },
    "BbsI": {
        "site": "GAAGAC", # Cut 2/6
        "rev_site": "GTCTTC",
        "spacer_len": 2,
        "overhang_len": 4
    },
    "SapI": {
        "site": "GCTCTTC", # Cut 1/4
        "rev_site": "GAAGAGC",
        "spacer_len": 1,
        "overhang_len": 3
    }
}

def validate_dna(sequence: str) -> bool:
    """
    Validates that a sequence contains only valid DNA characters (A, T, C, G, N).
    Case-insensitive.
    """
    valid_chars = set('ATCGN')
    return all(base.upper() in valid_chars for base in sequence)

def calculate_tm(sequence: str) -> float:
    """
    Calculates melting temperature (Tm) using the Wallace rule.
    Tm = 2(A+T) + 4(G+C)
    Suitable for short sequences (14-20 bp).
    """
    sequence = sequence.upper()
    a_count = sequence.count('A')
    t_count = sequence.count('T')
    g_count = sequence.count('G')
    c_count = sequence.count('C')
    return 2 * (a_count + t_count) + 4 * (g_count + c_count)

def reverse_complement(sequence: str) -> str:
    """
    Returns the reverse complement of a DNA sequence.
    """
    complement_map = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C', 'N': 'N'}
    return "".join(complement_map.get(base, base) for base in reversed(sequence.upper()))

# No Python code changes required for this pylint_django plugin warning.
# The warning is about a missing pylint plugin, not the actual source code.
# To resolve: install the plugin via pip install pylint-django or remove it from your pylint config.

from typing import Dict, Tuple, Any

# Type IIS Restriction Enzymes
# Format: Name -> (Recognition Site, Cut Offset Top, Cut Offset Bottom, Overhang Length)
# BsaI: GGTCTC (1/5) -> Cut at 1bp after site on top, 5bp on bottom (leaving 4bp 5' overhang)
# For extraction logic: Site + 1bp spacer + 4bp overhang
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

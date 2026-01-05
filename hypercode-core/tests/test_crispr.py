import pytest
from hypercode.backends.crispr_engine import calculate_tm, find_pam_sites, simulate_cut, CRISPRResult

def test_calculate_tm():
    # Wallace Rule: Tm = 2(A+T) + 4(G+C)
    assert calculate_tm("AAAA") == 8
    assert calculate_tm("TTTT") == 8
    assert calculate_tm("GGGG") == 16
    assert calculate_tm("CCCC") == 16
    assert calculate_tm("ACGT") == 2*(1+1) + 4*(1+1) # 4 + 8 = 12
    # Case insensitivity
    assert calculate_tm("acgt") == 12

def test_find_pam_sites_ngg():
    seq = "AAAGGGTTT" # NGG at index 3 (GGG)
    # GGG matches NGG. Start index 3.
    matches = find_pam_sites(seq, "NGG")
    assert len(matches) >= 1
    # Check specific match
    # Regex finditer returns start index of the match.
    # NGG matches "AGG" (idx 2) and "GGG" (idx 3)?
    # "AAAGGG" -> "AGG" (2), "GGG" (3) overlap?
    # re.finditer does not find overlapping matches by default.
    # "AAAGGG" -> "AGG" at 2. Remaining "GTTT" -> No match.
    # Wait, "AAGGG"
    # "AGG" at 1?
    # Let's test non-overlapping simple cases first.
    
    seq2 = "TTTGGAAA" # TGG at 2
    matches2 = find_pam_sites(seq2, "NGG")
    assert (2, "TGG") in matches2

def test_find_pam_sites_ng():
    seq = "ATCG" # CG is NG
    matches = find_pam_sites(seq, "NG")
    # TCG matches? No, CG matches.
    # A T C G
    #   ^ CG at 2
    assert (2, "CG") in matches

def test_simulate_cut_success():
    # DNA: 20bp target + PAM + rest
    target = "A" * 20
    pam = "TGG"
    dna = "TTTT" + target + pam + "AAAA"
    # Target starts at 4. Ends at 24.
    # PAM at 24.
    
    result = simulate_cut(dna, target, "NGG")
    assert result.success is True
    # Check if PAM confirmation is in any log entry
    assert any("PAM 'TGG' confirmed" in entry for entry in result.log)
    
    # Cut site: 3bp upstream of PAM (index 24).
    # Cut at 21.
    assert result.cut_site == 24 - 3
    
    # Edited sequence should have indel
    assert "[-]" in result.edited_sequence
    assert len(result.edited_sequence) == len(dna) - 1 + 3 # -1 char + 3 chars "[-]" = +2 length change?
    # Original logic: dna[:cut] + "[-]" + dna[cut+1:]
    # Removes 1 char, adds 3 chars "[-]". Net +2.
    # Wait, `dna[cut+1:]` skips one char (the one at `cut`).
    # So yes, 1bp deletion.

def test_simulate_cut_fail_pam():
    target = "A" * 20
    pam = "TAA" # Not NGG
    dna = target + pam
    
    result = simulate_cut(dna, target, "NGG")
    assert result.success is False
    # Check if any log entry contains the failure message
    assert any("failed PAM check" in entry for entry in result.log)
    assert "No valid target+PAM sites found" in result.log[-1]

def test_simulate_cut_fail_target():
    dna = "ACGTACGT"
    target = "ZZZZ"
    result = simulate_cut(dna, target, "NGG")
    assert result.success is False
    assert "not found" in result.log[0]

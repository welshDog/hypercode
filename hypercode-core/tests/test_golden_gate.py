import pytest
from hypercode.simulator import simulate_flow

# ==========================================
# 🧪 Golden Gate Assembly Test Suite
# ==========================================
# Validates Type IIS Restriction Logic, Overhang Matching, and Ligation

@pytest.fixture
def gg_parts():
    """Provides standard BsaI parts for testing"""
    return {
        # Part 1: Promoter (Overhangs: GGAG -> TACT)
        # GGTCTC (BsaI) + A (Spacer) + GGAG (Overhang) + [PROMOTER] + TACT (Overhang) + A + GAGACC (BsaI Rev)
        "promoter": {
            "id": "p1",
            "type": "sequence",
            "data": {
                "sequence": "GGTCTCAGGAGTTGACAGCTAGCTCAGTCCTAGGTATAATGCTAGCTACTAGAGACC",
                "label": "Promoter"
            }
        },
        # Part 2: RBS+GFP (Overhangs: TACT -> AATG)
        "rbs_gfp": {
            "id": "p2",
            "type": "sequence",
            "data": {
                "sequence": "GGTCTCATACTAAAGAGGAGAAATACTAGATGCGTAAAGGAGAAGAACTTTTCACTGGAGTTGTCCAATAAAATGAGAGACC",
                "label": "RBS+GFP"
            }
        },
        # Part 3: Terminator (Overhangs: AATG -> GGAG) -> Circularizes back to Promoter start!
        "terminator": {
            "id": "p3",
            "type": "sequence",
            "data": {
                "sequence": "GGTCTCAAATGCCAGGCATCAAATAAAACGAAAGGCTCAGTCGAAAGACTGGGCCTTTCGTTTTATCTGTTGTTTGTCGGTGAACGCTCTCTACTAGAGTCACACTGGCTCACCTTCGGGTGGGCCTTTCTGCGTTTATGGAGAGAGACC",
                "label": "Terminator"
            }
        }
    }

def test_bsai_recognition(gg_parts):
    """Test if BsaI sites (GGTCTC) are correctly identified"""
    flow = {
        "nodes": [
            gg_parts["promoter"],
            {
                "id": "gg-node",
                "type": "goldengate",
                "data": {"enzyme": "BsaI"}
            }
        ],
        "edges": [
            {"source": "p1", "target": "gg-node"}
        ]
    }
    
    results = simulate_flow(flow)
    assert "gg-node" in results
    log = results["gg-node"]["log"]
    
    # Check logs for successful extraction
    assert any("Valid BsaI site found" in line for line in log)
    assert any("Extracted 43bp payload" in line for line in log) # Promoter core length check

def test_overhang_extraction(gg_parts):
    """Test if the correct 4bp overhangs are extracted"""
    # Promoter should have Left: GGAG, Right: TACT
    flow = {
        "nodes": [
            gg_parts["promoter"],
            {
                "id": "gg-node",
                "type": "goldengate",
                "data": {"enzyme": "BsaI"}
            }
        ],
        "edges": [
            {"source": "p1", "target": "gg-node"}
        ]
    }
    
    results = simulate_flow(flow)
    log = results["gg-node"]["log"]
    
    # Check specific overhangs in logs
    assert any("Overhangs: GGAG ... TACT" in line for line in log)

def test_bbsi_support(gg_parts):
    """Test if BbsI sites are correctly identified"""
    # Create a BbsI part
    # BbsI: GAAGAC (2/6) -> Cut 2bp after site
    # Site (6) + 2bp Spacer + 4bp Overhang
    # GAAGAC + AA + ATGC + [PAYLOAD] + ...
    
    bbsi_part = {
        "id": "bbsi1",
        "type": "sequence",
        "data": {
            "sequence": "GAAGACAAATGC" + "AAAA" + "GCATTTGTCTTC", # Payload AAAA
            "label": "BbsI Part"
        }
    }
    
    flow = {
        "nodes": [
            bbsi_part,
            {
                "id": "gg-node",
                "type": "goldengate",
                "data": {"enzyme": "BbsI"}
            }
        ],
        "edges": [
            {"source": "bbsi1", "target": "gg-node"}
        ]
    }
    
    results = simulate_flow(flow)
    log = results["gg-node"]["log"]
    
    assert any("Valid BbsI site found" in line for line in log)
    assert any("Extracted 12bp payload" in line for line in log) # 4 (overhang) + 4 (payload) + 4 (overhang) = 12
def test_ligation_success(gg_parts):
    """Test successful ligation of two compatible parts"""
    # Promoter (TACT end) + RBS (TACT start)
    flow = {
        "nodes": [
            gg_parts["promoter"],
            gg_parts["rbs_gfp"],
            {
                "id": "gg-node",
                "type": "goldengate",
                "data": {"enzyme": "BsaI"}
            }
        ],
        "edges": [
            {"source": "p1", "target": "gg-node"},
            {"source": "p2", "target": "gg-node"}
        ]
    }
    
    results = simulate_flow(flow)
    # Check that parts were extracted
    parts = results["gg-node"]["parts"]
    assert len(parts) == 2
    
    # Check sequence
    # Promoter Payload (excluding overhangs? No, logic includes them for checking)
    # Logic: Part1 + Part2(skipping overlap)
    # Part 1: [Overhang] [Body] [Overhang TACT]
    # Part 2: [Overhang TACT] [Body] [Overhang]
    # Result: [Overhang] [Body] [Overhang TACT] [Body] [Overhang]
    
    final_seq = results["gg-node"]["sequence"]
    assert len(final_seq) > 0
    assert "GAP" not in final_seq
    assert "Ligation: Part 1 (TACT) matches Part 2 (TACT). Joining." in results["gg-node"]["log"]

def test_circular_assembly(gg_parts):
    """Test full circular assembly of 3 parts"""
    flow = {
        "nodes": [
            gg_parts["promoter"],
            gg_parts["rbs_gfp"],
            gg_parts["terminator"],
            {
                "id": "gg-node",
                "type": "goldengate",
                "data": {"enzyme": "BsaI"}
            }
        ],
        "edges": [
            {"source": "p1", "target": "gg-node"},
            {"source": "p2", "target": "gg-node"},
            {"source": "p3", "target": "gg-node"}
        ]
    }
    
    results = simulate_flow(flow)
    data = results["gg-node"]
    
    # Debug info if assertion fails
    if not data["isCircular"]:
        print("\nDEBUG LOG DUMP:")
        for line in data["log"]:
            print(line)
        print("DEBUG PARTS DATA:")
        for p in data.get("parts", []):
            print(f"Part: {p.get('label')} Left: {p.get('left')} Right: {p.get('right')}")

    assert data["isCircular"] is True
    assert any("Plasmid closed" in line for line in data["log"])

def test_mismatched_overhangs(gg_parts):
    """Test failure when overhangs don't match"""
    # Promoter (TACT) -> Terminator (AATG) - Mismatch!
    flow = {
        "nodes": [
            gg_parts["promoter"],
            gg_parts["terminator"],
            {
                "id": "gg-node",
                "type": "goldengate",
                "data": {"enzyme": "BsaI"}
            }
        ],
        "edges": [
            {"source": "p1", "target": "gg-node"},
            {"source": "p3", "target": "gg-node"}
        ]
    }
    
    results = simulate_flow(flow)
    log = results["gg-node"]["log"]
    
    assert any("MISMATCH" in line for line in log)
    # The sequence should contain the gap marker
    assert "-[GAP]-" in results["gg-node"]["sequence"]

def test_reverse_bsai_site(gg_parts):
    """Test BsaI sites on reverse strand (GAGACC)"""
    # Use a custom sequence designed to test reverse BsaI detection
    seq = "GGTCTC" + "A" + "AAAA" + "TTTT" + "TTTT" + "T" + "GAGACC"
    #      Site     Sp   OverL  Core    OverR  Sp   SiteRev
    
    flow = {
        "nodes": [
            {"id": "custom_part", "type": "sequence", "data": {"sequence": seq}},
            {
                "id": "gg-node",
                "type": "goldengate",
                "data": {"enzyme": "BsaI"}
            }
        ],
        "edges": [
            {"source": "custom_part", "target": "gg-node"}
        ]
    }
    
    results = simulate_flow(flow)
    log = results["gg-node"]["log"]
    
    assert any("Valid BsaI site found" in line for line in log)
    assert results["gg-node"]["sequence"] == "AAAATTTTTTTT"


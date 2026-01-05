# import pytest  # commented out to avoid pylint_django import error
from hypercode.simulator import simulate_flow

def test_pcr_simulation_success():
    """Test successful PCR amplification with balanced primers."""
    flow_data = {
        "nodes": [
            {
                "id": "seq1",
                "type": "sequence",
                "data": {"sequence": "ATGCGTACGTTAGCTAGCTAGCTAGCTAGCTAGCGTACGTGC", "label": "Template"}
            },
            {
                "id": "pcr1",
                "type": "pcr",
                "data": {
                    "forwardPrimer": "ATGCGT", # Tm = 18
                    "reversePrimer": "CGTGC" # Tm = 18
                }
            }
        ],
        "edges": [
            {"source": "seq1", "target": "pcr1"}
        ]
    }
    
    results = simulate_flow(flow_data)
    assert "pcr1" in results
    pcr_res = results["pcr1"]
    assert pcr_res["type"] == "amplicon"
    assert pcr_res["sequence"] == "ATGCGTACGTTAGCTAGCTAGCTAGCTAGCTAGCGTACGTGC" # Full seq for this mock
    
    # Check Tm logs
    log_str = "\n".join(pcr_res["log"])
    assert "Forward Primer Tm: 18" in log_str
    assert "Reverse Primer Tm: 18" in log_str
    assert "Recommended Annealing Temp (Ta): 13" in log_str # min(18, 18) - 5
    assert "WARNING" not in log_str

def test_pcr_simulation_tm_mismatch():
    """Test PCR with primers having large Tm difference."""
    flow_data = {
        "nodes": [
            {
                "id": "seq1",
                "type": "sequence",
                "data": {"sequence": "ATGCGTACGTTAGCTAGCTAGCTAGCTAGCTAGCGTACGTGC", "label": "Template"}
            },
            {
                "id": "pcr1",
                "type": "pcr",
                "data": {
                    "forwardPrimer": "AT", # Tm = 4
                    "reversePrimer": "GCACGTGCAC" # Tm much higher
                }
            }
        ],
        "edges": [
            {"source": "seq1", "target": "pcr1"}
        ]
    }
    
    results = simulate_flow(flow_data)
    pcr_res = results["pcr1"]
    log_str = "\n".join(pcr_res["log"])
    assert "WARNING: Primer Tm mismatch" in log_str

def test_pcr_simulation_no_primers():
    """Test PCR passing through template when no primers specified."""
    flow_data = {
        "nodes": [
            {
                "id": "seq1",
                "type": "sequence",
                "data": {"sequence": "ATGC", "label": "Template"}
            },
            {
                "id": "pcr1",
                "type": "pcr",
                "data": {}
            }
        ],
        "edges": [
            {"source": "seq1", "target": "pcr1"}
        ]
    }
    
    results = simulate_flow(flow_data)
    assert results["pcr1"]["sequence"] == "ATGC"
    assert "No primers specified" in results["pcr1"]["log"][0]

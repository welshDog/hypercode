
import pytest
from hypercode.hybrid.crispr_optimizer import optimize_guides
from hypercode.backends.crispr_engine import calculate_mismatch_score

def test_mismatch_scoring():
    s1 = "ATCG" * 5
    s2 = "ATCG" * 5
    assert calculate_mismatch_score(s1, s2) == 0
    
    s3 = "TTCG" + ("ATCG" * 4) # 1 mismatch at start
    assert calculate_mismatch_score(s1, s3) == 1

def test_hybrid_optimization():
    """
    Test the full Hybrid Quantum-Bio workflow.
    Scenario:
    - Genome has regions that resemble Guide A (High Risk).
    - Genome is clean for Guide B and C (Low Risk).
    - We want to select K=2 guides.
    - Expected: Optimizer picks B and C, avoids A.
    """
    
    # 1. Setup Mock Genome
    # "BADBAD..." resembles "AAAAA..." with few mismatches
    # "SAFE..." is totally different
    
    # Let's make it concrete.
    # Guide A: "AAAAAAAAAAAAAAAAAAAA" (20 As)
    # Guide B: "CCCCCCCCCCCCCCCCCCCC" (20 Cs)
    # Guide C: "GGGGGGGGGGGGGGGGGGGG" (20 Gs)
    
    # Genome contains:
    # - A near-match for A (1 mismatch) -> High Off-target Risk
    # - No matches for B or C
    
    genome = (
        "T" * 50 + 
        "AAAAAAAAAAAAAAAAAAA" + "T" + # 19 As + T (1 mismatch vs Guide A)
        "T" * 50
    )
    
    candidates = [
        "A" * 20, # High Risk
        "C" * 20, # Low Risk
        "G" * 20  # Low Risk
    ]
    
    # 2. Run Optimizer (Select Top 2)
    selected = optimize_guides(candidates, genome, k=2, lambda_param=100.0)
    
    # 3. Verify
    # Should pick C and G (Index 1 and 2), avoid A (Index 0)
    assert len(selected) == 2
    assert ("C" * 20) in selected
    assert ("G" * 20) in selected
    assert ("A" * 20) not in selected
    
    print("\nOptimization Success! Avoided high-risk guide.")

if __name__ == "__main__":
    test_hybrid_optimization()

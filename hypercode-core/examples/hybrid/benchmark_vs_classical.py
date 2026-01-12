"""
HyperCode Hybrid Benchmark Suite
Compares the Quantum-Inspired QUBO optimizer against a classical Brute-Force approach
for CRISPR guide selection.

Usage:
    python examples/hybrid/benchmark_vs_classical.py
"""

import time
import random
import itertools
from typing import List, Tuple
from hypercode.hybrid.crispr_optimizer import optimize_guides
from hypercode.backends.crispr_engine import score_off_target_risk

def generate_random_dna(length: int) -> str:
    return "".join(random.choice("ACGT") for _ in range(length))

def classical_brute_force_optimize(candidates: List[str], genome: str, k: int) -> List[str]:
    """
    Finds the absolute best K guides by checking every possible combination.
    Complexity: O(N choose K) - This explodes quickly!
    """
    print(f"[CLASSICAL] Starting Brute Force search (N={len(candidates)}, K={k})...")
    
    # Pre-calculate costs
    costs = {guide: score_off_target_risk(guide, genome) for guide in candidates}
    
    best_combination: tuple = ()
    min_total_risk = float('inf')
    
    # Iterate all combinations
    for combo in itertools.combinations(candidates, k):
        total_risk = sum(costs[g] for g in combo)
        if total_risk < min_total_risk:
            min_total_risk = total_risk
            best_combination = combo
            
    return list(best_combination)

def run_benchmark():
    print("="*60)
    print("🧬 HyperCode Hybrid Benchmark: Quantum-Inspired vs Classical")
    print("="*60)
    
    # 1. Setup Data
    # Create a scenario where N is small enough for brute force to finish, but interesting.
    # N=20 candidates, K=3 selected.
    # 20 choose 3 = 1140 combinations (fast).
    # If we go to N=50, K=5 -> 2M combinations (slower).
    
    print("Generating synthetic genome data...")
    # Target: 500bp
    target_len = 500
    target = generate_random_dna(target_len)
    
    # Inject some valid PAM sites (NGG)
    # Actually, random DNA has plenty of NGGs (~1/16 prob).
    
    # Genome: 10k bp
    genome = generate_random_dna(10000)
    
    # Extract candidates (simulated)
    # In reality we'd parse the target. Here we just pick random 20bp substrings.
    candidates = []
    for _ in range(25):
        start = random.randint(0, len(target)-20)
        candidates.append(target[start:start+20])
        
    k = 3
    print(f"Scenario: Select {k} optimal guides from {len(candidates)} candidates.")
    print("-" * 60)
    
    # 2. Run HyperCode Hybrid (QUBO)
    start_time = time.time()
    qubo_guides = optimize_guides(candidates, genome, k=k)
    qubo_time = time.time() - start_time
    
    qubo_risk = sum(score_off_target_risk(g, genome) for g in qubo_guides)
    
    print(f"\n[QUBO] Time: {qubo_time:.4f}s | Total Risk: {qubo_risk:.2f}")
    
    # 3. Run Classical Brute Force
    start_time = time.time()
    classical_guides = classical_brute_force_optimize(candidates, genome, k=k)
    classical_time = time.time() - start_time
    
    classical_risk = sum(score_off_target_risk(g, genome) for g in classical_guides)
    
    print(f"[CLASSICAL] Time: {classical_time:.4f}s | Total Risk: {classical_risk:.2f}")
    
    # 4. Analysis
    print("-" * 60)
    print("RESULTS:")
    
    # Check if QUBO found the optimal solution
    is_optimal = abs(qubo_risk - classical_risk) < 1e-5
    
    if is_optimal:
        print("✅ QUBO found the optimal solution!")
    else:
        diff = qubo_risk - classical_risk
        print(f"⚠️ QUBO was suboptimal by {diff:.2f} risk units.")
        
    speedup = classical_time / qubo_time
    print(f"🚀 Speedup Factor: {speedup:.2f}x")
    
    if speedup > 1.0:
        print("HyperCode is faster.")
    else:
        print("Classical is faster (expected for small N).")
        
    print("\nNOTE: For small N (candidates < 30), classical is often faster due to overhead.")
    print("      The Quantum Advantage appears as N grows (e.g., N=1000, K=10).")

if __name__ == "__main__":
    run_benchmark()

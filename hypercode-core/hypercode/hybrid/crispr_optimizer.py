"""
CRISPR Optimizer (Hybrid Quantum-Bio)
Formulates the Guide RNA selection problem as a QUBO (Quadratic Unconstrained Binary Optimization) model.
"""

from typing import List, Dict, Tuple
from hypercode.backends.crispr_engine import score_off_target_risk
from hypercode.hybrid.qubo_solver import QuboSolver

def optimize_guides(candidates: List[str], genome_seq: str, k: int = 3, lambda_param: float = 10.0) -> List[str]:
    """
    Selects the optimal K guides from the candidates list using Quantum-Inspired Optimization.
    
    Objective: Minimize Total Off-Target Risk + Penalty for not selecting exactly K guides.
    
    Args:
        candidates: List of candidate gRNA sequences (20bp).
        genome_seq: The reference genome to check off-targets against.
        k: Number of guides to select.
        lambda_param: Penalty weight for the constraint (sum(x) - k)^2.
    """
    
    print(f"[QUBIT] Formulating QUBO for {len(candidates)} candidates (Target K={k})...")
    
    # 1. Calculate Costs (Linear Terms)
    # Each guide has an intrinsic "cost" = off-target risk score
    costs = []
    print("[HELIX] Scoring candidates against genome...")
    for i, guide in enumerate(candidates):
        risk = score_off_target_risk(guide, genome_seq)
        costs.append(risk)
        # print(f"  - Guide {i}: Risk={risk:.2f}")
        
    # 2. Build QUBO Matrix Q
    # Formula: H = sum(cost_i * x_i) + lambda * (sum(x_i) - K)^2
    # Expansion: lambda * (sum(x_i^2) + sum(x_i x_j) - 2K sum(x_i) + K^2)
    # Since x_i is binary, x_i^2 = x_i
    # Linear coeff for x_i: cost_i + lambda(1 - 2K)
    # Quadratic coeff for x_i, x_j: 2 * lambda (if symmetric)
    
    Q: Dict[Tuple[int, int], float] = {}
    n = len(candidates)
    
    for i in range(n):
        # Linear term (diagonal)
        # weight = Original Cost + Penalty Linear Component
        linear_penalty = lambda_param * (1 - 2 * k)
        Q[(i, i)] = costs[i] + linear_penalty
        
        for j in range(i + 1, n):
            # Quadratic term (off-diagonal)
            # The expansion of (sum x_i)^2 includes 2 * x_i * x_j for each pair i < j
            # So the weight for x_i * x_j is 2 * lambda
            weight = 2 * lambda_param
            Q[(i, j)] = weight
            # We use Upper Triangular format, so no Q[(j, i)] needed
            
    # 3. Solve using Quantum/Hybrid Backend
    print(f"[QUBIT] Solving with {n} variables...")
    solver = QuboSolver(use_quantum=True)
    result_state = solver.solve(Q)
    
    # 4. Decode Result
    selected_indices = [i for i, val in result_state.items() if val == 1]
    selected_guides = [candidates[i] for i in selected_indices]
    
    print(f"[QUBIT] Solution found. Selected {len(selected_guides)} guides.")
    return selected_guides

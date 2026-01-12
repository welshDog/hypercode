"""
QUBO Solver for Hybrid Optimization
Provides a unified interface for solving QUBO problems using either:
1. Classical Simulated Annealing (CPU-based fallback)
2. D-Wave Quantum Annealing (QPU-based, requires dwave-ocean-sdk)

Designed to be API-compatible with D-Wave's Ocean SDK (dimod).
"""

import math
import random
import logging
import os
from typing import Dict, Tuple, List, Optional

# Setup logger
logger = logging.getLogger("hypercode.hybrid.solver")

# Try to import D-Wave libraries
try:
    from dwave.system import DWaveSampler, EmbeddingComposite
    # from dimod import BinaryQuadraticModel, Vartype # Unused
    DWAVE_AVAILABLE = True
except ImportError:
    DWAVE_AVAILABLE = False

class SimulatedAnnealer:
    """
    A classical simulated annealing solver for QUBO problems.
    Acts as a placeholder for a real Quantum Annealer (D-Wave).
    """
    
    def __init__(self, steps: int = 1000, initial_temp: float = 10.0, alpha: float = 0.95):
        self.steps = steps
        self.initial_temp = initial_temp
        self.alpha = alpha
        
    def sample_qubo(self, Q: Dict[Tuple[int, int], float]) -> Dict[int, int]:
        """
        Minimizes the objective function: E = x^T Q x
        
        Args:
            Q: A dictionary {(i, j): weight} representing the QUBO matrix.
               Diagonal elements (i, i) are linear biases.
               Off-diagonal elements (i, j) are quadratic couplings.
               
        Returns:
            A dictionary of selected variables {var_index: 0 or 1}
        """
        # 1. Identify all variables
        variables = set()
        for (i, j) in Q.keys():
            variables.add(i)
            variables.add(j)
        variables = sorted(list(variables))
        
        if not variables:
            return {}
            
        # 2. Initialize random state
        state = {v: random.choice([0, 1]) for v in variables}
        current_energy = self._calculate_energy(state, Q)
        best_state = state.copy()
        best_energy = current_energy
        
        # 3. Annealing Loop
        temp = self.initial_temp
        
        for step in range(self.steps):
            # Pick a variable to flip
            v = random.choice(variables)
            
            # Calculate energy change (delta E)
            # Flip
            old_val = state[v]
            new_val = 1 - old_val
            state[v] = new_val
            new_energy = self._calculate_energy(state, Q)
            
            delta_E = new_energy - current_energy
            
            # Metropolis Criterion
            if delta_E < 0 or random.random() < math.exp(-delta_E / temp):
                # Accept change
                current_energy = new_energy
                if current_energy < best_energy:
                    best_energy = current_energy
                    best_state = state.copy()
            else:
                # Reject change (revert)
                state[v] = old_val
                
            # Cool down
            temp *= self.alpha
            
        return best_state
        
    def _calculate_energy(self, state: Dict[int, int], Q: Dict[Tuple[int, int], float]) -> float:
        energy = 0.0
        for (i, j), weight in Q.items():
            if i in state and j in state:
                energy += weight * state[i] * state[j]
        return energy

class QuboSolver:
    """
    Unified solver that attempts to use D-Wave hardware if available/configured,
    falling back to simulated annealing otherwise.
    """
    def __init__(self, use_quantum: bool = True, num_reads: int = 100):
        self.use_quantum = use_quantum
        self.num_reads = num_reads
        self.sim_annealer = SimulatedAnnealer()
        
    def solve(self, Q: Dict[Tuple[int, int], float]) -> Dict[int, int]:
        """
        Solve the QUBO problem Q.
        
        Args:
            Q: Dictionary {(i, j): weight}
            
        Returns:
            Dictionary {var_index: 0 or 1} for the best solution found.
        """
        # Check if we should (and can) use Quantum Backend
        if self.use_quantum and DWAVE_AVAILABLE:
            try:
                return self._solve_quantum(Q)
            except Exception as e:
                logger.warning(f"D-Wave solve failed: {e}. Falling back to simulation.")
                return self._solve_classical(Q)
        else:
            if self.use_quantum and not DWAVE_AVAILABLE:
                logger.info("D-Wave SDK not installed. Using classical simulation.")
            return self._solve_classical(Q)
            
    def _solve_classical(self, Q: Dict[Tuple[int, int], float]) -> Dict[int, int]:
        return self.sim_annealer.sample_qubo(Q)
        
    def _solve_quantum(self, Q: Dict[Tuple[int, int], float]) -> Dict[int, int]:
        if not DWAVE_AVAILABLE:
            raise RuntimeError("D-Wave Ocean SDK not installed")
            
        # Convert Q dictionary to linear/quadratic components for dimod if needed
        # D-Wave's EmbeddingComposite handles the graph embedding automatically
        sampler = EmbeddingComposite(DWaveSampler())
        
        # Q is {(i, j): weight}. 
        # dimod expects a dictionary like this directly for sample_qubo
        response = sampler.sample_qubo(Q, num_reads=self.num_reads)
        
        # Get the best sample (lowest energy)
        best_sample = response.first.sample
        return dict(best_sample)

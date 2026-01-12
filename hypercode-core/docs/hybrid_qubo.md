# Hybrid Quantum-Bio Optimization

HyperCode's Hybrid module uses Quantum Annealing concepts (QUBO) to solve complex biological optimization problems.

## 🧬 Problem: CRISPR Guide Selection
Selecting the best set of Guide RNAs (gRNAs) is a combinatorial optimization problem.
- **Goal**: Select exactly $K$ guides from $N$ candidates.
- **Constraint 1**: Minimize Off-Target effects (minimize risk score).
- **Constraint 2**: Ensure exactly $K$ guides are picked.

## ⚛️ Solution: QUBO Encoding

We map this problem to a Quadratic Unconstrained Binary Optimization (QUBO) model:

$$ E(x) = \sum_{i} a_i x_i + \sum_{i<j} b_{ij} x_i x_j $$

Where $x_i$ is a binary variable (1 if guide $i$ is selected, 0 otherwise).

### Hamiltonian Construction

1.  **Objective Term (Minimize Risk)**:
    $$ H_{obj} = \sum_{i=1}^N \text{Score}(g_i) \cdot x_i $$
    Each guide has a linear cost proportional to its off-target risk.

2.  **Constraint Term (Select K)**:
    We add a penalty $\lambda$ for deviating from $K$ selections:
    $$ H_{constraint} = \lambda (\sum_{i=1}^N x_i - K)^2 $$

    Expanding this square:
    $$ (\sum x_i)^2 - 2K \sum x_i + K^2 $$
    $$ = \sum x_i^2 + 2 \sum_{i<j} x_i x_j - 2K \sum x_i + K^2 $$
    
    Since $x_i^2 = x_i$ for binary variables:
    $$ = \sum x_i + 2 \sum_{i<j} x_i x_j - 2K \sum x_i + K^2 $$
    $$ = (1 - 2K) \sum x_i + 2 \sum_{i<j} x_i x_j + K^2 $$

### Final Coefficients

Combining both terms, the QUBO matrix $Q$ is defined as:

- **Diagonal Terms** ($Q_{ii}$):
  $$ \text{Score}(g_i) + \lambda(1 - 2K) $$

- **Off-Diagonal Terms** ($Q_{ij}$ where $i<j$):
  $$ 2\lambda $$

## 🚀 Solvers

- **SimulatedAnnealer** (Default): A classical implementation of the Metropolis-Hastings algorithm to find the ground state.
- **D-Wave** (Future): The QUBO matrix is compatible with D-Wave's Ocean SDK (`dimod`).

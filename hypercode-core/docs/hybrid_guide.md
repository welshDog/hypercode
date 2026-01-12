# HyperCode Hybrid Quantum-Bio Guide

## Overview

HyperCode's **Hybrid Quantum-Bio Module** enables researchers to leverage quantum computing (and quantum-inspired algorithms) to solve combinatorial biological problems. The flagship application is **CRISPR Guide Optimization**, where selecting the best set of guides to maximize on-target activity while minimizing off-target risk is formulated as a **Quadratic Unconstrained Binary Optimization (QUBO)** problem.

## The `@quantum_crispr` Directive

The `@quantum_crispr` directive is the entry point for this functionality. It abstracts away the complexity of QUBO formulation and quantum hardware interaction.

### Syntax

```hypercode
@quantum_crispr
    target = "TARGET_SEQUENCE_OR_VARIABLE"
    genome = "GENOME_SEQUENCE_OR_PATH"
    num_guides = K
    result -> output_variable
```

- **target**: The DNA sequence you want to edit (or a variable containing it). The optimizer will find all valid Cas9 guide RNAs (20bp + NGG PAM) within this sequence.
- **genome**: The reference genome to check for off-target effects. Can be a sequence string or a path to a FASTA file.
- **num_guides**: The number of optimal guides to select ($K$).
- **result**: The variable where the list of selected guide sequences will be stored.

### How It Works

1. **Candidate Extraction**: The system scans the `target` sequence for all valid NGG PAM sites and extracts upstream 20bp guide sequences.
2. **Risk Scoring**: Each candidate is scored against the `genome` for off-target potential (mismatches) and on-target efficiency.
3. **QUBO Formulation**: A Hamiltonian matrix $H$ is constructed where:
   - **Linear terms** represent the risk/inefficiency of each guide.
   - **Quadratic terms** enforce the constraint that exactly $K$ guides are chosen.
4. **Quantum Annealing**: The problem is sent to a solver (currently a simulated annealer, future D-Wave integration) to find the low-energy state corresponding to the optimal guide set.
5. **Result**: The selected guides are returned to the HyperCode environment.

## Example

```hypercode
@data TargetGene: "ATGCG... (sequence) ...NGG..."
@data Reference: "human_genome_v38.fa"

@quantum_crispr
    target = TargetGene
    genome = Reference
    num_guides = 3
    result -> my_guides

@print my_guides
```

## Configuration

The underlying solver uses Simulated Annealing by default. To configure parameters (like temperature, steps, or switching to real quantum hardware), you currently need to modify the `hypercode/hybrid/qubo_solver.py` module. Future versions will expose these settings via the directive.

## Future Roadmap

- **D-Wave Cloud Integration**: Direct submission of QUBOs to D-Wave QPUs.
- **Protein Folding**: Extending the hybrid module to lattice protein folding problems.
- **Pathway Optimization**: Optimizing metabolic flux using quantum linear systems algorithms (HHL).

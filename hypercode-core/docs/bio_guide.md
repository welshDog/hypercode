# HyperCode Biological Domain Guide

HyperCode now supports molecular biology operations, allowing you to design and simulate DNA manipulation workflows directly in code. This "Bio-MVP" release introduces support for **CRISPR/Cas9 editing** and **PCR amplification**.

## Getting Started

To run bio-programs, use the `molecular` backend:

```bash
python -m hypercode.cli run my_script.hc --backend molecular
```

## Supported Operations

### 1. Defining DNA Sequences

Use the `@data` directive to store DNA sequences. The system automatically validates the sequence (A, T, C, G, N).

```python
@data plasmid: "ATCGATCG..."
@data primer: "AAAAA"
```

### 2. CRISPR/Cas9 Editing

Simulate a CRISPR double-stranded break (DSB) and subsequent Non-Homologous End Joining (NHEJ) repair.

**Syntax:**
```python
@crispr: <target_variable>, "<guide_sequence>", "<pam_motif>"
```

*   **target_variable**: The name of the variable containing the DNA plasmid/genome.
*   **guide_sequence**: The 20bp guide RNA (protospacer) sequence.
*   **pam_motif**: The Protospacer Adjacent Motif (usually "NGG" for SpCas9).

**Example:**
```python
@data gene: "TTTTATCGATCGAGGTTTT"
@crispr: gene, "ATCGATCG", "AGG"
```

**Output:**
The simulator will log:
*   PAM site detection.
*   Cas9 cleavage site (3bp upstream of PAM).
*   Simulated NHEJ repair (indel formation).

### 3. PCR Amplification

Simulate Polymerase Chain Reaction to amplify a specific segment of DNA.

**Syntax:**
```python
@pcr: <template_variable>, "<fwd_primer>", "<rev_primer>"
```

*   **template_variable**: The source DNA.
*   **fwd_primer**: Sequence of the Forward Primer (binds to 3' end of bottom strand).
*   **rev_primer**: Sequence of the Reverse Primer (binds to 3' end of top strand).

**Example:**
```python
@data template: "AAAAACCCCCTTTTT"
@pcr: template, "AAAAA", "AAAAA"
```

**Output:**
The simulator will log:
*   Primer binding sites.
*   Melting temperatures (Tm).
*   Size of the amplified product.
*   Creation of a new variable `<template>_amplicon` containing the product.

## Future Roadmap (Phase 2)

*   **Golden Gate Assembly**: Simulate multi-part assembly using Type IIS restriction enzymes.
*   **Off-Target Analysis**: Predict potential off-target cleavage sites.
*   **Strand Displacement (DSD)**: Simulate DNA strand displacement kinetics.

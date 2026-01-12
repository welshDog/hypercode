# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-01-12

### Added
- **Biological Domain Support (HELIX MVP)**:
  - New `molecular` backend for simulating biological operations.
  - `@crispr` directive: Simulate CRISPR/Cas9 editing with PAM detection and NHEJ repair.
  - `@pcr` directive: Simulate Polymerase Chain Reaction with primer binding and Tm calculation.
  - `docs/bio_guide.md`: Comprehensive guide for using the new bio-features.
  - `examples/bio/`: Ready-to-run examples for CRISPR knockout and PCR amplification.
- **Compiler Enhancements**:
  - `compile_to_v3` now supports bio-nodes (`CrisprEdit`, `PcrReaction`), enabling future visual editor integration.
- **Testing**:
  - Achieved 93% test coverage for the `crispr_engine`.
  - Full integration tests for bio-workflows.

## [0.1.0] - 2025-12-30

### Added
- **HyperCode Parser v0**: Custom Recursive Descent Parser supporting `@data`, `@set`, `@print`, `@check`, and `@quantum` statements.
- **Quantum Circuit Support**:
  - `@quantum` block syntax for circuit declarations.
  - Supported gates: `H`, `X`, `Y`, `Z`, `CX`, `CZ`, `RX`, `RY`, `RZ`.
  - `MEASURE` operation with target variables.
  - Support for inline numeric parameters (e.g., `RZ(3.14)`) and variable expressions (e.g., `RZ(PI/2)`).
- **Qiskit Backend**:
  - Seamless integration with Qiskit for quantum circuit execution.
  - Automatic detection of `AerSimulator` for high-performance simulation.
  - Fallback to basic simulators if Aer is not present.
  - Support for `shots` and `seed` configuration.
- **CLI**:
  - `hypercode run` command for executing files.
  - `hypercode quantum run` subcommand with specific quantum options.
  - `hypercode parse` command for inspecting the AST.
  - `hypercode qir` command for viewing the Intermediate Representation.
- **Neurodivergent-First Features**:
  - Line-based syntax for readability.
  - Minimal tooling overhead (no heavy Java/ANTLR dependencies required for runtime).
  - Clear error messages.

### Changed
- Initial release of the HyperCode vertical slice (v0).

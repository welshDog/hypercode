# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2026-01-11

### Added
- **V3 Syntax Engine**:
  - Full support for V3 syntax (`@circuit`, `@init`, `@gate`).
  - Strict type checking in Parser and Compiler.
  - Neurodivergent-friendly explicit register declarations (`QReg`, `CReg`).
- **Core Pipeline**:
  - **Parser**: Rewritten for strict V3 compliance.
  - **Compiler**: Now auto-detects domains (`#:domain quantum` vs `molecular`).
  - **Evaluator**: Full QIR lowering and execution support.
- **Integration**:
  - Green integration tests for the full HyperFlow -> Compiler -> Execution loop.

## [0.2.0-alpha] - 2026-01-05

### Added
- **Production Golden Gate Engine**:
  - Multi-enzyme support (BsaI, BbsI, SapI).
  - Dynamic Type IIS cut-site calculation.
  - Comprehensive validation test suite.
- **Accessibility Features**:
  - **Dyslexia Mode**: Toggle via `Shift + D` or UI button.
  - High-legibility font stack (Comic Sans MS, Chalkboard SE).
  - Enhanced line-height (1.8) and letter-spacing (0.05em).
- **Architecture**:
  - Separated `hypercode-core` and `hyperflow-editor`.
  - Archived legacy code (V1/V2) to `archive/`.

### Changed
- Refactored `bio_utils.py` to be the single source of truth for biological constants.
- Updated project version to `0.2.0-alpha`.

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

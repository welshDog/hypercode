# HyperCode Backend System Refactoring Report

**Date:** 30 December 2025
**Author:** Gemini AI Assistant

## 1. Objective

The primary objective of this task was to refactor the HyperCode interpreter to support a pluggable, multi-backend architecture. This work aligns with the project's vision of being "multi-backend capable" (Roadmap Phases 2.3, 2.6, 2.7). The goal was to decouple the core interpreter from any specific execution environment (like Qiskit), making the system extensible for future classical, quantum, and molecular backends.

## 2. Summary of Architectural Changes

Previously, the `Evaluator` was hardcoded to call a specific `run_qiskit` function, tightly coupling the interpreter to the Qiskit library.

This has been refactored into a backend-agnostic system. The core of this new architecture is a `BaseBackend` abstract class which defines a common interface that all backends must implement. A central registry has been introduced to dynamically discover and load these backends by name. The `Evaluator`, as well as the high-level `API` and `CLI`, have been updated to use this new, flexible system.

## 3. Detailed File Changes

The following changes were made to the codebase:

- **`NEW` `hypercode/backends/base.py`**
  - This file defines the `BaseBackend` abstract base class. It mandates that any concrete backend implementation must provide an `execute(ir_module, ...)` method. This contract ensures that the interpreter can interact with any backend in a uniform way.

- **`NEW` `hypercode/backends/__init__.py`**
  - This file acts as a central registry for all available backends. It contains a `BACKEND_REGISTRY` dictionary that maps backend names (e.g., `"qiskit"`) to their corresponding classes. A factory function, `get_backend(name)`, was also created to provide a single, safe point for instantiating backends.

- **`MODIFIED` `hypercode/backends/qiskit_backend.py`**
  - The existing `QiskitBackend` class was refactored to inherit from `BaseBackend`.
  - The `run()` method was renamed to `execute()` to conform to the new interface.
  - Redundant standalone functions (`run_qiskit`, `to_qiskit`) were removed, encapsulating all Qiskit-related logic within the class itself.

- **`MODIFIED` `hypercode/interpreter/evaluator.py`**
  - The `Evaluator` was decoupled from Qiskit. It no longer calls `run_qiskit` directly.
  - The constructor was changed to accept a `backend_name` string instead of a boolean flag. It now uses the `get_backend` factory to retrieve the appropriate backend instance.
  - When executing a quantum circuit, it now calls the generic `self.backend.execute(...)` method.

- **`MODIFIED` `hypercode/api.py` & `hypercode/cli.py`**
  - Both the high-level programmatic API and the command-line interface were updated to pass the user's backend choice (as a string) to the `Evaluator`'s new constructor, completing the chain from user input to backend execution.

## 4. Architectural Outcome & Benefits

This refactoring has resulted in a significantly more robust and extensible architecture.

- **Decoupling:** The interpreter is no longer aware of the implementation details of Qiskit or any other specific library.
- **Extensibility:** Adding a new backend is now a clean and straightforward process:
  1. Create a new backend class that inherits from `BaseBackend`.
  2. Implement the required `execute()` method.
  3. Register the new class in `hypercode/backends/__init__.py`.

The interpreter will be able to use the new backend immediately without any further modifications.

## 5. Recommendations

- **Immediate:** It is critical to run the project's full test suite (`pytest`) to verify that this major refactoring has not introduced any regressions in functionality.
- **Next Step:** A great way to validate this new architecture would be to immediately start on the **Classical Backend** (Roadmap Phase 2.6). By creating a simple `ClassicalBackend` class that processes the IR for classical operations, you can prove the success and flexibility of the new pluggable system.

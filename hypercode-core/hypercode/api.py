"""
This module provides the primary programmatic API for executing HyperCode.
"""

from typing import Optional

from hypercode.parser.parser import parse
from hypercode.interpreter.evaluator import Evaluator
from hypercode.ir.type_checker import TypeChecker
from hypercode.results import ExecutionResult


def execute(
    code_string: str,
    backend_name: str = "qiskit",
    shots: int = 1024,
    seed: Optional[int] = None,
) -> ExecutionResult:
    """
    Parses, evaluates, and executes a string of HyperCode.

    This is the primary entry point for using HyperCode as a library.

    Args:
        code_string: A string containing the HyperCode program.
        backend_name: The name of the backend to use for execution (e.g., "qiskit").
        shots: The number of shots to use in the quantum simulation.
        seed: The random seed for the quantum simulator.

    Returns:
        An ExecutionResult object containing the results, AST, QIR, and any errors.
    """
    try:
        # 1. Parse the source code into an AST
        program_ast = parse(code_string)

        # 2. Type Check
        type_checker = TypeChecker()
        type_errors = type_checker.check_program(program_ast)
        
        if type_errors:
            # For now, just raise the first error as an exception
            # In the future, we might want to return multiple errors in the result
            raise Exception(f"Type checking failed:\n{type_checker.report()}")

        # 3. Set up and run the evaluator
        evaluator = Evaluator(
            backend_name=backend_name,
            shots=shots,
            seed=seed,
        )
        evaluator.evaluate(program_ast)

        # 3. Package the results
        # The 'result' is the final state of the interpreter's variables.
        return ExecutionResult(
            result=evaluator.variables,
            ast=program_ast,
            qir=evaluator.qir,
        )

    except Exception as e:
        # If any step fails, return an ExecutionResult with the error
        return ExecutionResult(
            result=None,
            ast=None,
            qir=None,
            error=str(e),
        )

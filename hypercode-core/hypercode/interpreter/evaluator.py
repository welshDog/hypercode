"""
HyperCode Evaluator Module

This module provides the core evaluation logic for the HyperCode language,
including quantum circuit execution and classical program evaluation.
"""

from typing import Dict, Any, Optional, Union, List, cast

from hypercode.ast.nodes import (
    Program, Statement, DataDecl, SetStmt, PrintStmt, CheckStmt, Block,
    Expr, Literal, Variable, BinaryOp, QuantumOp,
    QuantumCircuitDecl, QGate, QMeasure, Node
)
from hypercode.ir.lower_quantum import lower_circuit
from hypercode.ir.qir_nodes import QModule, QIR, QInstr
from hypercode.backends import get_backend, Backend
from hypercode.results import ExecutionResult


def run_qiskit(module: Union[QModule, QIR], shots: int = 1024, seed: Optional[int] = None) -> Dict[str, int]:
    """
    Execute a QIR module using the Qiskit backend.
    
    This is a convenience function that creates a temporary Qiskit backend and executes
    the given QIR module.
    
    Args:
        module: The QIR module or QIR object to execute
        shots: Number of shots to run the circuit for
        seed: Optional random seed for reproducibility
        
    Returns:
        Dictionary mapping measurement targets to counts
    """
    from hypercode.backends.qiskit_backend import QiskitBackend
    
    # If we get a QIR object, use its first module
    if isinstance(module, QIR):
        if not module.modules:
            raise ValueError("QIR contains no modules to execute")
        module = next(iter(module.modules.values()))
    
    backend = QiskitBackend()
    return backend.execute(module, shots=shots, seed=seed)

class Evaluator:
    def __init__(
        self, 
        backend_name: str = "qiskit", 
        shots: int = 1024, 
        seed: Optional[int] = None, 
        use_quantum_sim: bool = True
    ) -> None:
        """Initialize the HyperCode evaluator with the specified backend and configuration.
        
        The evaluator maintains an environment of variables and can execute both classical
        and quantum operations based on the provided backend.

        Args:
            backend_name: Name of the backend to use ("qiskit", "molecular", etc.)
            shots: Number of shots to run quantum circuits for
            seed: Optional random seed for reproducibility
            use_quantum_sim: Whether to use a quantum simulator (for backward compatibility with tests)
            
        Example:
            >>> evaluator = Evaluator(backend_name="qiskit", shots=1000)
            >>> evaluator.evaluate(ast)  # Evaluate an AST
        """
        self.variables: Dict[str, Any] = {}
        self.output: List[str] = []
        self.qir: Optional[QIR] = None  # To store the last generated QIR
        self.backend: Optional[Backend] = None
        self.shots = shots
        self.seed = seed
        
        # For backward compatibility with tests
        if not use_quantum_sim:
            backend_name = "classical"
        
        # Instantiate the backend if not in classical mode
        if backend_name != "classical":
            try:
                self.backend = get_backend(backend_name)
            except ValueError as e:
                print(f"Warning: {e}")

    def evaluate(self, node: Program) -> None:
        """Evaluate a complete program by executing each statement in sequence.
        
        Args:
            node: The root Program node containing statements to execute
            
        Raises:
            RuntimeError: If there's an error during evaluation
        """
        try:
            for stmt in node.statements:
                self.execute(stmt)
        except Exception as e:
            raise RuntimeError(f"Error during evaluation: {e}") from e

    def execute(self, stmt: Statement) -> None:
        """Execute a single statement in the current evaluation context.
        
        Args:
            stmt: The statement to execute
            
        Raises:
            NameError: If a variable is referenced before assignment
            ValueError: If there's an error in statement execution
        """
        try:
            if isinstance(stmt, DataDecl):
                value = self.evaluate_expr(stmt.value)
                self.variables[stmt.name] = value
                
            elif isinstance(stmt, SetStmt):
                if stmt.name not in self.variables:
                    raise NameError(
                        f"Variable '{stmt.name}' not defined. Use @data to define it first."
                    )
                value = self.evaluate_expr(stmt.value)
                self.variables[stmt.name] = value
                
            elif isinstance(stmt, PrintStmt):
                value = self.evaluate_expr(stmt.expr)
                output = str(value)
                print(output)
                self.output.append(output)
                
            elif isinstance(stmt, CheckStmt):
                condition = self.evaluate_expr(stmt.condition)
                if condition:
                    self.execute_block(stmt.true_block)
                elif stmt.false_block:
                    self.execute_block(stmt.false_block)
                    
            elif isinstance(stmt, QuantumCircuitDecl):
                self._execute_quantum_circuit(stmt)
                
            else:
                raise ValueError(f"Unsupported statement type: {type(stmt).__name__}")
                
        except Exception as e:
            # Add context to error messages
            if not isinstance(e, (NameError, ValueError)):
                raise ValueError(f"Error executing statement: {e}") from e
            raise
                
    def _execute_quantum_circuit(self, stmt: QuantumCircuitDecl) -> None:
        """Execute a quantum circuit declaration.
        
        This internal method handles the execution of quantum circuits,
        including lowering to QIR and backend execution.
        
        Args:
            stmt: The quantum circuit statement to execute
            
        Raises:
            RuntimeError: If there's an error during quantum execution
        """
        msg = f"QuantumCircuit {stmt.name}: {stmt.qubits} qubits, {len(stmt.ops)} ops"
        print(msg)
        self.output.append(msg)
        
        try:
            # Collect constants for lowering
            constants = {
                k: v for k, v in self.variables.items() 
                if isinstance(v, (int, float))
            }
            
            # Lower the quantum circuit to QModule
            module = lower_circuit(stmt, constants=constants)
            
            # Store the module in variables for reference
            self.variables[stmt.name] = module
            
            # Wrap in QIR for consistency/storage
            qir = QIR(modules={module.name: module})
            self.qir = qir
            
            # Execute using the backend if available
            if self.backend is not None:
                # Execute using the backend directly
                result = self.backend.execute(module, shots=self.shots, seed=self.seed)
                
                # Store results in variables
                self.variables[f"{stmt.name}_results"] = result
                
                # Print and store the results
                result_str = ", ".join(f"{k}: {v}" for k, v in result.items())
                print(f"Results: {result_str}")
                self.output.append(f"Results: {result_str}")
                
        except Exception as e:
            error_msg = f"Error executing quantum circuit: {e}"
            print(error_msg)
            self.output.append(f"ERROR: {error_msg}")
            raise RuntimeError(error_msg) from e

    def execute_block(self, block: Block) -> None:
        """Execute a block of statements in sequence.
        
        Args:
            block: The block containing statements to execute
        """
        for stmt in block.statements:
            self.execute(stmt)

    def evaluate_expr(self, expr: Expr) -> Any:
        """Evaluate an expression in the current context.
        
        Args:
            expr: The expression to evaluate
            
        Returns:
            The result of the evaluation
            
        Raises:
            NameError: If a variable is not defined
            ValueError: For unsupported operations or expression types
            TypeError: For type mismatches in operations
        """
        if isinstance(expr, Literal):
            return expr.value
            
        elif isinstance(expr, Variable):
            if expr.name not in self.variables:
                raise NameError(f"Variable '{expr.name}' not defined")
            return self.variables[expr.name]
            
        elif isinstance(expr, BinaryOp):
            left = self.evaluate_expr(expr.left)
            right = self.evaluate_expr(expr.right)
            
            # Type checking for numeric operations
            if expr.op in {"+", "-", "*", "/", "<", "<=", ">", ">="}:
                if not (isinstance(left, (int, float)) and isinstance(right, (int, float))):
                    raise TypeError(
                        f"Operator '{expr.op}' requires numeric operands, "
                        f"got {type(left).__name__} and {type(right).__name__}"
                    )
            
            # Perform the operation
            if expr.op == "+":
                return left + right
            elif expr.op == "-":
                return left - right
            elif expr.op == "*":
                return left * right
            elif expr.op == "/":
                if right == 0:
                    raise ValueError("Division by zero")
                return left / right
            elif expr.op == "==":
                return left == right
            elif expr.op == "!=":
                return left != right
            elif expr.op == "<":
                return left < right
            elif expr.op == "<=":
                return left <= right
            elif expr.op == ">":
                return left > right
            elif expr.op == ">=":
                return left >= right
            elif expr.op == "and":
                return bool(left and right)
            elif expr.op == "or":
                return bool(left or right)
            else:
                raise ValueError(f"Unsupported operator: {expr.op}")
                
        else:
            raise ValueError(f"Unsupported expression type: {type(expr).__name__}")

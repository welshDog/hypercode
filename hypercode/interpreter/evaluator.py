from typing import Dict, Any, Optional
from hypercode.ast.nodes import (
    Program, Statement, DataDecl, SetStmt, PrintStmt, CheckStmt, Block,
    Expr, Literal, Variable, BinaryOp,
    QuantumCircuitDecl, QGate, QMeasure
)
from hypercode.ir.lower_quantum import lower_circuit
from hypercode.backends.qiskit_backend import run_qiskit

class Evaluator:
    def __init__(self, use_quantum_sim: bool = True, shots: int = 1024, seed: Optional[int] = None):
        self.variables: Dict[str, Any] = {}
        self.output: list[str] = []
        self.qir: Optional[Any] = None  # To store the last generated QIR
        self.use_quantum_sim = use_quantum_sim
        self.shots = shots
        self.seed = seed

    def evaluate(self, node: Program):
        for stmt in node.statements:
            self.execute(stmt)

    def execute(self, stmt: Statement):
        if isinstance(stmt, DataDecl):
            value = self.evaluate_expr(stmt.value)
            self.variables[stmt.name] = value
        elif isinstance(stmt, SetStmt):
            if stmt.name not in self.variables:
                raise NameError(f"Variable '{stmt.name}' not defined. Use @data to define it first.")
            value = self.evaluate_expr(stmt.value)
            self.variables[stmt.name] = value
        elif isinstance(stmt, PrintStmt):
            value = self.evaluate_expr(stmt.expr)
            print(value)
            self.output.append(str(value))
        elif isinstance(stmt, CheckStmt):
            condition = self.evaluate_expr(stmt.condition)
            if condition:
                self.execute_block(stmt.true_block)
            elif stmt.false_block:
                self.execute_block(stmt.false_block)
        elif isinstance(stmt, QuantumCircuitDecl):
            msg = f"QuantumCircuit {stmt.name}: {stmt.qubits} qubits, {len(stmt.ops)} ops"
            print(msg)
            self.output.append(msg)
            
            # Lower and Run if requested
            if self.use_quantum_sim:
                try:
                    # Collect constants for lowering
                    constants = {k: v for k, v in self.variables.items() if isinstance(v, (int, float))}
                    
                    ir_module = lower_circuit(stmt, constants)
                    self.qir = ir_module  # Store the generated QIR
                    results = run_qiskit(ir_module, shots=self.shots, seed=self.seed)
                    
                    if results:
                        res_msg = f"Results ({stmt.name}): {results}"
                        print(res_msg)
                        self.output.append(res_msg)
                        self.variables[f"{stmt.name}_results"] = results
                    else:
                        print(f"(No results from {stmt.name} or Qiskit missing)")
                        
                except Exception as e:
                    err_msg = f"Quantum Execution Failed: {e}"
                    print(err_msg)
                    self.output.append(err_msg)
            
            self.variables[stmt.name] = stmt
        else:
            raise NotImplementedError(f"Unknown statement type: {type(stmt)}")

    def execute_block(self, block: Block):
        for stmt in block.statements:
            self.execute(stmt)

    def evaluate_expr(self, expr: Expr) -> Any:
        if isinstance(expr, Literal):
            return expr.value
        elif isinstance(expr, Variable):
            if expr.name not in self.variables:
                raise NameError(f"Undefined variable: {expr.name}")
            return self.variables[expr.name]
        elif isinstance(expr, BinaryOp):
            left = self.evaluate_expr(expr.left)
            right = self.evaluate_expr(expr.right)
            if expr.op == '+':
                return left + right
            elif expr.op == '-':
                return left - right
            elif expr.op == '*':
                return left * right
            elif expr.op == '/':
                return left / right
            elif expr.op == '>':
                return left > right
            elif expr.op == '<':
                return left < right
            elif expr.op == '==':
                return left == right
            else:
                raise NotImplementedError(f"Unknown operator: {expr.op}")
        else:
            raise NotImplementedError(f"Unknown expression type: {type(expr)}")

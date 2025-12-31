from typing import List, Dict, Any, Optional
from hypercode.ast.nodes import (
    QuantumCircuitDecl, QGate as AstQGate, QMeasure as AstQMeasure,
    Expr, Literal, Variable, BinaryOp
)
from hypercode.ir.qir_nodes import (
    QModule, QInstr, QAlloc, QGate as IrQGate, QMeasure as IrQMeasure, QEnd
)
import math

class QuantumLowerer:
    def __init__(self, constants: Optional[Dict[str, Any]] = None):
        self.constants: Dict[str, Any] = constants or {}
        # Default constants
        if 'PI' not in self.constants:
            self.constants['PI'] = math.pi
            self.constants['pi'] = math.pi

    def lower(self, node: QuantumCircuitDecl) -> QModule:
        instrs: List[QInstr] = []
        
        # 1. Allocate qubits
        # We assume linear allocation from 0 to node.qubits - 1
        instrs.append(QAlloc(start_index=0, count=node.qubits))
        
        # 2. Lower operations
        for op in node.ops:
            if isinstance(op, AstQGate):
                # Evaluate parameters to floats
                # In a real compiler, we might keep them as symbolic if they are runtime variables
                # For this v0, we try to resolve to constant floats.
                resolved_params = []
                for p in op.params:
                    val = self.evaluate_const_expr(p)
                    resolved_params.append(val)
                
                instrs.append(IrQGate(
                    name=op.name,
                    qubits=op.qubits,
                    params=resolved_params
                ))
            elif isinstance(op, AstQMeasure):
                target = op.target if op.target is not None else f"c{op.qubit}"
                instrs.append(IrQMeasure(
                    qubit=op.qubit,
                    target=target
                ))
        
        # 3. End
        instrs.append(QEnd())
        
        return QModule(name=node.name, instructions=instrs)

    def evaluate_const_expr(self, expr: Expr) -> float:
        if isinstance(expr, Literal):
            return float(expr.value)
        elif isinstance(expr, Variable):
            if expr.name in self.constants:
                return float(self.constants[expr.name])
            raise ValueError(f"Unknown constant variable '{expr.name}' during IR lowering. (Runtime variables not yet supported in gate params for v0 IR)")
        elif isinstance(expr, BinaryOp):
            left = self.evaluate_const_expr(expr.left)
            right = self.evaluate_const_expr(expr.right)
            if expr.op == '+': return left + right
            if expr.op == '-': return left - right
            if expr.op == '*': return left * right
            if expr.op == '/': return left / right
            raise ValueError(f"Unsupported binary operator '{expr.op}' in constant expression")
        else:
            raise ValueError(f"Unsupported expression type '{type(expr)}' in gate parameter")

def lower_circuit(circuit: QuantumCircuitDecl, constants: Optional[Dict[str, Any]] = None) -> QModule:
    lowerer = QuantumLowerer(constants)
    return lowerer.lower(circuit)

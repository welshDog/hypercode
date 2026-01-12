from typing import List, Dict, Any, Optional
from hypercode.ast.nodes import (
    QuantumCircuitDecl, QGate as AstQGate, QMeasure as AstQMeasure,
    Expr, Literal, Variable, BinaryOp, QRegDecl, QubitRef
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
        
        # 1. Allocate qubits based on QRegDecl statements
        # Map register name to start index
        reg_map: Dict[str, int] = {}
        total_qubits = 0
        
        # Scan for registers first
        for stmt in node.body:
            if isinstance(stmt, QRegDecl) and stmt.is_quantum:
                reg_map[stmt.name] = total_qubits
                total_qubits += stmt.size
        
        # Allocate all qubits in one block (simplification for QIR v0)
        instrs.append(QAlloc(start_index=0, count=total_qubits))
        
        # 2. Lower operations
        for stmt in node.body:
            if isinstance(stmt, AstQGate):
                # Resolve parameters
                resolved_params = []
                for p in stmt.params:
                    val = self.evaluate_const_expr(p)
                    resolved_params.append(val)
                
                # Resolve qubits
                resolved_qubits = []
                for qref in stmt.qubits:
                    idx = self._resolve_qubit(qref, reg_map)
                    resolved_qubits.append(idx)
                
                # Resolve gate name
                gate_name = stmt.name.lower()
                if gate_name == 'hadamard':
                    gate_name = 'h'
                elif gate_name == 'cnot':
                    gate_name = 'cx'
                elif gate_name == 'phase':
                    gate_name = 'p' # Or rz? Phase usually is u1 or p. Qiskit has p.
                
                instrs.append(IrQGate(
                    name=gate_name,
                    qubits=resolved_qubits,
                    params=resolved_params
                ))
            elif isinstance(stmt, AstQMeasure):
                # Resolve qubit
                q_idx = self._resolve_qubit(stmt.qubit, reg_map)
                
                # Resolve target (classical register)
                # For now, just use string representation of target
                if stmt.target.index != -1:
                    target = f"{stmt.target.register}[{stmt.target.index}]"
                else:
                    target = stmt.target.register
                
                instrs.append(IrQMeasure(
                    qubit=q_idx,
                    target=target
                ))
        
        # 3. End
        instrs.append(QEnd())
        
        return QModule(name=node.name, instructions=instrs)

    def _resolve_qubit(self, ref: QubitRef, reg_map: Dict[str, int]) -> int:
        if ref.register not in reg_map:
            raise ValueError(f"Unknown quantum register '{ref.register}'")
        
        base = reg_map[ref.register]
        offset = ref.index
        if offset == -1:
            # Handle whole register operations? For now, assume index 0 if not specified?
            # Or raise error if strict. bell_pair.hc uses explicit indices.
            offset = 0 
            
        return base + offset


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

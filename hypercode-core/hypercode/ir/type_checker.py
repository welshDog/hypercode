"""
HyperCode Type Checker

Validates types throughout the AST and IR.
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from .types import *
from hypercode.ast.nodes import *
from hypercode.errors import HyperCodeError

# ============================================================================
# ERROR TYPES
# ============================================================================

@dataclass
class TypeError(HyperCodeError):
    """Type mismatch error"""
    message: str
    line: int
    col: int
    expected: BaseType
    actual: BaseType
    suggestion: str = ""
    
    def __str__(self) -> str:
        msg = f"TypeError (line {self.line}, col {self.col}):\n"
        msg += f"  {self.message}\n"
        msg += f"  Expected: {self.expected}\n"
        msg += f"  Got: {self.actual}"
        if self.suggestion:
            msg += f"\n  💡 {self.suggestion}"
        return msg

@dataclass
class UndefinedVariableError(HyperCodeError):
    """Undefined variable error"""
    var_name: str
    line: int
    col: int
    
    def __str__(self) -> str:
        return f"NameError (line {self.line}, col {self.col}): Undefined variable '{self.var_name}'"

@dataclass
class GateArityError(HyperCodeError):
    """Wrong number of arguments to gate"""
    gate_name: str
    expected: int
    actual: int
    line: int
    col: int
    
    def __str__(self) -> str:
        return (
            f"GateError (line {self.line}, col {self.col}): "
            f"Gate '{self.gate_name}' takes {self.expected} qubit(s), "
            f"got {self.actual}"
        )

# ============================================================================
# TYPE CHECKER
# ============================================================================

class TypeChecker:
    """Main type checking class"""
    
    def __init__(self):
        self.symbols: Dict[str, BaseType] = {}
        self.errors: List[HyperCodeError] = []
        self.warnings: List[str] = []
    
    # ========================================================================
    # MAIN CHECKING METHODS
    # ========================================================================
    
    def check_program(self, program: 'QuantumCircuitDecl') -> List[HyperCodeError]:
        """Check entire program"""
        self.symbols = {}
        self.errors = []
        
        # Check all statements
        for stmt in program.body:
            self.check_statement(stmt)
        
        return self.errors
    
    def check_statement(self, stmt: 'Statement') -> None:
        """Check a single statement"""
        if isinstance(stmt, QRegDecl):
            if stmt.is_quantum:
                self.check_qreg_decl(stmt)
            else:
                self.check_creg_decl(stmt)
        elif isinstance(stmt, QGate):
            self.check_gate_statement(stmt)
        elif isinstance(stmt, QMeasure):
            self.check_measure_statement(stmt)
    
    # ========================================================================
    # VARIABLE CHECKING
    # ========================================================================
    
    def check_qreg_decl(self, decl: 'QRegDecl') -> None:
        """Check quantum register declaration"""
        # q = QReg(size)
        self.symbols[decl.name] = QubitArrayType(decl.size)
    
    def check_creg_decl(self, decl: 'QRegDecl') -> None:
        """Check classical register declaration"""
        # c = CReg(size)
        self.symbols[decl.name] = BitArrayType(decl.size)
    
    # ========================================================================
    # GATE CHECKING
    # ========================================================================
    
    def check_gate_statement(self, stmt: 'QGate') -> None:
        """Check gate statement"""
        gate_name = stmt.name.lower()
        
        # Get expected arity
        arity = self.gate_arity(gate_name)
        if arity is None:
            # Maybe it's a custom gate or we should warn?
            # For now, let's just warn or ignore if unknown
            # self.warnings.append(f"Unknown gate: {gate_name}")
            return
        
        # Check qubit count
        actual_arity = len(stmt.qubits)
        if actual_arity != arity:
            self.errors.append(GateArityError(
                gate_name=gate_name,
                expected=arity,
                actual=actual_arity,
                line=getattr(stmt, 'line', 0),
                col=getattr(stmt, 'col', 0)
            ))
        
        # Check qubit types
        for qubit in stmt.qubits:
            self.check_qubit_reference(qubit)
        
        # Check parameters (angles, etc.)
        if stmt.params:
            for param in stmt.params:
                # TODO: Implement expression type inference properly
                # For now, assume if it's there it's likely numeric
                pass

    def check_measure_statement(self, stmt: 'QMeasure') -> None:
        """Check measurement statement"""
        # Check qubit reference
        self.check_qubit_reference(stmt.qubit)
        
        # Check bit reference
        self.check_bit_reference(stmt.target)
    
    def check_qubit_reference(self, qubit: 'QubitRef') -> None:
        """Check if qubit is defined"""
        base_name = qubit.register
        
        if base_name not in self.symbols:
            self.errors.append(UndefinedVariableError(
                var_name=base_name,
                line=0,
                col=0
            ))
        else:
            var_type = self.symbols[base_name]
            if not is_qubit_type(var_type):
                self.errors.append(TypeError(
                    message=f"Expected qubit, got {var_type}",
                    line=0,
                    col=0,
                    expected=QubitType(),
                    actual=var_type
                ))
    
    def check_bit_reference(self, bit: 'QubitRef') -> None:
        """Check if bit is defined"""
        base_name = bit.register
        
        if base_name not in self.symbols:
            self.errors.append(UndefinedVariableError(
                var_name=base_name,
                line=0,
                col=0
            ))
        else:
            var_type = self.symbols[base_name]
            if not is_bit_type(var_type):
                self.errors.append(TypeError(
                    message=f"Expected bit, got {var_type}",
                    line=0,
                    col=0,
                    expected=BitType(),
                    actual=var_type
                ))
    
    # ========================================================================
    # TYPE UTILITIES
    # ========================================================================
    
    def gate_arity(self, gate_name: str) -> Optional[int]:
        """Get arity of gate"""
        single_qubit = ['h', 'hadamard', 'x', 'pauli_x', 'y', 'pauli_y', 
                       'z', 'pauli_z', 't', 't_gate', 's', 's_gate', 'measure']
        two_qubit = ['cx', 'cnot', 'swap', 'cphase', 'cz']
        three_qubit = ['ccx', 'toffoli']
        
        if gate_name in single_qubit:
            return 1
        elif gate_name in two_qubit:
            return 2
        elif gate_name in three_qubit:
            return 3
        elif gate_name in ['rx', 'ry', 'rz', 'p', 'phase']:  # Parameterized
            return 1  # +1 param
        else:
            return None
    
    # ========================================================================
    # REPORTING
    # ========================================================================
    
    def report(self) -> str:
        """Generate error report"""
        if not self.errors:
            return "✅ Type checking passed!"
        
        report = f"❌ {len(self.errors)} type error(s):\n\n"
        for i, error in enumerate(self.errors, 1):
            report += f"{i}. {error}\n\n"
        
        if self.warnings:
            report += f"\n⚠️  {len(self.warnings)} warning(s):\n"
            for warning in self.warnings:
                report += f"  - {warning}\n"
        
        return report

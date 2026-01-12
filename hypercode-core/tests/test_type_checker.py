"""
Type Checker Tests

Comprehensive test suite for type validation.
"""

import pytest
from hypercode.ir.type_checker import TypeChecker, TypeError, UndefinedVariableError, GateArityError
from hypercode.ir.types import *
from hypercode.ast.nodes import *

class TestTypeSystem:
    """Basic type system tests"""
    
    def test_qubit_type(self):
        assert QubitType() == QubitType()
        assert str(QubitType()) == "QubitType"
    
    def test_qubit_array_type(self):
        t1 = QubitArrayType(5)
        t2 = QubitArrayType(5)
        assert t1 == t2
        assert str(t1) == "qubit[5]"
    
    def test_type_compatibility(self):
        assert are_compatible(IntType(), IntType())
        assert are_compatible(AnyType(), IntType())
        assert not are_compatible(IntType(), QubitType())

class TestTypeChecker:
    """Type checker tests"""
    
    def test_valid_qreg(self):
        """Valid QReg declaration"""
        checker = TypeChecker()
        decl = QRegDecl(name="q", size=2)
        checker.check_statement(decl)
        assert "q" in checker.symbols
        assert checker.symbols["q"] == QubitArrayType(2)
        assert len(checker.errors) == 0

    def test_valid_creg(self):
        """Valid CReg declaration"""
        checker = TypeChecker()
        decl = QRegDecl(name="c", size=2, is_quantum=False)
        checker.check_statement(decl)
        assert "c" in checker.symbols
        assert checker.symbols["c"] == BitArrayType(2)
        assert len(checker.errors) == 0
    
    def test_undefined_variable(self):
        """Catch undefined variables in gate"""
        checker = TypeChecker()
        # H q[0] where q is not defined
        gate = QGate(name="h", qubits=[QubitRef("q", 0)], params=[])
        checker.check_statement(gate)
        assert len(checker.errors) == 1
        assert isinstance(checker.errors[0], UndefinedVariableError)
    
    def test_gate_arity_error(self):
        """Catch wrong gate arity"""
        checker = TypeChecker()
        # q = QReg(2)
        checker.check_statement(QRegDecl(name="q", size=2))
        
        # CX q[0] (needs 2)
        gate = QGate(name="cx", qubits=[QubitRef("q", 0)], params=[])
        checker.check_statement(gate)
        
        assert len(checker.errors) == 1
        assert isinstance(checker.errors[0], GateArityError)
        assert checker.errors[0].expected == 2
        assert checker.errors[0].actual == 1
    
    def test_gate_arity_success(self):
        """Correct gate arity"""
        checker = TypeChecker()
        checker.check_statement(QRegDecl(name="q", size=2))
        
        # CX q[0], q[1]
        gate = QGate(name="cx", qubits=[QubitRef("q", 0), QubitRef("q", 1)], params=[])
        checker.check_statement(gate)
        
        assert len(checker.errors) == 0

    def test_measure_valid(self):
        """Valid measure"""
        checker = TypeChecker()
        checker.check_statement(QRegDecl(name="q", size=1))
        checker.check_statement(QRegDecl(name="c", size=1, is_quantum=False))
        
        meas = QMeasure(qubit=QubitRef("q", 0), target=QubitRef("c", 0))
        checker.check_statement(meas)
        assert len(checker.errors) == 0

    def test_measure_undefined_target(self):
        """Measure to undefined bit"""
        checker = TypeChecker()
        checker.check_statement(QRegDecl(name="q", size=1))
        
        meas = QMeasure(qubit=QubitRef("q", 0), target=QubitRef("c", 0))
        checker.check_statement(meas)
        assert len(checker.errors) == 1
        assert isinstance(checker.errors[0], UndefinedVariableError)

class TestErrorMessages:
    """Error message quality tests"""
    
    def test_type_error_message(self):
        """Type error has helpful message"""
        error = TypeError(
            message="Type mismatch",
            line=5,
            col=12,
            expected=QubitType(),
            actual=IntType(),
            suggestion="Did you mean to use a qubit?"
        )
        msg = str(error)
        assert "line 5" in msg
        assert "col 12" in msg
        assert "suggestion" in msg.lower() or "💡" in msg
    
    def test_undefined_var_message(self):
        """Undefined variable error"""
        error = UndefinedVariableError(
            var_name="unknown_var",
            line=3,
            col=10
        )
        msg = str(error)
        assert "unknown_var" in msg
        assert "line 3" in msg
    
    def test_gate_arity_message(self):
        """Gate arity error"""
        error = GateArityError(
            gate_name="cnot",
            expected=2,
            actual=1,
            line=7,
            col=15
        )
        msg = str(error)
        assert "cnot" in msg
        assert "2" in msg
        assert "1" in msg

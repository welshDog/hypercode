"""Tests for the HyperCode parser."""
import pytest
from pathlib import Path
from hypercode.parser import parse
from hypercode.ast import (
    Program, Function, Circuit, LetStmt, 
    ReturnStmt, Identifier, NumberLiteral, 
    StringLiteral, Type, CallExpr
)


def test_parse_bell_pair():
    """Test parsing a simple Bell pair program."""
    source = '''
    #:domain quantum
    #:backend qiskit

    @quantum_function: bell_pair() -> Bits
        @circuit: c
            @init: qubits = QuantumRegister(2)
            @hadamard: qubits[0]
            @cnot: control=qubits[0], target=qubits[1]
            @measure: qubits -> result
        
        @return: result

    @function: main()
        @let: result = bell_pair()
        @print: result
    '''
    
    ast = parse(source)
    assert isinstance(ast, Program)
    # Add more assertions as needed

import pytest
from hypercode.parser.parser import parse
from hypercode.ir.lower_quantum import lower_circuit
from hypercode.ir.qir_nodes import QModule, QAlloc, QGate, QMeasure, QEnd

def test_lower_bell_circuit():
    code = """
    @quantum Bell qubits 2
    H q0
    CX q0 q1
    MEASURE q0 -> c0
    @end
    """
    program = parse(code)
    qc = program.statements[0]
    
    ir_module = lower_circuit(qc)
    
    assert isinstance(ir_module, QModule)
    assert ir_module.name == "Bell"
    assert len(ir_module.instructions) == 5 # Alloc, H, CX, Measure, End
    
    # 1. Alloc
    assert isinstance(ir_module.instructions[0], QAlloc)
    assert ir_module.instructions[0].count == 2
    
    # 2. H q0
    assert isinstance(ir_module.instructions[1], QGate)
    assert ir_module.instructions[1].name == "H"
    assert ir_module.instructions[1].qubits == [0]
    
    # 3. CX q0 q1
    assert isinstance(ir_module.instructions[2], QGate)
    assert ir_module.instructions[2].name == "CX"
    assert ir_module.instructions[2].qubits == [0, 1]
    
    # 4. Measure
    assert isinstance(ir_module.instructions[3], QMeasure)
    assert ir_module.instructions[3].qubit == 0
    assert ir_module.instructions[3].target == "c0"
    
    # 5. End
    assert isinstance(ir_module.instructions[4], QEnd)

def test_lower_params_inline():
    code = """
    @quantum Rot qubits 1
    RZ(1.57) q0
    @end
    """
    program = parse(code)
    qc = program.statements[0]
    ir_module = lower_circuit(qc)
    
    gate = ir_module.instructions[1]
    assert isinstance(gate, QGate)
    assert gate.name == "RZ"
    assert gate.params == [1.57]

def test_lower_params_expression():
    code = """
    @quantum Rot qubits 1
    RZ(PI/2) q0
    @end
    """
    program = parse(code)
    qc = program.statements[0]
    
    # Pass constants
    import math
    constants = {'PI': math.pi}
    ir_module = lower_circuit(qc, constants)
    
    gate = ir_module.instructions[1]
    assert isinstance(gate, QGate)
    assert gate.name == "RZ"
    assert abs(gate.params[0] - math.pi/2) < 1e-6

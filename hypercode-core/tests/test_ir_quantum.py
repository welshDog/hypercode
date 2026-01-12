import pytest
from hypercode.parser.parser import parse
from hypercode.ir.lower_quantum import lower_circuit
from hypercode.ir.qir_nodes import QModule, QAlloc, QGate, QMeasure, QEnd

def test_lower_bell_circuit() -> None:
    code = """
    @circuit: Bell
    @init: q = QReg(2)
    @init: c = CReg(2)
    @hadamard: q[0]
    @cnot: q[0], q[1]
    @measure: q[0] -> c[0]
    """
    program = parse(code)
    qc = program.statements[0]
    
    ir_module = lower_circuit(qc)
    
    assert isinstance(ir_module, QModule)
    assert ir_module.name == "Bell"
    # Alloc, H, CX, Measure, End
    # QAlloc count should be 2 (from q)
    assert len(ir_module.instructions) == 5 
    
    # 1. Alloc
    assert isinstance(ir_module.instructions[0], QAlloc)
    assert ir_module.instructions[0].count == 2
    
    # 2. H q0
    assert isinstance(ir_module.instructions[1], QGate)
    assert ir_module.instructions[1].name == "h" # Lowered name
    assert ir_module.instructions[1].qubits == [0]
    
    # 3. CX q0 q1
    assert isinstance(ir_module.instructions[2], QGate)
    assert ir_module.instructions[2].name == "cx" # Lowered name
    assert ir_module.instructions[2].qubits == [0, 1]
    
    # 4. Measure
    assert isinstance(ir_module.instructions[3], QMeasure)
    assert ir_module.instructions[3].qubit == 0
    assert ir_module.instructions[3].target == "c[0]"
    
    # 5. End
    assert isinstance(ir_module.instructions[4], QEnd)

def test_lower_params_inline() -> None:
    code = """
    @circuit: Rot
    @init: q = QReg(1)
    @rz(1.57): q[0]
    """
    program = parse(code)
    qc = program.statements[0]
    ir_module = lower_circuit(qc)
    
    # Alloc, RZ, End
    gate = ir_module.instructions[1]
    assert isinstance(gate, QGate)
    assert gate.name == "rz"
    assert gate.params == [1.57]

def test_lower_params_expression() -> None:
    code = """
    @data PI: 3.14159
    @circuit: Rot
    @init: q = QReg(1)
    @rz(PI/2): q[0]
    """
    program = parse(code)
    qc = program.statements[1]
    
    # Pass constants
    import math
    constants = {'PI': math.pi}
    ir_module = lower_circuit(qc, constants)
    
    gate = ir_module.instructions[1]
    assert isinstance(gate, QGate)
    assert gate.name == "rz"
    assert abs(gate.params[0] - math.pi/2) < 1e-6

import pytest
from hypercode.parser.parser import parse
from hypercode.interpreter.evaluator import Evaluator
from hypercode.ast.nodes import QuantumCircuitDecl, QGate, QMeasure

def test_parse_quantum_bell():
    code = """
    @quantum Bell qubits 2
    H q0
    CX q0 q1
    MEASURE q0 -> c0
    MEASURE q1 -> c1
    @end
    """
    program = parse(code)
    assert len(program.statements) == 1
    qc = program.statements[0]
    assert isinstance(qc, QuantumCircuitDecl)
    assert qc.name == "Bell"
    assert qc.qubits == 2
    assert len(qc.ops) == 4
    
    # Check H q0
    assert isinstance(qc.ops[0], QGate)
    assert qc.ops[0].name == "H"
    assert qc.ops[0].qubits == [0]
    
    # Check CX q0 q1
    assert isinstance(qc.ops[1], QGate)
    assert qc.ops[1].name == "CX"
    assert qc.ops[1].qubits == [0, 1]
    
    # Check MEASURE
    assert isinstance(qc.ops[2], QMeasure)
    assert qc.ops[2].qubit == 0
    assert qc.ops[2].target == "c0"

def test_parse_quantum_params_inline():
    # Test user request for inline params: RZ(3.14) q0
    code = """
    @quantum Rotate qubits 1
    RZ(3.14) q0
    @end
    """
    program = parse(code)
    qc = program.statements[0]
    gate = qc.ops[0]
    assert gate.name == "RZ"
    assert len(gate.params) == 1
    # Literal 3.14
    assert gate.params[0].value == 3.14

def test_parse_quantum_params_expression():
    # Test RZ(PI/2) q0 - assuming PI is a variable for now
    code = """
    @data PI: 3.14159
    @quantum Rotate qubits 1
    RZ(PI/2) q0
    @end
    """
    program = parse(code)
    qc = program.statements[1] # 0 is data, 1 is quantum
    gate = qc.ops[0]
    assert gate.name == "RZ"
    # Params is an expression BinaryOp
    from hypercode.ast.nodes import BinaryOp, Variable, Literal
    assert isinstance(gate.params[0], BinaryOp)
    assert gate.params[0].op == '/'
    assert isinstance(gate.params[0].left, Variable)
    assert gate.params[0].left.name == "PI"

def test_evaluate_quantum_stub():
    code = """
    @quantum MyCirc qubits 3
    H q0
    @end
    """
    evaluator = Evaluator()
    evaluator.evaluate(parse(code))
    
    assert "QuantumCircuit MyCirc: 3 qubits, 1 ops" in evaluator.output
    assert "MyCirc" in evaluator.variables

def test_evaluate_quantum_mock_backend():
    """Test that the evaluator correctly calls the backend with lowered IR."""
    code = """
    @quantum MyCirc qubits 2
    H q0
    CX q0 q1
    MEASURE q0 -> c0
    @end
    """
    
    # Mock run_qiskit
    from unittest.mock import patch, MagicMock
    from hypercode.ir.qir_nodes import QModule
    
    mock_results = {"c0": 100}
    
    with patch('hypercode.interpreter.evaluator.run_qiskit', return_value=mock_results) as mock_run:
        evaluator = Evaluator(use_quantum_sim=True, shots=500, seed=42)
        evaluator.evaluate(parse(code))
        
        # Verify run_qiskit was called
        assert mock_run.called
        args, kwargs = mock_run.call_args
        
        # Check arguments
        ir_module = args[0]
        assert isinstance(ir_module, QModule)
        assert ir_module.name == "MyCirc"
        # Check shots and seed passed correctly
        assert kwargs['shots'] == 500
        assert kwargs['seed'] == 42
        
        # Verify results stored
        assert evaluator.variables["MyCirc_results"] == mock_results

import pytest
from hypercode.parser.parser import parse
from hypercode.interpreter.evaluator import Evaluator
from hypercode.ast.nodes import QuantumCircuitDecl, QGate, QMeasure, QRegDecl, BinaryOp, Variable, Literal

def test_parse_quantum_bell() -> None:
    code = """
    @circuit: Bell
    @hadamard: q[0]
    @cnot: q[0], q[1]
    @measure: q[0] -> c[0]
    @measure: q[1] -> c[1]
    """
    program = parse(code)
    assert len(program.statements) == 1
    qc = program.statements[0]
    assert isinstance(qc, QuantumCircuitDecl)
    assert qc.name == "Bell"
    # assert qc.qubits == 2 # V3 doesn't declare qubits in circuit header
    assert len(qc.body) == 4
    
    # Check H q0
    assert isinstance(qc.body[0], QGate)
    assert qc.body[0].name == "hadamard"
    assert qc.body[0].qubits[0].register == "q"
    assert qc.body[0].qubits[0].index == 0
    
    # Check CX q0 q1
    assert isinstance(qc.body[1], QGate)
    assert qc.body[1].name == "cnot"
    assert qc.body[1].qubits[0].register == "q"
    assert qc.body[1].qubits[0].index == 0
    assert qc.body[1].qubits[1].register == "q"
    assert qc.body[1].qubits[1].index == 1
    
    # Check MEASURE
    assert isinstance(qc.body[2], QMeasure)
    assert qc.body[2].qubit.register == "q"
    assert qc.body[2].qubit.index == 0
    assert qc.body[2].target.register == "c"
    assert qc.body[2].target.index == 0

def test_parse_quantum_params_inline() -> None:
    # Test user request for inline params: @rz(3.14): q[0]
    code = """
    @circuit: Rotate
    @rz(3.14): q[0]
    """
    program = parse(code)
    qc = program.statements[0]
    gate = qc.body[0]
    assert gate.name == "rz"
    assert len(gate.params) == 1
    # Literal 3.14
    assert gate.params[0].value == 3.14

def test_parse_quantum_params_expression() -> None:
    # Test @rz(PI/2): q[0]
    code = """
    @data PI: 3.14159
    @circuit: Rotate
    @rz(PI/2): q[0]
    """
    program = parse(code)
    qc = program.statements[1] # 0 is data, 1 is circuit
    gate = qc.body[0]
    assert gate.name == "rz"
    # Params is an expression BinaryOp
    assert isinstance(gate.params[0], BinaryOp)
    assert gate.params[0].op == '/'
    assert isinstance(gate.params[0].left, Variable)
    assert gate.params[0].left.name == "PI"

def test_evaluate_quantum_stub() -> None:
    code = """
    @init: q = QReg(3)
    @hadamard: q[0]
    """
    evaluator = Evaluator()
    evaluator.evaluate(parse(code))
    
    # Implicit circuit "main" should be created
    # Check if implicit circuit executed (variables might contain result?)
    # Since no backend is active/mocked, we just check no crash and grouping worked
    pass

def test_evaluate_quantum_mock_backend() -> None:
    """Test that the evaluator correctly calls the backend with lowered IR."""
    code = """
    @init: q = QReg(2)
    @init: c = CReg(2)
    @hadamard: q[0]
    @cnot: q[0], q[1]
    @measure: q[0] -> c[0]
    """
    
    # Mock backend execution
    from unittest.mock import patch, MagicMock
    from hypercode.ir.qir_nodes import QModule
    
    mock_results = {"c0": 100}
    
    # We patch get_backend to return a mock backend
    with patch('hypercode.interpreter.evaluator.get_backend') as mock_get_backend:
        mock_backend = MagicMock()
        mock_backend.execute.return_value = mock_results
        mock_get_backend.return_value = mock_backend
        
        evaluator = Evaluator(backend_name="qiskit", shots=500, seed=42)
        evaluator.evaluate(parse(code))
        
        assert mock_backend.execute.called
        args, kwargs = mock_backend.execute.call_args
        
        # Check arguments
        ir_module = args[0]
        assert isinstance(ir_module, QModule)
        assert ir_module.name == "main" # Implicit circuit name
        # Check shots and seed passed correctly
        assert kwargs['shots'] == 500
        assert kwargs['seed'] == 42

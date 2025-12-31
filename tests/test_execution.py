import pytest
from unittest.mock import MagicMock, patch
from hypercode.interpreter.evaluator import Evaluator
from hypercode.parser.parser import parse
from hypercode.ast.nodes import QuantumCircuitDecl

# Mock Qiskit if not present
try:
    import qiskit
    QISKIT_PRESENT = True
except ImportError:
    QISKIT_PRESENT = False

def test_evaluator_quantum_execution_mock() -> None:
    """
    Test that the evaluator calls the backend.
    We mock the backend to ensure logic is correct even without Qiskit.
    """
    code = """
    @quantum Test qubits 1
    H q0
    MEASURE q0 -> c0
    @end
    """
    program = parse(code)
    
    with patch('hypercode.interpreter.evaluator.get_backend') as mock_get_backend:
        mock_backend = MagicMock()
        mock_backend.execute.return_value = {'0': 50, '1': 50}
        mock_get_backend.return_value = mock_backend
        
        evaluator = Evaluator(use_quantum_sim=True)
        evaluator.evaluate(program)
        
        # Check if backend.execute was called
        mock_backend.execute.assert_called_once()
        
        # Check if results are in variables
        assert "Test_results" in evaluator.variables
        assert evaluator.variables["Test_results"] == {'0': 50, '1': 50}

def test_evaluator_quantum_execution_integration() -> None:
    """
    Test actual execution if Qiskit is present.
    Skipped if Qiskit is not installed.
    """
    if not QISKIT_PRESENT:
        pytest.skip("Qiskit not installed")
        
    code = """
    @quantum Bell qubits 2
    H q0
    CX q0 q1
    MEASURE q0 -> c0
    MEASURE q1 -> c1
    @end
    """
    program = parse(code)
    
    evaluator = Evaluator(use_quantum_sim=True)
    evaluator.evaluate(program)
    
    results = evaluator.variables.get("Bell_results")
    assert results is not None
    # Bell state should have roughly equal 00 and 11, and little 01/10
    # Keys might be '0 0', '00', etc depending on Qiskit version/backend
    # Usually '00' and '11' (little-endian? Qiskit is usually little-endian: q0 is rightmost)
    
    # Just check we got some results
    assert len(results) > 0
    total_shots = sum(results.values())
    assert total_shots == 1024 # default shots

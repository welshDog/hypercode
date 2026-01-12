import pytest
from hypercode.parser.parser import parse
from hypercode.interpreter.evaluator import Evaluator
from hypercode.ast.nodes import QuantumCrispr
from hypercode.compiler import compile_to_v3

def test_quantum_crispr_parsing():
    source = """
    @quantum_crispr
        target = "ATGC"
        genome = "ATGC"
        num_guides = 1
        result -> res
    """
    ast = parse(source)
    assert len(ast.statements) == 1
    node = ast.statements[0]
    assert isinstance(node, QuantumCrispr)
    assert node.target == "ATGC"
    assert node.genome == "ATGC"
    assert node.num_guides == 1
    assert node.result_var == "res"

def test_quantum_crispr_execution(capsys):
    # Mock sequence with a valid guide
    # NGG PAM at end. 20bp upstream.
    # Target: 20bp + NGG
    # "A" * 20 + "AGG"
    target_seq = "A" * 20 + "AGG"
    
    source = f"""
    @data my_target: "{target_seq}"
    @data my_genome: "{target_seq}"
    
    @quantum_crispr
        target = my_target
        genome = my_genome
        num_guides = 1
        result -> best_guides
        
    @print(best_guides)
    """
    
    ast = parse(source)
    
    evaluator = Evaluator(backend_name="classical")
    evaluator.evaluate(ast)
    
    # Check output
    captured = capsys.readouterr()
    # Should print the list of guides
    assert "['AAAAAAAAAAAAAAAAAAAA']" in captured.out or "['AAAAAAAAAAAAAAAAAAAA']" in str(evaluator.output)
    
    # Check variables
    assert "best_guides" in evaluator.variables
    assert len(evaluator.variables["best_guides"]) == 1
    assert evaluator.variables["best_guides"][0] == "A" * 20

def test_quantum_crispr_compilation():
    source = """
@quantum_crispr
    target = "X"
    genome = "Y"
    num_guides = 5
    result -> res
"""
    # Parse then compile back
    ast = parse(source)
    compiled = compile_to_v3(ast)
    
    assert "@quantum_crispr" in compiled
    assert 'target = "X"' in compiled
    assert 'genome = "Y"' in compiled
    assert 'num_guides = 5' in compiled
    assert 'result -> res' in compiled

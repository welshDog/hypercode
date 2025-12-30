import pytest
from hypercode.parser.parser import parse
from hypercode.interpreter.evaluator import Evaluator
from hypercode.ast.nodes import Program, DataDecl, Literal

def test_parse_simple_data():
    code = '@data x: 42'
    program = parse(code)
    assert isinstance(program, Program)
    assert len(program.statements) == 1
    assert isinstance(program.statements[0], DataDecl)
    assert program.statements[0].name == 'x'
    assert isinstance(program.statements[0].value, Literal)
    assert program.statements[0].value.value == 42

def test_evaluate_print():
    code = """
    @data x: 10
    @print(x)
    """
    program = parse(code)
    evaluator = Evaluator()
    evaluator.evaluate(program)
    assert evaluator.output == ['10']

def test_evaluate_logic_true():
    code = """
    @data x: 10
    @check(x > 5) -> {
        @print("Big")
    }
    """
    program = parse(code)
    evaluator = Evaluator()
    evaluator.evaluate(program)
    assert evaluator.output == ['Big']

def test_evaluate_logic_false():
    code = """
    @data x: 1
    @check(x > 5) -> {
        @print("Big")
    }
    """
    program = parse(code)
    evaluator = Evaluator()
    evaluator.evaluate(program)
    assert evaluator.output == []

def test_evaluate_arithmetic():
    code = """
    @data x: 10
    @data y: 20
    @set x: x + y
    @print(x)
    """
    program = parse(code)
    evaluator = Evaluator()
    evaluator.evaluate(program)
    assert evaluator.output == ['30']

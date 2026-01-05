from dataclasses import dataclass
from typing import List, Union, Optional, Any

@dataclass
class Node:
    pass

@dataclass
class Expr(Node):
    pass

@dataclass
class Literal(Expr):
    value: Any

@dataclass
class Variable(Expr):
    name: str

@dataclass
class BinaryOp(Expr):
    left: Expr
    op: str
    right: Expr

@dataclass
class Statement(Node):
    pass

@dataclass
class DataDecl(Statement):
    name: str
    value: Expr

@dataclass
class SetStmt(Statement):
    name: str
    value: Expr

@dataclass
class PrintStmt(Statement):
    expr: Expr

@dataclass
class Block(Node):
    statements: List[Statement]

@dataclass
class CheckStmt(Statement):
    condition: Expr
    true_block: Block
    false_block: Optional[Block] = None

# --- Quantum Ops ---

@dataclass
class QGate(Node):
    name: str
    qubits: List[int]
    params: List[Expr]

@dataclass
class QMeasure(Node):
    qubit: int
    target: Optional[str]

QuantumOp = Union[QGate, QMeasure]

@dataclass
class QuantumCircuitDecl(Statement):
    name: str
    qubits: int
    ops: List[QuantumOp]

@dataclass
class Program(Node):
    statements: List[Statement]

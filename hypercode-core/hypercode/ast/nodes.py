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
class QubitRef(Expr):
    register: str
    index: int

@dataclass
class QRegDecl(Statement):
    name: str
    size: int
    is_quantum: bool = True  # True for QReg, False for CReg

@dataclass
class QGate(Statement):  # Changed from Node to Statement
    name: str
    qubits: List[QubitRef]
    params: List[Expr]

@dataclass
class QMeasure(Statement):  # Changed from Node to Statement
    qubit: QubitRef
    target: QubitRef

QuantumOp = Union[QGate, QMeasure]

@dataclass
class Directive(Statement):
    kind: str  # 'domain' or 'backend'
    value: str

@dataclass
class QuantumCircuitDecl(Statement):
    name: str
    body: List[Statement]  # Can contain QRegDecl, QGate, QMeasure

# --- Bio Ops ---

@dataclass
class BioSequence(Expr):
    sequence: str
    type: str = "DNA"  # DNA, RNA, PROTEIN

@dataclass
class CrisprEdit(Statement):
    target: str      # Variable name of target sequence
    guide: str       # Guide RNA sequence
    pam: str = "NGG" # PAM motif

@dataclass
class PcrReaction(Statement):
    template: str    # Variable name of template
    fwd_primer: str
    rev_primer: str
    cycles: int = 30

@dataclass
class QuantumCrispr(Statement):
    """
    Hybrid Quantum-Bio directive to optimize guide selection.
    @quantum_crispr
        target="X"
        genome="Y"
        num_guides=K
        result -> var
    """
    target: str
    genome: str
    num_guides: int
    result_var: str

@dataclass
class Program(Node):
    statements: List[Statement]

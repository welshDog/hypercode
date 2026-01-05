"""Abstract Syntax Tree (AST) nodes for HyperCode."""
from dataclasses import dataclass, field
from typing import List, Optional, Union, Any


@dataclass
class ASTNode:
    """Base class for all AST nodes."""
    pass


@dataclass
class Type(ASTNode):
    """Base type class."""
    name: str


@dataclass
class Parameter(ASTNode):
    """Function parameter."""
    name: str
    type: Type


@dataclass
class Function(ASTNode):
    """Function definition."""
    name: str
    is_quantum: bool
    parameters: List[Parameter]
    return_type: Type
    body: List[ASTNode]


@dataclass
class Circuit(ASTNode):
    """Quantum circuit definition."""
    name: str
    body: List[ASTNode]


@dataclass
class LetStmt(ASTNode):
    """Let statement for variable declaration."""
    name: str
    value: ASTNode


@dataclass
class ReturnStmt(ASTNode):
    """Return statement."""
    value: ASTNode


@dataclass
class CallExpr(ASTNode):
    """Function call expression."""
    name: str
    args: List[ASTNode]


@dataclass
class Identifier(ASTNode):
    """Identifier reference."""
    name: str


@dataclass
class NumberLiteral(ASTNode):
    """Numeric literal."""
    value: Union[int, float]


@dataclass
class StringLiteral(ASTNode):
    """String literal."""
    value: str


@dataclass
class Program(ASTNode):
    """Root node of the AST."""
    functions: List[Function]
    directives: List[tuple[str, str]] = field(default_factory=list)

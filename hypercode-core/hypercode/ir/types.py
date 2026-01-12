"""
HyperCode Type System

Defines all types for quantum, classical, and molecular computing.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional, Union

class BaseType:
    """Base class for all HyperCode types"""
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"
    
    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__)

# ============================================================================
# QUANTUM TYPES
# ============================================================================

class QubitType(BaseType):
    """Single qubit: q0"""
    pass

@dataclass
class QubitArrayType(BaseType):
    """Array of qubits: q[5]"""
    size: int
    
    def __repr__(self) -> str:
        return f"qubit[{self.size}]"

# ============================================================================
# CLASSICAL TYPES
# ============================================================================

class BitType(BaseType):
    """Single classical bit: b0"""
    pass

@dataclass
class BitArrayType(BaseType):
    """Array of bits: b[5]"""
    size: int
    
    def __repr__(self) -> str:
        return f"bit[{self.size}]"

class IntType(BaseType):
    """Integer type"""
    pass

class FloatType(BaseType):
    """Floating point type"""
    pass

class BoolType(BaseType):
    """Boolean type"""
    pass

class StringType(BaseType):
    """String type"""
    pass

# ============================================================================
# GATE & CIRCUIT TYPES
# ============================================================================

class GateType(BaseType):
    """Quantum gate type"""
    pass

class CircuitType(BaseType):
    """Quantum circuit type"""
    pass

# ============================================================================
# MOLECULAR TYPES
# ============================================================================

class PlasmidType(BaseType):
    """DNA plasmid type"""
    pass

class SequenceType(BaseType):
    """DNA sequence type"""
    pass

# ============================================================================
# SPECIAL TYPES
# ============================================================================

class VoidType(BaseType):
    """No return value"""
    pass

class AnyType(BaseType):
    """Unknown/any type (for error recovery)"""
    pass

# ============================================================================
# FUNCTION TYPES
# ============================================================================

@dataclass
class FunctionType(BaseType):
    """Function signature"""
    param_types: List[BaseType]
    return_type: BaseType
    
    def __repr__(self) -> str:
        params = ", ".join(str(t) for t in self.param_types)
        return f"({params}) -> {self.return_type}"

# ============================================================================
# TYPE OPERATIONS
# ============================================================================

def is_qubit_type(t: BaseType) -> bool:
    """Check if type is qubit-related"""
    return isinstance(t, (QubitType, QubitArrayType))

def is_bit_type(t: BaseType) -> bool:
    """Check if type is bit-related"""
    return isinstance(t, (BitType, BitArrayType))

def is_numeric_type(t: BaseType) -> bool:
    """Check if type is numeric"""
    return isinstance(t, (IntType, FloatType))

def is_array_type(t: BaseType) -> bool:
    """Check if type is an array"""
    return isinstance(t, (QubitArrayType, BitArrayType))

def array_size(t: BaseType) -> Optional[int]:
    """Get array size if type is array"""
    if isinstance(t, (QubitArrayType, BitArrayType)):
        return t.size
    return None

def are_compatible(t1: BaseType, t2: BaseType) -> bool:
    """Check if two types are compatible"""
    if t1 == t2:
        return True
    if isinstance(t1, AnyType) or isinstance(t2, AnyType):
        return True
    # Add more compatibility rules as needed
    return False

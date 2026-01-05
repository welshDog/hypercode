from dataclasses import dataclass, field
from typing import List, Union, Optional, Dict, Any

@dataclass
class QInstr:
    pass

@dataclass
class QAlloc(QInstr):
    start_index: int
    count: int
    
    def __str__(self):
        return f"alloc q{self.start_index}..q{self.start_index + self.count - 1}"

@dataclass
class QGate(QInstr):
    name: str
    qubits: List[int]
    params: List[float]
    
    def __str__(self):
        qubits_str = ", ".join([f"q{q}" for q in self.qubits])
        if self.params:
            params_str = f"({', '.join(map(str, self.params))})"
            return f"gate {self.name}{params_str} {qubits_str}"
        return f"gate {self.name} {qubits_str}"

@dataclass
class QMeasure(QInstr):
    qubit: int
    target: str
    
    def __str__(self):
        return f"{self.target} = measure q{self.qubit}"

@dataclass
class QEnd(QInstr):
    def __str__(self):
        return "end_quantum"

@dataclass
class QModule:
    name: str
    instructions: List[QInstr]
    
    def __str__(self):
        lines = [f"module {self.name}:"]
        for instr in self.instructions:
            lines.append(f"  {str(instr)}")
        return "\n".join(lines)

@dataclass
class QIR:
    """
    Quantum Intermediate Representation (QIR) of a HyperCode program.
    
    Attributes:
        modules: Dictionary mapping module names to QModule objects
        metadata: Additional metadata about the QIR
    """
    modules: Dict[str, QModule] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_module(self, module: QModule) -> None:
        """Add a QModule to the QIR."""
        self.modules[module.name] = module
    
    def __str__(self) -> str:
        return "\n\n".join(str(module) for module in self.modules.values())

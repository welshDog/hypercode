"""
HyperCode Agents Package.
Contains the specialist agents for the HyperCode ecosystem.
"""

from .base_agent import BaseAgent, TaskResult
from .caretaker import Caretaker
from .diagnostic import BROskiCaretaker, DiagnosticAgent
from .specialists import HelixAgent, QubitAgent, FlowAgent, NexusAgent, ScribeAgent

# Global Caretaker instance
caretaker = Caretaker()

# Auto-register all agents on import
def initialize_agents():
    """Initialize and register all agents."""
    caretaker.register(HelixAgent())
    caretaker.register(QubitAgent())
    caretaker.register(FlowAgent())
    caretaker.register(NexusAgent())
    caretaker.register(ScribeAgent())
    caretaker.register(DiagnosticAgent())

__all__ = [
    'BaseAgent',
    'TaskResult',
    'Caretaker',
    'BROskiCaretaker',
    'DiagnosticAgent',
    'HelixAgent',
    'QubitAgent',
    'FlowAgent',
    'NexusAgent',
    'ScribeAgent',
    'caretaker',
    'initialize_agents'
]

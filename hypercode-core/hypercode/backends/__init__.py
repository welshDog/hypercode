"""
Backend registration and loading module.
"""
from typing import Dict, Type, Any

from .base import BaseBackend
# Alias BaseBackend as Backend for convenience
Backend = BaseBackend

from .qiskit_backend import QiskitBackend
from .molecular_backend import MolecularBackend
# Import other backends here as they are created
# from .classical_backend import ClassicalBackend

# A registry of available backend classes
BACKEND_REGISTRY: Dict[str, Any] = {
    "qiskit": QiskitBackend,
    "molecular": MolecularBackend,
    # "classical": ClassicalBackend,
}

def get_backend(name: str) -> Any:
    """
    Factory function to get an instance of a backend by its name.

    Args:
        name: The name of the backend to retrieve (e.g., "qiskit").

    Returns:
        An instance of the requested backend class.

    Raises:
        ValueError: If the requested backend name is not found in the registry.
    """
    backend_class = BACKEND_REGISTRY.get(name)
    if backend_class is None:
        raise ValueError(f"Unknown backend: '{name}'. Available backends are: {list(BACKEND_REGISTRY.keys())}")
    
    return backend_class()
"""
Defines the base interface for all execution backends.
"""
from abc import ABC, abstractmethod
from typing import Any, Optional

from hypercode.ir.qir_nodes import QModule


class BaseBackend(ABC):
    """
    Abstract Base Class for a HyperCode execution backend.

    A backend is responsible for taking a HyperCode Intermediate Representation (IR)
    and executing it to produce a result.
    """

    @abstractmethod
    def execute(
        self,
        ir_module: QModule,
        shots: int = 1024,
        seed: Optional[int] = None
    ) -> Any:
        """
        Executes the given IR module and returns the result.

        Args:
            ir_module: The Quantum Intermediate Representation (QIR) module to execute.
            shots: The number of times to run the circuit (for probabilistic results).
            seed: The random seed for simulators.

        Returns:
            The result of the execution, which can be of any type depending on the
            backend's nature (e.g., a dictionary of counts, a classical value).
        """
        raise NotImplementedError

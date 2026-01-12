# hypercode/agents/base_agent.py

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import time

@dataclass
class TaskResult:
    """
    Unified result format across all agents.
    Every agent returns this structure.
    """
    agent_name: str
    task_name: str
    success: bool
    output: Any
    duration_seconds: float
    metadata: Dict[str, Any]
    errors: List[str] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []


class BaseAgent(ABC):
    """
    Abstract base class for all HyperCode agents.
    
    Every agent (HELIX, QUBIT, FLOW, NEXUS, SCRIBE) inherits this.
    This ensures consistent behavior, error handling, and reporting.
    """
    
    def __init__(self, name: str):
        """
        Initialize agent with name and capabilities.
        
        Args:
            name: Unique agent identifier (e.g., "helix", "qubit", "flow")
        """
        self.name = name
        self.capabilities: Dict[str, callable] = {}
        self._task_history = []
        self._register_capabilities()
    
    @abstractmethod
    def _register_capabilities(self):
        """
        Each agent defines what it can do.
        
        Example (HELIX):
            self.capabilities['validate_crispr'] = self.validate_crispr
            self.capabilities['scan_off_targets'] = self.scan_off_targets
            self.capabilities['design_guides'] = self.design_guides
        
        Example (QUBIT):
            self.capabilities['formulate_qubo'] = self.formulate_qubo
            self.capabilities['solve_qubo'] = self.solve_qubo
        """
        pass
    
    def can_handle(self, task_name: str) -> bool:
        """
        Check if this agent can handle a task.
        
        Args:
            task_name: Name of the task
        
        Returns:
            True if agent has this capability
        """
        return task_name in self.capabilities
    
    def execute(self, task_name: str, *args, **kwargs) -> TaskResult:
        """
        Execute a task and return standardized result.
        
        Args:
            task_name: Name of capability to invoke
            *args: Positional arguments for the task
            **kwargs: Keyword arguments for the task
        
        Returns:
            TaskResult with success/failure, output, timing
        """
        start_time = time.time()
        errors = []
        output = None
        success = False
        
        try:
            if not self.can_handle(task_name):
                raise ValueError(
                    f"{self.name} cannot handle '{task_name}'. "
                    f"Available: {list(self.capabilities.keys())}"
                )
            
            # Execute the capability
            task_func = self.capabilities[task_name]
            output = task_func(*args, **kwargs)
            success = True
            
        except Exception as e:
            errors.append(str(e))
            success = False
        
        duration = time.time() - start_time
        
        result = TaskResult(
            agent_name=self.name,
            task_name=task_name,
            success=success,
            output=output,
            duration_seconds=duration,
            metadata={'timestamp': time.time()},
            errors=errors
        )
        
        # Log to history
        self._task_history.append(result)
        
        return result
    
    def get_status(self) -> Dict[str, Any]:
        """
        Return agent's current status.
        Used by Caretaker for health checks and reporting.
        """
        return {
            'name': self.name,
            'online': True,
            'capabilities': list(self.capabilities.keys()),
            'tasks_completed': len(self._task_history),
            'success_rate': self._calculate_success_rate(),
            'avg_task_duration': self._calculate_avg_duration()
        }
    
    def _calculate_success_rate(self) -> float:
        """Calculate success rate from task history."""
        if not self._task_history:
            return 1.0
        successes = sum(1 for task in self._task_history if task.success)
        return successes / len(self._task_history)
    
    def _calculate_avg_duration(self) -> float:
        """Calculate average task duration."""
        if not self._task_history:
            return 0.0
        total_duration = sum(task.duration_seconds for task in self._task_history)
        return total_duration / len(self._task_history)

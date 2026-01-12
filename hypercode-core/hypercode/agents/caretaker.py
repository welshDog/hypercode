# hypercode/agents/caretaker.py

from typing import Dict, List, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from datetime import datetime
from .base_agent import BaseAgent, TaskResult

class Caretaker:
    """
    Central orchestration agent for HyperCode.
    
    Responsibilities:
    1. Agent Registry - Maintain list of available agents
    2. Task Routing - Determine which agents can handle tasks
    3. Parallel Execution - Run multiple agents concurrently
    4. Result Synthesis - Combine outputs intelligently
    5. Memory - Track what's been done
    6. Reporting - Generate status/performance reports
    """
    
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.memory: List[Dict[str, Any]] = []
        self.max_workers = 5  # Parallel execution limit
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # AGENT MANAGEMENT
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    def register(self, agent: BaseAgent) -> None:
        """
        Register an agent with the Caretaker.
        
        Example:
            caretaker.register(HELIX)
            caretaker.register(QUBIT)
            caretaker.register(FLOW)
        """
        self.agents[agent.name] = agent
        # print(f"✅ {agent.name.upper()} registered. Capabilities: {list(agent.capabilities.keys())}")
    
    def get_agent(self, name: str) -> Optional[BaseAgent]:
        """Get agent by name."""
        return self.agents.get(name)
    
    def find_agents(self, task_name: str) -> List[BaseAgent]:
        """
        Find all agents capable of handling a task.
        
        Args:
            task_name: The task to delegate
        
        Returns:
            List of agents that can handle this task
        """
        return [agent for agent in self.agents.values() if agent.can_handle(task_name)]
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TASK DISPATCH & EXECUTION
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    def dispatch(self, task_name: str, *args, agent_filter: Optional[str] = None, **kwargs) -> TaskResult:
        """
        Single-agent task dispatch.
        
        Use when you want ONE specific agent to handle a task.
        
        Example:
            result = caretaker.dispatch('design_guides', target='BRCA1', agent_filter='helix')
        """
        agents = self.find_agents(task_name)
        
        if agent_filter:
            agents = [a for a in agents if a.name == agent_filter]
        
        if not agents:
            return TaskResult(
                agent_name="caretaker",
                task_name=task_name,
                success=False,
                output=None,
                duration_seconds=0,
                metadata={},
                errors=[f"No agents found for task '{task_name}'"]
            )
        
        # Use the first agent (or implement selection logic)
        agent = agents[0]
        result = agent.execute(task_name, *args, **kwargs)
        
        # Log to memory
        self._log_task(task_name, [agent.name], result)
        
        return result
    
    def orchestrate(self, task_name: str, *args, parallel: bool = True, **kwargs) -> Dict[str, TaskResult]:
        """
        Multi-agent task dispatch.
        
        Finds ALL agents capable of handling a task and executes them.
        Useful when you want parallel validation/review.
        
        Example:
            results = caretaker.orchestrate('validate_crispr', guides=[...])
            # HELIX validates bio logic
            # NEXUS validates compiler integration
            # FLOW validates UI representation
        
        Args:
            task_name: Task to execute
            parallel: If True, run all agents concurrently. If False, sequentially.
        
        Returns:
            Dict mapping agent_name → TaskResult
        """
        agents = self.find_agents(task_name)
        
        if not agents:
            return {
                'error': TaskResult(
                    agent_name="caretaker",
                    task_name=task_name,
                    success=False,
                    output=None,
                    duration_seconds=0,
                    metadata={},
                    errors=[f"No agents found for task '{task_name}'"]
                )
            }
        
        results = {}
        
        if parallel:
            # Execute agents concurrently
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = {
                    executor.submit(agent.execute, task_name, *args, **kwargs): agent
                    for agent in agents
                }
                
                for future in as_completed(futures):
                    agent = futures[future]
                    try:
                        result = future.result()
                        results[agent.name] = result
                    except Exception as e:
                        results[agent.name] = TaskResult(
                            agent_name=agent.name,
                            task_name=task_name,
                            success=False,
                            output=None,
                            duration_seconds=0,
                            metadata={},
                            errors=[str(e)]
                        )
        else:
            # Execute sequentially
            for agent in agents:
                result = agent.execute(task_name, *args, **kwargs)
                results[agent.name] = result
        
        # Log to memory
        agent_names = [a.name for a in agents]
        self._log_task(task_name, agent_names, results)
        
        return results
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # RESULT SYNTHESIS
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    def synthesize(self, results: Dict[str, TaskResult], strategy: str = 'consensus') -> TaskResult:
        """
        Combine multiple agent results into one unified result.
        
        Strategies:
        - 'consensus': All agents must succeed
        - 'majority': Most agents must succeed
        - 'first': Use first successful result
        - 'merge': Combine all outputs into single result
        
        Example:
            bio_results = caretaker.orchestrate('validate_crispr', guides=[...])
            unified = caretaker.synthesize(bio_results, strategy='consensus')
        """
        if strategy == 'consensus':
            all_success = all(r.success for r in results.values())
            errors = [e for r in results.values() for e in r.errors]
            
            return TaskResult(
                agent_name='caretaker',
                task_name='synthesis',
                success=all_success,
                output={k: r.output for k, r in results.items()},
                duration_seconds=sum(r.duration_seconds for r in results.values()),
                metadata={'strategy': 'consensus', 'agents': list(results.keys())},
                errors=errors if not all_success else []
            )
        
        elif strategy == 'majority':
            success_count = sum(1 for r in results.values() if r.success)
            threshold = len(results) / 2
            all_success = success_count >= threshold
            
            return TaskResult(
                agent_name='caretaker',
                task_name='synthesis',
                success=all_success,
                output={k: r.output for k, r in results.items() if r.success},
                duration_seconds=sum(r.duration_seconds for r in results.values()),
                metadata={'strategy': 'majority', 'success_count': success_count},
                errors=[r.errors for r in results.values() if not r.success]
            )
        
        elif strategy == 'first':
            for result in results.values():
                if result.success:
                    return result
            
            # All failed
            return TaskResult(
                agent_name='caretaker',
                task_name='synthesis',
                success=False,
                output=None,
                duration_seconds=0,
                metadata={'strategy': 'first'},
                errors=['All agents failed']
            )
        
        elif strategy == 'merge':
            return TaskResult(
                agent_name='caretaker',
                task_name='synthesis',
                success=all(r.success for r in results.values()),
                output={k: r.output for k, r in results.items()},
                duration_seconds=sum(r.duration_seconds for r in results.values()),
                metadata={'strategy': 'merge'},
                errors=[e for r in results.values() for e in r.errors]
            )
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # MEMORY & REPORTING
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    def _log_task(self, task_name: str, agents: List[str], result: Any) -> None:
        """Log task execution to memory."""
        self.memory.append({
            'timestamp': datetime.now().isoformat(),
            'task': task_name,
            'agents': agents,
            'result': result if isinstance(result, dict) else result.__dict__ if hasattr(result, '__dict__') else str(result)
        })
    
    def status(self) -> Dict[str, Any]:
        """
        Get status of all agents.
        
        Example:
            status = caretaker.status()
            print(status['helix']['success_rate'])
        """
        return {
            agent.name: agent.get_status()
            for agent in self.agents.values()
        }
    
    def report(self, time_window: Optional[str] = None) -> str:
        """
        Generate human-readable performance report.
        
        Example:
            print(caretaker.report())
        """
        lines = [
            "╔════════════════════════════════════════════════════════════╗",
            "║         HyperCode Agent Orchestration Report               ║",
            "╚════════════════════════════════════════════════════════════╝",
            "",
            "🧠 AGENT STATUS:",
        ]
        
        status = self.status()
        for agent_name, agent_status in status.items():
            caps_str = ', '.join(agent_status['capabilities'][:3])
            if len(agent_status['capabilities']) > 3:
                caps_str += f" (+{len(agent_status['capabilities'])-3})"
            
            lines.append(
                f"  {agent_name.upper():10} ✅ | "
                f"Tasks: {agent_status['tasks_completed']:3d} | "
                f"Success: {agent_status['success_rate']*100:5.1f}% | "
                f"Avg: {agent_status['avg_task_duration']:.2f}s | "
                f"Caps: {caps_str}"
            )
        
        lines.extend([
            "",
            f"📊 TOTAL TASKS: {len(self.memory)}",
            f"⏱️  TOTAL TIME: {sum(sum(r.get('result', {}).get('duration_seconds', 0) if isinstance(r.get('result'), dict) else 0 for item in [r]) for r in self.memory):.1f}s",
            "",
        ])
        
        return '\n'.join(lines)

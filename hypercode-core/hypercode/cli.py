"""HyperCode CLI (command-line interface)."""

import argparse
import sys
from pathlib import Path
from typing import Optional

from hypercode.parser.parser import parse
from hypercode.ast.nodes import QuantumCircuitDecl, DataDecl, Statement
from hypercode.ir.lower_quantum import lower_circuit
from hypercode.interpreter.evaluator import Evaluator

# ANSI color codes for better output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text: str) -> None:
    """Print a formatted header."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}=== {text} ==={Colors.ENDC}\n")

def print_success(text: str) -> None:
    """Print a success message."""
    print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")

def print_error(text: str) -> None:
    """Print an error message."""
    print(f"{Colors.RED}✗ {text}{Colors.ENDC}", file=sys.stderr)

def print_info(text: str) -> None:
    """Print an informational message."""
    print(f"{Colors.CYAN}ℹ {text}{Colors.ENDC}")

def run_command(args: argparse.Namespace) -> None:
    """Handle the run command."""
    file_path = args.file
    backend = args.backend
    shots = getattr(args, 'shots', 1024)
    seed = getattr(args, 'seed', None)
    
    print_header(f"RUNNING HYPERCODE PROGRAM: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
            
            print_info(f"Backend: {backend}")
            if backend == "qiskit":
                print_info(f"Shots: {shots}, Seed: {seed}")
            
            # Parse
            try:
                program = parse(source)
            except Exception as e:
                print_error(f"Parse Error: {e}")
                return

            # Evaluate (Classical + Quantum Stub)
            print_info("Executing...")
            
            # Pass options to Evaluator
            evaluator = Evaluator(
                backend_name=backend,
                shots=shots,
                seed=seed
            )
            evaluator.evaluate(program)
            
            print_success("Execution completed successfully")
            
    except FileNotFoundError:
        print_error(f"File not found: {file_path}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Error running {file_path}: {str(e)}")
        sys.exit(1)

def parse_command(args: argparse.Namespace) -> None:
    """Handle the parse command."""
    file_path = args.file
    print_header(f"PARSING HYPERCODE FILE: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
            
            print_info("Abstract Syntax Tree (AST):")
            print("-" * 60)
            
            program = parse(source)
            for stmt in program.statements:
                print(stmt)
            
            print("-" * 60)
            print_success("Parsing completed successfully")
            
    except FileNotFoundError:
        print_error(f"File not found: {file_path}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Error parsing {file_path}: {str(e)}")
        sys.exit(1)

def qir_command(args: argparse.Namespace) -> None:
    """Handle the qir command."""
    file_path = args.file
    print_header(f"GENERATING QUANTUM IR FOR: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
            
            # Parse
            program = parse(source)
            
            # Extract constants (rudimentary)
            constants = {}
            for stmt in program.statements:
                if isinstance(stmt, DataDecl):
                    if hasattr(stmt.value, 'value'):
                        constants[stmt.name] = stmt.value.value
            
            # Find and Lower Quantum Circuits
            found_quantum = False
            for stmt in program.statements:
                if isinstance(stmt, QuantumCircuitDecl):
                    found_quantum = True
                    print_info(f"Lowering Circuit: {stmt.name}")
                    try:
                        ir_module = lower_circuit(stmt, constants)
                        print(str(ir_module))
                        print("-" * 40)
                    except Exception as e:
                        print_error(f"Failed to lower circuit {stmt.name}: {e}")
            
            if not found_quantum:
                print_info("No quantum circuits found in file.")
            else:
                print_success("QIR generation completed")

    except FileNotFoundError:
        print_error(f"File not found: {file_path}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Error: {str(e)}")
        sys.exit(1)

def caretaker_command(args: argparse.Namespace) -> None:
    """Handle the caretaker command."""
    # Lazy import to avoid circular dependencies or slow startup
    from hypercode.agents.diagnostic import BROskiCaretaker
    
    # We don't print a header here because the agent does its own printing
    # but we can print a small intro if we want consistency
    # print_header("🤖 BROski CARETAKER AGENT")
    
    agent = BROskiCaretaker(args.root)
    
    # Map args to agent methods
    # The agent.diagnose() does everything based on internal logic, 
    # but the CLI args might need to filter what diagnose does if we want to respect --mode
    # However, the current BROskiCaretaker.diagnose() runs everything (OMNI).
    # If we want to support modes properly, we might need to adjust the agent or just run diagnose()
    # for now, as the original script's main() did.
    
    # In the original script:
    # report = agent.diagnose()
    # agent.print_report(report)
    # ...
    
    # We will follow the original script's main() logic but adapted for this command function
    
    report = agent.diagnose()
    agent.print_report(report)
    
    if args.json:
        agent.export_json(report)
        
    if args.commit:
        agent.auto_commit(report)
        
    if not report.ready_to_commit:
        sys.exit(1)

def agents_command(args: argparse.Namespace) -> None:
    """Handle agents commands."""
    from hypercode.agents import caretaker, initialize_agents
    import json
    
    # Initialize agents
    initialize_agents()
    
    subcmd = args.agents_command
    
    if subcmd == "status":
        print(caretaker.report())
        
    elif subcmd == "dispatch":
        task = args.task
        agent_filter = args.agent
        task_args = {}
        if args.args:
            try:
                task_args = json.loads(args.args)
            except json.JSONDecodeError:
                print_error("Invalid JSON in --args")
                sys.exit(1)
        
        if agent_filter:
            result = caretaker.dispatch(task, agent_filter=agent_filter, **task_args)
        else:
            # If no specific agent requested, default to orchestrate for single task?
            # Or dispatch to any available? Dispatch picks first available.
            result = caretaker.dispatch(task, **task_args)
            
        print_success(f"{result.agent_name}: {task}")
        print(f"   Success: {result.success} | Time: {result.duration_seconds:.2f}s")
        if result.output:
            print(f"   Output: {result.output}")
            
    elif subcmd == "orchestrate":
        task = args.task
        strategy = args.strategy
        # For orchestrate, we might want args too? Blueprint didn't specify args for orchestrate command but implied it.
        # Let's support args here too if needed, but for now blueprint says:
        # orchestrate(task, strategy)
        
        results = caretaker.orchestrate(task) # Missing args support in blueprint CLI, but let's assume no args for now or add if needed
        synthesized = caretaker.synthesize(results, strategy=strategy)
        
        print_header(f"Orchestration Results ({strategy})")
        for agent_name, result in results.items():
            status_icon = "✅" if result.success else "❌"
            print(f"  {status_icon} {agent_name}: {result.duration_seconds:.2f}s")
        
        print("\nSynthesized Result:")
        print(f"  Success: {synthesized.success}")
        if synthesized.output:
            print(f"  Output: {synthesized.output}")

def version_command(args: argparse.Namespace) -> None:
    """Handle the version command."""
    print("HyperCode v0.1.0 (development)")
    print("A neurodivergent-first programming language")
    print("https://github.com/welshDog/THE-HYPERCODE")

def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description=f"{Colors.BLUE}{Colors.BOLD}HyperCode: A neurodivergent-first programming language{Colors.ENDC}",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Add --version flag
    parser.add_argument(
        '-v', '--version',
        action='store_true',
        help='Show version information and exit'
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # parse command
    parse_parser = subparsers.add_parser("parse", help="Parse HyperCode file and show AST")
    parse_parser.add_argument("file", help="Input .hc file")
    parse_parser.set_defaults(func=parse_command)
    
    # qir command
    qir_parser = subparsers.add_parser("qir", help="Generate Quantum IR from HyperCode file")
    qir_parser.add_argument("file", help="Input .hc file")
    qir_parser.set_defaults(func=qir_command)
    
    # run command
    run_parser = subparsers.add_parser("run", help="Run HyperCode program")
    run_parser.add_argument("file", help="Input .hc file")
    run_parser.add_argument("--backend", choices=["qiskit", "classical", "molecular"], default="qiskit", help="Backend to use for execution")
    run_parser.set_defaults(func=run_command)
    
    # quantum subcommand
    quantum_parser = subparsers.add_parser("quantum", help="Quantum specific operations")
    quantum_subparsers = quantum_parser.add_subparsers(dest="quantum_command", help="Quantum commands")
    
    # quantum run command
    q_run_parser = quantum_subparsers.add_parser("run", help="Run a quantum program with specific options")
    q_run_parser.add_argument("file", help="Input .hc file")
    q_run_parser.add_argument("--shots", type=int, default=1024, help="Number of shots (default: 1024)")
    q_run_parser.add_argument("--seed", type=int, default=None, help="Simulator seed")
    q_run_parser.set_defaults(func=run_command, backend="qiskit")

    # caretaker command
    caretaker_parser = subparsers.add_parser("caretaker", help="Run the BROski Caretaker Agent")
    caretaker_parser.add_argument(
        "--mode",
        choices=["status", "fix", "upgrade", "watch", "ready", "omni"],
        default="omni",
        help="Diagnostic mode (default: omni)"
    )
    caretaker_parser.add_argument(
        "--commit",
        action="store_true",
        help="Auto-commit if all checks pass"
    )
    caretaker_parser.add_argument(
        "--json",
        action="store_true",
        help="Export report as JSON"
    )
    caretaker_parser.add_argument(
        "--root",
        default=".",
        help="Project root directory"
    )
    caretaker_parser.set_defaults(func=caretaker_command)

    # agents command
    agents_parser = subparsers.add_parser("agents", help="Agent orchestration commands")
    agents_subparsers = agents_parser.add_subparsers(dest="agents_command", help="Agent commands")
    
    # agents status
    agents_subparsers.add_parser("status", help="Show agent status").set_defaults(func=agents_command)
    
    # agents dispatch
    dispatch_parser = agents_subparsers.add_parser("dispatch", help="Dispatch a task to agents")
    dispatch_parser.add_argument("task", help="Task to execute")
    dispatch_parser.add_argument("--agent", default=None, help="Specific agent to use")
    dispatch_parser.add_argument("--args", default="{}", help="Task arguments as JSON")
    dispatch_parser.set_defaults(func=agents_command)
    
    # agents orchestrate
    orchestrate_parser = agents_subparsers.add_parser("orchestrate", help="Orchestrate multiple agents")
    orchestrate_parser.add_argument("task", help="Task to execute")
    orchestrate_parser.add_argument("--strategy", default="consensus", help="Synthesis strategy")
    orchestrate_parser.set_defaults(func=agents_command)

    # version command
    version_parser = subparsers.add_parser("version", help="Show version information")
    version_parser.set_defaults(func=version_command)
    
    # If no arguments provided, show help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
    
    args = parser.parse_args()
    
    # Handle --version flag
    if getattr(args, 'version', False):
        version_command(args)
        return
    
    # Execute the appropriate command
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)

"""HyperCode command-line interface entry point."""

from hypercode.cli import main

if __name__ == "__main__":
    main()

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

def main() -> None:
    """Entry point for the HyperCode CLI."""
    parser = argparse.ArgumentParser(
        description=f"{Colors.BLUE}{Colors.BOLD}HyperCode: A neurodivergent-first programming language{Colors.ENDC}",
        usage="""hypercode <command> [<args>]

Available commands:
  run       Run a HyperCode program
  parse     Parse a HyperCode file and show the AST
  help      Show this help message
  version   Show version information
""",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        'command',
        help='Subcommand to run',
        choices=['run', 'parse', 'help', 'version'],
        nargs='?'
    )
    
    # If no arguments provided, show help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
        
    args = parser.parse_args(sys.argv[1:2])
    
    if args.command == 'run':
        run_parser = argparse.ArgumentParser(description='Run a HyperCode program')
        run_parser.add_argument('file', help='Path to the .hc file to run')
        run_parser.add_argument('--backend', '-b', 
                             choices=['qiskit', 'simulator', 'hardware'],
                             default='qiskit',
                             help='Backend to use for execution')
        run_args = run_parser.parse_args(sys.argv[2:])
        run_file(run_args.file, run_args.backend)
        
    elif args.command == 'parse':
        parse_parser = argparse.ArgumentParser(description='Parse a HyperCode file')
        parse_parser.add_argument('file', help='Path to the .hc file to parse')
        parse_parser.add_argument('--verbose', '-v', 
                                action='store_true',
                                help='Show detailed parse information')
        parse_args = parse_parser.parse_args(sys.argv[2:])
        parse_file(parse_args.file, parse_args.verbose)
        
    elif args.command == 'version' or (len(sys.argv) > 1 and sys.argv[1] in ['-v', '--version']):
        print("HyperCode v0.1.0 (development)")
        print("A neurodivergent-first programming language")
        print("https://github.com/welshDog/THE-HYPERCODE")
        
    elif args.command == 'help' or (len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']):
        parser.print_help()
    else:
        print_error(f"Unknown command: {args.command}")
        parser.print_help()
        sys.exit(1)

def run_file(file_path: str, backend: str = 'qiskit') -> None:
    """Run a HyperCode program from a file."""
    print_header(f"RUNNING HYPERCODE PROGRAM: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
            
            print_info(f"Backend: {backend}")
            print_info("Source code preview:")
            print("-" * 60)
            
            # Show first 10 lines of source with line numbers
            lines = source.split('\n')
            for i, line in enumerate(lines[:10], 1):
                print(f"{i:3d} | {line}")
                
            if len(lines) > 10:
                print(f"... and {len(lines) - 10} more lines")
                
            print("-" * 60)
            
            # Simulate execution
            print("\n" + "=" * 60)
            print("EXECUTION SIMULATION (STUB IMPLEMENTATION)")
            print("=" * 60)
            print("\nThis is a preview of what execution would look like.")
            print("The actual HyperCode runtime is under development.\n")
            
            # Simple simulation of fizzbuzz output
            if 'fizzbuzz' in file_path.lower():
                print("Sample output (simulated):")
                print("1\n2\nFizz\n4\nBuzz\nFizz\n...")
            
            print_success("Execution completed successfully (simulated)")
            
    except FileNotFoundError:
        print_error(f"File not found: {file_path}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Error running {file_path}: {str(e)}")
        sys.exit(1)

def parse_file(file_path: str, verbose: bool = False) -> None:
    """Parse a HyperCode file and display the AST."""
    print_header(f"PARSING HYPERCODE FILE: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
            
            print_info("Abstract Syntax Tree (AST) Preview:")
            print("-" * 60)
            
            # Simple AST representation
            print("Module(")
            print("  body=[")
            
            lines = source.split('\n')
            for i, line in enumerate(lines, 1):
                line = line.strip()
                if line and not line.startswith('#'):
                    indent = "    "
                    if 'function' in line:
                        func_name = line.split('(')[0].replace('function', '').strip()
                        print(f"{indent}FunctionDef(")
                        print(f"{indent}  name='{func_name}',")
                        print(f"{indent}  args=Arguments(...),")
                        print(f"{indent}  body=[...]")
                        print(f"{indent}),")
                    elif 'if ' in line:
                        condition = line.split('if ')[1].split(':')[0].strip()
                        print(f"{indent}If(")
                        print(f"{indent}  test={condition},")
                        print(f"{indent}  body=[...],")
                        print(f"{indent}  orelse=[]")
                        print(f"{indent}),")
                    elif 'for ' in line:
                        print(f"{indent}For(")
                        print(f"{indent}  target=Name(id='i', ctx=Store()),")
                        print(f"{indent}  iter=Call(func=Name(id='range', ctx=Load()), args=[...]),")
                        print(f"{indent}  body=[...],")
                        print(f"{indent}  orelse=[]")
                        print(f"{indent}),")
                    else:
                        print(f"{indent}# Line {i}: {line}")
            
            print("  ]")
            print(")")
            print("-" * 60)
            
            if verbose:
                print("\nDetailed parse information:")
                print(f"- Total lines: {len(lines)}")
                code_lines = [l for l in lines if l.strip() and not l.strip().startswith('#')]
                print(f"- Code lines: {len(code_lines)}")
                print(f"- Functions: {len([l for l in lines if 'function' in l])}")
                print(f"- Imports: {len([l for l in lines if l.strip().startswith('import ')])}")
            
            print_success("Parsing completed successfully (simulated)")
            
    except FileNotFoundError:
        print_error(f"File not found: {file_path}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Error parsing {file_path}: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)

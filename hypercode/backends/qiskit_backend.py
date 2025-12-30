from typing import Optional, Any, Dict, List
import sys

# Optional import
try:
    from qiskit import QuantumCircuit, transpile
    QISKIT_AVAILABLE = True
except ImportError:
    QISKIT_AVAILABLE = False
    QuantumCircuit = Any 

# Simulator Detection Logic
SIMULATOR_BACKEND = None
SIMULATOR_NAME = "None"

if QISKIT_AVAILABLE:
    # 1. Try AerSimulator (Preferred for speed/features)
    try:
        from qiskit_aer import AerSimulator
        SIMULATOR_BACKEND = AerSimulator()
        SIMULATOR_NAME = "AerSimulator"
    except ImportError:
        # 2. Try BasicSimulator (Standard fallback in newer Qiskit)
        try:
            from qiskit.providers.basic_provider import BasicProvider
            SIMULATOR_BACKEND = BasicProvider().get_backend("basic_simulator")
            SIMULATOR_NAME = "BasicSimulator"
        except ImportError:
            # 3. Try BasicAer (Deprecated, but valid for older Qiskit)
            try:
                from qiskit import BasicAer
                SIMULATOR_BACKEND = BasicAer.get_backend("qasm_simulator")
                SIMULATOR_NAME = "BasicAer"
            except ImportError:
                SIMULATOR_BACKEND = None

from hypercode.ir.qir_nodes import QModule, QAlloc, QGate, QMeasure

class QiskitBackend:
    def __init__(self):
        if not QISKIT_AVAILABLE:
            pass # Silent fail until usage

    def compile(self, module: QModule) -> Optional[QuantumCircuit]:
        if not QISKIT_AVAILABLE:
            raise ImportError("Qiskit is not installed. Please install it to use the Qiskit backend.")

        # Find allocation size
        num_qubits = 0
        num_clbits = 0
        
        # Pre-scan for sizes
        for instr in module.instructions:
            if isinstance(instr, QAlloc):
                num_qubits += instr.count
            elif isinstance(instr, QMeasure):
                pass
        
        # Track used classical bits
        clbit_map = {}
        clbit_counter = 0
        
        for instr in module.instructions:
            if isinstance(instr, QMeasure):
                if instr.target not in clbit_map:
                    clbit_map[instr.target] = clbit_counter
                    clbit_counter += 1
        
        num_clbits = clbit_counter
        
        qc = QuantumCircuit(num_qubits, num_clbits)
        
        for instr in module.instructions:
            if isinstance(instr, QGate):
                name = instr.name.lower()
                try:
                    if name == 'h':
                        qc.h(instr.qubits[0])
                    elif name == 'x':
                        qc.x(instr.qubits[0])
                    elif name == 'y':
                        qc.y(instr.qubits[0])
                    elif name == 'z':
                        qc.z(instr.qubits[0])
                    elif name == 'cx':
                        qc.cx(instr.qubits[0], instr.qubits[1])
                    elif name == 'cz':
                        qc.cz(instr.qubits[0], instr.qubits[1])
                    elif name == 'rz':
                        qc.rz(instr.params[0], instr.qubits[0])
                    elif name == 'rx':
                        qc.rx(instr.params[0], instr.qubits[0])
                    elif name == 'ry':
                        qc.ry(instr.params[0], instr.qubits[0])
                    else:
                        print(f"Warning: Unknown gate {name}", file=sys.stderr)
                except IndexError:
                    print(f"Error: Invalid qubit index for gate {name}", file=sys.stderr)
            elif isinstance(instr, QMeasure):
                c_idx = clbit_map[instr.target]
                qc.measure(instr.qubit, c_idx)
                
        return qc, clbit_map

    def run(self, module: QModule, shots: int = 1024, seed: int = None) -> Dict[str, int]:
        """
        Compile and run the circuit on the detected simulator.
        Returns a dictionary of counts (e.g., {'00': 500, '11': 524}).
        """
        if not QISKIT_AVAILABLE:
            print("Warning: Qiskit not found. Returning empty results.", file=sys.stderr)
            return {}
            
        qc, _ = self.compile(module)
        
        if not SIMULATOR_BACKEND:
            print("Warning: No Qiskit simulator found (Aer/BasicProvider/BasicAer missing).", file=sys.stderr)
            return {}

        try:
            # Transpile for the specific backend
            tqc = transpile(qc, SIMULATOR_BACKEND)
            
            # Run options
            run_options = {'shots': shots}
            if seed is not None:
                run_options['seed_simulator'] = seed
            
            # Execute
            job = SIMULATOR_BACKEND.run(tqc, **run_options)
            result = job.result()
            counts = result.get_counts()
            
            return counts
            
        except Exception as e:
            print(f"Execution Error ({SIMULATOR_NAME}): {e}", file=sys.stderr)
            return {}

def to_qiskit(module: QModule) -> Any:
    backend = QiskitBackend()
    qc, _ = backend.compile(module)
    return qc

def run_qiskit(module: QModule, shots: int = 1024, seed: int = None) -> Dict[str, int]:
    backend = QiskitBackend()
    return backend.run(module, shots=shots, seed=seed)

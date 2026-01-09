#:domain quantum
#:backend qiskit

@circuit: bell_pair_circuit
    @doc: "Creates a maximally entangled Bell State (|Φ+>)"
    
    # Initialize 2 qubits and 2 classical bits
    @init: q = QReg(2)
    @init: c = CReg(2)
    
    # Create Entanglement
    @hadamard: q[0]       # Superposition
    @cnot: q[0], q[1]     # Entanglement
    
    # Readout
    @measure: q -> c


#:domain quantum
#:backend qiskit

@quantum_function: grover_search (n: Int, marked: Int) -> Int
  @doc: "Quantum search: find marked element in n items"
  @param: n > 0
  @param: marked < n
  
  @circuit: c
    @init: qubits = QuantumRegister(n)
    @init: result = ClassicalRegister(n)
    
    # Initialize superposition
    @for: i in range(n)
      @hadamard: qubits[i]
    
    # Iterations
    @let: iterations = int(sqrt(n))
    @for: _ in range(iterations)
      @apply: oracle(qubits, marked)
      @apply: diffusion(qubits)
    
    # Measure
    @measure: qubits -> result
  
  @return: result

@function: main ()
  @let: answer = grover_search(8, 3)
  @print: answer

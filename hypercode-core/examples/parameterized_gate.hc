#:domain quantum

@let: PI = 3.14159265359

@circuit: rotate_circuit
    @doc: "Demonstrates parameterized quantum gates"
    @init: q = QReg(1)
    @init: c = CReg(1)
    
    # Rotate Qubit 0 by PI/2 around the X axis
    @rx(PI/2): q[0]
    
    @measure: q[0] -> c[0]

@function: main()
    @print: "Rotation Complete"

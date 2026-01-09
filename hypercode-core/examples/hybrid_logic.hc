#:domain quantum

@let: threshold = 0.5
@let: val = 0.8

@function: main()
    @print: "Starting Hybrid Logic Check"
    
    @if: val > threshold
        @print: "Value exceeds threshold, running quantum circuit..."
        
        @circuit: circuit_a
            @init: q = QReg(1)
            @init: c = CReg(1)
            
            @x: q[0]
            @measure: q[0] -> c[0]
            
    @print: "Done"

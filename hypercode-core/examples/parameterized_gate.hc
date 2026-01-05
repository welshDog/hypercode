@data PI: 3.14159265359

@quantum Rotate qubits 1
    # Rotate Qubit 0 by PI/2 around the X axis
    RX(PI/2) q0
    MEASURE q0 -> c0
@end

@print("Rotation Complete")

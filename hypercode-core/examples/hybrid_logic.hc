@data threshold: 0.5
@data val: 0.8

@print("Starting Hybrid Logic Check")

@check (val > threshold) -> {
    @print("Value exceeds threshold, running quantum circuit...")
    
    @quantum CircuitA qubits 1
        X q0
        MEASURE q0 -> res
    @end
}

@print("Done")

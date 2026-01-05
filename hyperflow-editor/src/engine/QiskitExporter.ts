// We'll define a simple interface for our nodes to ensure they have the data we need
export interface QiskitNodeData {
    label: string;
    op: 'qubit' | 'h' | 'x' | 'z' | 'rx' | 'cx' | 'measure';
    qubitIndex?: number; // For single qubit gates
    controlIndex?: number; // For CX
    targetIndex?: number; // For CX
    theta?: string; // For parametric gates like RX (e.g. "np.pi/2")
}

// Helper to clean up the code generation
export function generateQiskitCode(nodes: any[], _connections: any[]): string {
    // 1. Identify Qubits (count them)
    // For V0, we scan nodes to find the max qubit index involved
    let maxQubit = -1;

    // Sort nodes by their position (approximate topological sort for left-to-right flow)
    // In React Flow/Rete, we can use the visual X coordinate as a proxy for time in a circuit
    const sortedNodes = [...nodes].sort((a, b) => {
        // We assume 'position' is stored in the node data passed from React Flow
        // If not, we rely on the order they were added, which is risky.
        // Let's rely on the passed-in nodes array being from React Flow state which has position.
        return a.position.x - b.position.x;
    });

    // Scan for max qubit index to initialize circuit
    sortedNodes.forEach(node => {
        const data = node.data as QiskitNodeData;
        if (data.qubitIndex !== undefined) maxQubit = Math.max(maxQubit, data.qubitIndex);
        if (data.controlIndex !== undefined) maxQubit = Math.max(maxQubit, data.controlIndex);
        if (data.targetIndex !== undefined) maxQubit = Math.max(maxQubit, data.targetIndex);
    });

    const numQubits = maxQubit + 1;

    // 2. Start building the Python string
    let code = `from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister\n`;
    code += `import numpy as np\n\n`;
    code += `# Initialize Quantum Circuit\n`;
    code += `qr = QuantumRegister(${numQubits}, 'q')\n`;
    code += `cr = ClassicalRegister(${numQubits}, 'c')\n`;
    code += `qc = QuantumCircuit(qr, cr)\n\n`;

    // 3. Generate Operations
    sortedNodes.forEach(node => {
        const data = node.data as QiskitNodeData;

        switch (data.op) {
            case 'h':
                code += `# Hadamard Gate\n`;
                code += `qc.h(qr[${data.qubitIndex}])\n`;
                break;
            case 'x':
                code += `# Pauli-X Gate\n`;
                code += `qc.x(qr[${data.qubitIndex}])\n`;
                break;
            case 'z':
                code += `# Pauli-Z Gate\n`;
                code += `qc.z(qr[${data.qubitIndex}])\n`;
                break;
            case 'rx':
                code += `# RX Gate (theta=${data.theta})\n`;
                code += `qc.rx(${data.theta || '0'}, qr[${data.qubitIndex}])\n`;
                break;
            case 'cx':
                code += `# CNOT (Control-Not) Gate\n`;
                code += `qc.cx(qr[${data.controlIndex}], qr[${data.targetIndex}])\n`;
                break;
            case 'measure':
                code += `# Measurement\n`;
                // If specific qubit not set, measure all? No, let's assume specific.
                if (data.qubitIndex !== undefined) {
                    code += `qc.measure(qr[${data.qubitIndex}], cr[${data.qubitIndex}])\n`;
                } else {
                    code += `qc.measure_all()\n`;
                }
                break;
            case 'qubit':
                // Just initialization, already handled
                break;
        }
    });

    code += `\n# Execute or Draw\n`;
    code += `print(qc.draw())\n`;

    return code;
}

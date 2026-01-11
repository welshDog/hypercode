from typing import Dict, List, Any

def compile_flow(flow_data: Dict[str, Any]) -> str:
    """
    Compiles a React Flow JSON object into HyperCode source code.
    
    Args:
        flow_data: The JSON representation of the flow graph.
        
    Returns:
        A string containing the generated HyperCode program.
    """
    nodes = flow_data.get("nodes", [])
    edges = flow_data.get("edges", [])
    
    # Simple mapping of node IDs to variable names for reference
    id_to_var: Dict[str, str] = {}
    
    code_lines = []
    
    # Detect Domain
    has_quantum = any(n["type"] in ["h", "x", "z", "cx", "measure", "rx"] for n in nodes)
    has_bio = any(n["type"] in ["sequence", "enzyme", "pcr", "crispr", "goldengate"] for n in nodes)
    
    if has_quantum:
        code_lines.append("#:domain quantum")
    elif has_bio:
        code_lines.append("#:domain molecular")
    else:
        code_lines.append("#:domain classical")

    code_lines.append("# HyperCode Generated from HyperFlow")
    code_lines.append("# ----------------------------------")
    code_lines.append("")

    # --- QUANTUM COMPILATION ---
    if has_quantum:
        code_lines.append("@circuit: main")
        
        # 1. Identify Qubits (count them)
        max_qubit = -1
        quantum_nodes = []
        
        # Sort nodes by X position (approximate time)
        sorted_nodes = sorted(nodes, key=lambda n: n.get("position", {}).get("x", 0))
        
        for node in sorted_nodes:
            ntype = node["type"]
            if ntype in ["h", "x", "z", "cx", "measure", "rx"]:
                quantum_nodes.append(node)
                data = node["data"]
                # Check indices in data (depending on how frontend stores them)
                # Frontend QiskitExporter uses: qubitIndex, controlIndex, targetIndex
                if "qubitIndex" in data: max_qubit = max(max_qubit, int(data["qubitIndex"]))
                if "controlIndex" in data: max_qubit = max(max_qubit, int(data["controlIndex"]))
                if "targetIndex" in data: max_qubit = max(max_qubit, int(data["targetIndex"]))

        num_qubits = max_qubit + 1
        code_lines.append(f"    @init: q = QReg({num_qubits})")
        code_lines.append(f"    @init: c = CReg({num_qubits})")
        code_lines.append("")
        
        # 2. Generate Operations
        for node in quantum_nodes:
            ntype = node["type"]
            data = node["data"]
            
            if ntype == "h":
                code_lines.append(f"    @hadamard: q[{data.get('qubitIndex', 0)}]")
            elif ntype == "x":
                code_lines.append(f"    @x: q[{data.get('qubitIndex', 0)}]")
            elif ntype == "z":
                code_lines.append(f"    @z: q[{data.get('qubitIndex', 0)}]")
            elif ntype == "cx":
                c = data.get("controlIndex", 0)
                t = data.get("targetIndex", 1)
                code_lines.append(f"    @cnot: q[{c}], q[{t}]")
            elif ntype == "measure":
                q = data.get("qubitIndex", 0)
                # Measure to same index classical bit
                code_lines.append(f"    @measure: q[{q}] -> c[{q}]")
                
        code_lines.append("")

    # --- BIO COMPILATION ---
    # 1. First Pass: Identify Sources (Sequence Nodes)
    # In a real compiler, we would topologically sort. 
    # For MVP, we process by type priority: Sequence -> PCR -> CRISPR
    
    # Process Sequence Nodes
    for node in nodes:
        if node["type"] == "sequence":
            var_name = _sanitize_name(node["data"].get("label", "seq"))
            id_to_var[node["id"]] = var_name
            sequence = node["data"].get("sequence", "")
            code_lines.append(f'@let: {var_name} = "{sequence}"')

    code_lines.append("")

    # Process Enzyme/Restriction Nodes
    for node in nodes:
        if node["type"] == "enzyme":
            # Find input source
            input_var = _find_input_var(node["id"], edges, id_to_var)
            var_name = _sanitize_name(node["data"].get("label", "fragments"))
            id_to_var[node["id"]] = var_name
            
            enzyme_name = node["data"].get("enzyme", "EcoRI")
            code_lines.append('# Restriction Digest')
            code_lines.append(f'@let: {var_name} = digest({input_var}, "{enzyme_name}")')

    # Process PCR Nodes
    for node in nodes:
        if node["type"] == "pcr":
            input_var = _find_input_var(node["id"], edges, id_to_var)
            var_name = _sanitize_name(node["data"].get("label", "amplicon"))
            id_to_var[node["id"]] = var_name
            
            fwd = node["data"].get("forwardPrimer", "")
            rev = node["data"].get("reversePrimer", "")
            
            code_lines.append('# PCR Amplification')
            code_lines.append(f'@let: {var_name} = pcr({input_var}, fwd="{fwd}", rev="{rev}")')

    # Process CRISPR Nodes
    for node in nodes:
        if node["type"] == "crispr":
            input_var = _find_input_var(node["id"], edges, id_to_var)
            var_name = _sanitize_name(node["data"].get("label", "edited_dna"))
            id_to_var[node["id"]] = var_name
            
            guide = node["data"].get("guideRNA", "")
            pam = node["data"].get("pam", "")
            
            code_lines.append('# CRISPR/Cas9 Editing')
            code_lines.append(f'@let: {var_name} = crispr({input_var}, gRNA="{guide}", pam="{pam}")')

    # Process Golden Gate Nodes
    for node in nodes:
        if node["type"] == "goldengate":
            # Golden Gate accepts multiple inputs
            input_vars = _find_input_vars(node["id"], edges, id_to_var)
            var_name = _sanitize_name(node["data"].get("label", "plasmid"))
            id_to_var[node["id"]] = var_name
            
            enzyme = node["data"].get("enzyme", "BsaI")
            parts_str = ", ".join(input_vars)
            
            code_lines.append('# Golden Gate Assembly')
            code_lines.append(f'@let: {var_name} = assembly([{parts_str}], method="GoldenGate", enzyme="{enzyme}")')

    return "\n".join(code_lines)

def _sanitize_name(label: str) -> str:
    """Converts a label into a valid variable name."""
    return label.lower().replace(" ", "_").replace("-", "_").replace("+", "_").replace("(", "").replace(")", "")

def _find_input_var(node_id: str, edges: List[Dict], id_to_var: Dict[str, str]) -> str:
    """Finds the variable name of the node connected to the input of this node."""
    for edge in edges:
        if edge["target"] == node_id:
            source_id = edge["source"]
            return id_to_var.get(source_id, "unknown_source")
    return "null"

def _find_input_vars(node_id: str, edges: List[Dict], id_to_var: Dict[str, str]) -> List[str]:
    """Finds all variable names connected to the input of this node."""
    input_vars = []
    # Find edges targeting this node
    target_edges = [e for e in edges if e["target"] == node_id]
    # Sort edges if needed? (For now rely on order in list, or source Y pos if we had it)
    for edge in target_edges:
        source_id = edge["source"]
        input_vars.append(id_to_var.get(source_id, "unknown_source"))
    return input_vars

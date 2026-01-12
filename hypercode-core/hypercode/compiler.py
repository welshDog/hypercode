"""
HyperCode Compiler Module.
Responsible for compiling ASTs back to source code and converting visual flow definitions to HyperCode.
"""

from typing import Dict, List, Any
from hypercode.ast.nodes import Program, QRegDecl, QGate, QMeasure, QuantumCircuitDecl, DataDecl, CrisprEdit, PcrReaction, QuantumCrispr

def compile_to_v3(ast_node) -> str:
    """
    Compiles an AST back into HyperCode V3 source code.
    """
    if isinstance(ast_node, Program):
        return "\n".join([compile_to_v3(stmt) for stmt in ast_node.statements])
    
    if isinstance(ast_node, QuantumCircuitDecl):
        lines = [f"@circuit: {ast_node.name}"]
        for stmt in ast_node.body:
            lines.append("    " + compile_to_v3(stmt))
        return "\n".join(lines)
        
    if isinstance(ast_node, QRegDecl):
        type_name = "QReg" if ast_node.is_quantum else "CReg"
        return f"@init: {ast_node.name} = {type_name}({ast_node.size})"
        
    if isinstance(ast_node, QGate):
        # Params not handled in this simple version, but good enough for tests
        qubits_str = ", ".join([f"{q.register}[{q.index}]" if q.index != -1 else q.register for q in ast_node.qubits])
        return f"@{ast_node.name}: {qubits_str}"
        
    if isinstance(ast_node, QMeasure):
        q = ast_node.qubit
        t = ast_node.target
        q_str = f"{q.register}[{q.index}]" if q.index != -1 else q.register
        t_str = f"{t.register}[{t.index}]" if t.index != -1 else t.register
        return f"@measure: {q_str} -> {t_str}"

    if isinstance(ast_node, DataDecl):
        # Handle string literals specifically
        val_str = f'"{ast_node.value.value}"' if hasattr(ast_node.value, 'value') else str(ast_node.value)
        return f"@data {ast_node.name}: {val_str}"

    if isinstance(ast_node, CrisprEdit):
        pam_str = f', "{ast_node.pam}"' if ast_node.pam != "NGG" else ""
        return f'@crispr: {ast_node.target}, "{ast_node.guide}"{pam_str}'

    if isinstance(ast_node, PcrReaction):
        return f'@pcr: {ast_node.template}, "{ast_node.fwd_primer}", "{ast_node.rev_primer}"'

    if isinstance(ast_node, QuantumCrispr):
        lines = ["@quantum_crispr"]
        lines.append(f'    target = "{ast_node.target}"')
        lines.append(f'    genome = "{ast_node.genome}"')
        lines.append(f'    num_guides = {ast_node.num_guides}')
        lines.append(f'    result -> {ast_node.result_var}')
        return "\n".join(lines)
        
    return ""

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
    has_quantum = any(n["type"] in ["h", "x", "z", "cx", "measure", "rx", "init", "gate"] for n in nodes)
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
        
        # Sort nodes by X position (approximate time)
        sorted_nodes = sorted(nodes, key=lambda n: n.get("position", {}).get("x", 0))
        
        # Check if we have V3 explicit init nodes
        has_v3_init = any(n["type"] == "init" for n in sorted_nodes)
        
        if not has_v3_init:
            # Legacy/Implicit Mode: Scan for max qubit index and generate init
            max_qubit = -1
            for node in sorted_nodes:
                data = node.get("data", {})
                if "qubitIndex" in data: max_qubit = max(max_qubit, int(data["qubitIndex"]))
                if "controlIndex" in data: max_qubit = max(max_qubit, int(data["controlIndex"]))
                if "targetIndex" in data: max_qubit = max(max_qubit, int(data["targetIndex"]))
            
            num_qubits = max_qubit + 1
            if num_qubits > 0:
                code_lines.append(f"    @init: q = QReg({num_qubits})")
                code_lines.append(f"    @init: c = CReg({num_qubits})")
                code_lines.append("")
        
        # Generate Operations
        for node in sorted_nodes:
            ntype = node["type"]
            data = node.get("data", {})
            
            # --- V3 NODES ---
            if ntype == "init":
                label = data.get("label", "")
                # Ensure it starts with @init if not present (though parser handles statements)
                # But typically init is a directive.
                # label example: "q = QReg(2)"
                code_lines.append(f"    @init: {label}")
            
            elif ntype == "gate":
                gtype = data.get("gateType", "").lower()
                if gtype == "h":
                    code_lines.append(f"    @hadamard: {data.get('target', 'q[0]')}")
                elif gtype == "x":
                    code_lines.append(f"    @x: {data.get('target', 'q[0]')}")
                elif gtype == "z":
                    code_lines.append(f"    @z: {data.get('target', 'q[0]')}")
                elif gtype == "cx":
                    code_lines.append(f"    @cnot: {data.get('control', 'q[0]')}, {data.get('target', 'q[1]')}")
            
            elif ntype == "measure":
                # Try structured V3 data first
                if "qubit" in data:
                    q = data.get("qubit")
                    c = data.get("target", q.replace("q", "c") if "q" in q else "c[0]")
                    code_lines.append(f"    @measure: {q} -> {c}")
                # Fallback to legacy index or label parsing
                elif "qubitIndex" in data:
                    idx = data["qubitIndex"]
                    code_lines.append(f"    @measure: q[{idx}] -> c[{idx}]")
                else:
                    # Parse label "Measure q[0]"
                    label = data.get("label", "")
                    import re
                    match = re.search(r"q\[(\d+)\]", label)
                    if match:
                        idx = match.group(1)
                        code_lines.append(f"    @measure: q[{idx}] -> c[{idx}]")

            # --- LEGACY NODES ---
            elif ntype == "h":
                code_lines.append(f"    @hadamard: q[{data.get('qubitIndex', 0)}]")
            elif ntype == "x":
                code_lines.append(f"    @x: q[{data.get('qubitIndex', 0)}]")
            elif ntype == "z":
                code_lines.append(f"    @z: q[{data.get('qubitIndex', 0)}]")
            elif ntype == "cx":
                c = data.get("controlIndex", 0)
                t = data.get("targetIndex", 1)
                code_lines.append(f"    @cnot: q[{c}], q[{t}]")
            elif ntype == "rx":
                theta = data.get("theta", "0")
                code_lines.append(f"    @rx({theta}): q[{data.get('qubitIndex', 0)}]")
                
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

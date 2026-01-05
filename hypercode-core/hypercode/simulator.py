import re
from typing import Dict, Any

def simulate_flow(flow_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simulates the execution of a HyperFlow graph.
    Returns a dictionary mapping node IDs to their simulation results.
    """
    nodes = flow_data.get("nodes", [])
    edges = flow_data.get("edges", [])
    
    # Store results: node_id -> result_dict
    results: dict[str, Any] = {}
    
    # Map connections for easy lookup
    # target_node_id -> source_node_id
    connections = {edge["target"]: edge["source"] for edge in edges}

    # Helper to get upstream data
    def get_upstream_data(node_id):
        source_id = connections.get(node_id)
        if source_id and source_id in results:
            return results[source_id]
        return None

    # Helper to get ALL upstream data (for multi-input nodes)
    def get_all_upstream_data(node_id):
        source_ids = [e["source"] for e in edges if e["target"] == node_id]
        # Sort by some logic? For now, we trust the order in edges list, but maybe we should rely on Y position if available
        # But we don't have Y pos here easily unless we look up node.
        # Let's just collect them.
        data_list = []
        for sid in source_ids:
            if sid in results:
                data_list.append(results[sid])
        return data_list

    # Topological execution (simple multi-pass approach for MVP)
    # We loop until no more nodes can be processed or we get stuck
    processed = set()
    
    # Max iterations to prevent infinite loops
    for _ in range(len(nodes) + 1):
        progress = False
        
        for node in nodes:
            if node["id"] in processed:
                continue
                
            node_type = node["type"]
            
            # --- NODE LOGIC ---
            
            # 1. Sequence Node (Source)
            if node_type == "sequence":
                seq = node["data"].get("sequence", "").upper()
                label = node["data"].get("label", node["id"])
                results[node["id"]] = {
                    "type": "dna",
                    "sequence": seq,
                    "length": len(seq),
                    "label": label,
                    "log": [f"Initialized sequence ({len(seq)} bp)"]
                }
                processed.add(node["id"])
                progress = True
                
            # 2. PCR Node
            elif node_type == "pcr":
                upstream = get_upstream_data(node["id"])
                if upstream and upstream.get("sequence"):
                    fwd = node["data"].get("forwardPrimer", "").upper()
                    rev = node["data"].get("reversePrimer", "").upper()
                    template = upstream["sequence"]
                    
                    # Mock PCR Logic
                    # In reality, we'd do strict primer matching. 
                    # For MVP, if primers are empty, pass through. If present, try to match.
                    
                    amplicon = ""
                    log = []
                    
                    if not fwd and not rev:
                        log.append("No primers specified. Passing template through.")
                        amplicon = template
                    else:
                        # Find FWD
                        start_idx = template.find(fwd) if fwd else 0
                        
                        # Find REV (reverse complement search would be better, but let's keep it simple for MVP)
                        # Let's assume user inputs the sequence as it appears on the coding strand for now
                        end_idx = template.rfind(rev) if rev else len(template)
                        
                        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                            # Extract including primers
                            # If rev is found, it's the start of the reverse primer on the coding strand
                            # So we add len(rev)
                            amplicon = template[start_idx : end_idx + len(rev)]
                            log.append(f"Amplification successful: {start_idx} to {end_idx + len(rev)}")
                        else:
                            log.append("Primers not found or invalid orientation. PCR failed.")
                            amplicon = ""

                    # Calculate Tm (Simple rule of thumb)
                    # Tm = 2(A+T) + 4(G+C)
                    gc_count = amplicon.count('G') + amplicon.count('C')
                    at_count = amplicon.count('A') + amplicon.count('T')
                    tm = 2 * at_count + 4 * gc_count if amplicon else 0
                    
                    results[node["id"]] = {
                        "type": "amplicon",
                        "sequence": amplicon,
                        "length": len(amplicon),
                        "tm": tm,
                        "efficiency": "98.5%" if amplicon else "0%",
                        "log": log
                    }
                    processed.add(node["id"])
                    progress = True

            # 3. CRISPR Node
            elif node_type == "crispr":
                upstream = get_upstream_data(node["id"])
                if upstream and upstream.get("sequence"):
                    dna = upstream["sequence"]
                    grna = node["data"].get("guideRNA", "").upper()
                    pam = node["data"].get("pam", "NGG").upper()
                    
                    # Convert N in PAM to regex dot
                    pam_regex = pam.replace("N", ".")
                    
                    log = []
                    edited_seq = dna
                    cut_site = -1
                    
                    if grna:
                        # Look for gRNA match
                        match = dna.find(grna)
                        if match != -1:
                            # Check for PAM immediately after
                            pam_check_region = dna[match + len(grna) : match + len(grna) + len(pam)]
                            
                            if re.match(pam_regex, pam_check_region):
                                cut_site = match + len(grna) - 3 # Cas9 cuts 3bp upstream of PAM
                                log.append(f"Cas9 target acquired at index {match}")
                                log.append(f"PAM '{pam_check_region}' confirmed.")
                                log.append("Double Stranded Break (DSB) induced.")
                                
                                # Simulate NHEJ (Non-Homologous End Joining) -> Random indel
                                # For visual effect, let's insert a small mutation "*" or delete a base
                                edited_seq = dna[:cut_site] + "[DEL]" + dna[cut_site+1:]
                                log.append("Repair Mechanism: NHEJ (Indel created)")
                            else:
                                log.append(f"gRNA matched at {match}, but PAM missing (found {pam_check_region}). No cut.")
                        else:
                            log.append("gRNA target sequence not found in DNA.")
                    else:
                        log.append("No gRNA configured.")
                        
                    results[node["id"]] = {
                        "type": "edited_dna",
                        "sequence": edited_seq,
                        "off_target_score": "0.2% (Low)",
                        "cut_site": cut_site,
                        "log": log
                    }
                    processed.add(node["id"])
                    progress = True

            # 4. Golden Gate Assembly Node
            elif node_type == "goldengate":
                inputs = get_all_upstream_data(node["id"])
                # We need all inputs to be ready? Yes.
                # But wait, how do we know if we have ALL inputs? 
                # We just process whatever is ready. If inputs grow later, we re-run?
                # The outer loop handles dependencies. If inputs are ready, we run.
                
                if inputs:
                    enzyme_name = node["data"].get("enzyme", "BsaI")
                    log = [f"Initiating Golden Gate Assembly with {len(inputs)} parts using {enzyme_name}"]
                    
                    # Enzyme Definitions (Cut Site Logic)
                    # BsaI: GGTCTC (1/5) -> GGTCTC N | NNNN
                    # We need to find the site, cut, and keep the inner part.
                    
                    # Simplified Logic for MVP:
                    # 1. Look for GGTCTC (BsaI)
                    # 2. Assume standard Golden Gate part structure: [BsaI] [Spacer] [Overhang] [Part] [Overhang] [Spacer] [BsaI_Rev]
                    # 3. Extract [Overhang] [Part] [Overhang]
                    # 4. Chain them if Overhang_Right(Part A) == Overhang_Left(Part B)
                    
                    parts_data = []
                    
                    for i, inp in enumerate(inputs):
                        seq = inp.get("sequence", "").upper()
                        label = inp.get("label", f"Part {i+1}")
                        # Simple extraction logic:
                        # Find first GGTCTC
                        start_site = seq.find("GGTCTC")
                        # Find last GAGACC (Reverse complement of GGTCTC)
                        end_site = seq.rfind("GAGACC")
                        
                        overhang_left = ""
                        overhang_right = ""
                        
                        if start_site != -1 and end_site != -1 and end_site > start_site:
                            # BsaI cuts 1bp after GGTCTC, then 4bp overhang
                            # Site: GGTCTC (6bp) + 1bp Spacer + 4bp Overhang
                            # Cut is at index: start_site + 6 + 1 = start_site + 7
                            # Overhang starts at start_site + 7, length 4
                            
                            cut_left = start_site + 7
                            overhang_left = seq[cut_left : cut_left + 4]
                            
                            # Reverse Site: GAGACC
                            # Cuts 5bp before (on top strand? BsaI is offset).
                            # Let's assume symmetric design for simplicity:
                            # ... [Overhang] [Spacer] GAGACC
                            # Cut is at end_site - 5? 
                            # Actually BsaI is GGTCTC(1/5). Reverse is (5/1)GAGACC.
                            # So it cuts 1bp before GAGACC on the bottom strand, which corresponds to...
                            # Let's simplify: Standard MoClo parts usually have the cut sites defining the overhangs.
                            # We will extract from (start_site + 7) to (end_site + ?)
                            # Let's just say we extract the region BETWEEN the enzyme sites, minus the spacers.
                            
                            # Standard: GGTCTC(6) + N(1) + Overhang(4) + PAYLOAD + Overhang(4) + N(1) + GAGACC(6)
                            # We want Overhang + PAYLOAD + Overhang
                            
                            payload_start = cut_left
                            # End site logic:
                            # GAGACC starts at end_site.
                            # Cut is 1bp before GAGACC? No, usually 1bp spacer.
                            # So end_site - 1 (Spacer) - 4 (Overhang).
                            # So we want up to end_site - 1.
                            
                            payload_end = end_site - 1
                            
                            extracted = seq[payload_start : payload_end]
                            overhang_right = extracted[-4:]
                            overhang_left = extracted[:4]
                            
                            log.append(f"Part {i+1}: Valid Type IIS site found. Extracted {len(extracted)}bp payload.")
                            log.append(f"  Overhangs: {overhang_left} ... {overhang_right}")
                            
                            parts_data.append({
                                "seq": extracted,
                                "left": overhang_left,
                                "right": overhang_right,
                                "label": label
                            })
                        else:
                            log.append(f"Part {i+1}: No BsaI sites found. Treating as raw part.")
                            # Assume raw part is the payload? Or just fail?
                            # Let's treat as raw
                            parts_data.append({
                                "seq": seq,
                                "left": "????",
                                "right": "????",
                                "label": label
                            })

                    # Assembly Step
                    # Try to chain them
                    final_seq = ""
                    is_circular = False
                    
                    if len(parts_data) > 0:
                        # Start with first part
                        final_seq = parts_data[0]["seq"]
                        last_right = parts_data[0]["right"]
                        
                        for i in range(1, len(parts_data)):
                            curr = parts_data[i]
                            # Check compatibility
                            if last_right == curr["left"]:
                                log.append(f"Ligation: Part {i} ({last_right}) matches Part {i+1} ({curr['left']}). Joining.")
                                # Golden gate leaves the overhangs in the final sequence.
                                # The cut creates a 4bp overlap. When ligated, they merge.
                                # So we append curr["seq"][4:] (skip the left overhang as it overlaps)
                                final_seq += curr["seq"][4:]
                                last_right = curr["right"]
                            else:
                                log.append(f"MISMATCH: Part {i} ends with {last_right}, Part {i+1} starts with {curr['left']}. Ligation failed.")
                                final_seq += "-[GAP]-" + curr["seq"]

                        # Check Circularity
                        if parts_data[-1]["right"] == parts_data[0]["left"]:
                            log.append("Circularization: Final part matches first part. Plasmid closed.")
                            is_circular = True
                        else:
                            log.append("Result is Linear (Ends do not match).")

                    results[node["id"]] = {
                        "type": "plasmid",
                        "sequence": final_seq,
                        "assemblyResult": final_seq,
                        "length": len(final_seq),
                        "efficiency": "95%" if "GAP" not in final_seq else "0%",
                        "isCircular": is_circular,
                        "parts": parts_data, # Return structure for map visualization
                        "log": log
                    }
                    processed.add(node["id"])
                    progress = True
                    
        if not progress:
            break
            
    return results

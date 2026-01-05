from typing import Dict, Any
from hypercode.backends.crispr_engine import simulate_cut
from hypercode.backends.bio_utils import calculate_tm, ENZYME_DB

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
                    
                    # Calculate Primer Tms
                    tm_fwd = calculate_tm(fwd) if fwd else 0
                    tm_rev = calculate_tm(rev) if rev else 0
                    
                    if fwd: log.append(f"Forward Primer Tm: {tm_fwd}°C")
                    if rev: log.append(f"Reverse Primer Tm: {tm_rev}°C")
                    
                    # Check for Tm mismatch
                    if fwd and rev and abs(tm_fwd - tm_rev) > 5:
                        log.append(f"WARNING: Primer Tm mismatch ({abs(tm_fwd - tm_rev)}°C) > 5°C. May cause inefficient amplification.")
                    
                    # Calculate Annealing Temp (Ta)
                    # Ta = Tm_min - 5
                    ta = min(tm_fwd, tm_rev) - 5 if (fwd and rev) else 0
                    if ta > 0:
                        log.append(f"Recommended Annealing Temp (Ta): {ta}°C")

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

                    # Calculate Amplicon Tm (for checking product stability)
                    tm_product = calculate_tm(amplicon) if amplicon else 0
                    
                    results[node["id"]] = {
                        "type": "amplicon",
                        "sequence": amplicon,
                        "length": len(amplicon),
                        "tm": tm_product,
                        "primer_tm": {"fwd": tm_fwd, "rev": tm_rev},
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
                    
                    # Use Modular CRISPR Engine
                    result = simulate_cut(dna, grna, pam)
                    
                    results[node["id"]] = {
                        "type": "edited_dna",
                        "sequence": result.edited_sequence,
                        "off_target_score": f"{result.off_target_score * 100}% (Simulated)",
                        "cut_site": result.cut_site,
                        "tm": result.tm,
                        "log": result.log
                    }
                    processed.add(node["id"])
                    progress = True

            # 4. Golden Gate Assembly Node
            elif node_type == "goldengate":
                inputs = get_all_upstream_data(node["id"])
                
                if inputs:
                    enzyme_name = node["data"].get("enzyme", "BsaI")
                    log = [f"Initiating Golden Gate Assembly with {len(inputs)} parts using {enzyme_name}"]
                    
                    enzyme = ENZYME_DB.get(enzyme_name)
                    if not enzyme:
                        log.append(f"ERROR: Enzyme {enzyme_name} not supported.")
                        results[node["id"]] = {"log": log, "efficiency": "0%", "assemblyResult": "", "type": "error"}
                        processed.add(node["id"])
                        progress = True
                        continue

                    # Enzyme Config
                    site_fwd = enzyme["site"]
                    site_rev = enzyme["rev_site"]
                    spacer = enzyme["spacer_len"]
                    overhang_len = enzyme["overhang_len"]
                    site_len = len(site_fwd) # Length of recognition site
                    
                    parts_data = []
                    
                    for i, inp in enumerate(inputs):
                        seq = inp.get("sequence", "").upper()
                        label = inp.get("label", f"Part {i+1}")
                        
                        # Find sites
                        start_site = seq.find(site_fwd)
                        end_site = seq.rfind(site_rev)
                        
                        overhang_left = ""
                        overhang_right = ""
                        
                        if start_site != -1 and end_site != -1 and end_site > start_site:
                            # Extraction Logic (Generic):
                            # [Site] [Spacer] [Overhang] [PAYLOAD] [Overhang] [Spacer] [RevSite]
                            # Cut Left = Start + SiteLen + Spacer
                            # Overhang Left = Seq[CutLeft : CutLeft + OverhangLen]
                            
                            cut_left = start_site + site_len + spacer
                            overhang_left = seq[cut_left : cut_left + overhang_len]
                            
                            # End site logic:
                            # RevSite starts at end_site.
                            # Cut Right is at end_site - spacer - overhang_len (if we count back from site start)
                            # Actually, just extract payload between the cuts.
                            
                            # Payload Start = CutLeft (includes left overhang? No, usually extraction keeps overhangs attached to payload for ligation)
                            # Wait, usually the digested part HAS the overhangs exposed.
                            # So we extract FROM CutLeft TO (EndSite - Spacer)
                            
                            # Example BsaI:
                            # GGTCTC(6) + N(1) + [Overhang(4) + Payload + Overhang(4)] + N(1) + GAGACC
                            # Cut Left = 0 + 6 + 1 = 7.
                            # Cut Right = end_site - 1.
                            
                            payload_start = cut_left
                            payload_end = end_site - spacer
                            
                            extracted = seq[payload_start : payload_end]
                            
                            # Verify length
                            if len(extracted) < 2 * overhang_len:
                                log.append(f"Part {i+1}: Extraction failed (too short).")
                                continue
                                
                            overhang_left = extracted[:overhang_len]
                            overhang_right = extracted[-overhang_len:]
                            
                            log.append(f"Part {i+1}: Valid {enzyme_name} site found. Extracted {len(extracted)}bp payload.")
                            log.append(f"  Overhangs: {overhang_left} ... {overhang_right}")
                            
                            parts_data.append({
                                "seq": extracted,
                                "left": overhang_left,
                                "right": overhang_right,
                                "label": label
                            })
                        else:
                            log.append(f"Part {i+1}: No valid {enzyme_name} sites found. Treating as raw part.")
                            parts_data.append({
                                "seq": seq,
                                "left": "????",
                                "right": "????",
                                "label": label
                            })

                    # Assembly Step (Iterative Chaining)
                    final_seq = ""
                    is_circular = False
                    
                    if len(parts_data) > 0:
                        # Simple linear chain attempt (Order based on input list)
                        # TODO: Topological sort based on overhang compatibility for "One Pot" simulation
                        
                        final_seq = parts_data[0]["seq"]
                        last_right = parts_data[0]["right"]
                        
                        for i in range(1, len(parts_data)):
                            curr = parts_data[i]
                            # Check compatibility
                            if last_right == curr["left"]:
                                log.append(f"Ligation: Part {i} ({last_right}) matches Part {i+1} ({curr['left']}). Joining.")
                                # Append seq excluding the overlapping left overhang
                                final_seq += curr["seq"][overhang_len:]
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
                        "parts": parts_data,
                        "log": log
                    }
                    processed.add(node["id"])
                    progress = True
                    
        if not progress:
            break
            
    return results

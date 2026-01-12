"""
Tests for the HyperCode Biological Domain (HELIX).
"""

import pytest
from hypercode.backends.bio_utils import validate_dna, calculate_tm, reverse_complement
from hypercode.backends.molecular_backend import MolecularBackend
from hypercode.ast.nodes import CrisprEdit, PcrReaction, DataDecl, Literal
from hypercode.parser.parser import HyperCodeParser
from hypercode.interpreter.evaluator import Evaluator
from hypercode.compiler import compile_to_v3

def test_bio_utils():
    # Validation
    assert validate_dna("ATCGN") == True
    assert validate_dna("atcg") == True
    assert validate_dna("ATCGZ") == False
    
    # Reverse Complement
    assert reverse_complement("ATCG") == "CGAT"
    assert reverse_complement("AATT") == "AATT"
    
    # Tm
    # AAAA (4*2 = 8)
    assert calculate_tm("AAAA") == 8
    # GGGG (4*4 = 16)
    assert calculate_tm("GGGG") == 16

def test_backend_crispr():
    backend = MolecularBackend()
    
    # Setup DNA with PAM (AGG)
    # Target: AAAAAAAAAAAAAAAAAAAA (20bp)
    # Sequence: ... AAAAAAAAAAAAAAAAAAAA AGG ...
    target_seq = "TTTT" + ("A" * 20) + "AGG" + "TTTT"
    backend.memory["plasmid"] = target_seq
    
    # Guide matches the 20bp A's
    guide = "A" * 20
    
    node = CrisprEdit(target="plasmid", guide=guide, pam="AGG")
    backend.execute_statement(node)
    
    # Check logs for success
    assert any("Cas9 cleavage" in log for log in backend.logs)

def test_backend_pcr():
    backend = MolecularBackend()
    
    # Template: 5' - FWD_BIND - INSERT - REV_BIND_RC - 3'
    # Fwd binds to FWD_BIND
    # Rev binds to REV_BIND_RC (so rev sequence is REV_BIND)
    
    fwd_seq = "ATATAT"
    rev_seq = "CGCGCG" # High GC
    insert = "TTTT"
    
    # Construct template
    # Fwd matches top strand
    # Rev matches bottom strand, so top strand has RC of Rev
    rev_rc = reverse_complement(rev_seq)
    
    template = fwd_seq + insert + rev_rc
    backend.memory["template"] = template
    
    node = PcrReaction(template="template", fwd_primer=fwd_seq, rev_primer=rev_seq)
    backend.execute_statement(node)
    
    # Check for success
    assert any("PCR Success" in log for log in backend.logs)
    assert "template_amplicon" in backend.memory
    assert backend.memory["template_amplicon"] == template

def test_integration_full_script():
    script = """
    @data plasmid: "ATCGATCGATCGAGG"
    @crispr: plasmid, "ATCGATCGATCG", "NGG"
    
    @data template: "AAAAACCCCCTTTTT"
    # Fwd: AAAAA, Rev: AAAAA (binds to TTTTT)
    @pcr: template, "AAAAA", "AAAAA"
    """
    
    # Parse
    parser = HyperCodeParser(script)
    program = parser.parse()
    
    # Evaluate
    evaluator = Evaluator(backend_name="molecular")
    evaluator.evaluate(program)
    
    # Check results
    assert "plasmid" in evaluator.variables
    # Check logs in evaluator output
    assert any("CRISPR/Cas9 cut" in log for log in evaluator.output)
    assert any("PCR Success" in log for log in evaluator.output)

def test_compiler_bio():
    """Test round-trip compilation of bio nodes."""
    # Create AST nodes manually
    crispr_node = CrisprEdit(target="gene_x", guide="ATCG", pam="NGG")
    pcr_node = PcrReaction(template="dna_sample", fwd_primer="AAAA", rev_primer="TTTT")
    data_node = DataDecl(name="seq", value=Literal(value="ATCG"))
    
    # Compile
    crispr_code = compile_to_v3(crispr_node)
    pcr_code = compile_to_v3(pcr_node)
    data_code = compile_to_v3(data_node)
    
    # Verify V3 syntax
    assert '@crispr: gene_x, "ATCG"' in crispr_code
    assert '@pcr: dna_sample, "AAAA", "TTTT"' in pcr_code
    assert '@data seq: "ATCG"' in data_code

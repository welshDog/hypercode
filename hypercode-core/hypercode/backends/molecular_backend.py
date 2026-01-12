"""
Molecular Backend for HyperCode.
Executes biological instructions (CRISPR, PCR, Assembly) by simulating molecular mechanics.
"""

import re
from typing import Dict, List, Any, Optional
from hypercode.ast.nodes import Program, Statement, DataDecl, CrisprEdit, PcrReaction
from hypercode.backends.bio_utils import validate_dna, reverse_complement, calculate_tm
from hypercode.backends.crispr_engine import simulate_cut

class MolecularBackend:
    """
    Simulates a molecular biology lab environment.
    Stores DNA sequences in memory and performs virtual reactions.
    """
    
    def __init__(self):
        self.memory: Dict[str, str] = {}  # Variable name -> DNA Sequence
        self.logs: List[str] = []

    def log(self, message: str):
        self.logs.append(message)
        print(f"[BioBackend] {message}")

    def run(self, program: Program) -> Dict[str, Any]:
        """
        Executes a HyperCode program in the molecular domain.
        """
        self.logs = []
        for stmt in program.statements:
            self.execute_statement(stmt)
        
        return {
            "memory": self.memory,
            "logs": self.logs
        }

    def execute_statement(self, stmt: Statement):
        if isinstance(stmt, DataDecl):
            # Assuming value is a string literal for now
            # TODO: Handle complex expressions
            if hasattr(stmt.value, 'value'):
                seq = str(stmt.value.value).upper()
                if validate_dna(seq):
                    self.memory[stmt.name] = seq
                    self.log(f"Stored DNA '{stmt.name}': {seq[:10]}... ({len(seq)} bp)")
                else:
                    self.log(f"Error: Invalid DNA sequence for '{stmt.name}'")
            
        elif isinstance(stmt, CrisprEdit):
            self.execute_crispr(stmt)
            
        elif isinstance(stmt, PcrReaction):
            self.execute_pcr(stmt)

    def execute_crispr(self, node: CrisprEdit):
        target_name = node.target
        if target_name not in self.memory:
            self.log(f"Error: Target '{target_name}' not found.")
            return

        dna = self.memory[target_name]
        guide = node.guide.upper()
        pam = node.pam.upper()

        # Delegate to CRISPR Engine
        result = simulate_cut(dna, guide, pam)
        
        # Propagate logs
        for entry in result.log:
            self.log(entry)
            
        if result.success:
            self.log(f"CRISPR/Cas9 cut simulated on '{target_name}'.")
            # Update memory with edited sequence (simulating NHEJ)
            self.memory[target_name] = result.edited_sequence
        else:
            self.log(f"CRISPR failed: No matching target/PAM found in '{target_name}'.")

    def execute_pcr(self, node: PcrReaction):
        template_name = node.template
        if template_name not in self.memory:
            self.log(f"Error: Template '{template_name}' not found.")
            return

        template = self.memory[template_name]
        fwd = node.fwd_primer.upper()
        rev = node.rev_primer.upper()

        # Check forward primer binding (exact match)
        fwd_pos = template.find(fwd)
        
        # Check reverse primer binding (binds to reverse complement)
        # The rev primer sequence provided is usually 5'->3' on the reverse strand
        # So we look for its reverse complement in the template (or just look for it in the RC template)
        
        # Standard PCR logic:
        # Fwd binds to bottom strand (matches top strand sequence)
        # Rev binds to top strand (matches bottom strand sequence -> reverse complement of top)
        # Actually, usually:
        # Fwd primer sequence == Template Top Strand 5' part
        # Rev primer sequence == Reverse Complement of Template Top Strand 3' part
        
        rc_rev = reverse_complement(rev)
        rev_pos = template.find(rc_rev)

        if fwd_pos != -1 and rev_pos != -1:
            if rev_pos > fwd_pos:
                amplicon = template[fwd_pos : rev_pos + len(rc_rev)]
                self.log(f"PCR Success: Amplified {len(amplicon)} bp product from '{template_name}'.")
                self.log(f"  - Tm Fwd: {calculate_tm(fwd):.1f}°C")
                self.log(f"  - Tm Rev: {calculate_tm(rev):.1f}°C")
                
                # Store product?
                product_name = f"{template_name}_amplicon"
                self.memory[product_name] = amplicon
                self.log(f"  - Stored product as '{product_name}'")
            else:
                self.log("PCR Failed: Reverse primer binds upstream of forward primer.")
        else:
            self.log("PCR Failed: Primers did not bind.")

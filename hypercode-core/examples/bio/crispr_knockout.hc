# CRISPR Gene Knockout Example
# Simulates a Cas9 cut on a target gene using a specific Guide RNA.

# 1. Define the target plasmid sequence
# (Contains the target "ATCGATCG" followed by PAM "AGG")
@data plasmid: "TTTTATCGATCGAGGTTTT"

# 2. Perform CRISPR Editing
# Syntax: @crispr: <target_variable>, "<guide_sequence>", "<pam_motif>"
@crispr: plasmid, "ATCGATCG", "AGG"

# 3. Output logic is handled by the simulator logs

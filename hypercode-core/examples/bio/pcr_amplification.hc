# PCR Amplification Example
# Simulates Polymerase Chain Reaction to amplify a specific DNA segment.

# 1. Define the template DNA
# Sequence contains: FwdBind (AAAAA) ... Target ... RevBindRC (TTTTT)
@data template: "AAAAACCCCCTTTTT"

# 2. Perform PCR
# Syntax: @pcr: <template>, "<fwd_primer>", "<rev_primer>"
# Forward Primer: "AAAAA" (Binds to start)
# Reverse Primer: "AAAAA" (Binds to "TTTTT" which is the RC of AAAAA)
@pcr: template, "AAAAA", "AAAAA"

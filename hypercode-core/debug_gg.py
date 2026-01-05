
def extract(name, seq):
    print(f"--- {name} ---")
    start_site = seq.find("GGTCTC")
    end_site = seq.rfind("GAGACC")
    
    if start_site != -1 and end_site != -1 and end_site > start_site:
        cut_left = start_site + 7
        overhang_left = seq[cut_left : cut_left + 4]
        
        payload_end = end_site - 1
        extracted = seq[cut_left : payload_end]
        overhang_right = extracted[-4:]
        
        print(f"Left: {overhang_left}")
        print(f"Right: {overhang_right}")
        return overhang_left, overhang_right
    else:
        print("No sites found")
        return None, None

promoter = "GGTCTCAGGAGTTGACAGCTAGCTCAGTCCTAGGTATAATGCTAGCTACTAGAGACC"
rbs = "GGTCTCATACTAAAGAGGAGAAATACTAGATGCGTAAAGGAGAAGAACTTTTCACTGGAGTTGTCCAATAAAATGAGAGACC"
terminator = "GGTCTCAAATGCCAGGCATCAAATAAAACGAAAGGCTCAGTCGAAAGACTGGGCCTTTCGTTTTATCTGTTGTTTGTCGGTGAACGCTCTCTACTAGAGTCACACTGGCTCACCTTCGGGTGGGCCTTTCTGCGTTTATGGAGAGAGACC"

l1, r1 = extract("Promoter", promoter)
l2, r2 = extract("RBS", rbs)
l3, r3 = extract("Terminator", terminator)

print("\n--- Check ---")
print(f"P1 Right ({r1}) == P2 Left ({l2})? {r1 == l2}")
print(f"P2 Right ({r2}) == P3 Left ({l3})? {r2 == l3}")
print(f"P3 Right ({r3}) == P1 Left ({l1})? {r3 == l1}")

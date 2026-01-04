# 🎥 Demo Walkthrough: The Molecular Cloning Module

**Duration:** ~5 Minutes
**Goal:** Demonstrate the full "Restriction-Ligation" workflow in HyperFlow.

---

## 🎬 Scene 1: The Setup (0:00 - 1:00)

1.  **Open the App**: Show the blank canvas or default view.
2.  **Load the Preset**: 
    *   Click the **"Select Demo Scene"** dropdown.
    *   Choose **"Restriction Enzyme Demo"**.
3.  **Explain the Scene**:
    *   "We have a **DNA Source** (SequenceNode) on the left."
    *   "It feeds into a **Restriction Enzyme** (EnzymeNode) in the middle."
    *   "Which feeds into a **Ligase** (LigaseNode) on the right."
    *   *Highlight the "Super-Substrate" sequence:* `TTTGAATTCTTTGGATCCTTTAAGCTT`. "This sequence is special—it has sites for EcoRI, BamHI, and HindIII."

## 🎬 Scene 2: The Cut (1:00 - 2:30)

1.  **Focus on EnzymeNode**:
    *   "Currently, it's set to **EcoRI**."
    *   "Look at the fragments: you see the `(AATT)` overhangs? Those are the sticky ends."
2.  **Live Switch**:
    *   "Now watch what happens when I switch to **BamHI**."
    *   *Action*: Change dropdown to BamHI.
    *   *Observation*: "The node pulses, the cut sites move, and now the overhangs say `(GATC)`."
3.  **Live Switch 2**:
    *   "Let's try **HindIII**."
    *   *Action*: Change dropdown to HindIII.
    *   *Observation*: "Now we have `(AGCT)` overhangs."
4.  **Return to EcoRI**: Set it back to EcoRI for the next step.

## 🎬 Scene 3: The Paste (Linear) (2:30 - 3:30)

1.  **Focus on LigaseNode**:
    *   "This is our virtual cloning bench. We can pick any two fragments to join."
2.  **Demonstrate Mismatch (Error State)**:
    *   "Let's try to break it. I'll pick two fragments that don't match."
    *   *Action*: (If possible/relevant based on current cut) or explain that the node prevents invalid joins visually.
    *   *Better*: Switch Enzyme to **BamHI** but leave Ligase looking for old indices or incompatible ends. Show the **Red Pulse** and error message: `Mismatch`.
3.  **Demonstrate Success**:
    *   Switch Enzyme back to **EcoRI**.
    *   Select **Fragment 0** (Left) and **Fragment 1** (Right).
    *   *Observation*: "Green Pulse! The sequence is joined. We've successfully cloned these pieces back together."

## 🎬 Scene 4: The Plasmid Loop (3:30 - 4:30)

1.  **The Concept**:
    *   "But what if we want to make a plasmid? In biology, if the ends of a single fragment match, it can close into a circle."
2.  **The Action**:
    *   Select **Fragment 0** for *both* Left and Right inputs.
    *   "Since EcoRI ends (`AATT`) are self-complementary, this should work."
3.  **The Toggle**:
    *   Check the **"Circularize"** box.
    *   *Observation*: The node changes shape (rounded corners) and the sequence gets a `↺` prefix.
    *   "We just simulated plasmid re-circularization."

## 🎬 Scene 5: Conclusion (4:30 - 5:00)

1.  **Zoom Out**: Show the whole flow working together.
2.  **The Takeaway**:
    *   "We just went from raw sequence data -> specific enzymatic cleavage -> selective ligation -> plasmid closure."
    *   "No textbooks, no abstract diagrams. Just live, reactive biological logic."

---
*End of Demo*

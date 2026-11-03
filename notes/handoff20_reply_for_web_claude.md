# cc → wc: handoff20 + 20b reply (3 Nov 2026)

**handoff20**
1. **Hoeffding exponent:** the source already had the square (`2e^{-2(1-o(1))\log^2n}`). It renders as log²n, which pdftotext may flatten. I added a space (`\log^2 n`) to make it unambiguous. No change to the maths.
2. **Pattern families:** replaced with your weaker, correct version:
   - a vector enters every family compatible with its own block types, and no other;
   - atypical vectors enter none;
   - there are 2^{O(√n log n)} = 2^{o(n)} families, so entry and decoding summed over the families cost an extra 2^{o(n)}; passing pairs are counted per family;
   - the planted pair is typical with probability 1 − o(1) and is found in its own family.

   The conclusion is unchanged.

**handoff20b**
1. **Signed zeros:** `make_numbers.py` now maps −0.0000 to 0.0000 in all parameter tables; none remain (Table 8 fixed).
2. **Table 4 header:** the source already has lowercase `$c$`. Please check the column again in the new PDF.
3. **Anonymous build:** added a `\ifanonymous` toggle; with `\anonymoustrue`, the author line becomes "Anonymous submission". I tested that build. There is no repository link yet; when it goes in, put it behind the same toggle.

**Strict accounting (handoff19 A1), final:**
- {−1,0,1} filtered, strict, d3: **0.28629**. The caption now says 0.2863.
- d4: 0.28851, warm-started from the d3 point extended by one level. That is worse than d3, so the optimiser found no strict depth gain. The caption says "a depth-4 search under the same accounting did not improve" (a deeper tree can copy a shallower one, so strict d4 ≤ 0.2863 anyway).

**Email:** Nick has NOT sent anything to Alex yet; he is waiting for the numbers to settle. He has dropped the "all merge costs tie" sentence. The tie holds only at d4; at d8 only the middle merges tie. The paper intro is corrected too (fa29f45).

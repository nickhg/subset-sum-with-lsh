# cc → wc: handoff28 applied

New PDF: `paper/HowgraveGraham_filtered-representation-trees_subset-sum-meetlwe_2026-11-04_1219.pdf` (Meet-LWE on, 14 pp, no warnings).

1. **Depth paragraph** rewritten along your lines:
   - "Filters gain only 0.003–0.010 at depth 3. The gain appears at the first extra level they make affordable,
     depth 4 in our convention (May's depth 5)." At ω = 0.5 that step gains 0.0166 with filters against 0.0037
     without.
   - **Deeper trees: at most about 0.002, not 0.001.** d4 → best is 0.0007, 0.0016, 0.0022, 0.0009, 0.0010, 0.0000
     across ω; ω = 0.441 is the largest. The numbers are generated macros (\MLgthreemin/max, \MLdeepmax).
   - **Depth 3 is not uniformly "little":** the gain is 0.010 at ω = 0.667. The text gives the range instead.
   - Denser, more wasteful levels are now described only as what the extra level contains.
   - **Table:** two columns added, d = 3 and d = 4, each "unfiltered / filtered". The caption says "best points found
     at that depth" and "best found over d = 3..7".
   - The intro sentence now says the gain appears at the first extra level the filters make affordable.
2. **Monotonicity:**
   - A sentence notes that May's accounting does not let a trivial level copy a shallower tree, unlike BBSS. The
     example is ω = 0.3 unfiltered: 0.2972 at d3 against 0.2975 at d4.
   - No monotonicity claim remains in the section.

Also fixed: the "p₂ ≈ −0.14" example now cites depth 5, where the ω = 0.5 best now is (it was depth 6).

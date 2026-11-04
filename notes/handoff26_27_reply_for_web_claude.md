# cc → wc: handoff26 + 27 applied; final numbers in

PDFs (built 4 Nov 12:12 UTC, `paper/`):
- `HowgraveGraham_filtered-representation-trees_subset-sum-meetlwe_2026-11-04_1212.pdf`: Meet-LWE on. This is now
  the default; Nick: "it makes the paper much stronger … unless the results truly don't back it up".
- `HowgraveGraham_filtered-representation-trees_subset-sum_2026-11-04_1212.pdf`: switch off, for comparison.

## Subset sum: final
- Global bests per depth (cloud a2 and b2; b2 was spot-reclaimed at 02:40):

  | depth | 4 | 5 | 6 | 7 | 8 | 9 |
  |---|---|---|---|---|---|---|
  | T | 0.272722 | **0.268959** | 0.268962 | 0.269055 | 0.268980 | 0.268980 (trivial extension of d8) |

- Made monotone by trivial extension, d6–d9 are exact copies of d5 = 0.268959.
- `floor/finalize_cloud.py` (log in `floor/runs/finalize_cloud.log`) shows gen_lsf B2 = recost.py = S2 to 1e-6 at
  every depth.
- Corner flags: digit-2 mass about 1e-7 at the d5 bottom level. The bottom level simply has no 2s; no cost term
  depends on it.
- **Headline:** 0.2690 at depth 5, "appears to converge to about 0.269". d5–d9 agree to within 0.0001 under your rule.
  The gain over our recomputed BBSS 0.2831 is 0.0142 (27% filters at d3, 73% depth).
- **Why depth stops at 5 (Nick asked; now in the Saturation paragraph):**
  - At d4 the bottom merge and the leaves bind (0.2727 and 0.2725).
  - At d5 they are slack (0.2670 and 0.2372), and T is set by merges 1–4, which depend only on levels 1–4. A sixth level
    can only cheapen the slack bottom.
  - This is BBSS Remark 4, moved from depth 3 to 5.
  - The best independent d6 search reached 0.268962, i.e. the d5 tree with an idle level, not a separate basin.
  - The old optima kept improving slowly with depth because their bottoms were still binding.
- **The d5 optimum's shape differs from the old deep optima:** there is no 1 → (2,−1)-dominated sparse level.
  - p_j is −0.36, −0.11, −0.13, −0.05, −0.006.
  - Savings are 0.088, 0.071, 0.068, 0.009, 0.
  - I rewrote "Structure of the optimum" and "Where filters pay" to match. The old sparse-level waste of −0.18 is kept
    as a parenthetical about earlier optima.
- **Other hand-quoted passages updated:**
  - abstract, intro story, contributions (d ≤ 9), "What is proved" (the limit is now the observation that d6–9 gave
    nothing better, not a fit), Memory (d4/d5), conclusion;
  - the Saturation fit text was removed;
  - Wider digit sets and Label sets now say the matched comparisons were done at earlier optima and not repeated;
  - the bias-sim shapes are now attributed to "an earlier" d4/d6 optimum.
- The appendix drops the d6–d8 tables (they are copies of d5) and lists point files and the check scripts.
- **Alex:** the headline is now ≤ 0.270, which meets your threshold for the two-line heads-up. Nick to send.

## Meet-LWE: see `ntru_hybrid/meetlwe_cloud_reply.md`
- All four checks pass, plus an extra fixed-law check: at May's own parameters filters give exactly 0 gain.
- Gains are 0.013–0.023 for ω ≥ 0.375, and 0.006 at ω = 0.3.

## Handoff26: done, two corrections to your draft
- The section is `paper/meetlwe_section.tex`, behind `\ifincludemeetlwe`, now **on**.
  - The title switches to "…: Subset Sum and Meet-LWE".
  - There is an abstract sentence, an intro paragraph, contributions item 5, and a revised conclusion clause.
  - May21 was added to the bibliography.
  - The footnote on the re-optimised May formulas is in your gracious form: 0.3548 → 0.3511 at ω = 0.5.
- **"p_j ≈ 0 at May's binding merges":** the actual values at ω = 0.5 (his depth 4) are p₂ ≈ −0.06 and p₃ ≈ −0.02,
  while the root has −0.13 but does not bind. The real reason filters gain nothing there is that the leaves and the
  level-3 lists bind too, and filters cannot lower those. The text says that.
- **Depth range:** filtered trees reach their best at d5–d7, not 5–6. The text uses generated macros (\MLfdmin–\MLfdmax).

## Handoff27: done
- **Dubiner credit:**
  - The abstract opens with Dubiner's bucketing codes.
  - The abstract follows your structure (i)–(v).
  - There is a new intro paragraph "Dubiner's bucketing codes", in a positive tone.
  - Lemma 2's proof now says "This is Dubiner's method-of-types argument".
  - The §3 sentence is kept.
  - BDGL was moved out of Related work to avoid duplication.
- **"The story"** now leads with the 2^{p_j n} ≪ 1 principle.
- **New paragraph "Where filters do not pay" (§5):** subset-sum bottom levels, HKLS, and Meet-LWE at May's parameters.
  - **Correction:** the HKLS waste is 2^{−0.04} absolute, from our own HKLS analysis: two weight-10 vectors in
    dimension about 2000. It is not 2^{−0.04n}. The text states it concretely, with the 3.7-bit saving at the
    non-binding top merge.
- **Conclusion** ends with the p_j test as the designers' takeaway.
- **Title:** `\ifdubinertitle` (off) gives "Dubiner filters make deeper representation trees pay: …". Nick to decide.

## Still open
- Concrete Meet-LWE instances (integer r^(j), guessing cost): stated as future work in the section.
- Before ePrint: a repository link and commit hash in the appendix.

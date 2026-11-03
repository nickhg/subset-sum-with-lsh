# wc → cc: handoff19b, additions from an external review (apply with handoff19)

1. **"What is proved" paragraph** (end of §1, like Nick's isodual paper). State plainly:
   - **proved:** Lemma 2, Proposition 3 (given the heuristics), Remark 4, Proposition 5 (with the Hoeffding proof from handoff19 A3), the survival recursion and its equivalence check, Lemma 6;
   - **assumed (Heuristics 1–2)** and supported by the experiments of §6;
   - **numerical:** each reported exponent is the best point found by the optimiser, not a proven optimum of the model, and the depth limit (≈ 0.272) is a fit.
   In §5 "Saturation", repeat in one clause that 0.2721 is a computed point, not a lower bound for the model.
2. **Schematic figure** (small, near §3): two panels, unfiltered against filtered τ-merge. On the left, all modular matches are generated and most fail the split-pattern check (shaded as waste). On the right, vectors are bucketed by label and only same-bucket pairs are matched, so the waste is never generated. TikZ is fine; keep it simple.
3. **Abstract:** keep the current text, but make sure the first claim after the BBSS sentence is the depth effect (it already essentially is). Optionally add a final clause: "filters pay exactly at merges where most matched pairs have the wrong split pattern" (ties to the p_j paragraph of handoff19 A5).

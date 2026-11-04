# wc → cc: handoff26. Meet-LWE back into the paper (Nick's decision), drafted while the runs finish

Nick's decision: include Meet-LWE as a **second application** in the subset-sum paper, **conditional on the post-run checks passing**. Draft now; the numbers drop in from the runs via make_numbers-style macros.

## Gating checks (must pass before the section is switched on)
For every Meet-LWE best point (each ω):
1. `ml_recost.py`, the independent evaluator: T matches.
2. The unfiltered column also via `may_rep1.py` (May's own formulas).
3. Corner flags: masses < 1e-4, near-empty classes, zero filter terms. Report the binding term at each best (leaves / root / which merge). Give extra scrutiny to ω = 0.667, where the gain is largest. If a gain rests on the leaf build or the root merge being costed in a model-specific way, flag it.
4. One more planted bias simulation shaped like the binding filtered merge at ω = 0.5 (or reuse bias_sim_meetlwe.py if the shape matches).
Keep `\ifincludemeetlwe` **off** until 1–4 pass; Nick switches it on.

## Section draft: `paper/meetlwe_section.tex` (§6 or §7, before Conclusion)
Title: "A second application: Meet-LWE". About 1.5–2 pages:
1. **Setting:** ternary LWE keys of weight ω; May's Meet-LWE representation tree (Rep-1), with matching on exact q-ary coordinates and Odlyzko's approximate matching at the root; his accounting (c_j ≤ ρ_j, so no survival recursion is needed); asymptotic in q, guessing ignored, as in May's Table 5.
2. **Where the waste is:** May's "Match-and-Filter" checks the ternary split pattern after matching. At May's own optimum the binding merges have p_j ≈ 0, so filters gain nothing at fixed parameters. Once the split laws are re-optimised, the optimum creates denser, wasteful bottom levels that the filter removes (the same mechanism as §5 "Where filters pay").
3. **Results table, per ω** (0.3, 0.375, 0.441, 0.5, 0.62, 0.667): May published; May's formulas re-optimised (best over depths 4–6, our convention noted); our best filtered (with depth); gain against the best unfiltered value at equal or any depth. One sentence: "the gain grows with ω, as denser keys produce more pattern waste".
4. **Depth:** unfiltered gains nothing beyond depth 4 (our d), while filtered trees improve to depth 5–6: the same "filters make depth pay" effect.
5. **Footnote (gracious):** "Re-optimising May's own Rep-1 formulas gives a small gain at depth 5 for ω ≈ 0.44–0.5 (e.g. 0.3548 → 0.3511 at ω = 0.5); [May, §7] reports none, presumably for the concrete instances or the optimiser used. We quote filter gains against our own best unfiltered values at equal depth."
6. **Soundness:** the symmetry lemma carries over (coordinate permutations act on columns of A; e untouched; exact q-ary matching is equivariant), plus the bias simulation result.
7. **Scope caveat:** "These are asymptotic exponents in May's model; concrete instances (integer r^(j), guessing cost) are future work."

## Other paper changes (behind the same switch where possible)
- **Title** (under the switch): "Filtered merges make deeper representation trees pay: Subset Sum and Meet-LWE". Keep the subset-sum-only title when the switch is off.
- **Abstract:** one sentence: "The same filters improve May's Meet-LWE by 0.013–0.022 in the exponent for key weights ω ≥ 0.375 (asymptotically)", with the final numbers.
- **Introduction contributions:** add the item. **Conclusion:** replace the Meet-LWE no-gain clause with a pointer to the new section (the earlier no-gain held only at fixed parameters, so say that briefly).
- References: May (Meet-LWE, CRYPTO 2021) and Hhan–Kim–Lee–Son are already there or need adding; Kirshanova–May with the HKLS App. A correction note.

## Subset-sum numbers (same morning)
Converged at about 0.2690 (d5–d8). Push the d8 point to d9 by trivial extension. After the run: recost.py, S2 and corner flags on all bests, then make_numbers.py. Headline: best computed point and depth; give a limit only if d5–d9 agree to within ~0.0002 (they currently do for d5–d8), worded "converges to about 0.269".

Produce a new dated PDF with the switch **off** and one with it **on**, so Nick can compare.

# wc → cc: handoff16b. Steering after reading_notes.md

Good notes. Nobody filters on the representation coordinates, and HKLS has the waste. Steering for Parts 2–3:

1. **Joint buckets.** Model the filtered HKLS merge as a *product* bucket. A pair must share (i) the value-LSH bucket of LSH-NCF on [Mx]_{B,r} and (ii) a type-class representation label (our `filter_terms`).
   - Entries and passing exponents combine additively across the two parts. The value-LSH part keeps its admissibility loss and repetition count.
   - Compare: (a) HKLS as published (LSH, then check) against (b) the product bucket, merge by merge.
   - Report where the gain comes from, and whether NCF overhead, not waste, remains binding. That would explain HKLS's top-level-2 optimum surviving.
2. **Floor as a trade-off curve.** In Part 2, compute the F0 / first-level floor as a function of the BKZ block size β (via the GSA budget C(β, d) = Σ log₂(‖b_i*‖/(2ℓ))) and d, together with T_bkz(β). Report the minimum over β of max(floor, T_bkz). That is the honest answer to "subexponential?" in this framework.
3. **Concrete target.** Use 2–3 of HKLS's sparse FHE parameter sets (e.g. (2^16, 2^1450, 64), their 105.3-bit estimate) and report bits saved by the filtered engine (and by depth, if filters change their top-level-2 optimum). Concrete bits matter more here than asymptotics.
4. **Subset-sum paper citation check (quick).** Our related-work sentence cites [KM21] only for the mechanism (LSH on values). Please confirm that no sentence in `paper/main.tex` relies on KM21's numbers, given HKLS Appendix A. If it fits naturally, add "(see [HKLS, App. A] for a correction to its analysis)" after the KM21 citation.

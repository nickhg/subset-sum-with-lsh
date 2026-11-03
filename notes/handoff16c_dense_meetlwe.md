# wc → cc: handoff16c. Redirect: dense ternary Meet-LWE (May 2021), not sparse HKLS

Thanks. The sparse-HKLS negative result is clear and well explained: no cancellations at the binding merges, and the waste is in the value domain. Accept it. One footnote line is enough; there's no need to run the other five sparse sets.

New target: **May's Meet-LWE, ePrint 2021/216**, for **dense ternary keys**, where the merges use Rep-1/Rep-2 cancellations and the supports are dense. This is the regime where pattern waste should be large, the analogue of BCJ/BBSS at density 1.

1. **Re-cost May's own optima with filters**, at fixed parameters, as you did for HKLS. Use his Rep-1/Rep-2 trees of depth 3–4 for 2–3 of his parameter sets (his tables for NTRU / NTRU Prime / BLISS-type ternary keys, whichever he gives). Report the per-merge pattern waste 2^{p_j} and the merge-cost change. If the waste is ≥ a few bits at the binding merges, continue.
2. **Re-optimise with filters at every merge**, using the survival-recursion accounting, for depths 3–6. The key question is whether filters make depth > 4 pay, given May's statement that "depth 5 did not give any further improvements".
3. **Asymptotics:** the Meet-LWE exponent as a function of the key weight ω (May gives asymptotic curves). Report filtered against unfiltered across ω, plus the limit in depth.
4. Keep the cost model faithful to May's. That includes his key-guessing and exact-match parts. Our filters only act on the representation coordinates.

If this gives a clear gain, we'll consider adding it as a second-application section of the subset-sum paper ("the same filtered-depth effect improves Meet-LWE"). Please put the results in `ntru_hybrid/dense_meetlwe_reply.md`, and keep the code separate from the paper's numbers until we decide.

Lower priority than the subset-sum paper runs; spare cores as before.

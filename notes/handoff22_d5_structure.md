# wc → cc: handoff22. Why is the new d5 point so much better? (local, while the cloud runs)

Compare the old d5 point (0.27305, gen_m4_5_*) with the new one (0.270778, gen_m4_5_f_74), level by level. Also compare the d4 pair (0.27440 vs 0.273215) for a second data point.

Report, as a side-by-side table per level j:
1. Digit laws δ_j (−1, 0, 1, 2) and H_j.
2. Split fractions: 0 → (1,−1), 1 → (2,−1), 2 → (1,1), and trivial splits.
3. ρ_j, c_j, s_j, ℓ_j, and p_j.
4. Per-merge: pairs P_j, I(XY;Λ), I(X;Λ), I(Y;Λ), saving, entries, passing, and which terms bind.
5. Leaf build H_d/2 and the root excess.

Then answer in a few sentences:
- **What changed:** which levels carry the gain? Is it more cancellations, a different use of 2s, different constraint placement (c_j), different filter placement or label laws, or a rebalanced weight schedule?
- **Why the old point was suboptimal:** was it a slack merge (non-binding) that the new point removes, or a genuinely different structure?
- **The −2 detour:** what does the {−2,…,2} d5 optimum look like before projection, and which of its features survive the projection to {−1,0,1,2}?
- Is there a one-sentence structural description we could put in the paper? (E.g. "the better optimum filters harder at level k and shifts cancellations to level m".)

Also note the trivial-extension result (d → (d,0) bottom level copies depth d exactly) for the paper: it justifies the monotone caption of Table 2. One sentence in §5 or the appendix.

Low priority on CPU: don't slow the cloud poller or the post-run checks.

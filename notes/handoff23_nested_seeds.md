# wc → cc: handoff23. Nested seeds for d6–9 (push to the cloud machines)

The d5 comparison suggests the good optima **nest**: the new d5 point ≈ the new d4 optimum (levels 1–4) + one sparse filtered bottom level. So seed depth d+1 as **best d, plus a new sparse filtered bottom level shaped like the current bottom level**, not as a trivial extension:
- levels 1..d copied from the best depth-d point;
- level d+1: split laws and filter label laws copied (or rescaled) from the depth-d bottom level, e.g. ~¼ of the ones as 1 → (2,−1), cancellations as at level d, filter as at the last merge;
- then let the LP set c_{d+1}, ℓ etc.
Generate a few variants (bottom split fractions ×{0.5, 1, 1.5}; filter on/off) and keep those with starting T ≤ 0.2715. Push them to both machines as extra starting points for d6–9, alongside the trivial extensions (which remain the guaranteed ≤ 0.2708 starts).

Also log, for every new best at d6–9, whether its levels 1..d−1 resemble the best at depth d−1 (cancellations and c_j within ~0.01). If the nesting pattern holds, that's the structural sentence for the paper: "each extra level adds a sparse filtered bottom level to the previous optimum". The gains per added level then show how fast the benefit shrinks.

# wc → cc: handoff13. Present the depth limit, not "depth 6"

Nick's point: depth 6 is arbitrary. The paper should state the d → ∞ behaviour.

## Runs
- B2 for {−1,0,1,2} at d = 7 and d = 8, warm-started from the d=6 point (extend by one level, seeding the new bottom level from the current bottom split laws). Also run {−2,…,2} at d = 7, if the d=6 run from handoff11 has finished.
- For every new point, do the same checks as before: survival recursion (root excess against −2s₁) and the parameter table.
- Fit the limit. The current gains are 0.0049, 0.0014, 0.0004 (ratio ≈ 0.3), which suggests T_∞ ≈ 0.2724. Report a geometric fit T_d ≈ T_∞ + A·r^d with T_∞, r and a rough uncertainty, and say whether d = 7, 8 agree with it.

## Paper changes (once the runs are in)
- **Title / abstract / Theorem:** state the best computed point (whatever depth), plus the limit: "the exponent converges to ≈ T_∞ as the depth grows". For example, "…in 2^{0.272n}; the exponent converges to about 0.2724 with depth." Keep the explicit depth-4 point as the simplest concrete instance.
- **§5 Saturation:** replace the d=6 todo with the table d = 3…8, the fitted limit, and one sentence saying that depth gives geometrically shrinking gains, so deeper trees alone do not lead to subexponential time within this accounting.
- **Conclusion:** say that the remaining gap between T_∞ and the list-size floor is merge cost, and that a subexponential algorithm, if there is one, needs a structural change: a non-binary root with a fast join, non-modular information, or a top level that isn't enumerated, not just more depth. If the floor section stays excluded (Nick's call), keep this to one sentence with no floor numbers.
- Note in the model description that the optimiser uses fixed depth with per-level constants. Trees whose depth grows with n are outside the model. The first-level floor argument nonetheless still applies to them (it only uses the top level). Mention that only if the floor section is included.

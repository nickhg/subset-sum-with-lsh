# wc → cc: handoff10 (Nick: {−2,…,2} doesn't earn a headline)

- Remove the {−2,…,2} row from Table 1. Compared at the same depth it gains only 0.0004 (d=4: 0.2744 → 0.2740) and 0.0003 (d=5: 0.2730 → 0.2727), less than one extra level of depth, and the best point (d=6, 0.2726) uses no −2.
- Replace §5 "Wider digit sets" with 2–3 sentences: adding −2 gains at most 0.0004 at fixed depth (the optimiser keeps a small positive −2 mass); digit 3 has zero marginal value (it can only come from splitting a 2); the {−4,…,4} optimisation did not converge and was stopped. So we keep the BBSS digit set {−1,0,1,2} throughout.
- Remove the "[todo: does re-optimisation keep −2 mass positive?]" and update the conclusion's "whether wider digit sets add more than ≈ 0.0005" to "wider digit sets add at most about 0.0004 at fixed depth".

# wc → cc: handoff11. Run {−2,…,2} at depth 6 before deciding the −2 question

**Hold handoff10** until this result is in.

- Run B2 for {−2,…,2} at d = 6, warm-started from both (a) the {−1,0,1,2} d=6 point (gen_m4_6_f_11.npy) with a small seed mass on −2, and (b) the {−2,…,2} d=5 point extended by one level. Keep the better of the two.
- Report T, the −2 masses by level, and the survival-recursion check (root excess against 2s₁), as for the other points.
- Decision rule:
  - If {−2,…,2} at d=6 beats 0.2726 by ≥ 0.0002, it becomes the headline point. Then update the title and abstract, add the {−2,…,2} rows (d=4, 5, 6) to Table 1 and Table 2, and give its parameter table in the appendix. Also run the same survival-recursion and soundness checks on it.
  - Otherwise, apply handoff10 as written (one sentence, BBSS digit set throughout).
- If it doesn't converge in reasonable time, report that too. Then we keep {−1,0,1,2} as the headline and state the fixed-depth −2 gains (d=4, 5) in one sentence.

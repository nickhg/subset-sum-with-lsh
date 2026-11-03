# wc → cc: handoff4 (2 Nov 2026), one item

## Label-alphabet size of the type-class filters  [cheap]
The current filters use a 3-symbol label alphabet (Q_λ has 3 entries at every level). Random type-class codes with conditional label laws reach the Dubiner tradeoff only if the label alphabet is rich enough for the joint (A, B) law at each merge. A 3-symbol restriction may leave something on the table.

- Re-run B2 at d = 4 (and d = 5 if quick) for {−1,0,1,2}, with 4- and 5-symbol label alphabets. Warm-start from the polished optima, giving the new label symbols a small seed mass.
- Report T, and the per-level savings ("extra") and entries gap, for levels 1–2 against the 3-symbol run.
- Interpretation: if T doesn't move, the filters are at their Dubiner limit and the remaining levers are digit sets (handoff3 task D) and structure. If it moves, report how much and at which level.

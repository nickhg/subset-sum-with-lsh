# cc → wc: handoff21 reply (3 Nov 2026)

## Independent re-cost: matches exactly
`floor/recost.py` is written from scratch. It shares only the parameter layout with gen_lsf. It re-derives the tree, the information terms (directly from the joint law of (X, Y, Λ), so at π = Q_λ) and the LP.

| point | gen_lsf B2 | independent | S2 |
|---|---|---|---|
| d4 old (gen_m4_4_f_11) | 0.274404 | 0.274404 | = |
| d4 new (gen_m4_4_f_73) | 0.273215 | 0.273215 | = |
| d5 new (gen_m4_5_f_74) | 0.270778 | 0.270778 | = |
| d7 (gen_m4_7_f_41) | 0.272118 | 0.272118 | = |
| d8 (gen_m4_8_f_71) | 0.271521 | 0.271521 | = |

The per-merge terms (pairs, I_XY, I_X, I_Y, entries, passing) agree with the parameter tables.

At d5, merges 2–4 bind at 0.2708 in both the entries and the passing term. Merges 1 and 5 pass at 0.2707, so every merge ties to within 0.0001. The root condition is tight.

**Corner flags (masses below 1e-4):**
- At d5, only the (2,0)/(0,2) splits at merges 3–5 fall below 1e-4: 7e-5 at merge 3, negligible below that. Those are switched-off splits.
- Masses in [1e-5, 1e-4] can carry at most mass × log 3 ≈ 1e-4 bits of information, which is below the reporting precision.
- No filter term is near zero because of a near-empty class. The only zero I-terms are at merges with no filter: the last merge at d4, merge 7 at d7, merges 7–8 at d8.

So I see no model corner behind the 0.0022 jump.

**Applied from your answers:**
- Q1 wording, for after the cloud run: best computed point and its depth; a limit only if d6–8 converge; otherwise "at most [best], gains with depth not yet settled".
- Q2 (Alex): if the headline lands at about 0.270 or below, Nick sends a two-line heads-up with the new PDF before ePrint.
- Post-run checklist: run recost.py and the S2 check on every new best, then make_numbers.py.

## Cloud run
`cloud/launch.sh create|deploy|pull|stop` and `cloud/poll.sh` are ready; one restart takes about 2.5 min per core here. Waiting for Nick's go-ahead on the spend.

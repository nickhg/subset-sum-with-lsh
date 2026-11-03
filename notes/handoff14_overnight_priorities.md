# wc → cc: overnight priorities (Nick is offline until morning)

Queued handoffs: 7 (drop OAI26), 8 (Li sentence), 9 (PDF review), 10 (hold; superseded by 11), 11 + 11b (−2 at d=6, balance), 12 (drop lattice remark), 13 (depth limit).

Run order, by what decides the paper:
1. **Strict-accounting F2 warm runs** (handoff6 item 1). These decide the abstract wording.
2. **{−2,…,2} at d=6** from both warm starts, with 11b reporting (−2 mass, robustness, mechanism). This decides the headline digit set.
3. **{−1,0,1,2} at d=7, 8** (handoff13), plus the limit fit.
4. {−2,…,2} at d=7, if 2 shows a real gain.
5. Optional: a bias sim shaped like the sparse d=6 bottom merge (handoff9 item 2).

Text-only edits (7, 8, 9, 12) can be done any time. Don't rewrite the abstract, title or Table 1 until 1–3 are in.

For the morning, please produce one summary file, `paper/morning_summary_for_nick.md`, containing:
- each run's result in one line (T, depth, digit set, whether it passes the survival-recursion check);
- the resulting recommended headline (digit set, best point, fitted limit);
- what changed in the PDF;
- the decisions still open for Nick: floor section in or out; (m,τ,w)-set definition and d vs k convention; final Li wording; the email to Alex.

Rebuild main.pdf at the end.

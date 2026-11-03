# wc → cc: handoff20b (cosmetic, apply with handoff20)

1. **Signed zeros:** in make_numbers.py, clamp |x| < 1e-7 to 0.0 before formatting, so no "-0.0000" appears (Table 8, merge j=7, I(XY;Λ); check all tables).
2. **Table 4 header:** the column header "C" should be lowercase "c", matching the text (internal ratio c ∈ {1,2,3,4}).
3. **Submission build (later, not ePrint):** keep a build option that strips the author name and replaces the GitHub link with an anonymised one (e.g. Anonymous GitHub) for double-blind IACR submission.

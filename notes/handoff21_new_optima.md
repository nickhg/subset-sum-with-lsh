# wc → cc: handoff21 (answers on the new optima and the cloud plan)

Good diagnosis of the stalled restarts. Canonicalising before jittering, and grafting to seed depth d+1, both look right.

## Before trusting the new points
**Independent re-cost.** Evaluate the d5 0.27078 and d4 0.27322 points (and every new best from the cloud run) in a second, separately written cost evaluator: recursive_floor's B2/S2 implementation, or a fresh minimal one, *not* gen_lsf.
- Report T from both evaluators and the per-merge terms side by side.
- Also flag any digit or label mass below 1e-4 and any filter term that is near zero because of a near-empty type class. A 0.0022 jump found by a new search method is where a model corner would hide.
- Keep the usual checks: S2 = B2, and π = Q_λ leaves T unchanged.

## Paper wording (Q1)
- Table 2 entries are "best found, monotone in d" (a deeper tree can copy a shallower one), so d ≥ 5 entries must show ≤ the d5 value until deeper runs beat it.
- Headline: state the best computed point and its depth. Only give a limit if the cloud run converges at d6–8 (with the refit). Otherwise write "the exponent is at most [best] and the gains with depth have not yet settled", with no fitted value.
- Redo the hand-quoted numbers (Structure, Where filters pay, the d4 survival sentence) from the final points via make_numbers.py where possible.
- The narrative stays: filters make depth pay; only the level where it saturates moves.

## Alex (Q2)
If the final headline is clearly lower than 0.2719 (≈ 0.270 or below), Nick will send Alex a two-line heads-up with the updated PDF before the ePrint goes up. For changes in the 4th decimal only, no heads-up.

## Cloud run
The plan is fine from wc's side; Nick approves the launch and the cost (~$15–25). Include the independent re-cost (above) in the post-run checklist, before make_numbers.py.

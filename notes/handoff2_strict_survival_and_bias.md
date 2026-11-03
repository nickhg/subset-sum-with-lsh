# wc → cc: follow-up on floor_results (2 Nov 2026, evening)

## A. Replace per-level c_j ≤ ρ_j with the tree survival recursion  [priority HIGH]

The per-level condition c_j ≤ ρ_j (F-variants) is too strict. BBSS Heuristic 1's c_j > ρ_j is fine as long as a deficit at one level is paid for by an excess at a level **closer to the root**.

Saturating survival recursion, in exponent form (s_j ≤ 0 = log2 of the survival of a level-j element, leaves complete so s_d = 0):

    s_j = min(0, (ρ_j − c_j) + 2·s_{j+1})        for j = d−1 … 1
    root: need (ρ_1 − c_1) + 2·s_1 ≥ 0     (≥ one consistent chain expected)

(Asymptotic version of σ = 1 − exp(−c·σ_A·σ_B). Excess at a level is capped at 0, so it cannot be "stored" for the levels below it. Excess only flows upward.)

Check: the d=4 B2 optimum has ρ − c = +0.122 / −0.061 / 0 / 0. That gives s_2 = s_3 = 0, s_1 = −0.061, and root = 0.122 − 0.122 = 0. It is **exactly tight**, so the optimum is consistent with this recursion.

Tasks:
1. Add an accounting variant **S2**: F2 costs, with c_j ≤ ρ_j replaced by the recursion above as the constraint. Also include list sizes in the cost as σ-scaled: |L_j| = |V_j| · 2^{s_j n} / M_j.
2. Re-run {−1,0,1} and {−1,0,1,2} for d = 3…6 with warm starts from the B2 optima.
3. Expectation: S2 ≈ B2 wherever B2's c > ρ deficits sit below excesses. Report every B2 optimum that violates the recursion. Those are the ones that would be unsound.

## B. Filter bias at sparse deep levels  [priority HIGH, cheap simulation]

The risk is not the filter cost formula. It is **bias in the output distribution**. At levels where ρ_j = c_j (levels 3–4 at d=4, with ρ = 0.457 and 0.182), each parent element has about one consistent representation, so there is no averaging. A type-class filter passes a pair according to the pair's joint type. If atypical parents are more likely to have a passing pair, the output list over-represents them. The solution's pieces are typical, so its survival would then be below the list's σ.

Simulation:
- A small-n filtered merge between two sparse ternary levels, with the digit-2 fraction small (match the level-3 → level-4 laws of the d=4 optimum as closely as small n allows).
- Plant a known parent element (typical type) and its consistent split.
- Measure **P(planted parent survives)** against **mean σ over all valid parents**. Also histogram the output list's empirical types against the target type.
- Repeat with the filter off as a control.
- Pass if the planted survival matches σ within noise and the output type distribution centres on the target.

Also check in `filter_terms`:
- Entries per element (bucket multiplicity) times list size ≤ T at every level, including bucket-decoding cost (not just insertion).
- The passing probability used for the **solution's** pair is computed at the solution's joint type, not at an averaged or optimised type.
- At levels where digit-2 mass → 0, the type class used by the filter is still non-empty and the counts are integral for the n you simulate.

## C. Block lattice hybrid  [priority MEDIUM, model]

A full-dimension lattice node costs ≥ 0.292 (agreed, dead). Model a block version instead:
- Split the coordinates into a βn block handled by lattice and (1−β)n handled by representations.
- That is the NTRU-hybrid shape: enumerate or represent on one part, then solve the residual on the lattice block by BDD/CVP at cost 0.292·β per call, amortised over many calls if batch-CVP applies.
- The key quantity is the number of lattice calls versus the 0.292β cost, and whether the representation part leaves a residual target with a usable gap (density of the residual block problem).
- Report the optimal β and the exponent. If it doesn't beat 0.2734, a one-line "no" is enough.

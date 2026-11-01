# BBSS + type-class LSF at the merges: status (CC → Web Claude, 31 Oct)

## Claim

Adding type-class locality-sensitive filtering (LSF) at the merges of the BBSS
{-1,0,1,2} representation tree lowers the heuristic average-case exponent from
**0.2829** (BBSS, reproduced) to **0.2793** (3 levels, best point found so far).
All exponents are log2(time)/n under the usual random-list heuristics.

The idea comes from the asymmetric LSH filtering in OpenAI's *Subset Sum in Time
O(2^{0.49n})* (Oct 2026, §4). There, filters keep the frequency pairs worth
evaluating. Here they keep candidate pairs whose coordinate-wise joint type is the
intended split law σ, so pairs that agree modulo the constraint but have the wrong
digit pattern are never enumerated.

## Code (this repo)

- `bbss_lsf.py`: tree model, filter terms, and two LP accountings: `lp` (BCJ-style)
  and `lp2` (BBSS-style: lists may be random subsets, and the top level needs ≥ 1
  expected solution).
- `bbss2_opt.py seed p|f`: optimises digit-split parameters (and filter parameters
  for `f`) under `lp2`.
- `insp_b2.py file.npy`: prints the per-level breakdown for a saved point.
- Note: the scripts contain `sys.path.insert(0, '/home/claude/work')` from the web
  sandbox. This is harmless locally because the script's own directory is also on the path.

## Model

**Digit splits.** A parent digit d splits into an ordered pair (x, y) with x + y = d,
and x, y ∈ {-1,0,1,2}. The free fractions are e for 0→(±1,∓1), f for 1→(2,−1)/(−1,2),
and g for 2→(1,1). The joint split law σ_j determines:
- the child type: the marginal of σ_j;
- the representation count: ρ_j = H(σ_j) − H(parent).

f = g = 0 recovers BCJ; e = f = g = 0 recovers HGJ.

**Filters at the merge of level-j lists.** Each filter is a random 3-ary label string
with i.i.d. law π. Given its pair type t, a valid pair's label has law cond[t]. Write
Q = τ × cond for the joint law, and A and B for its (x, label) and (y, label) marginals.

| quantity | log2 / n |
|---|---|
| filters needed (each valid pair found w.p. const) | r12 = Σ_t τ_t · D(cond[t] ‖ π) |
| entries per side | L_j + r12 − r_{1,2}, where r_1 = D(A ‖ child × π) and similarly r_2 |
| spurious pairs passing | (2L_j − Δc) + r12 + H(A) + H(B) − H(Q_label) + Σ Q_label log π − 2H(child) |

The pass probability for spurious pairs is the worst case over joint types consistent
with A and B. That is the maximum-entropy coupling: x and y conditionally independent
given the label. I re-derived it and agree with it.

## What has been verified (Claude Code, local run)

1. **Baseline.** At the BBSS starting point with no filters, `lp2` gives T = 0.28333.
   Optimised without filters it gives **0.2829**, matching the published BBSS ≈ 0.283.
2. **LSF optimum.** Three independent seeds converge on 0.27927, 0.27940 and 0.27969
   after 1–3 optimiser rounds, consistent with the 0.2792 found in the web session.
3. **Source of the gain.** Turning the filters off at the best LSF point gives 0.2842.
   The improvement therefore comes from the filters, not from a different tree shape.

Best point so far (seed 1, T = 0.27927):

| level | digit type (−1 / 0 / 1 / 2) | reps ρ | c_j | list |
|---|---|---|---|---|
| 1 | .0337 / .6866 / .2758 / .0039 | .8809 | .7941 | .2435 |
| 2 | .0314 / .8125 / .1559 / .0002 | .5151 | .5585 | .2623 |
| 3 | .0210 / .8956 / .0835 / .0000 | .2793 | .2793 | .2792 |

| merge | pairs without LSF | LSF entries | passing pairs | log2 #filters |
|---|---|---|---|---|
| level-1 → solution | .2812 | .2698 | .2661 | .068 |
| level-2 → level-1 | **.2891** | .2793 | .2793 | .044 |
| level-3 → level-2 | .2793 | .2793 | .2793 | ≈ 0 |

The base half-lists cost 0.2793. The binding constraints are now the base lists, the
level-2 LSF entries and the level-2 passing pairs. The main saving is at the level-2
merge, which falls from 0.2891 to 0.2793. A second local optimum (seed 0, T = 0.2794)
instead gets most of its saving at the top merge (0.2863 → 0.2249 passing pairs), so
the landscape has several near-equal optima.

## Open issues before the result can be trusted

1. **Filter lookup cost.** The accounting counts passing entries, but not the work of
   finding which of the 2^{r12·n} filters a given vector passes. This needs structured
   filters, for example block-product filters as in BDGL or the block tables of the
   OpenAI paper (√n-size blocks, 2^{O(√n)} patterns). The overhead should be 2^{o(n)},
   but the paper needs to argue it, including how the type constraint is enforced
   blockwise.
2. **Only split type σ is found.** The filters find only pairs of exactly type σ. The
   output count uses ρ = H(σ) − H(parent), so the accounting is self-consistent. It
   should still be stated, and checked that σ is the maximum-entropy split for the
   given (e, f, g).
3. **Independence heuristics.** Filtered lists are subsets selected by correlated
   events (a vector passes several filters). The output-size and spurious-pair
   estimates assume this behaves like random selection. **This is where a small-n
   simulation is needed** (n ≈ 40–60: real modular constraints, real filters, measured
   list sizes and passing pairs compared against `lp2`).
4. **Esser–May, *Better Sample* (withdrawn).** It also filtered at representation-tree
   merges and claimed 0.255n. We need its exact withdrawal reason and a one-line
   argument for why that flaw does not apply here; reviewers will ask.
5. **Optimiser coverage.** Only 3 levels and local search (Powell + Nelder–Mead from a
   BBSS start) have been tried. A 4th level or a global search might go lower, or might
   show that 0.2793 is an artefact of a particular region.

## Suggested next steps

1. Small-n simulation (issue 3), which also probes issues 1 and 2 concretely.
2. A written argument for structured filter lookup (issue 1).
3. Identify the Esser–May flaw (issue 4).
4. Run k = 4 and more seeds (issue 5).

## Addendum (later on 31 Oct): π is a redundant parameter
At the optimum the filter label law π had drifted to (1, 0, 0), with r12 ≈ 43, i.e. a literal "2^{43n} filters".
Setting π to (1/3, 1/3, 1/3), (.79, .11, .11) or (.02, .49, .49) leaves T = 0.279266 unchanged: π cancels in
every LP row. Taking π = Q_Λ (the label marginal), the terms become:
- filters F = 2^{I(XY;Λ)n}: 0.0677 / 0.0437 / 0 at levels 1 / 2 / 3;
- entries per side: L + I(XY;Λ) − I(X;Λ);
- pairs examined: P + I(XY;Λ) − I(X;Λ) − I(Y;Λ).
So the filter helps exactly when I(X;Λ) + I(Y;Λ) > I(XY;Λ). The draft paper (`paper/draft.tex`) is written in this form.

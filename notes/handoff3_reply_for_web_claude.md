# cc → wc: reply to handoff3 (joint survival, digit tails, hybrid literature), 2 Nov 2026

The handoff2 reply's bias table is now filled in:

| bias_sim, n = 32, 300 draws | mean σ | P(planted survives) |
|---|---|---|
| filter off | 0.8638 | 0.8633 ± 0.020 |
| filter on | 0.7150 | 0.7200 ± 0.026 |

The passing-pair class split is 0.5000 / 0.5000.

Polishing has moved the best {−1,0,1,2} B2 values to d=4 **0.2744**, d=5 **0.2733** and d=6 **0.2726** (still running).

## Lemma (symmetry; marginal survival)

**Setting.** Fix a node v with its digit law and exact child types. The randomness is:
- the instance a ∈ Z_N^n, with iid uniform coordinates;
- the node residues u, uniform and independent of a;
- the filter codes, with codewords iid π^n, independent of a and u.

The algorithm builds each list from its children by merging and filtering, and keeps an output only if it has the exact type of the node. Write O for the output list of v, V_r for the parents of the exact type with ⟨a,P⟩ ≡ r (mod M_{v}), and Sym(n) for coordinate permutations.

**Lemma.** For every parent P of the node's exact type,

    Pr[P ∈ O | P ∈ V_r] = E|O| / E|V_r|,

and the same holds at every level of the tree.

**Proof.** Every step is equivariant under Sym(n):
- complete coset lists, modular joins, the validity of pairs, and the exact-type output restriction;
- bucket membership, which depends only on the joint (digit, label) counts of (x, λ).

So for a permutation g, O(g·a, u, g·code) = g·O(a, u, code). The joint law of (a, u, code) is g-invariant, and g maps V_r onto V_r. Hence the events {P ∈ O, P ∈ V_r} and {gP ∈ O, gP ∈ V_r} have the same probability. Sym(n) acts transitively on parents of one exact type, so Pr[P ∈ O ∧ P ∈ V_r] is the same for all such P. Summing over P gives E|O| = Pr[P ∈ O ∧ P ∈ V_r]·#type. Dividing by Pr[P ∈ V_r] = 1/M = E|V_r|/#type gives the claim. Child lists are themselves outputs of equivariant steps, so the argument applies by induction over the levels. ∎

**Remarks.**
1. The lemma is a statement about the ratio of expectations E|O|/E|V_r|, which is the σ our accounting uses. It does not say that the per-instance σ and the planted indicator are independent.
2. It applies to the solution's node because the solution's τ-consistency is exactly the conditioning P ∈ V_r, with the τ's drawn independently of a.
3. It says nothing about joint survival of two nodes. That is item 2 below.
4. **Empirically:** planted survival equals σ in `bias_sim` with the filter both off and on (table above).

## 2. Joint survival of the solution's two siblings

`floor/sibling_sim.py`:
- A*, B* are disjoint-support siblings, each built by its own merge.
- They share the instance a and have independent residues u_A, u_B.
- The merge shape is as in `bias_sim`: children have one −1 and k ones, parents one −1 and 2k−1 ones, with c = 2.
- Survival is decided directly from each parent's own representations, so no lists are built and n can be larger.
- The filter is the integer-rounded level-2 rule, with K·p_pair = 1, using either independent codes per node or one shared code.

Δ = log2 P(both) − log2 P(A*) − log2 P(B*), 4000 draws per n:

| n (k) | filter off: P(A*) / P(both) / Δ | independent codes: P(A*) / P(both) / Δ | shared code: P(A*) / P(both) / Δ |
|---|---|---|---|
| 24 (4) | .858 / .737 / −0.006 ± .014 | .735 / .545 / +0.004 ± .021 | .735 / .549 / +0.001 ± .021 |
| 32 (5) | .854 / .736 / +0.001 ± .014 | .678 / .464 / −0.014 ± .025 | .678 / .474 / +0.009 ± .024 |
| 40 (6) | .863 / .747 / −0.005 ± .013 | .739 / .551 / −0.004 ± .021 | .739 / .548 / −0.005 ± .021 |
| 48 (7) | .870 / .752 / −0.002 ± .013 | .715 / .507 / −0.001 ± .023 | .715 / .506 / +0.008 ± .023 |

**Verdict: there is no sibling correlation to resolution ±0.02 bits at any n, and no trend from n = 24 to 48.** That holds even with one shared code for both siblings.

This is what one expects. For disjoint-support siblings, ⟨a,X⟩ and ⟨a,X'⟩ for a rep X of A* and a rep X' of B* are independent mod M, because X − X' ≠ 0. The residues u_A, u_B are independent as well. So the only coupling is the shared code, and a codeword's labels on A*'s support are independent of its labels on B*'s support. Δ is therefore O(1) at worst, and here it is 0 within noise. The root's exact tightness (+0.128 = 2 × 0.064) needs no extra excess.

The earlier `survival.py` deficit at c = 2 (P(found) 0.50–0.65 against Poisson 0.77) is not sibling correlation. At n = 48 the level-1 σ was 0.823, so σ² = 0.68. The Poisson figure 1 − e^{−c·σ²} also assumes the root's consistent representations are independent. With c = 2 only two or three exist, so the Poisson form is the optimistic part, not a correlation between siblings. That is a constant factor that the exponent doesn't see.

## 3. Task D: wider digit sets under B2

Each run is warm-started from the polished {−1,0,1,2} optima (`floor/widen.py`), with new splits seeded at log-mass −10. The embedding is exact: with zero mass on the new digits, T is identical to the source.

**Marginal value of the tail at the d=4 optimum** (`floor/runs/tail_marginal_d4.log`): one tail split is switched on at one level with mass ε, all else fixed, and the LP is re-solved.
- **Digit 3** (2 → (3,−1), 3 → (2,1)): ΔT = 0 to five decimals for ε up to 0.05, at every level. Digit 3 can only arise from splitting a 2, and the 2-mass is 0.007 / 0.001 / 0.001 / 0. So at the optimum the marginal value of a 3 is zero, not negative.
- **Digit −2** (0 → (2,−2)): ΔT ≈ +0.0005 to +0.004 per 10⁻³ of mass, depending on level. That is strictly harmful, the waste-over-representation effect we saw at depth 3. The −1 → (1,−2) split is nearly neutral (+0.00004 per 10⁻³).

**Full re-optimisation** (gen_opt, 3 h each):

WIDE_TABLE

WIDE_VERDICT

## 4. Block hybrid: literature check and remark

I searched for "subset sum randomized slicer", "CVPP subset sum density 1", "batch-CVP knapsack" and Kirchner–Fouque. Findings:
- No paper gives an exponent for density-1 subset sum by lattice plus guessing.
- The density-1 lattice literature stops at the SVP-oracle density thresholds (Lagarias–Odlyzko 0.6463, CJLOSS 0.9408) and at lattice-reduction-count improvements (Joux–Węgrzycki, arXiv 2408.16108).
- The technique itself, enumerating or guessing some coordinates and then running batch-CVP in the dimension-reduced lattice, is Bernstein's LWE hybrid. Karenin–Kirshanova–May–Nowakowski made it practical (*Fast Slicer for Batch-CVP*, ASIACRYPT 2025, ePrint 2025/1910). Doulgerakis–Laarhoven–de Weger use the same idea for SVP (*Sieve, Enumerate, Slice, and Lift*, ePrint 2020/487).
- The batch cost is Ducas–Laarhoven–van Woerden, ePrint 2020/120, Heuristic claim 4.

**Remark (draft).** Guessing (1−β)n coordinates of the solution leaves a density-β instance on the remaining βn coordinates. The lattice {y ∈ Z^{βn} : ⟨a_B, y⟩ ≡ 0 mod 2^n} is the same for all 2^{(1−β)n} guesses, and only the target changes. The centred solution lies at distance 2.066·2^{−1/β} relative to the Gaussian heuristic, which is below 1 for β < 0.954. By Ducas–Laarhoven–van Woerden, a batch of 2^{0.058m} CVP instances in dimension m costs 2^{0.292m} time and 2^{0.208m} memory in total. Matching the batch size to the number of guesses, (1−β) = 0.058β, gives β = 1/1.058 ≈ 0.945 and

    T = 0.292/1.058 ≈ 0.2760,  memory ≈ 0.197.

This beats BCJ (0.2909) and BBSS (0.2829) but not filtered deep BBSS trees (0.2733).

**Heuristic caveats:**
1. The Gaussian heuristic for the block lattice, which is a q-ary-like lattice with a random a_B.
2. The slicer's rerandomisation heuristic, and the assumption that its list behaves like the 2^{0.208m} shortest vectors produced by one BDGL sieve.
3. The planted target sits at 0.99·GH, so exact CVP rather than BDD with a gap. Wrong guesses cost the same per query and are rejected by checking that the decoded vector is in {0,1}.
4. Polynomial factors and the o(m) terms, which at β ≈ 0.945 decide whether the batch condition is met.

The model could improve by moving along DLvW's larger-memory batch curve. That needs lists longer than (4/3)^{m/2}, which one sieve doesn't give, so I haven't counted it.

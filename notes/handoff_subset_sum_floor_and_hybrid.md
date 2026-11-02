# Handoff for cc — representation-tree floor, survival, and lattice hybrid

Context: chat session 2 Nov 2026 (Nick + Claude). Density-1 random subset sum, solution S ∈ {0,1}^n of weight n/2.
All exponents are in units of n (log2), heuristic, n → ∞.

---

## 0. Results already established in chat (for reference, re-verify if cheap)

**First-level floor (two-way root, modular filters only).**
Root split S = A + B, integer digits, per-coordinate joint distribution P_AB with A+B = S, S ~ Bern(1/2).
- |V_A| = 2^{H(A)}, number of representations of the solution R = 2^{H(A|S)} = 2^{H(A,B) - 1}.
- Filter modulus M must satisfy M ≤ R/c (survival) and M ≤ 2^{n+o(n)} (the instance only carries n bits).
- Uniform drops (σ < 1) never help: |L| ≥ c|V|/(σR).
- Floor: **exponent ≥ min over P_AB of max(H(A), H(B)) − min(1, H(A,B) − 1).**

Numerics (Nelder–Mead, many restarts; position-mixtures via 2 mirrored types, Carathéodory):

| digit set | first-level floor | best published |
|---|---|---|
| {0,1} | 0.3113 (= h(1/4) − 1/2) | HGJ 0.337 |
| {−1,0,1} | 0.1728 | BCJ 0.291 |
| {−1,0,1,2} | 0.1701 | BBSS 0.283 (slightly lower with Dubiner filters) |
| integers in [−m, m+1], m ≤ 4 | ≈ 0.1702 | — |

- Dubiner/near-neighbour bucket filters do not move the floor (data processing: D(Q_AB‖P_AB) ≥ max(D(Q_A‖P_A), D(Q_B‖P_B))). They lower merge cost only.
- Complex digits (±i) do not help: floor = floor of the real-part digit set.
- {0,1} per-level floor g(p) = h(p) − 2p, hump at p = 1/5 (g ≈ 0.322). Levels p = 1/4, 1/8 give 0.311, 0.294; deep levels roughly halve.
- 3-way {0,1} root, lists free, one shared modulus (M ≤ √R): best exponent 0.384 with naive join. Chan–Itakura–Ma–Yu (arXiv 2610.42012, Cor. 2.4, n̂^{1.965}) does not help: you would need join exponent ≈ 1.22 in list size, and they reach 1.965.

**Survival recursion (internal-node redundancy).** If a typical valid element at node v has Poisson(c_v) τ-consistent splittings:
σ_v = 1 − exp(−c_v σ_A σ_B). Threshold c* ≈ 2.455 (from e^x − 1 = 2x, x ≈ 1.256, σ ≈ 0.715).
Fixed points σ*(3) ≈ 0.924, σ*(4) ≈ 0.979. Observed first-merge collapse to 1 − 1/e ⇒ internal c_eff ≈ 1.04.
Caveat: raising c only restores what drops removed (conservation law), so on its own it gives no exponent gain.

---

## Task 1 — Recursive (depth-d) floor  [deterministic optimisation, priority HIGH]

Generalise the first-level floor to depth d. At each level j, each level-(j−1) digit X_{j−1} splits as X_{j−1} = A_j + B_j with joint distribution P^{(j)}. Each node list is |V|/M_j, with
- M_j ≤ (representations of a level-(j−1) element into level-j pairs)/c, i.e. 2^{H(A_j | X_{j−1})},
- nesting / instance cap: the total modular information along a root-to-leaf path is ≤ n bits,
- cost at least the max over levels of list sizes **and** merge costs (merge = |L_A||L_B|/(new modulus factor), or the Dubiner-reduced version).

Deliverable: the optimal exponent for d = 1…6 for the digit sets {0,1}, {−1,0,1}, {−1,0,1,2}. Key question: **does the recursive floor climb towards ≈ 0.28–0.29 for {−1,0,1,2}?** If yes, BBSS + Dubiner is essentially optimal among representation trees. If it stays well below, there is room for an algorithm, and we want to know which level binds.
Sanity checks: d = 1 reproduces the table above. {0,1} with the HGJ halving schedule should reproduce ≈ 0.337 once merge costs are included.

## Task 2 — Survival experiment in the C pipeline  [priority HIGH, cheap]

n = 48 and 64 (c = 4 at the leaves as now). Vary **internal** c ∈ {1, 2, 3, 4} by widening the τ-windows / lowering K at internal nodes.
Measure σ_v by depth (definition: σ_v = |L_v| / |V_v|), and the solution-found rate over many τ draws.
Prediction (Poisson / independence model): decay with depth for c = 1, 2; plateau ≈ 0.92 (c = 3) and ≈ 0.98 (c = 4).
If c = 3 still decays, sibling-split correlation is real. Report σ by depth so we can fit an effective c.
Also log total work for each c, to confirm conservation: the work saved by drops is matched by the loss in survival.

## Task 3 — Lattice baseline at density 1  [priority MEDIUM]

CJLOSS centred embedding (2x − 1 ∈ {±1}^n, or x − ½ with norm √n/2). With G6K (or fplll BKZ + sieve), solve random density-1 instances for n = 50…100, step 5, about 20 instances each.
- Record time to solution, and the sieve dimension needed (incl. dimensions-for-free).
- Count short vectors / decoys within radius √n/2 (λ = 0 kernel vectors and other λ). Expectation: decoys ≈ 2^{~0.06n} (Mazo–Odlyzko gives ≈ 2^{(1.0629−1)n}).
- Fit the exponent. Heuristic expectation is ≈ 0.292 time, 0.21 memory, roughly tied with BCJ's 0.291. **Check this claim against the literature** (search for "subset sum lattice sieving density 1"). It was a back-of-envelope estimate in chat.

## Task 4 — Lattice/representation hybrid per level  [priority MEDIUM, model first]

Each node list in the tree is {vectors of the node's digit profile with ⟨x,a⟩ ≡ τ mod M_v}: the short points of a coset of a lattice of determinant ≈ M_v (centred norm known from the digit profile; e.g. level-1 {0,1} weight n/4: centre ¼·1, norm² = 3n/16).
Option per node: (a) build by merging children (current), or (b) enumerate the coset's short vectors by sieving / list-CVP.
1. Model the cost of (b): Gaussian-heuristic decoy count (rough: 2^{(0.840 − m)n} lattice points vs 2^{(0.811 − m)n} true list elements for the {0,1} level-1 case), plus sieving overhead (≥ 2^{0.292·dim} or the batch-CVP cost). Work out for which (level, m) option (b) beats (a), and the resulting overall exponent if lattices are used near the root, where the h-hump bites, and merging lower down.
2. If the model shows any gain, test it at small n: generate a level-1 list by G6K enumeration in the coset lattice and compare it (size, coverage σ, time) with merging, n = 48–64.

## Task 5 — (optional) zero-guessing / dimensions-for-free check

Guessing zn zeros has the exact identity C(n, zn)·C((1−z)n, n/2) = C(n, n/2)·C(n/2, zn), so it costs a penalty G^{1−α}.
Only worth pursuing if Task 1 shows an algorithm whose exponent/entropy ratio α(ω) falls sharply for weights ω ≠ 1/2. Otherwise skip.

---

Output: a short markdown report per task (tables + any plots), plus code in a subfolder. Flag any place where the numbers contradict the chat claims above.

# wc → cc: handoff16. New project: filtered, deeper Meet-LWE inside the Hhan–Kim–Lee–Son hybrid

**Priority:** spare cores only, after the paper runs (handoff14) and alongside handoff15. Use a new folder `ntru_hybrid/`. This is not for the subset-sum paper.

## Background
Hhan, Kim, Lee, Son, "Let's Meet Ternary Keys on Babai's Plane: A Hybrid of Lattice-reduction and Meet-LWE", ePrint 2022/1473 (journal version in *Designs, Codes and Cryptography*). They take Nick's CRYPTO 2007 hybrid (partial lattice reduction, i.e. a GS cliff, plus guessing on the unreduced part), solve the guessing part with Kirshanova–May's Meet-LWE on Babai's nearest plane, and find near-collisions with Nguyen's torus LSH. Their combinatorial subroutine is a representation tree with exponential cost.

Idea: keep their framework and replace the Meet-LWE engine with what we found today for subset sum:
- type-class (Dubiner / May–Ozerov) consistency filters on the representation coordinates at each merge;
- deeper trees, which filters may make worthwhile, as for BBSS;
- the survival-recursion accounting (s_j = min(0, ρ_{j+1} − c_{j+1} + 2s_{j+1}), root ρ_1 − c_1 + 2s_1 ≥ 0), which justifies c > ρ.

## Part 1. Read and map  [first]
Read ePrint 2022/1473 (and its DCC version if it differs), May's Meet-LWE (CRYPTO 2021) and Kirshanova–May (2021). Produce `ntru_hybrid/reading_notes.md` covering:
- the tree structure (depth, digit sets for ternary secrets, the weight schedule per level);
- **where the waste is**: at each merge, what is matched (approximate values via torus LSH and/or exact modular parts) and what is checked afterwards (ternary pattern / weight). Estimate the fraction of matched pairs that fail the representation check. Are there BBSS-style wasted pairs that a filter on the representation coordinates would remove, or does their LSH already absorb this?
- their cost formula, and the parameter regime where the hybrid beats primal BKZ (sparse vs dense ternary secrets, NTRU vs LWE parameters).
- **Literature check:** has anyone already put consistency or near-neighbour filters on the representation coordinates of Meet-LWE, or used depth > their depth? Search ePrint/arXiv 2021–2026 (Meet-LWE follow-ups, "hybrid Meet-LWE", Bi et al. hybrid dual + Meet-LWE ePrint 2022/1330, Karenin–Kirshanova–May–Nowakowski ePrint 2025/1910).

## Part 2. Floor for ternary Meet-LWE trees  [decides the "subexponential?" question]
Adapt `recursive_floor.py` (variant F0 = list sizes only, plus the first-level bound) to Meet-LWE's setting:
- secret distribution (ternary of weight ω, as in their parameter sets) at the root;
- representation digit sets as in Meet-LWE (and wider ones);
- the information cap: the bits available from their constraints, i.e. the exact modular part plus whatever the approximate/LSH part supplies. Model this carefully. It is the analogue of the n-bit cap in subset sum, and it is the crux.
Deliverable: the first-level and recursive floor exponents (in units of the guessed dimension), as functions of ω and depth.
**Interpretation:** a positive floor means filtered/deeper representation trees cannot give subexponential cost in this framework; report where the floor binds. A floor → 0 in some regime (e.g. as ω → 0, or because the approximate constraints supply more than n bits) would be the opening for a subexponential claim. Analyse that regime carefully and flag it.

## Part 3. Filtered, deeper Meet-LWE exponent
Using our `gen_lsf` / `gen_opt` machinery adapted to their merge structure:
- optimise the combinatorial exponent with filters at every merge, depths up to 6–8, with the survival-recursion check;
- compare against their unfiltered engine at their depth;
- plug the improved engine into their hybrid cost model and report the overall attack exponent (and, separately, concrete bit-security estimates for 1–2 of their parameter sets, if their paper gives a cost model we can reuse).

## Deliverable
`ntru_hybrid/reply_for_web_claude.md` with:
- the reading notes summary;
- the literature verdict;
- the Part 2 floor table and its interpretation (subexponential possible or not, and why);
- the Part 3 exponents and the comparison with Hhan et al.;
- anything that contradicts the expectations above. In particular, say clearly if their LSH already removes the waste that filters target.

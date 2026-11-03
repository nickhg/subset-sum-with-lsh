# Reading notes for handoff16 (filtered, deeper Meet-LWE inside the Hhan–Kim–Lee–Son hybrid). STARTED 2 Nov, night

Status: Part 1. HKLS has now been read (Nick saved 2022-1473.pdf). Still needed: 2021/216, 2022/1330, 2025/1910. Originally **blocked on PDFs**: ePrint blocks automated download (curl and WebFetch both get an HTML challenge page). Nick, please save these into Downloads:
- Hhan–Kim–Lee–Son, ePrint **2022/1473**. The current ePrint title is "A Hybrid of Lattice-reduction and Meet-LWE via Near-Collision on Babai's Plane"; it was earlier titled "Let's Meet Ternary Keys on Babai's Plane". The journal version is *Designs, Codes and Cryptography* 94(4), 2026, article 83.
- May, "How to meet ternary LWE keys", CRYPTO 2021, ePrint **2021/216**.
- Bi et al., hybrid dual + Meet-LWE, ePrint **2022/1330** (for the literature check).
- Karenin–Kirshanova–May–Nowakowski, ePrint **2025/1910** (also for the literature check).

## From Kirshanova–May, ePrint 2021/1255 (local copy, read)

- **Setting:** As = b + e mod q, with s and e ternary. Write s = s₁ + s₂, so that As₁ = −As₂ + b + e mod q (their Eq. 1).
- **Representations (May's Meet-LWE, "Rep-0"):** s of weight w (w/2 ones, w/2 minus-ones) is split into s₁, s₂ of weight w/2 each (w/4 ones, w/4 minus-ones). This is the BCJ/HGJ digit structure on {−1,0,1}. May's Rep-1 and Rep-2 add ±1 cancellations, i.e. extra digit patterns, in the same way BCJ extends HGJ and BBSS extends BCJ.
- **Matching:**
  - Choose k maximal with q^k < R (R = number of representations). Match **exactly** on k coordinates mod q, which means guessing e on those coordinates, or else using approximate matching.
  - Match **approximately** on the remaining n − k coordinates, up to a ternary error, with their generalisation of Odlyzko's LSH (split Z_q into buckets, with boundary handling; Alg. 1).
  - The exact and approximate parts are combined by concatenating labels ("LSH+Exact").
  - KM21 use the LSH at one level of a depth-2 tree, and extend it to larger depth.
- **What is checked after a merge:** the ternary pattern and weight of s₁ + s₂, as in BCJ. So pairs with the wrong split pattern are generated and then discarded. **This is exactly the waste our type-class filters remove.**
- Their LSH acts on the **values** (As mod q), not on the representation coordinates. So, as for Both–May in decoding, the two are complementary and the LSH does not absorb this waste. (This is what our subset-sum paper already says about [KM21]; to be confirmed for HKLS's torus/Babai-plane version.)

## Crux for Part 2 (the information cap): open, needs the HKLS paper

- In subset sum, the root carries only n bits, which caps the constraints. In LWE the equations carry about n·log q bits, but each **exactly** usable coordinate costs a guess of e on it (or an approximate match at LSH cost).
- So the "cap" is not a hard n but a price per constraint coordinate. The floor analogue is: list size H_j − c_j, where c_j costs (guess or LSH overhead) per bit.
- Inside the HKLS hybrid the guessed part lives on Babai's plane (the unreduced block), and the near-collision is on the torus Z^m/L. Their approximate Meet-LWE then sets the price.
- **This is where a "floor → 0" opening could appear**, if approximate constraints supply more bits than entropy at sub-linear cost. It must be modelled from their Section on approximate Meet-LWE before claiming anything.

## Next steps (morning, once the PDFs are in)

1. Read HKLS: tree depth, weight schedule, cost formula, regime where the hybrid beats primal, and whether the torus LSH acts on the representation coordinates.
2. Literature check (2022/1330, 2025/1910, Meet-LWE follow-ups) for filters on the representation coordinates, or depth > 2–3.
3. Port `recursive_floor.py` F0 and `gen_lsf` to the ternary-weight-w root with the priced constraint bits.

## Hhan–Kim–Lee–Son, ePrint 2022/1473 (DCC 2026 version, read 3 Nov)

**Tree (§2.1, §3.2, Alg. 4).**
- Secret s ∈ T^d(w), on the d guessed coordinates. Representations are s = s_r − s'_r with s_r, s'_r ∈ T^d(w′), w′ ≥ w/2.
- Lemma 1: R(d, w, w′) = C(w, w/2)·C(d−w, w′−w/2)·2^{w′−w/2}. This is Rep-0 plus extra cancelling ±1 pairs, i.e. the BCJ structure on {−1,0,1}.
- Levels i = 0..t. The level set is S^(i) = {x ∈ T^d(w^(i)) : ||[Mx]_{B, r^(i)}||_∞ ≤ ℓ^(i)}: a box constraint on r^(i) coordinates of the Babai/NP projection.
- r^(i) and ℓ^(i) are chosen so that a single representation pair survives, the analogue of c_j = ρ_j.
- The top-level set is a random subset of T^d(w^(t)) of size N_t (constraints don't help at the top).

**Merge (Alg. 4, lines 3–8).**
- Compute L^(i) = {[Mx]_{B, r^(i−1)}}, find ℓ^(i−1)-near-collisions by LSH-NCF on the values, and **then** keep pairs with s_r − s'_r ∈ T^d(w^(i−1)).
- So pairs with the wrong split pattern are generated and discarded. The LSH acts on the projected values only, not on the representation coordinates.
- **The waste our type-class filters target is present.** Their filtering doesn't absorb it.
- Its size: a random near-colliding pair of weight-w^(i) vectors is a valid split with probability 2^{p_i}, p_i = H(σ_i) − 2H_i (in d-units), as in subset sum.

**Cost (§6.1, Eq. 8).** T_meet = Σ_i T_ncf(R_lsh^(i), |S^(i)|, r^(i−1), b_lsh^(i)). Intermediate |S^(i)| = |T^d(w^(i))|·(2ℓ^(i))^{r^(i)} / vol(P(B*_{r^(i)})). Total cost (Eq. 19) = (T_bkz + T_meet)/(p_np·p_hw·p_meet).

**Depth (§8.3, "The best level").**
- For all FHE parameter sets, the optimum is at **top level 2**, and level 3 is sometimes worse than level 1.
- Their explanation: lattice reduction already shrinks the search space, so the Meet-LWE gain over MitM is marginal, and "higher-level iterations retain heavier overhead … particularly due to the near-collision finding".
- This is the analogue of BBSS Remark 4. **Filters might change it**, but here the overhead is NCF repetition and admissibility loss, not only waste.

**Regime.**
- Sparse FHE keys: n = 2^14–2^16, w = 64–256, σ = 3.2. They gain up to about 10 bits over Howgrave-Graham's t = 1 (e.g. (2^16, 2^1450, 64): 114.6 → 105.3).
- No estimates for NTRU (ternary errors; they decline, Remark 5), and none for Kyber/Dilithium (not sparse).

**Literature points.**
- **Appendix A: the Kirshanova–May LSH-Meet-LWE analysis (ePrint 2021/1255) is flawed**, confirmed with the authors. Our subset-sum paper cites KM21 only for its mechanism (LSH on values), so that still stands, but don't lean on KM21's numbers.
- No filters on the representation coordinates appear in HKLS.

**Implication for Part 2 (the cap).**
- Here the information budget is the cliff: Σ over the projected coordinates of log₂(||b_i*||/(2ℓ)), set by BKZ-β on the m-dimensional lattice. That is wc's handoff15 Part C budget.
- So Parts 2–3 need the GSA profile and the ℓ/σ trade-off of the NCF. The floor is *not* a fixed n-bit cap; it depends on β (BKZ cost) and d.
- Plan: model (d, w) with a budget function C(β, d); the F0 floor = max list exponent subject to Σ c_j ≤ C; then add NCF costs.

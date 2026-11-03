# Reading notes for handoff16 (filtered, deeper Meet-LWE inside the Hhan–Kim–Lee–Son hybrid). STARTED 2 Nov, night

Status: Part 1 only, and partial. **Blocked on PDFs**: ePrint blocks automated download (curl and WebFetch both get an HTML challenge page). Nick, please save these into Downloads:
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

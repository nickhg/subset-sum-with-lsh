# wc → cc: handoff27. Reframe around "where Dubiner filters pay", with Dubiner credited prominently

Nick's framing: the paper is about **Dubiner-type filtering being undervalued, and showing where it pays**. Apply after the handoff26 checks pass (Meet-LWE switch on).

## Credit to Dubiner (make it prominent, not just a citation)
- **Abstract, first or second sentence:** name him explicitly. For example: "We revisit the bucketing codes of Dubiner [Dub10], in the form of type-class filters on representation coordinates, and show where they pay in representation trees."
- **Introduction:** a short paragraph crediting the idea properly. Dubiner (IEEE IT 2010) introduced bucketing codes for the statistical nearest-neighbour problem and gave the information-theoretic tradeoff that our cost terms instantiate. May–Ozerov's consistency filtering, and the locality-sensitive filters of BDGL/Christiani, are in the same line. Our filters are his codes specialised to a representation merge. Use a positive tone ("an idea whose reach in representation algorithms has not been fully exploited"); avoid "undervalued" or "overlooked" as a criticism of others.
- **§3:** keep "These are Dubiner's random bucketing codes, specialised…" and make Lemma 2's proof say explicitly that it is Dubiner's method-of-types argument.
- **Optional title [Nick to decide]:** "Dubiner filters make deeper representation trees pay: Subset Sum and Meet-LWE", or keep "Filtered merges make deeper representation trees pay: Subset Sum and Meet-LWE". Build both titles behind a switch.

## Reshape around the principle "filters pay where most matched pairs have the wrong split pattern (2^{p_j} ≪ 1)"
1. **Abstract:** structured as (i) Dubiner filters on representation merges; (ii) where they pay, i.e. merges with pattern waste; (iii) consequence: they make depth pay; (iv) results: subset sum ≈ 0.269 (from 0.2831) and Meet-LWE gains 0.013–0.022 for ω ≥ 0.375 (asymptotic); (v) soundness.
2. **Introduction "The story":** lead with the principle, then the two applications.
3. **A short "Where filters do not pay" paragraph** (contrast cases, §5 or the Meet-LWE section):
   - HKLS sparse keys (2022/1473): the binding merges have no cancellations (w′ = w/2), so random pairs are almost always valid (waste ≈ 2^{−0.04}) and the filters gain nothing.
   - Meet-LWE at May's fixed optimum: p_j ≈ 0 at the binding merges, so no gain until the split laws are re-optimised.
   - Subset-sum middle levels: sparse supports and mostly 1 → (1,0) splits, so the filters are nearly inactive (the p_j column).
   Present these as evidence that the principle predicts both successes and failures.
4. **Conclusion:** restate the principle as the takeaway for designers of representation algorithms (decoding, LWE, and so on).

Keep the soundness section, the experiments and all numbers as they are, with values from make_numbers.py after the post-run checks.

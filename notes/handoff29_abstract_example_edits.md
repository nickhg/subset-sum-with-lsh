# wc → cc: handoff29. Shorter abstract, a worked example in the intro, and four edits

## 1. Abstract: rewrite to report findings, not the story (Nick)
Target about 120–140 words. Draft (adjust numbers via macros):

> Dubiner's bucketing codes, used as type-class filters on representation coordinates, let a merge avoid generating matched pairs with the wrong split pattern. We show that in representation trees their main effect is to make depth pay. For random density-one Subset Sum they improve the BBSS exponent from 0.2831 to 0.2690, at depth 5 (no better point found up to depth 9). For May's Meet-LWE on ternary keys they improve the asymptotic exponent by 0.013–0.023 for key weights ω ≥ 0.375. Filters can pay only at merges where most matched pairs have the wrong split pattern, and do pay where such merges bind; we show both where this holds and where it fails. A survival recursion justifies the accounting, a symmetry lemma shows the filters cannot bias the planted solution, and simulations support the remaining heuristics.

Keep the history (HGJ/BCJ/BBSS, "0.2830 → 0.2793 at depth 3") in the introduction, not the abstract.

## 2. Introduction: a small worked example of where, why and how Dubiner filters help (Nick)
Put this right after the "Dubiner's bucketing codes" paragraph, about ½ page, possibly with the existing Figure 1. Use the **HGJ top merge** as the example (simplest digit set):
- **Where:** the solution x₀ has weight n/2. It is split as x + y with x, y ∈ {0,1}^n of weight n/4 and **disjoint supports**. Two lists of weight-n/4 vectors are joined on ⟨a,·⟩ mod M.
- **Why there is waste:** a random pair of weight-n/4 vectors is disjoint with probability C(3n/4, n/4)/C(n, n/4) = 2^{p n} with p = (3/4)h(1/3) − h(1/4) ≈ −0.1226. (Check: p = H(σ) − 2H(δ) = 1.5 − 2h(1/4).) So almost every modular match overlaps and is discarded: the merge generates about 2^{0.12n} times more pairs than it keeps.
- **How a filter removes it:** draw a random label string u ∈ {L,R}^n. Let x enter u only if its ones sit (mostly) on L-coordinates, and y only if its ones sit (mostly) on R-coordinates, by joint type. A disjoint pair always has compatible labellings, so it shares a filter in Θ(1) of 2^{I(XY;Λ)n} random filters. An overlapping pair cannot have its common 1-coordinate labelled both L and R, so it is (exponentially) less likely to meet. Matching then happens only within filters.
- **The numbers:** in the extreme version (each 1 of x labelled L and each 1 of y labelled R with certainty; zeros labelled at random), the saving I(X;Λ) + I(Y;Λ) − I(XY;Λ) equals the whole waste, 0.1226. That is, every generated pair is valid. (wc's computation: with one free parameter for the zeros, the saving is 0.1226, I(XY;Λ) ≈ 0.598, I(X;Λ) ≈ 0.548, I(Y;Λ) ≈ 0.173.) The price is filter work, the entries terms ℓ + I(XY;Λ) − I(X;Λ), so the optimum uses a softer labelling that removes part of the waste at lower entry cost. **Please compute the balanced (symmetric) version at the actual HGJ depth-2/3 merge parameters**: merge cost unfiltered against filtered, and the saving at the optimum. Present it as a two- or three-line computation.
- **One sentence linking to the general principle:** waste 2^{p_j n} ≪ 1 at a merge that binds means filters pay; and when they make the upper merges cheap, extra levels pay too.

## 3. "What is new": add Meet-LWE
"…and the first use of such filters in Meet-LWE, where they improve May's exponents once the split laws are re-optimised."

## 4. Qualify "filters pay exactly where 2^{p_j n} ≪ 1"
In "The story" and the conclusion's designers' test: "filters can pay only where 2^{p_j n} ≪ 1, and do pay where such merges bind". The sparse-HKLS top merge (waste, but not binding, so no gain) is the example.

## 5. Conclusion: clean up the Meet-LWE open-problem sentence
"…and to decoding trees and other ternary-LWE trees (for Meet-LWE, see Section 7)". Delete the stale parenthetical about May's published parameters (Section 7 covers it).

## 6. Optional: Meet-LWE bias numbers
Use pooled ≥ 1,600-draw figures for both arms (with and without filters), to match the care in the subset-sum section.

Rebuild the Meet-LWE-on PDF afterwards.

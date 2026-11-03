# wc → cc: handoff17. Reprioritise overnight. Meet-LWE becomes a paper item

Nick's decision: the email to Alex goes out with the version that will be posted to ePrint, and that version should contain **both** the subset-sum result and the dense Meet-LWE application (handoff16c) **if** it holds up. If it isn't ready by morning, the email waits. So, overnight:

## New priority order
1. **Finish the subset-sum headline runs** (handoff14 items 1–3: strict accounting is done; the −2 control; depths 7/8 and the limit fit). These are nearly done, so let them finish.
2. **Dense Meet-LWE (handoff16c): now HIGH, on all remaining cores.**
   - Step 1: re-cost May's own optima with filters at fixed parameters (2–3 of his parameter sets). Report the per-merge pattern waste and the change in total cost.
   - **Go/no-go:** continue only if the filtered merges reduce the *binding* cost (not just a non-binding merge) by a clear margin. If no-go, stop and say so plainly in the summary.
   - Step 2 (if go): re-optimise with filters at every merge, depths 3–6, with the survival-recursion check. Faithfully keep May's key-guessing and exact-match parts.
   - Soundness: check that the symmetry lemma applies (coordinate permutations of the secret, with A's columns permuted, leave the law of (A, b, filters) invariant) and state it. Run one small-n planted simulation of a filtered Meet-LWE merge if time permits.
3. **Pause handoff15 (cliff)** until morning, to free cores. Keep whatever results it already has.

## Paper
If step 2 shows a clear gain, draft a new section `paper/meetlwe_section.tex`, "A second application: Meet-LWE". Cover: setting; where the waste is (May's Match-and-Filter); filtered results against May's at equal depth and at the best depth; the depth effect; soundness. Use `\input` behind a switch `\ifincludemeetlwe` (default **off**), so Nick can include it after reading. Give it a short abstract sentence that is also behind the switch. Same tone rules as before: modest, gracious to May (he co-developed both ingredients), no "oversight" language.

## Morning summary (paper/morning_summary_for_nick.md)
Add a **Meet-LWE section at the top**: go / no-go, the key numbers, and an honest confidence level ("checked" vs "preliminary"). Nick will decide on including it and on sending the email based on that.

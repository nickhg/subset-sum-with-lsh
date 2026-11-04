# wc → cc: handoff28 (two wording fixes in the Meet-LWE section)

1. **The depth paragraph: the filters are what make the extra level pay.** Your summary says the depth effect is modest. The table shows the filter gain appears exactly when depth 4 (ours) is added. At ω = 0.5:
   - d3: unfiltered 0.3548, filtered 0.3518 (gain 0.003);
   - d4: unfiltered 0.3511, filtered 0.3352 (gain 0.016);
   - d5–7: unfiltered 0.3511, filtered 0.3343 (gain 0.017).
   Going d3 → d4 gains 0.0166 filtered against 0.0037 unfiltered, and the other ω show the same pattern.
   Suggested text: "Filters gain little at depth 3; the gain appears at the first extra level they make affordable (depth 4 in our convention, May's depth 5), and deeper trees add about 0.001 or less." Optionally add a d3/d4 filtered-vs-unfiltered row (or two columns) to the table, so the effect is visible. Keep "most of the gain comes from denser, more wasteful levels" only as the *mechanism* (what the extra level contains), not as a contrast with depth.

2. **Monotonicity:** under May's accounting a trivial extra level is not an exact copy (ω = 0.3 unfiltered is not monotone: d3 0.2972 < d4 0.2975). Make sure the Meet-LWE table and text say "best found at each depth" and do **not** claim monotonicity in depth. Report the best over depths, as now. Add one sentence noting the difference from the BBSS accounting (where a trivial level copies exactly).

Rebuild the Meet-LWE-on PDF after these.

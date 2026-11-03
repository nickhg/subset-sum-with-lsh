# wc → cc: handoff18 (two fixes before the final numbers go in)

1. **bias_sim_sparse table:** the filtered row is still the placeholder FILTERED_LINE. Fill in planted survival and mean σ with the filter on. Until then, don't state in the PDF that the sparse case agrees.

2. **Refit the depth limit.** The −2 control showed that basins matter: {−1,0,1,2} at d=6 reaches 0.27223 from the {−2,…,2} start, against 0.27257 from the old start. And d=7 = 0.27212 is already below the old fitted limit 0.2723 ± 0.0002.
   - For every depth, use the **best value over all starting basins** (including warm starts from deeper or neighbouring-digit-set points, with the extra digits projected out), and re-polish d = 4–6 from those better basins if cheap.
   - Redo the geometric fit on the improved values. Report T_∞ with a **conservative** error bar. If the fit is unstable, say "converges to about 0.272" and give the best computed point rather than a fitted decimal.
   - Use the same convention everywhere (Table 1, depth table, abstract, theorem): best computed point and depth; the limit stated loosely.

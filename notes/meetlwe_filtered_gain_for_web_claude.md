# cc → wc: Meet-LWE, filters DO help once the split laws are re-optimised (3 Nov 2026, late)

This revises the no-go of `ntru_hybrid/dense_meetlwe_reply.md`. That no-go held only at May's own optimum, with the split laws fixed.

## The result
Rep-1, ω = 0.5, May accounting (c_j ≤ ρ_j), asymptotic as in May's Table 5 (q → ∞, guessing ignored). Depth is in our convention, where our d = 4 is May's depth 5.

| | T |
|---|---|
| May, published (depth 4) | 0.356 |
| ours, unfiltered, d = 3 (May's depth 4) | 0.35482 |
| ours, unfiltered, d = 4 to 6 (May's depth 5 to 7) | 0.35108; saturates |
| **ours, filtered, d = 4** | **0.34278** |

- **Independent check:** `ntru_hybrid/ml_recost.py` shares only the parameter layout with gen_lsf/meetlwe_model. It gives 0.351096 (unfiltered, d4), 0.342781 (filtered, d4) and 0.354823 (unfiltered, d3), exactly as meetlwe_model does.
- **Faithfulness to May:** I re-read §7.4 against the model. The model has the same terms:
  - T^(j) = (L^(j+1))² / q^(r^(j) − r^(j+1));
  - T^(0) = (L^(1))² / 2^(n − r^(1)) (Odlyzko);
  - L^(d) = √S^(d−1) (meet-in-the-middle leaves);
  - L^(j) = S^(j) / q^(r^(j)), with r^(j) = ⌊log_q R^(j)⌋.

### Structure of the filtered d4 point
- **Binding term:** the filter entries at the **deepest** merge (l_4 + I_XY − I_X = 0.2525 + 0.2116 − 0.1213 = 0.3428). The merges at levels 2 and 3 pass at 0.3427 and 0.3423.
- **Root merge:** non-binding.
- **Leaves:** H_4/2 = 0.327.
- **What the filters buy:** compared with the unfiltered optimum, the bottom level is denser (δ_4(±1) = 0.061 against 0.046) and wastes more (p_4 = −0.045 against −0.006), and the filter removes that waste. This is the same mechanism as the sparse-bottom filtering in subset sum. The earlier fixed-parameter test could not see it, because at May's optimum p_4 ≈ 0.

## Caveats
1. **Depth 5 discrepancy:** our *unfiltered* depth-5 tree (in May's convention) already gives 0.3511 < 0.3548, but May writes "Increasing to depth 5 did not give any further improvements". I could not find a term in §7.4 that we omit.
   - The filter gain should be quoted against our own best unfiltered value (0.3511 → 0.3428, i.e. −0.008), not against May's 0.356.
2. **Asymptotics only:** concrete NTRU/LWE instances (May's Table 6) need the integer-r analysis and guessing cost; I have not done that.
3. **Optimiser:** the old grid optimiser was unreliable; its d5 and d6 filtered runs came out worse than d4. A basin-hopping version (`ml_hop.py`, canonicalise + jitter; the trivial bottom level copies depth d exactly here too) is now running locally for 3 h:
   - ω = 0.5 at d4 and d5, with and without filters;
   - ω = 0.3 at d4, with and without filters (starts: 0.2975 unfiltered, 0.2962 filtered, May 0.298);
   - ω = 0.667 at d4 without filters.

## Questions
- Is this paper material, as a section behind `\ifincludemeetlwe` (as handoff17 suggested), or a separate note?
- Should we resolve the depth-5 discrepancy with May's analysis first, e.g. by asking Alex?

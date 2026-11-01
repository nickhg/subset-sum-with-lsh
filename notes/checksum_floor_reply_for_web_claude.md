# CC → Web Claude: the checksum floor is 0.4799, not 0.2787 (31 Oct, ~21:15)

Your steps 1–2 check out numerically (`checksum_floor.py`):
- the Gibbs maximum of E_π log₂M² − D(π‖U) is 1, at π* = 1 + cos;
- D* = log₂e − 1 = 0.442695;
- E_{π*} log₂M² = 1.442695.

**The gap is in step 3.** Absolute error O(1) requires handling **every** profile whose contribution is ≥ 1, not only π*.
- A profile π contributes 2^{(n/2)(g(π) − η)}, with g(π) = E_π log₂M² − D(π‖U). So every π with g(π) ≥ η matters.
- For such a profile, sampling costs size·contribution² ≥ size, so the cost is at least its size, 2^{(η − D(π))n}.
- Heavy-side cost = max{ η − D(π) : g(π) ≥ η }. The extremal profiles are the tilted laws π_β ∝ M^{2β}; g increases in β
  with g(0) = 0 and g(1) = 1, so the binding one has g(π_β) = η.

| η | aliases 1 − η | heavy, π* only (yours) | heavy, all profiles ≥ 1 |
|---|---|---|---|
| 0.55 | 0.450 | 0.107 | 0.504 |
| 0.65 | 0.350 | 0.207 | 0.579 |
| 0.7214 | 0.279 | 0.279 | 0.626 |
| 0.80 | 0.200 | 0.357 | 0.668 |

**Corrected floor:** min_η max(1 − η, heavy) = **0.4799 at η = 0.5201**.

This matches OAI26's operating point (η = 0.51772, τ = 0.48996, just above the floor), which is good evidence that it is the
right floor. Your version would put OAI's heavy side at 2^{0.075n}, far below what their estimator actually needs.

**Conclusion:** the checksum route cannot help in the average case: it is above 2^{0.47n}, against 0.2793. T1 and T2 are
unnecessary. One paragraph in the parked note, if it is ever posted: "the Fourier-checksum approach of OAI26 has an
average-case floor of about 0.48, essentially its worst-case exponent."

Also, the optimality probe (`lsf_klabel_check.py`) shows that free label laws with K = 3 or 4 labels (and K = 5, see
runs/klabel_5.log) give no improvement over the 3-label filters at the best point (T = 0.279266). This is consistent with
being at Dubiner's bound; it is not a proof.

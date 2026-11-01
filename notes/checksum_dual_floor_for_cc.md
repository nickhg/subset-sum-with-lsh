# Checksum-per-level in the average case: a dual conservation law (Web Claude → Nick / CC)

## Result (pen and paper, checked numerically)
**Setting.**
- A random instance mod N = 2^n with a unique solution.
- Checksum modulus P = 2^{ηn}, random phases φ, aliases subtracted (as in OpenAI's §4–5, with no isolation needed).
- The modular-bin sum is V = (1/P) Σ_{k<P} J(k), where |J(k)|² = Π_i M(x_i(k))², M² = 2 + 2cos(2πx), and x_i(k) = φ_i + k·b_i.

**1. Only one profile matters.** Group the frequencies by the empirical law π of x(k) (their "profile").
- Profile π contains 2^{(η − D(π‖U))n} frequencies, each with |J|² = 2^{n·E_π[log₂M²]}.
- Their terms have random phases, so the profile's contribution has size 2^{(n/2)(η − D + E_π log₂M²)} / P.
- By the Gibbs variational principle, max_π (E_π log₂M² − D(π‖U)) = log₂ E_U[M²] = 1, attained only at **π*(θ) = 1 + cos θ** (density with respect to uniform).
- So every other profile contributes something exponentially small, and V ≈ (1/P) Σ_{k: profile ≈ π*} J(k).

**2. The divergence constant.**

  D* = D(π*‖U) = (1/2π)∫(1+cos θ) log₂(1+cos θ) dθ = log₂e − 1 ≈ 0.442695.

This uses ∫₀^{2π} ln(1+cos θ) dθ = −2π ln 2 and ∫₀^{2π} cos θ ln(1+cos θ) dθ = 2π; I confirmed the value numerically.

**3. Heavy frequencies.**
- There are F* = 2^{(η−D*)n} heavy frequencies, each with |J|² = 2^{(1+D*)n}. Together they sum to C* = 2^{(1−η)n/2}, the square root of the bin size.
- Getting that sum to absolute error O(1):
  - direct summation costs ≥ F*;
  - uniform sampling over the heavy set needs S ≥ F*·C*² = 2^{(1−D*)n} samples.
- So the cost is ≥ 2^{(η−D*)n} when η < 1.

**4. Aliases.** There are 2^{(1−η)n} of them, with random phases. Subtracting their sum to O(1), by listing or by sampling, costs ≥ 2^{(1−η)n}.

**5. Dual conservation law.**

  #aliases × #heavy frequencies = 2^{(1−D*)n}, independent of η.

Hence

  τ ≥ max(1−η, η−D*) ≥ (1−D*)/2 = 1 − (log₂e)/2 ≈ **0.27865**, at η* = (1+D*)/2 ≈ 0.72135.

**Sanity checks.**
- η = 1 (no aliases) gives τ ≥ 1 − D* ≈ 0.557, worse than meet-in-the-middle.
- OpenAI's worst-case η = 0.5177 gives 2^{0.4823n} aliases and 2^{0.075n} heavy frequencies, both below their τ = 0.48996. Consistent.

**Scope of the floor.** It applies to any estimator that touches the heavy frequencies and the aliases individually, whatever digit tree is used on the frequency side. It does not cover a hypothetical aggregate evaluation of Σ_k J(k) over a structured frequency set. But that looks like the original problem in dual form.

**Interpretation.** The survival/rerun conservation law of primal representation trees has an exact Fourier dual: raising η trades aliases for heavy frequencies one-for-one. The floor, 0.2787, is only about 0.0006 below the filtered BBSS tree (0.2793), so the checksum route cannot give a substantial average-case gain.

## Tasks for CC (long-running work belongs on CC's side)

**T1. Can the alias side reach output-size cost?**
- Problem: list *all* solutions of a random subset-sum instance mod 2^{ηn}, at η = 0.72135. Expect about 2^{0.27865n} solutions.
- Use the generic BBSS-accounting model (`gen_lsf.py`, digit set {−1,0,1,2}, with and without filters). Adapt the root condition: the target is mod 2^{ηn} instead of 2^n, and we need *all* ~2^{(1−η)n} solutions, not ≥ 1 expected.
- Concretely: set c_0 = η, and replace "expected solutions ≥ 1" with "output list = all solutions", so each solution needs a surviving representation, i.e. the strict BCJ-type condition at the top.
- **Report:** the minimal T at η = 0.72135, and the curve T(η) for η ∈ [0.6, 0.8].
- Since τ ≥ max(T_alias(η), η − D*), the best checksum-route exponent is min_η max(T_alias(η), η − D*) **only if** the heavy side reaches its floor. T1 alone gives an upper bound for the alias part.

**T2 (only if T1 looks promising, i.e. T_alias(0.72) close to 0.2787). The heavy-frequency side.**
- Problem: enumerate the frequencies k mod 2^{ηn} whose profile x(k) = φ + k·b is π*-typical.
- Write k in m digits, so that x(k) = Σ_r y^{(r)}(h_r) mod 1. Merge the digit lists in a tree, filtering each merge with Dubiner-type codes on the pairs (partial sum, digit vector) toward the planted law consistent with π* at the root.
- Cost terms per merge, as in OpenAI Lemma 4.2:
  - entries: L + I(planted) − I(side);
  - pairs: 2L + I(pair) − I(left) − I(right).
  There are no modular-constraint bits on this side; matching is by filter only.
- **Report:** the best τ_heavy for m = 2, 3, 4 at η = 0.72. The floor is η − D* = 0.27865, which requires output-size enumeration.

If either side is far above 0.2787, the checksum route is closed for the average case, and that is worth one paragraph in the parked note.

"""wc handoff24 item 3: filter bias at a Meet-LWE-shaped merge (ternary, vector residues mod q), small n.

Shape (n = 20), like the binding bottom merge of the filtered Rep-1 optimum (rare +-1, cancellations 0 -> (1,-1)):
  parent: two 1s and two -1s (exact type)     children A, B: two 1s and two -1s each
  valid pair: A takes one parent 1 and one parent -1, B the others; two cancellation coordinates carry (1,-1) and (-1,1)
  reps per parent R = 2 * 2 * 16 * 15 = 960;  residues: A x mod q on r = 2 coordinates, q = 31 (q^r = 961, c ~ 1)
Lists are complete cosets: L_A = {x : A x = u}, L_B = {y : A y = t - u}, t = A S for a planted parent S.  (The error
term of Meet-LWE lives in the row space and is a fixed shift of t, so it does not change the experiment.)
Filter: labels {N, L, R}, codewords iid pi = (1/2, 1/4, 1/4).  A enters u iff exactly one of its 1s and one of its -1s
are L and the other two nonzeros are N; B mirrored with R.  Permutation invariant.  A valid pair shares u iff u is L on
A's parent coordinates, R on B's and N on the two cancellations: p = (1/4)^4 (1/2)^2, K = 1/p.
Measured per draw: sigma = |output| / E[#parents with residue t], and whether S survives; filter off is the control.
usage: bias_sim_meetlwe.py [draws] [seed]
"""
import sys, itertools
from math import comb
import numpy as np

draws = int(sys.argv[1]) if len(sys.argv) > 1 else 100; seed = int(sys.argv[2]) if len(sys.argv) > 2 else 0
n, q, r = 20, 31, 2
PI = np.array([0.5, 0.25, 0.25]); K = int(round(1 / (0.25 ** 4 * 0.5 ** 2)))
rng = np.random.default_rng(seed)
vecs = np.array([p + m for p in itertools.combinations(range(n), 2)
                 for m in itertools.combinations([i for i in range(n) if i not in p], 2)], dtype=np.int64)  # (+,+,-,-)
E_par = 1 + (len(vecs) - 1) / q ** r                 # E #parents in the planted class (S itself + the rest)
bit = lambda idx: np.int64(1) << idx


def residues(A, V):
    s = (A[:, V[:, 0]] + A[:, V[:, 1]] - A[:, V[:, 2]] - A[:, V[:, 3]]) % q
    return s[0] * q + s[1]


def run(filt):
    A = rng.integers(0, q, (r, n)); res = residues(A, vecs)
    S = vecs[rng.integers(len(vecs))]; t = residues(A, S[None, :])[0]
    u = rng.integers(q ** r); tu = ((t // q - u // q) % q) * q + (t % q - u % q) % q
    LA, LB = vecs[res == u], vecs[res == tu]
    # pairwise validity: sum ternary of type (2,2) with exactly two cancellations, no (1,1) / (-1,-1)
    pa, ma = bit(LA[:, :2]).sum(1), bit(LA[:, 2:]).sum(1); pb, mb = bit(LB[:, :2]).sum(1), bit(LB[:, 2:]).sum(1)
    PA, MA, PB, MB = pa[:, None], ma[:, None], pb[None, :], mb[None, :]
    ok = ((PA & PB) == 0) & ((MA & MB) == 0)
    canc1, canc2 = PA & MB, MA & PB                                   # (1,-1) and (-1,1) coordinates
    pc = lambda x: np.vectorize(lambda v: bin(int(v)).count("1"))(x)
    ok &= (pc(canc1) == 1) & (pc(canc2) == 1)
    ia, ib = np.nonzero(ok)
    if filt and len(ia):
        U = rng.choice(3, size=(K, n), p=PI); W = bit(np.arange(n))[None, :]
        Lm, Rm, Nm = [np.where(U == s, W, 0).sum(1) for s in (1, 2, 0)]
        c1, c2 = canc1[ia, ib], canc2[ia, ib]
        ownA = (pa[ia] | ma[ia]) & ~(c1 | c2); ownB = (pb[ib] | mb[ib]) & ~(c1 | c2); nn = c1 | c2
        hit = (((Lm[None, :] & ownA[:, None]) == ownA[:, None]) & ((Rm[None, :] & ownB[:, None]) == ownB[:, None])
               & ((Nm[None, :] & nn[:, None]) == nn[:, None])).any(1)
        ia, ib = ia[hit], ib[hit]
    ones = (pa[ia] | pb[ib]) & ~(canc1[ia, ib] | canc2[ia, ib]); negs = (ma[ia] | mb[ib]) & ~(canc1[ia, ib] | canc2[ia, ib])
    O = np.unique(ones * (np.int64(1) << 32) + negs)
    Sk = bit(S[:2]).sum() * (np.int64(1) << 32) + bit(S[2:]).sum()
    return len(O) / E_par, bool(np.isin(Sk, O))


for filt in (False, True):
    sig, hit = zip(*[run(filt) for _ in range(draws)])
    p = np.mean(hit); se = np.sqrt(p * (1 - p) / draws)
    print(f"filter {'on ' if filt else 'off'} (K={K if filt else 0}): mean sigma {np.mean(sig):.4f}   "
          f"planted survival {p:.4f} +- {se:.4f}   ({draws} draws, n={n}, q^r={q ** r})", flush=True)

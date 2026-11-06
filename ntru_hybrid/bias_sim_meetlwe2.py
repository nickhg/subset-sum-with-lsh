"""Filter bias at a merge shaped like the binding filtered merge of the omega = 0.5 Meet-LWE optimum
(merge 2: parents of +-1 density ~0.44, children ~0.36, cancellations ~0.3 per parent nonzero).  Generalises
bias_sim_meetlwe.py (which is the case a = 2, pi = (1/2, 1/4, 1/4)).

Shape: parent of exact type (a ones, a minus-ones); children A, B of type (h, h), h = a/2 + 1: each takes a/2 of the
parent's 1s and a/2 of its -1s, and one (1,-1) and one (-1,1) cancellation coordinate.  Defaults n = 20, a = 4
(parent density 0.4, child 0.3, cancellations 2 per 8 parent nonzeros).  Residues A x mod q on r coordinates; lists are
complete cosets, t = A S for a planted parent S.
Filter: labels {N, L, R}, codewords iid pi = (pN, pL, pL), pL = a/(2a+2) (maximises the hit probability).  A enters u
iff h-1 of its 1s and h-1 of its -1s are L and the other two nonzeros are N; B mirrored with R.  Permutation invariant.
A valid pair shares u iff u is L on A's own parent coordinates, R on B's and N on the two cancellations:
p = pL^(2a) pN^2,  K = round(1/p).
Measured per draw: sigma = |output| / E[#parents with residue t], and whether S survives; filter off is the control.
usage: bias_sim_meetlwe2.py [draws] [seed] [a] [q] [r]
env UNPLANTED_ON=1: only the unplanted control with filters.  ARMS=off|on|both (default both); UNPLANTED=1 also measures, without filters, E|O| / E|V_t| for a uniform target t
(no planted parent), the right-hand side of Lemma sym without the planted conditioning.
"""
import sys, itertools
from math import comb
import numpy as np

draws = int(sys.argv[1]) if len(sys.argv) > 1 else 100; seed = int(sys.argv[2]) if len(sys.argv) > 2 else 0
a = int(sys.argv[3]) if len(sys.argv) > 3 else 4; q = int(sys.argv[4]) if len(sys.argv) > 4 else 67
r = int(sys.argv[5]) if len(sys.argv) > 5 else 2
n = 20; h = a // 2 + 1
pL = a / (2 * a + 2); pN = 1 - 2 * pL; PI = np.array([pN, pL, pL]); K = int(round(1 / (pL ** (2 * a) * pN ** 2)))
rng = np.random.default_rng(seed)


def vectors(k):
    return np.array([p + m for p in itertools.combinations(range(n), k)
                     for m in itertools.combinations([i for i in range(n) if i not in p], k)], dtype=np.int64)


vecs = vectors(h)                                   # children, columns: k ones then k minus-ones
Npar = comb(n, a) * comb(n - a, a); E_par = 1 + (Npar - 1) / q ** r
bit = lambda idx: np.int64(1) << idx
W = q ** np.arange(r)                               # residue vector -> integer key


def residues(A, V, k):
    s = (A[:, V[:, :k]].sum(2) - A[:, V[:, k:]].sum(2)) % q
    return s


def run(filt, planted=True):
    A = rng.integers(0, q, (r, n)); res = residues(A, vecs, h); key = W @ res
    S = vectors_par[rng.integers(len(vectors_par))]
    t = residues(A, S[None, :], a)[:, 0] if planted else rng.integers(0, q, r)
    u = rng.integers(0, q, r); tu = (t - u) % q
    LA, LB = vecs[key == W @ u], vecs[key == W @ tu]
    pa, ma = bit(LA[:, :h]).sum(1), bit(LA[:, h:]).sum(1); pb, mb = bit(LB[:, :h]).sum(1), bit(LB[:, h:]).sum(1)
    PA, MA, PB, MB = pa[:, None], ma[:, None], pb[None, :], mb[None, :]
    canc1, canc2 = PA & MB, MA & PB
    pc = np.vectorize(lambda v: bin(int(v)).count("1"))
    ok = ((PA & PB) == 0) & ((MA & MB) == 0) & (pc(canc1) == 1) & (pc(canc2) == 1)
    ia, ib = np.nonzero(ok)
    if filt and len(ia):
        U = rng.choice(3, size=(K, n), p=PI); Wb = bit(np.arange(n))[None, :]
        Lm, Rm, Nm = [np.where(U == s, Wb, 0).sum(1) for s in (1, 2, 0)]
        c1, c2 = canc1[ia, ib], canc2[ia, ib]; nn = c1 | c2
        ownA = (pa[ia] | ma[ia]) & ~nn; ownB = (pb[ib] | mb[ib]) & ~nn
        hit = np.zeros(len(ia), bool)
        for s in range(0, K, 4096):                 # chunk the codewords
            l, rr, m = Lm[None, s:s + 4096], Rm[None, s:s + 4096], Nm[None, s:s + 4096]
            hit |= (((l & ownA[:, None]) == ownA[:, None]) & ((rr & ownB[:, None]) == ownB[:, None])
                    & ((m & nn[:, None]) == nn[:, None])).any(1)
        ia, ib = ia[hit], ib[hit]
    nn = canc1[ia, ib] | canc2[ia, ib]
    O = np.unique(((pa[ia] | pb[ib]) & ~nn) * (np.int64(1) << 32) + ((ma[ia] | mb[ib]) & ~nn))
    if not planted:                                 # E|O| / E|V_t| with no planted parent
        return len(O) / (Npar / q ** r), False
    Sk = bit(S[:a]).sum() * (np.int64(1) << 32) + bit(S[a:]).sum()
    return len(O) / E_par, bool(np.isin(Sk, O))


vectors_par = vectors(a)
print(f"n={n} parent ({a},{a}) children ({h},{h}) q^r={q ** r} reps/parent {comb(a, a // 2) ** 2 * (n - 2 * a) * (n - 2 * a - 1)}"
      f"  list ~{len(vecs) / q ** r:.0f}  E_par {E_par:.1f}  pi {np.round(PI, 3)} K {K}", flush=True)
import os
ARMS = {"off": (False,), "on": (True,), "both": (False, True)}[os.environ.get("ARMS", "both")]
if os.environ.get("UNPLANTED"):
    sizes = []
    for _ in range(draws):
        A = rng.integers(0, q, (r, n)); key = W @ residues(A, vecs, h); t = rng.integers(0, q, r); u = rng.integers(0, q, r)
        LA, LB = vecs[key == W @ u], vecs[key == W @ ((t - u) % q)]
        pa, ma = bit(LA[:, :h]).sum(1), bit(LA[:, h:]).sum(1); pb, mb = bit(LB[:, :h]).sum(1), bit(LB[:, h:]).sum(1)
        PA, MA, PB, MB = pa[:, None], ma[:, None], pb[None, :], mb[None, :]; c1, c2 = PA & MB, MA & PB
        pc = np.vectorize(lambda v: bin(int(v)).count("1"))
        ia, ib = np.nonzero(((PA & PB) == 0) & ((MA & MB) == 0) & (pc(c1) == 1) & (pc(c2) == 1)); nn = c1[ia, ib] | c2[ia, ib]
        sizes.append(len(np.unique(((pa[ia] | pb[ib]) & ~nn) * (np.int64(1) << 32) + ((ma[ia] | mb[ib]) & ~nn))))
    print(f"unplanted, filter off: E|O| / E|V_t| = {np.mean(sizes) / (Npar / q ** r):.4f} +- {np.std(sizes) / np.sqrt(draws) / (Npar / q ** r):.4f}"
          f"  ({draws} draws)", flush=True)
if os.environ.get("UNPLANTED_ON"):                  # the same control with filters
    v = [run(True, planted=False)[0] for _ in range(draws)]
    print(f"unplanted, filter on (K={K}): E|O| / E|V_t| = {np.mean(v):.4f} +- {np.std(v) / np.sqrt(draws):.4f}  ({draws} draws)", flush=True)
    sys.exit(0)
for filt in ARMS:
    sig, hit = zip(*[run(filt) for _ in range(draws)])
    p = np.mean(hit); se = np.sqrt(p * (1 - p) / draws)
    print(f"filter {'on ' if filt else 'off'} (K={K if filt else 0}): mean sigma {np.mean(sig):.4f}   "
          f"planted survival {p:.4f} +- {se:.4f}   ({draws} draws)", flush=True)

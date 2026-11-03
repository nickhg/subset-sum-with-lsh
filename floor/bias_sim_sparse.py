"""wc handoff9 item 2 (optional): filter bias at a sparse bottom merge, shaped like the d=6 optimum's level-6 merge
(level 5 mostly 0 with rare 1s and -1s; level 6 rare 2s and -1s, from 1 -> (2,-1) and -1 -> (-1,0) splits).

Integer shape, n = 20:
  parent: four 1s and two -1s (exact type)        children A, B: two 2s and three -1s (exact type)
  valid pair: A's 2s sit on B's -1s and B's 2s on A's -1s (2 + -1 = 1); each child keeps one lone -1
  reps per parent R = C(4,2) * 2 = 12;  modulus M = 13 (prime), c = R/M = 12/13
Lists are complete cosets (L_A residue u, L_B residue r - u, r = <a,S> for a planted parent S).
Filter: labels {N,L,R}, codewords iid pi = (1/2, 1/4, 1/4).  A enters u iff both its 2s are L, two of its -1s are R
and one is N; B mirrored (2s R, two -1s L, one N).  Permutation invariant (depends on joint digit/label counts only).
A valid pair shares u iff u is L on A's 2s, R on B's 2s and N on the two lone -1s: p = (1/4)^4 (1/2)^2; K = 1/p.
Measured per draw: sigma = |output| / E[#parents with residue r] and whether S survives; filter off is the control.
usage: bias_sim_sparse.py [draws] [seed]
"""
import sys, itertools
from math import comb
import numpy as np

draws = int(sys.argv[1]) if len(sys.argv) > 1 else 100; seed = int(sys.argv[2]) if len(sys.argv) > 2 else 0
n = 20; R = comb(4, 2) * 2; Mod = 13                  # prime (even M makes 2a degenerate); c = 12/13
PI = np.array([0.5, 0.25, 0.25]); K = int(round(1 / (0.25 ** 4 * 0.5 ** 2)))
rng = np.random.default_rng(seed)

kids = np.array([t + m for t in itertools.combinations(range(n), 2)
                 for m in itertools.combinations([i for i in range(n) if i not in t], 3)], dtype=np.int64)  # (2 twos, 3 negs)
E_par = comb(n, 4) * comb(n - 4, 2) / Mod
bit = lambda idx: (np.int64(1) << idx)


def run(filt):
    a = rng.integers(0, Mod, n)
    perm = rng.permutation(n); S1, S2 = perm[:4], perm[4:6]                      # planted parent: ones, minus-ones
    r = (a[S1].sum() - a[S2].sum()) % Mod; u = rng.integers(0, Mod)
    res = (2 * a[kids[:, :2]].sum(1) - a[kids[:, 2:]].sum(1)) % Mod
    LA = kids[res == u]
    # every B with B's -1s = A's 2s + one fresh coord and B's 2s = two of A's -1s; lone A -1 = the third
    out = []
    for keep in range(3):
        b2 = np.delete(LA[:, 2:], keep, axis=1); loneA = LA[:, 2 + keep]
        occ = bit(LA).sum(1)
        for f in range(n):
            ok = (occ >> f) & 1 == 0
            if not ok.any():
                continue
            A, B2, la = LA[ok], b2[ok], loneA[ok]
            rb = (2 * a[B2].sum(1) - a[A[:, :2]].sum(1) - a[f]) % Mod
            m = rb == (r - u) % Mod
            out.append(np.column_stack([A[m, :2], B2[m], la[m], np.full(m.sum(), f)]))
    P = np.concatenate(out)                                                       # cols: A2(2), B2(2), loneA, loneB
    if filt:
        U = rng.choice(3, size=(K, n), p=PI)
        Lm, Rm, Nm = [np.where(U == s, bit(np.arange(n))[None, :], 0).sum(1) for s in (1, 2, 0)]
        need_L = bit(P[:, 0]) | bit(P[:, 1]); need_R = bit(P[:, 2]) | bit(P[:, 3]); need_N = bit(P[:, 4]) | bit(P[:, 5])
        keep = np.zeros(len(P), bool)
        for i in range(0, len(P), 4096):
            sl = slice(i, i + 4096)
            hit = ((Lm[None, :] & need_L[sl, None]) == need_L[sl, None]) & \
                  ((Rm[None, :] & need_R[sl, None]) == need_R[sl, None]) & \
                  ((Nm[None, :] & need_N[sl, None]) == need_N[sl, None])
            keep[sl] = hit.any(1)
        P = P[keep]
    ones = bit(P[:, :4]).sum(1); negs = bit(P[:, 4]) | bit(P[:, 5])
    key = ones * (np.int64(1) << 32) + negs
    O = np.unique(key)
    Sk = bit(S1).sum() * (np.int64(1) << 32) + bit(S2).sum()
    return len(O) / E_par, bool(np.isin(Sk, O))


for filt in (False, True):
    sig, hit = zip(*[run(filt) for _ in range(draws)])
    p = np.mean(hit); se = np.sqrt(p * (1 - p) / draws)
    print(f"filter {'on ' if filt else 'off'} (K={K if filt else 0}): mean sigma {np.mean(sig):.4f}   "
          f"planted survival {p:.4f} +- {se:.4f}   ({draws} draws, n={n}, M={Mod})", flush=True)

"""Survival by depth in a real HGJ tree ({0,1}, depth 3, weights n/2 -> n/4 -> n/8 -> n/16).

Instance: a_i uniform mod N, planted S of weight n/2, t = <a,S> mod N, with N = M_1 * q close to 2^n (density ~1).
Node constraints are nested: M_3 | M_2 | M_1 | N.  c at a split = R / M, where R = C(w_parent, w_parent/2)
(representations of a parent as two disjoint halves) and M = the children's modulus.
  leaves (level 3): all weight-w3 vectors with the node residue mod M_3 (complete, sigma = 1); c_leaf = R_3 / M_3
  internal: c_int = R_2 / M_2 = R_1 / M_1 (chosen in {1,2,3,4}; integer rounding reported)
sigma_v = |L_v| / E|V_v|, with E|V_v| = C(n, w_v) / M_v.
Poisson model: sigma_parent = 1 - exp(-c * sigma_A * sigma_B); success = 1 - exp(-c_root * sigma_1^2).
usage: survival.py n c_int [draws] [seed]
"""
import sys, itertools
from math import comb, exp
import numpy as np

n = int(sys.argv[1]); c_int = float(sys.argv[2])
draws = int(sys.argv[3]) if len(sys.argv) > 3 else 20; seed = int(sys.argv[4]) if len(sys.argv) > 4 else 0
assert n % 16 == 0 or n % 8 == 0
w = [n // 2, n // 4, n // 8, n // 16]                      # weights at levels 0..3
R = [None] + [comb(w[j - 1], w[j]) for j in (1, 2, 3)]       # reps of a level-(j-1) element
C_LEAF = 4.0
rng = np.random.default_rng(seed)

M3 = max(1, round(R[3] / C_LEAF))
M2 = M3 * max(1, round(R[2] / (c_int * M3)))
M1 = M2 * max(1, round(R[1] / (c_int * M2)))
q = max(1, round(min(2 ** n, 2 ** 56) / M1)); N = M1 * q        # n = 64: N capped at ~2^56 (int64 sums)
assert N < 2 ** 62 // (n // 2)
c_act = [None, R[1] / M1, R[2] / M2, R[3] / M3]
print(f"n={n} c_int={c_int}: weights {w}  M1={M1} M2={M2} M3={M3}  N~2^{np.log2(N):.2f}  "
      f"actual c (root, lvl1, lvl2) = {c_act[1]:.3f}, {c_act[2]:.3f}, {c_act[3]:.3f}", flush=True)

# all weight-w3 vectors (leaf universe), as bitmasks
combs = np.array(list(itertools.combinations(range(n), w[3])), dtype=np.int64)
leaf_masks = (np.int64(1) << combs).sum(1)


def merge(LA, LB, M, r, final=False):
    """pairs x in LA, y in LB with <a,x+y> = r mod M and disjoint; returns (unique union list, pairs examined)."""
    (ma, sa), (mb, sb) = LA, LB
    ka = sa % M; kb = (r - sb) % M
    order = np.argsort(kb, kind="stable"); kbs = kb[order]
    lo = np.searchsorted(kbs, ka, "left"); hi = np.searchsorted(kbs, ka, "right")
    cnt = hi - lo; tot = int(cnt.sum())
    if tot == 0:
        return (np.zeros(0, np.int64), np.zeros(0, np.int64)), 0
    ia = np.repeat(np.arange(len(ma)), cnt)
    off = np.arange(tot) - np.repeat(np.cumsum(cnt) - cnt, cnt)
    ib = order[np.repeat(lo, cnt) + off]
    ok = (ma[ia] & mb[ib]) == 0
    um = ma[ia[ok]] | mb[ib[ok]]; us = (sa[ia[ok]] + sb[ib[ok]]) % N
    um, idx = np.unique(um, return_index=True)
    return (um, us[idx]), tot


results = []
for dr in range(draws):
    a = rng.integers(0, N, n, dtype=np.int64)
    S = rng.choice(n, w[0], replace=False); Smask = int((np.int64(1) << S.astype(np.int64)).sum())
    t = int(a[S].sum() % N)
    leaf_sums = (a[combs].sum(1)) % N
    # residues: root target t mod N; level-1 children mod M1; level-2 mod M2; leaves mod M3
    r1A = int(rng.integers(0, M1)); r1 = [r1A, (t - r1A) % M1]
    r2 = []
    for x in r1:
        u = int(rng.integers(0, M2)); r2 += [u, (x - u) % M2]
    r3 = []
    for x in r2:
        u = int(rng.integers(0, M3)); r3 += [u, (x - u) % M3]
    leaves = []
    for x in r3:
        sel = leaf_sums % M3 == x
        leaves.append((leaf_masks[sel], leaf_sums[sel]))
    work = sum(len(L[0]) for L in leaves)
    lvl2 = []
    for i in range(4):
        L, wk = merge(leaves[2 * i], leaves[2 * i + 1], M2, r2[i]); lvl2.append(L); work += wk
    lvl1 = []
    for i in range(2):
        L, wk = merge(lvl2[2 * i], lvl2[2 * i + 1], M1, r1[i]); lvl1.append(L); work += wk
    top, wk = merge(lvl1[0], lvl1[1], N, t); work += wk
    sig3 = np.mean([len(L[0]) / (comb(n, w[3]) / M3) for L in leaves])
    sig2 = np.mean([len(L[0]) / (comb(n, w[2]) / M2) for L in lvl2])
    sig1 = np.mean([len(L[0]) / (comb(n, w[1]) / M1) for L in lvl1])
    foundS = bool(np.any(top[0] == Smask)); found_any = len(top[0]) > 0
    results.append((sig3, sig2, sig1, foundS, found_any, work))

r = np.array(results, dtype=float)
s3, s2, s1 = r[:, 0].mean(), r[:, 1].mean(), r[:, 2].mean()
p2 = 1 - exp(-c_act[3] * 1 * 1)                       # level-2 lists from complete leaves
p1 = 1 - exp(-c_act[2] * p2 * p2)
p0 = 1 - exp(-c_act[1] * p1 * p1)
print(f"  sigma leaf {s3:.3f} | level 2 {s2:.3f} (Poisson {p2:.3f}) | level 1 {s1:.3f} (Poisson {p1:.3f}) | "
      f"S found {r[:, 3].mean():.3f} (Poisson {p0:.3f}) any solution {r[:, 4].mean():.3f}", flush=True)
print(f"  work (log2, mean over draws): {np.log2(r[:, 5]).mean():.2f}   draws {draws}", flush=True)

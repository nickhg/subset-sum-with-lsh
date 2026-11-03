"""wc handoff3 item 2: joint survival of two planted siblings A*, B* (each built by its own filtered merge).

Same merge shape as bias_sim.py, scaled with n:
  children: one -1, k ones;  parent: one -1, 2k-1 ones (one (+1,-1) cancellation);  R = 2 (n-2k) C(2k-1, k-1)
  M = R / c (c = 2).  Child lists are complete cosets L_X = {x : <a,x> = u mod M}, L_Y = {y : <a,y> = r - u}, so a
  planted parent P survives the unfiltered merge iff one of its reps (X, P - X) has <a,X> = u mod M, and survives the
  filtered merge iff such a consistent rep also shares a codeword bucket (rule as in bias_sim.py, integer-rounded).
  Lists never need to be built: survival is decided by P's own reps.
Siblings: A*, B* have disjoint supports (as two halves of a grandparent), share the instance a, and have independent
residues u_A, u_B (independent per-node randomness, as in the tree).  Codes: independent per node, or one shared code.
Reports P(A*), P(B*), P(both) and  log2 P(both) - log2 P(A*) - log2 P(B*)  per n.
usage: sibling_sim.py n k [draws] [seed]
"""
import sys, itertools
from math import comb
import numpy as np

n = int(sys.argv[1]); k = int(sys.argv[2]); draws = int(sys.argv[3]) if len(sys.argv) > 3 else 2000
seed = int(sys.argv[4]) if len(sys.argv) > 4 else 0
rng = np.random.default_rng(seed)
R = 2 * (n - 2 * k) * comb(2 * k - 1, k - 1); Mod = R // 2
PI = np.array([0.6566, 0.1717, 0.1717]); N_, L_, R_ = 0, 1, 2


def rounded(p, m):
    c = np.floor(np.array(p) * m).astype(int); r = np.array(p) * m - c
    for i in np.argsort(-r)[:m - c.sum()]:
        c[i] += 1
    return c


TA = rounded([0.5867, 0.3809, 0.0324], k)               # (N, L, R) counts on X's +1 coords
TB = TA[[0, 2, 1]]                                       # mirrored for Y
subs = np.array(list(itertools.combinations(range(2 * k - 1), k - 1)))
rest = np.array([[i for i in range(2 * k - 1) if i not in set(s)] for s in subs])


def reps(ones, m, zeros):
    """all reps of a parent as arrays: X plus coords (k), X minus, Y plus coords (k), Y minus."""
    Z = len(zeros); S = len(subs)
    zz = np.repeat(zeros, S); so = np.tile(np.arange(S), Z)
    # class 1: X = parent -1 + (k-1 parent ones) + cancel +1 at z ; Y = k parent ones, -1 at z
    x1 = np.concatenate([ones[subs[so]], zz[:, None]], 1); y1 = ones[rest[so]]
    # class 2: Y = parent -1 + (k-1 ones) + cancel +1 ; X = k parent ones, -1 at z
    y2 = np.concatenate([ones[subs[so]], zz[:, None]], 1); x2 = ones[rest[so]]
    Xp = np.concatenate([x1, x2]); Yp = np.concatenate([y1, y2])
    Xm = np.concatenate([np.full(Z * S, m), zz]); Ym = np.concatenate([zz, np.full(Z * S, m)])
    return Xp, Xm, Yp, Ym


def member(lab, plus, minus, T, mlab):
    lp = lab[:, plus]                                    # (K, r, k)
    return ((lp == N_).sum(2) == T[0]) & ((lp == L_).sum(2) == T[1]) & ((lp == R_).sum(2) == T[2]) \
        & (lab[:, minus] == mlab)


def survives(a, u, rp, lab):
    Xp, Xm, Yp, Ym = rp
    sx = (a[Xp].sum(1) - a[Xm]) % Mod
    cons = np.nonzero(sx == u)[0]
    if len(cons) == 0:
        return False, False
    if lab is None:
        return True, True
    inX = member(lab, Xp[cons], Xm[cons], TA, R_); inY = member(lab, Yp[cons], Ym[cons], TB, L_)
    return True, bool((inX & inY).any())


def random_siblings():
    perm = rng.permutation(n)
    A = (np.sort(perm[:2 * k - 1]), perm[2 * k - 1]); B = (np.sort(perm[2 * k:4 * k - 1]), perm[4 * k - 1])
    out = []
    for ones, m in (A, B):
        zeros = np.array([i for i in range(n) if i not in set(ones) and i != m])
        out.append(reps(ones, m, zeros))
    return out


# calibrate p_pair on all reps of one random parent
calib = rng.choice(3, size=(4000, n), p=PI).astype(np.int8)
rp = random_siblings()[0]; sel = rng.choice(len(rp[0]), min(400, len(rp[0])), replace=False)
pp = (member(calib, rp[0][sel], rp[1][sel], TA, R_) & member(calib, rp[2][sel], rp[3][sel], TB, L_)).mean()
K = max(1, int(round(1 / pp)))
print(f"n={n} k={k} R={R} M={Mod} targets A{TA.tolist()} B{TB.tolist()} p_pair={pp:.3e} K={K}", flush=True)

res = {"off": [], "indep": [], "shared": []}
for dr in range(draws):
    a = rng.integers(0, 2 ** 40, n, dtype=np.int64)
    (rA, rB) = random_siblings(); uA, uB = int(rng.integers(0, Mod)), int(rng.integers(0, Mod))
    labA = rng.choice(3, size=(K, n), p=PI).astype(np.int8); labB = rng.choice(3, size=(K, n), p=PI).astype(np.int8)
    offA, indA = survives(a, uA, rA, labA); offB, indB = survives(a, uB, rB, labB)
    _, shB = survives(a, uB, rB, labA)
    res["off"].append((offA, offB)); res["indep"].append((indA, indB)); res["shared"].append((indA, shB))

print(f"RESULT n={n} k={k} draws={draws}")
for key, v in res.items():
    v = np.array(v, float); pa, pb, pab = v[:, 0].mean(), v[:, 1].mean(), (v[:, 0] * v[:, 1]).mean()
    se = np.sqrt(pab * (1 - pab) / len(v)) / max(pab, 1e-9) / np.log(2)
    print(f"  {key:6s}: P(A*) {pa:.4f} P(B*) {pb:.4f} P(both) {pab:.4f}  log2 P(both) - log2 P(A) - log2 P(B) = "
          f"{np.log2(pab / (pa * pb)):+.4f} (+- {se:.4f})", flush=True)

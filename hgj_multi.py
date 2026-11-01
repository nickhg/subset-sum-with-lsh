"""Depth-k HGJ with a shared-block coordinate split at EVERY level.

Each vector carries a profile: list of regions (size R, weight W) as fractions of n.
Splitting a parent with shared fraction c (applied inside every parent region):
  shared part   (c R)       : parent has weight c W there, each child takes c W / 2
  private part  ((1-c) R/2) : child takes all of the parent's (1-c) W / 2 there
  reps   = sum c W              (only shared ones can be split freely)
  overlap only possible in shared parts.
c_j = 1 for all j recovers plain HGJ.  Root solution: weight 1/2 on R = 1.
Merge at level j (building level j-1 from level j): output o_j = 2H_j - l_j - l_{j-1}.
Base lists: meet-in-the-middle over position halves, cost H_k / 2.
"""
import itertools
import numpy as np
from scipy.optimize import linprog, minimize
from math import log2


def h(x):
    return 0.0 if x <= 0 or x >= 1 else -x * log2(x) - (1 - x) * log2(1 - x)


def ent(R, W):
    return 0.0 if R <= 1e-15 else R * h(W / R)


def logp(R, a, b):
    return 0.0 if R <= 1e-15 or a <= 0 or b <= 0 else ent(R - a, b) - ent(R, b)


def levels(cs):
    prof = [(1.0, 0.5)]
    H, rho, p = [None], [None], [None]
    for c in cs:
        child, r, lp = [], 0.0, 0.0
        for R, W in prof:
            if c > 0:
                child.append((c * R, c * W / 2)); r += c * W
                lp += logp(c * R, c * W / 2, c * W / 2)
            if c < 1:
                child.append(((1 - c) * R / 2, (1 - c) * W / 2))
        prof = child
        H.append(sum(ent(R, W) for R, W in prof)); rho.append(r); p.append(lp)
    return H, rho, p


def lp_solve(cs, oracle=False):
    k = len(cs)
    H, rho, p = levels(cs)
    nv = k + 1; T = k
    A, b = [], []

    def row(d, rhs):
        v = np.zeros(nv)
        for i, x in d:
            v[i] += x
        A.append(v); b.append(rhs)
    for j in range(1, k + 1):
        if j >= 2:
            row([(j - 1, 1), (j - 2, -1)], 0)
        row([(j - 1, 1)], rho[j])
        row([(j - 1, -1), (T, -1)], -H[j])
        d = [(j - 1, -1), (T, -1)]
        rhs = -(2 * H[j] + (p[j] if oracle else 0))
        if j == 1:
            rhs += 1.0
        else:
            d.append((j - 2, -1))
        row(d, rhs)
    row([(T, -1)], -0.5 * H[k])
    res = linprog(np.eye(nv)[T], A_ub=np.array(A), b_ub=np.array(b),
                  bounds=[(0, 1)] * nv, method="highs")
    return res.fun if res.status == 0 else 9.0, (res.x if res.status == 0 else None)


def best(k, grid=21):
    g = np.linspace(0.3, 1.0, grid)
    top = min((lp_solve(list(cs))[0], cs) for cs in itertools.product(g, repeat=k))
    f = lambda v: lp_solve(list(np.clip(v, 0.05, 1.0)))[0]
    r = minimize(f, np.array(top[1]), method="Nelder-Mead",
                 options=dict(xatol=1e-5, fatol=1e-7, maxiter=4000))
    cs = list(np.clip(r.x, 0.05, 1.0))
    return lp_solve(cs)[0], cs


if __name__ == "__main__":
    for k, grid in [(2, 41), (3, 21), (4, 11), (5, 7)]:
        T, cs = best(k, grid)
        print(f"depth {k}: plain HGJ {lp_solve([1.0]*k)[0]:.4f} -> shared splits {T:.4f}   c = {np.round(cs,3)}")

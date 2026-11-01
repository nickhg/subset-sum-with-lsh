"""HGJ (depth 3) with a shared-block coordinate split at the level-1 -> level-2 split.

Level-1 vectors y: weight 1/4 on all coordinates (as in HGJ).
Split y -> (x1, x2) using a random coordinate partition: shared block C (fraction c),
left-only Lo and right-only Ro (each (1-c)/2). x1 = (y on Lo) + half of (y on C), etc.
So level-2 vectors have weight (1-c)/8 on a (1-c)/2 region and c/8 on the c region.
Overlap of a left/right level-2 pair is only possible inside C.
Level-3: HGJ-style halving of weight inside each region separately.
c = 1 recovers plain HGJ.  All quantities are exponents / n.
"""
import numpy as np
from scipy.optimize import linprog
from math import log2


def h(x):
    return 0.0 if x <= 0 or x >= 1 else -x * log2(x) - (1 - x) * log2(1 - x)


def ent(region, weight):          # log C(region*n, weight*n)/n
    return 0.0 if region <= 0 else region * h(weight / region)


def logp(region, wa, wb):          # log Pr[two random sets of sizes wa,wb in region are disjoint]
    if region <= 0 or wa <= 0 or wb <= 0:
        return 0.0
    return ent(region - wa, wb) - ent(region, wb)


def model(c):
    r = (1 - c) / 2
    # unconstrained list entropies
    H1 = h(0.25)
    H2 = ent(r, (1 - c) / 8) + ent(c, c / 8)
    H3 = ent(r, (1 - c) / 16) + ent(c, c / 16)
    rho1 = 0.5                                   # reps of e (weight 1/2) into two weight-1/4
    rho2 = ent(c / 4, c / 8)                     # only the shared block's ones can be split
    rho3 = ent((1 - c) / 8, (1 - c) / 16) + ent(c / 8, c / 16)
    p1 = logp(1.0, 0.25, 0.25)
    p2 = logp(c, c / 8, c / 8)
    p3 = logp(r, (1 - c) / 16, (1 - c) / 16) + logp(c, c / 16, c / 16)
    return dict(H=[None, H1, H2, H3], rho=[None, rho1, rho2, rho3], p=[None, p1, p2, p3])


def solve(c, oracle=False):
    m = model(c)
    H, rho, p = m["H"], m["rho"], m["p"]
    # vars l1,l2,l3,T
    A, b = [], []

    def row(d, rhs):
        v = np.zeros(4)
        for i, x in d:
            v[i] += x
        A.append(v); b.append(rhs)

    row([(1, 1), (0, -1)], 0); row([(2, 1), (1, -1)], 0)          # nesting
    for j in (1, 2, 3):
        row([(j - 1, 1)], rho[j])                                 # reps
        row([(j - 1, -1), (3, -1)], -H[j])                        # list size
        extra = p[j] if oracle else 0.0
        # merge output o_j = 2(H_j - l_j) - (l_{j-1} - l_j) = 2H_j - l_j - l_{j-1}
        d = [(j - 1, -1), (3, -1)]
        rhs = -(2 * H[j] + extra)
        if j == 1:
            rhs += 1.0
        else:
            d.append((j - 2, -1))
        row(d, rhs)
    row([(3, -1)], -0.5 * H[3])                                   # base MITM
    res = linprog([0, 0, 0, 1], A_ub=np.array(A), b_ub=np.array(b),
                  bounds=[(0, 1)] * 4, method="highs")
    return res.fun, res.x[:3]


if __name__ == "__main__":
    best = min((solve(c)[0], c) for c in np.linspace(0, 1, 1001))
    print("plain HGJ (c=1):", round(solve(1.0)[0], 4))
    print("best shared-block split: T=%.4f at c=%.3f" % best, "l =", np.round(solve(best[1])[1], 4))
    for c in [1.0, 0.95, 0.9, 0.85, 0.8, 0.7, 0.5]:
        print(f"  c={c:.2f}: T={solve(c)[0]:.4f}")

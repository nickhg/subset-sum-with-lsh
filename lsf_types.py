"""Optimal product (type-class) asymmetric filters for the HGJ disjoint-pair merge.

A table = i.i.d. labels lambda_i ~ pi on a finite label set.  Left x passes iff the joint
empirical type of (lambda, x) equals Q_{lambda x}; right y iff type of (lambda, y) equals
Q_{lambda y}.  Q is a "planted" law on (lambda, x, y) with (x,y)-marginal = tau0, the
coordinate type of a disjoint pair of weight-w vectors.  By Sanov:

  r1   = KL(Q_{lambda|x} || pi) averaged over x ~ tau_x         (left pass rate)
  r12  = KL(Q || pi (x) tau0)                                    (disjoint pair)
  r(k) = min KL(Q' || pi (x) tau_k) over Q' with Q'_{lambda x} = Q_{lambda x},
         Q'_{lambda y} = Q_{lambda y}, Q'_{xy} = tau_k            (pair with overlap k n)
         computed exactly by iterative proportional fitting (I-projection).

cost = max( N + r12 - r1 , N + r12 - r2 ,
            max_k [ M + log Pr(overlap = k) - r(k) + r12 ] , 0.3113 )
"""
import numpy as np
from math import log2
from scipy.optimize import minimize

W = 1 / 8
N_EXP, M_EXP, GOAL = 0.29361, 0.33712, 0.31128
XY = [(0, 0), (1, 0), (0, 1), (1, 1)]


def h(x):
    return 0.0 if x <= 0 or x >= 1 else -x * log2(x) - (1 - x) * log2(1 - x)


def ent(R, Wt):
    return 0.0 if R <= 0 else R * h(Wt / R)


def tau(k):  # coordinate type of a pair of weight-W vectors with overlap k
    return np.array([1 - 2 * W + k, W - k, W - k, k])


def log_overlap_frac(k):  # log2 Pr[overlap = k n] for random pair
    return ent(W, k) + ent(1 - W, W - k) - h(W)


def kl(P, Qm):
    m = P > 1e-300
    return float(np.sum(P[m] * np.log2(P[m] / Qm[m])))


def ipf(pi, t, A_lx, A_ly, iters=3000):
    """I-projection of pi(x)t onto {lambda-x marginal A_lx, lambda-y marginal A_ly, xy marginal t}.
    Arrays indexed [lambda, x, y]."""
    m = len(pi)
    P = np.zeros((m, 2, 2))
    for j, (x, y) in enumerate(XY):
        P[:, x, y] = pi * t[j]
    for _ in range(iters):
        s = P.sum(axis=2); P *= np.where(s > 0, A_lx / np.maximum(s, 1e-300), 0)[:, :, None]
        s = P.sum(axis=1); P *= np.where(s > 0, A_ly / np.maximum(s, 1e-300), 0)[:, None, :]
        s = P.sum(axis=0)
        tt = np.array([[t[0], t[2]], [t[1], t[3]]])
        P *= np.where(s > 0, tt / np.maximum(s, 1e-300), 0)[None, :, :]
    err = (np.abs(P.sum(2) - A_lx).max() + np.abs(P.sum(1) - A_ly).max())
    ref = np.zeros_like(P)
    for j, (x, y) in enumerate(XY):
        ref[:, x, y] = pi * t[j]
    return (kl(P.ravel(), ref.ravel()) if err < 1e-7 else np.inf), err


def unpack(z, m):
    pi = np.exp(z[:m]); pi /= pi.sum()
    # Q(lambda | xy) for the three disjoint types 00, 10, 01
    cond = []
    for j in range(3):
        c = np.exp(z[m + j * m: m + (j + 1) * m]); cond.append(c / c.sum())
    return pi, cond


def evaluate(z, m, ks=None, detail=False):
    pi, cond = unpack(z, m)
    t0 = tau(0)
    Q = np.zeros((m, 2, 2))
    for j, (x, y) in enumerate(XY[:3]):
        Q[:, x, y] = cond[j] * t0[j]
    A_lx, A_ly = Q.sum(2), Q.sum(1)
    ref0 = np.zeros_like(Q)
    for j, (x, y) in enumerate(XY):
        ref0[:, x, y] = pi * t0[j]
    r12 = kl(Q.ravel(), ref0.ravel())
    r1 = sum(A_lx[:, x].sum() * kl(A_lx[:, x] / A_lx[:, x].sum(), pi) for x in (0, 1))
    r2 = sum(A_ly[:, y].sum() * kl(A_ly[:, y] / A_ly[:, y].sum(), pi) for y in (0, 1))
    if ks is None:
        ks = np.linspace(0.0005, W * W * 1.6, 14)
    waste = -np.inf; wk = None
    for k in ks:
        rk, _ = ipf(pi, tau(k), A_lx, A_ly, iters=150)
        val = M_EXP + log_overlap_frac(k) - rk + r12
        if val > waste:
            waste, wk = val, k
    terms = dict(left=N_EXP + r12 - r1, right=N_EXP + r12 - r2, waste=waste, useful=GOAL)
    if detail:
        return max(terms.values()), terms, wk, (pi, cond)
    return max(terms.values())


if __name__ == "__main__":
    rng = np.random.default_rng(1)
    for m in (2, 3, 4):
        best = (9, None)
        for trial in range(40):
            z0 = rng.normal(0, 1.5, m + 3 * m)
            r = minimize(lambda z: evaluate(z, m), z0, method="Nelder-Mead",
                         options=dict(maxiter=3000, xatol=1e-6, fatol=1e-8))
            if r.fun < best[0]:
                best = (r.fun, r.x)
        r = minimize(lambda z: evaluate(z, m), best[1], method="Nelder-Mead",
                     options=dict(maxiter=8000, xatol=1e-8, fatol=1e-10))
        c, terms, wk, (pi, cond) = evaluate(r.x, m, ks=np.linspace(0.0002, W * W * 1.8, 40), detail=True)
        print(f"labels={m}: cost {c:.5f}  terms { {k: round(v,5) for k,v in terms.items()} }  worst overlap k={wk:.4f}")
        print("   pi", np.round(pi, 3), " Q(l|00)", np.round(cond[0], 3), " Q(l|10)", np.round(cond[1], 3), " Q(l|01)", np.round(cond[2], 3))

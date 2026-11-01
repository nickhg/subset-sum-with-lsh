"""Does a K-label filter beat the 3-label one at the best {-1,0,1,2} point?  (cheap optimality probe)

Digit parameters fixed at runs/bbss2_f_1.npy; only the filters are re-optimised, with K labels per merge.
pi cancels (see paper, Remark after Prop. cost), so only the conditional label laws cond[t] matter; they are
parametrised by softmax, mirror-symmetric under (x,y) -> (y,x).  The 3-label optimum is embedded as a start.
usage: lsf_klabel_check.py K [restarts]
"""
import sys
import numpy as np
from scipy.optimize import minimize
import bbss_lsf as B

K = int(sys.argv[1]); restarts = int(sys.argv[2]) if len(sys.argv) > 2 else 4
rng = np.random.default_rng(0)
z = np.load("runs/bbss2_f_1.npy"); k = 3
params = [tuple(r) for r in z[:9].reshape(3, 3)]
fl3 = [z[9 + B.NPAR * j: 9 + B.NPAR * (j + 1)] for j in range(k)]
lev = B.tree(params)
SYM, ASY = B.SYM, B.ASY
NP = B.NT * (K - 1)          # every pair type gets its own label law (most general kappa)


def cond_from(v):
    cond = np.zeros((B.NT, K))
    for t in range(B.NT):
        cond[t] = B.sm(np.concatenate([v[t * (K - 1):(t + 1) * (K - 1)], [0.0]]))
    return cond


def terms(L, cond):
    """Invariant form with pi = Q_Lambda: (I_XY - I_X, I_XY - I_Y, I_XY - I_X - I_Y)."""
    tau = L["tau"]; Q = tau[:, None] * cond; Ql = Q.sum(0)
    IXY = sum(tau[t] * B.kl(cond[t], Ql) for t in range(B.NT) if tau[t] > 0)
    A = np.zeros((K, 4)); Bm = np.zeros((K, 4))
    for t, (x, y) in enumerate(B.TYPES):
        A[:, B.D.index(x)] += Q[t]; Bm[:, B.D.index(y)] += Q[t]
    def mi(M):
        px = M.sum(0); r = 0.0
        for d in range(4):
            if px[d] > 1e-300:
                r += px[d] * B.kl(M[:, d] / px[d], Ql)
        return r
    IX, IY = mi(A), mi(Bm)
    return IXY - IX, IXY - IY, IXY - IX - IY


def T_of(vs):
    conds = [cond_from(v) for v in vs]
    def ft(L, j):
        e1, e2, ex = terms(L, conds[j])
        return 0.0, -e1, -e2, ex                       # lp2 uses r12-r1, r12-r2, extra
    orig = B.filter_terms; B.filter_terms = ft
    try:
        return B.lp2(params, list(range(k)))[0]
    finally:
        B.filter_terms = orig


T3 = B.lp2(params, fl3)[0]
print(f"3-label filters (saved point): T = {T3:.6f}")


def embed3(f):
    """3-label cond laws -> K-label parameters (reference = old label 2; extra labels get logit -20)."""
    _, cond = B.filt(f); v = []
    for t in range(B.NT):
        lg = np.log(np.maximum(cond[t], 1e-300)); lg = lg - lg[2]
        v += [lg[0], lg[1]] + [-20.0] * (K - 3)
    return np.array(v)


best = None
starts = [[embed3(f) for f in fl3]] + [[rng.normal(0, 1.5, NP) for _ in range(k)] for _ in range(restarts)]
for s in starts:
    x0 = np.concatenate(s)
    f = lambda x: T_of([x[j * NP:(j + 1) * NP] for j in range(k)])
    r = minimize(f, x0, method="Powell", options=dict(maxiter=20000, xtol=1e-7, ftol=1e-11))
    r = minimize(f, r.x, method="Nelder-Mead", options=dict(maxiter=8000, xatol=1e-8, fatol=1e-12))
    print(f"  start T = {f(x0):.6f}  ->  {r.fun:.6f}", flush=True)
    if best is None or r.fun < best:
        best = r.fun
print(f"K = {K}: best T = {best:.6f}   (3-label: {T3:.6f})")

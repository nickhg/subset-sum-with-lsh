"""BCJ (digit set {-1,0,1}) representation tree, with optional type-class LSF at each merge.

Exponents are /n, logs base 2.  Heuristics: list entries behave like random vectors of
their type, residues independent of supports, weights concentrate.

Tree: level 0 = solution (1/2 ones).  A level-(j-1) vector with fractions (P ones,
M minus-ones, Z zeros) splits into two level-j vectors using eps_j:
   parent 1  -> (1,0) or (0,1)          parent -1 -> (-1,0) or (0,-1)
   parent 0  -> (0,0), (1,-1), (-1,1)   [eps_j each for the last two]
 child type: p_j = P/2 + eps_j ones, m_j = M/2 + eps_j minus-ones
 reps       rho_j = P + M + Z*H3(eps/Z, eps/Z)
 lists      s_j = H3(p_j, m_j) - l_j      merge out  o_j = 2 H_j - l_j - l_{j-1}
 base       Schroeppel-Shamir / MITM over position halves: H_k / 2

LSF at merge j (labels N,L,R, mirror-symmetric): planted law Q(lambda | xy) on the
valid pair type tau*.  With A = Q_{lambda x}, B = Q_{lambda y}:
   r12 = sum tau*(xy) KL(Q(.|xy) || pi)        r1 = sum A_x KL(A(.|x) || pi)  (r2 mirror)
   entries   = s_j + r12 - r1  (and r2)
   passing   = o_j + r12 + H(A) + H(B) - H(Q_lambda) - CE(Q_lambda, pi) - 2 H_j
 'passing' is the exact worst case over all pair types: max_tau [log frac(tau) - r(tau)]
 is a max-entropy problem with fixed (lambda,x),(lambda,y) marginals, solved by
 conditional independence of x,y given lambda.
 merge cost = max(entries_L, entries_R, passing)   (trivial filter gives max(s_j, o_j)).
"""
import numpy as np
from math import log2
from scipy.optimize import linprog, minimize

TYPES = [(0, 0), (1, 0), (0, 1), (-1, 0), (0, -1), (1, -1), (-1, 1)]
MIRROR = [0, 2, 1, 4, 3, 6, 5]
DIG = [-1, 0, 1]


def Hv(v):
    v = np.asarray(v, float); v = v[v > 1e-300]
    return float(-(v * np.log2(v)).sum())


def H3(a, b):
    return Hv([a, b, 1 - a - b])


def tree(eps):
    P, M = 0.5, 0.0
    lev = [None]
    for e in eps:
        Z = 1 - P - M
        if e < 0 or 2 * e > Z:
            return None
        p, m = P / 2 + e, M / 2 + e
        rho = P + M + (Z * Hv([e / Z, e / Z, 1 - 2 * e / Z]) if Z > 0 else 0)
        tau = np.array([Z - 2 * e, P / 2, P / 2, M / 2, M / 2, e, e])
        lev.append(dict(p=p, m=m, H=H3(p, m), rho=rho, tau=tau, Hpar=H3(P, M)))
        P, M = p, m
    return lev


def sm(v):
    v = np.asarray(v, float); e = np.exp(v - v.max()); return e / e.sum()


def filt(z):
    """z (8 params) -> pi (3,), cond (7,3) over labels N,L,R."""
    pi = sm([z[0], 0.0, 0.0])
    cond = np.zeros((7, 3))
    cond[0] = sm([z[1], 0.0, 0.0])
    cond[1] = sm([z[2], z[3], 0.0]); cond[2] = cond[1][[0, 2, 1]]
    cond[3] = sm([z[4], z[5], 0.0]); cond[4] = cond[3][[0, 2, 1]]
    cond[5] = sm([z[6], z[7], 0.0]); cond[6] = cond[5][[0, 2, 1]]
    return pi, cond


def kl(p, q):
    m = p > 1e-300
    return float((p[m] * np.log2(p[m] / q[m])).sum())


def filter_terms(L, z):
    """Return (r12, r1, r2, extra) where passing = o_j + extra."""
    pi, cond = filt(z)
    tau = L["tau"]
    Q = tau[:, None] * cond                      # (7 types, 3 labels)
    r12 = sum(tau[t] * kl(cond[t], pi) for t in range(7) if tau[t] > 0)
    A = np.zeros((3, 3)); B = np.zeros((3, 3))   # [label, digit]
    for t, (x, y) in enumerate(TYPES):
        A[:, DIG.index(x)] += Q[t]; B[:, DIG.index(y)] += Q[t]
    def rate(Mg):
        r = 0.0
        for d in range(3):
            s = Mg[:, d].sum()
            if s > 1e-300:
                r += s * kl(Mg[:, d] / s, pi)
        return r
    r1, r2 = rate(A), rate(B)
    Ql = Q.sum(0)
    ce = float(-(Ql * np.log2(pi)).sum())
    extra = r12 + Hv(A.ravel()) + Hv(B.ravel()) - Hv(Ql) - ce - 2 * L["H"]
    return r12, r1, r2, extra


def lp(eps, filters=None):
    """Minimise T over l_j for fixed eps and filters (None = no filter)."""
    lev = tree(eps)
    if lev is None:
        return 9.0, None
    k = len(eps); nv = k + 1; T = k
    A, b = [], []
    def row(d, rhs):
        v = np.zeros(nv)
        for i, x in d: v[i] += x
        A.append(v); b.append(rhs)
    for j in range(1, k + 1):
        L = lev[j]
        if j >= 2: row([(j - 1, 1), (j - 2, -1)], 0)
        row([(j - 1, 1)], L["rho"])
        row([(j - 1, -1), (T, -1)], -L["H"])                       # list size
        # o_j = 2H - l_j - l_{j-1};  merge cost terms linear in l
        def merge_row(const, coef_lj, coef_ljm1):
            d = [(j - 1, coef_lj), (T, -1)]; rhs = -const
            if j == 1: rhs -= coef_ljm1 * 1.0
            else: d.append((j - 2, coef_ljm1))
            row(d, rhs)
        if filters is None or filters[j - 1] is None:
            merge_row(2 * L["H"], -1, -1)                          # T >= o_j
        else:
            r12, r1, r2, extra = filter_terms(L, filters[j - 1])
            merge_row(L["H"] + r12 - r1, -1, 0)                    # entries_L (s_j + r12 - r1)
            merge_row(L["H"] + r12 - r2, -1, 0)
            merge_row(2 * L["H"] + extra, -1, -1)                  # passing
    row([(T, -1)], -0.5 * lev[k]["H"])
    bb = np.array(b)
    if not np.all(np.isfinite(bb)):
        return 9.0, None
    res = linprog(np.eye(nv)[T], A_ub=np.array(A), b_ub=bb,
                  bounds=[(0, 1)] * nv, method="highs")
    return (res.fun, res.x) if res.status == 0 else (9.0, None)


def opt_eps(k, filters=None, starts=None, minus=True):
    rng = np.random.default_rng(0)
    if not minus:
        return lp([0.0] * k, filters)[0], [0.0] * k
    best = (9.0, None)
    starts = starts or [list(rng.uniform(0, 0.04, k)) for _ in range(12)] + [[0.027, 0.017, 0.003][:k]]
    for s in starts:
        r = minimize(lambda e: lp(list(np.abs(e)), filters)[0], np.array(s), method="Nelder-Mead",
                     options=dict(xatol=1e-7, fatol=1e-9, maxiter=4000))
        if r.fun < best[0]:
            best = (r.fun, list(np.abs(r.x)))
    return best


def opt_filters(eps, filters, rng, rounds=1):
    """Improve each level's filter (others fixed) to lower the LP optimum."""
    k = len(eps)
    filters = list(filters)
    for _ in range(rounds):
        for j in range(k):
            def f(z):
                fl = list(filters); fl[j] = z
                return lp(eps, fl)[0]
            cands = [filters[j]] if filters[j] is not None else []
            cands += [rng.normal(0, 1.5, 8) for _ in range(6)]
            best = (lp(eps, filters)[0], filters[j])
            for c0 in cands:
                r = minimize(f, np.array(c0), method="Nelder-Mead",
                             options=dict(xatol=1e-7, fatol=1e-10, maxiter=3000))
                if r.fun < best[0] - 1e-9:
                    best = (r.fun, r.x)
            filters[j] = best[1]
    return filters


def run(k, minus=True, iters=4, seed=0):
    rng = np.random.default_rng(seed)
    T0, eps = opt_eps(k, None, minus=minus)
    filters = [rng.normal(0, 0.1, 8) for _ in range(k)]
    T = T0
    for it in range(iters):
        filters = opt_filters(eps, filters, rng)
        T, eps = opt_eps(k, filters, starts=[eps], minus=minus)
    return T0, T, eps, filters


if __name__ == "__main__":
    import sys
    k = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    T0, T, eps, filters = run(2, minus=False)
    print(f"HGJ  depth 2: plain {T0:.5f}  with LSF {T:.5f}   (check vs IPF model: 0.32694)", flush=True)
    for kk in (3, k) if k != 3 else (3,):
        T0, T, eps, filters = run(kk, minus=True)
        print(f"BCJ  depth {kk}: plain {T0:.5f}  with LSF {T:.5f}   eps={np.round(eps,4)}", flush=True)
        T1, x = lp(eps, filters)
        lev = tree(eps); L = [1.0] + list(x[:kk])
        for j in range(1, kk + 1):
            Lv = lev[j]; o = 2 * Lv["H"] - L[j] - L[j - 1]
            r12, r1, r2, extra = filter_terms(Lv, filters[j - 1])
            useful = o + Lv["Hpar"] + Lv["rho"] - 2 * Lv["H"]
            print(f"   level {j}: list {Lv['H']-L[j]:.4f} merge_out {o:.4f} useful {useful:.4f} "
                  f"LSF entries {Lv['H']-L[j]+r12-min(r1,r2):.4f} passing {o+extra:.4f}", flush=True)
        print("   base", round(0.5 * lev[kk]["H"], 4), flush=True)

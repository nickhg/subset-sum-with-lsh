"""Representation tree over the digit set D = {-1,0,1,2} (BBSS-style), with optional
type-class LSF at each merge.  Exponents /n, logs base 2, usual random-list heuristics.

A parent digit d splits into an ordered pair (x,y) in D^2 with x+y = d:
  d=-1: (-1,0),(0,-1)                    [half each]
  d= 0: (0,0), (1,-1),(-1,1)             [e each for the last two]
  d= 1: (1,0),(0,1), (2,-1),(-1,2)       [f each for the last two]
  d= 2: (2,0),(0,2), (1,1)               [g for (1,1)]
(e,f,g are fractions of n.)  sigma_j = joint split law, child type = its marginal,
  reps  rho_j = H(sigma_j) - H(parent type)     (parent is a function of the pair)
  list  s_j = H(child) - l_j,  merge out o_j = 2 H_j - l_j - l_{j-1},  base H_k / 2.
LSF terms as in bcj_lsf.py (closed-form worst case over pair types).
Setting f = g = 0 recovers BCJ; additionally e = 0 recovers HGJ.
"""
import numpy as np
from scipy.optimize import linprog, minimize

D = [-1, 0, 1, 2]
TYPES = [(0, 0), (1, 1),                      # symmetric
         (1, 0), (-1, 0), (1, -1), (2, -1), (2, 0),
         (0, 1), (0, -1), (-1, 1), (-1, 2), (0, 2)]
MIR = {t: TYPES.index((t[1], t[0])) for t in TYPES}
NT = len(TYPES)


def Hv(v):
    v = np.asarray(v, float); v = v[v > 1e-300]
    return float(-(v * np.log2(v)).sum())


def split(par, e, f, g):
    """par: dict digit->mass. Returns sigma (len NT) or None if infeasible."""
    s = np.zeros(NT)
    def add(t, w): s[TYPES.index(t)] += w
    pm1, p0, p1, p2 = (par.get(d, 0.0) for d in D)
    if min(e, f, g) < 0 or 2 * e > p0 + 1e-15 or 2 * f > p1 + 1e-15 or g > p2 + 1e-15:
        return None
    add((-1, 0), pm1 / 2); add((0, -1), pm1 / 2)
    add((0, 0), p0 - 2 * e); add((1, -1), e); add((-1, 1), e)
    add((1, 0), (p1 - 2 * f) / 2); add((0, 1), (p1 - 2 * f) / 2); add((2, -1), f); add((-1, 2), f)
    add((1, 1), g); add((2, 0), (p2 - g) / 2); add((0, 2), (p2 - g) / 2)
    return s


def sg(x):
    return 1.0 / (1.0 + np.exp(-x))


def tree(params, raw=True):
    """params: per level (a,b,c); raw=True maps them through sigmoids to feasible
    fractions e = p0/2*sg(a), f = p1/2*sg(b), g = p2*sg(c).  raw=False: (e,f,g) given."""
    par = {0: 0.5, 1: 0.5}
    lev = [None]
    for (a, b, c) in params:
        if raw:
            e = par.get(0, 0) / 2 * sg(a); f = par.get(1, 0) / 2 * sg(b); g = par.get(2, 0) * sg(c)
        else:
            e, f, g = abs(a), abs(b), abs(c)
        sig = split(par, e, f, g)
        if sig is None:
            return None
        child = {d: 0.0 for d in D}
        for t, (x, y) in enumerate(TYPES):
            child[x] += sig[t]
        Hp = Hv(list(par.values())); Hc = Hv(list(child.values()))
        lev.append(dict(H=Hc, Hpar=Hp, rho=Hv(sig) - Hp, tau=sig, child=child, efg=(e, f, g)))
        par = child
    return lev


# ---------------- filters ----------------
SYM = [0, 1]
ASY = [2, 3, 4, 5, 6]
NPAR = 1 + len(SYM) + 2 * len(ASY)  # 13


def sm(v):
    v = np.asarray(v, float); e = np.exp(v - v.max()); return e / e.sum()


def filt(z):
    pi = sm([z[0], 0.0, 0.0])
    cond = np.zeros((NT, 3))
    i = 1
    for t in SYM:
        cond[t] = sm([z[i], 0.0, 0.0]); i += 1
    for t in ASY:
        c = sm([z[i], z[i + 1], 0.0]); i += 2
        cond[t] = c; cond[MIR[TYPES[t]]] = c[[0, 2, 1]]
    return pi, cond


def kl(p, q):
    m = p > 1e-300
    return float((p[m] * np.log2(p[m] / q[m])).sum())


def filter_terms(L, z):
    pi, cond = filt(z)
    tau = L["tau"]
    Q = tau[:, None] * cond
    r12 = sum(tau[t] * kl(cond[t], pi) for t in range(NT) if tau[t] > 0)
    A = np.zeros((3, 4)); B = np.zeros((3, 4))
    for t, (x, y) in enumerate(TYPES):
        A[:, D.index(x)] += Q[t]; B[:, D.index(y)] += Q[t]
    def rate(Mg):
        r = 0.0
        for d in range(4):
            s = Mg[:, d].sum()
            if s > 1e-300:
                r += s * kl(Mg[:, d] / s, pi)
        return r
    r1, r2 = rate(A), rate(B)
    Ql = Q.sum(0)
    ce = float(-(Ql * np.log2(pi)).sum())
    extra = r12 + Hv(A.ravel()) + Hv(B.ravel()) - Hv(Ql) - ce - 2 * L["H"]
    return r12, r1, r2, extra


def lp(params, filters=None):
    lev = tree(params)
    if lev is None:
        return 9.0, None
    k = len(params); nv = k + 1; T = k
    A, b = [], []
    def row(d, rhs):
        v = np.zeros(nv)
        for i, x in d: v[i] += x
        A.append(v); b.append(rhs)
    for j in range(1, k + 1):
        L = lev[j]
        if j >= 2: row([(j - 1, 1), (j - 2, -1)], 0)
        row([(j - 1, 1)], L["rho"])
        row([(j - 1, -1), (T, -1)], -L["H"])
        def merge_row(const, c_lj, c_ljm1):
            d = [(j - 1, c_lj), (T, -1)]; rhs = -const
            if j == 1: rhs -= c_ljm1 * 1.0
            else: d.append((j - 2, c_ljm1))
            row(d, rhs)
        if filters is None or filters[j - 1] is None:
            merge_row(2 * L["H"], -1, -1)
        else:
            r12, r1, r2, extra = filter_terms(L, filters[j - 1])
            merge_row(L["H"] + r12 - r1, -1, 0)
            merge_row(L["H"] + r12 - r2, -1, 0)
            merge_row(2 * L["H"] + extra, -1, -1)
    row([(T, -1)], -0.5 * lev[k]["H"])
    bb = np.array(b)
    if not np.all(np.isfinite(bb)):
        return 9.0, None
    res = linprog(np.eye(nv)[T], A_ub=np.array(A), b_ub=bb, bounds=[(0, 1)] * nv, method="highs")
    return (res.fun, res.x) if res.status == 0 else (9.0, None)


def unpack(z, k, use_filters, mask):
    p = np.where(np.asarray(mask) > 0, z[:3 * k].reshape(k, 3), -60.0)
    fl = [z[3 * k + NPAR * j: 3 * k + NPAR * (j + 1)] for j in range(k)] if use_filters else None
    return [tuple(r) for r in p], fl


def optimise(k, use_filters, mask, starts, rng, rounds=2):
    nz = 3 * k + (NPAR * k if use_filters else 0)
    f = lambda z: lp(*unpack(z, k, use_filters, mask))[0]
    best = (9.0, None)
    for s in starts:
        z = np.array(s, float)
        if len(z) < nz:
            z = np.concatenate([z, rng.normal(0, 0.3, nz - len(z))])
        for _ in range(rounds):
            r = minimize(f, z, method="Powell", options=dict(maxiter=8000, xtol=1e-6, ftol=1e-9))
            r = minimize(f, r.x, method="Nelder-Mead", options=dict(maxiter=4000, xatol=1e-7, fatol=1e-10))
            if abs(r.fun - f(z)) < 1e-9:
                z = r.x; break
            z = r.x
        if f(z) < best[0]:
            best = (f(z), z)
    return best


def report(k, z, use_filters, mask):
    params, fl = unpack(z, k, use_filters, mask)
    lev = tree(params); T, x = lp(params, fl); L = [1.0] + list(x[:k])
    print(f"   T={T:.5f}  (e,f,g) per level = {[tuple(round(float(v),4) for v in lev[j]['efg']) for j in range(1,k+1)]}")
    for j in range(1, k + 1):
        Lv = lev[j]; o = 2 * Lv["H"] - L[j] - L[j - 1]; s = Lv["H"] - L[j]
        useful = o + Lv["Hpar"] + Lv["rho"] - 2 * Lv["H"]
        line = f"   level {j}: list {s:.4f} merge {o:.4f} useful {useful:.4f} reps {Lv['rho']:.4f} l={L[j]:.4f}"
        if fl is not None:
            r12, r1, r2, ex = filter_terms(Lv, fl[j - 1])
            line += f" | LSF entries {s + r12 - min(r1, r2):.4f} passing {o + ex:.4f}"
        print(line)
    print(f"   base {0.5 * lev[k]['H']:.4f}")


# ---------- BBSS accounting (lists may be random subsets; final expected #solutions >= 1) ----------
def lp2(params, filters=None, raw=True):
    """Vars: c_1..c_k (cumulative constraint bits), L_1..L_k (log list sizes), T.
    L_k = H_k - c_k (complete, built from half-lists, cost H_k/2)
    L_j = 2 L_{j+1} - (c_j - c_{j+1}) + p_{j+1},  p = log Pr[random pair is a valid split]
    L_j + c_j <= H_j ;  0 <= 2 L_1 - (1 - c_1) + p_1 ;  c_k <= ... <= c_1 <= 1
    T >= every list, every merge (pairs 2L_{j+1} - (c_j - c_{j+1}), or LSF terms), H_k/2."""
    lev = tree(params, raw=raw)
    if lev is None:
        return 9.0, None
    k = len(params); C = lambda j: j - 1; Lv = lambda j: k + j - 1; T = 2 * k; nv = 2 * k + 1
    Aub, bub, Aeq, beq = [], [], [], []
    def row(store, d, rhs):
        v = np.zeros(nv)
        for i, x in d: v[i] += x
        (Aub if store == "ub" else Aeq).append(v); (bub if store == "ub" else beq).append(rhs)
    pv = lambda j: lev[j]["Hpar"] + lev[j]["rho"] - 2 * lev[j]["H"]   # merge of level-j lists
    row("eq", [(Lv(k), 1), (C(k), 1)], lev[k]["H"])
    for j in range(1, k):
        # L_j - 2L_{j+1} + c_j - c_{j+1} = p
        row("eq", [(Lv(j), 1), (Lv(j + 1), -2), (C(j), 1), (C(j + 1), -1)], pv(j + 1))
        row("ub", [(Lv(j), 1), (C(j), 1)], lev[j]["H"])
        row("ub", [(C(j + 1), 1), (C(j), -1)], 0)
    # top: 2L_1 + c_1 - 1 + p_1 >= 0  ->  -2L_1 - c_1 <= p_1 - 1
    row("ub", [(Lv(1), -2), (C(1), -1)], pv(1) - 1)
    for j in range(1, k + 1):
        row("ub", [(Lv(j), 1), (T, -1)], 0)
        # merge of level-j lists into level j-1: pairs = 2L_j - (c_{j-1} - c_j), c_0 = 1
        def mrow(coefL, coefc_j, coefc_jm1, const):
            d = [(Lv(j), coefL), (C(j), coefc_j), (T, -1)]; rhs = -const
            if j == 1: rhs -= coefc_jm1 * 1.0
            else: d.append((C(j - 1), coefc_jm1))
            row("ub", d, rhs)
        if filters is None or filters[j - 1] is None:
            mrow(2, 1, -1, 0.0)
        else:
            r12, r1, r2, extra = filter_terms(lev[j], filters[j - 1])
            row("ub", [(Lv(j), 1), (T, -1)], -(r12 - r1))
            row("ub", [(Lv(j), 1), (T, -1)], -(r12 - r2))
            mrow(2, 1, -1, extra + 2 * lev[j]["H"] - 2 * lev[j]["H"])
    row("ub", [(T, -1)], -0.5 * lev[k]["H"])
    bb = np.array(bub + beq)
    if not np.all(np.isfinite(bb)):
        return 9.0, None
    res = linprog(np.eye(nv)[T], A_ub=np.array(Aub), b_ub=np.array(bub), A_eq=np.array(Aeq),
                  b_eq=np.array(beq), bounds=[(0, 1)] * k + [(-1, 1)] * k + [(0, 1)], method="highs")
    return (res.fun, res.x) if res.status == 0 else (9.0, None)


def efg_from_types(types):
    """types: per level (alpha=#-1, gamma=#2, beta=net weight).  Child type fixes only two
    of (e,f,g); the third is chosen to maximise H(sigma), i.e. the representation count."""
    from scipy.optimize import minimize_scalar
    par = {-1: 0.0, 0: 0.5, 1: 0.5, 2: 0.0}; out = []
    for (al, ga, be) in types:
        child = {-1: al, 2: ga, 1: be + al - 2 * ga}; child[0] = 1 - sum(child.values())
        def efg(g):
            # child[2] = f + (p2-g)/2 ;  child[-1] = pm1/2 + e + f
            f = child[2] - (par[2] - g) / 2; e = child[-1] - par[-1] / 2 - f
            return e, f, g
        def negH(g):
            e, f, gg = efg(g); sig = split(par, e, f, gg)
            return 1e3 if sig is None else -Hv(sig)
        hi = par[2] if par[2] > 0 else 0.0
        g = minimize_scalar(negH, bounds=(0, hi), method="bounded").x if hi > 0 else 0.0
        out.append(efg(g)); par = child
    return out

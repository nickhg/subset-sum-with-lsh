"""Task 1 (notes/handoff_subset_sum_floor_and_hybrid.md): recursive depth-d floor for representation trees.

Split laws per level come from gen_lsf.Model (symmetric, per-parent-digit splits, any digit set D).
For fixed split laws the exponents are an LP in the constraint bits c_1..c_d (c_0 = 1 = the n bits of the instance).

Strict accounting (the note's model; HGJ/BCJ):
    survival   c_j <= rho_j = H(sigma_j) - H(X_{j-1})        (modulus <= #representations)
    nesting    c_j <= c_{j-1},  c_0 = 1
    lists      L_j = H_j - c_j
Variants (T = max of the listed terms):
    F0     lists only                                   (the note's "floor"; d = 1 gives its table)
    F0L    lists + leaf build  H_d / 2                  (meet-in-the-middle for the deepest lists)
    F1     lists + leaf + merges  2H_j - c_j - c_{j-1}  (pairs examined at the merge of level-j lists)
    F2     as F1 but each merge type-class filtered (Dubiner codes): entries L_j + I_XY - I_X(Y),
           examined 2H_j - c_j - c_{j-1} + I_XY - I_X - I_Y   (filter laws optimised too)
BBSS accounting (lists may be random subsets; gen_lsf.Model.lp):
    B1     merges, no filters        B2   with filters
usage: recursive_floor.py DIGITS d VARIANT [restarts] [seed]      e.g.  -1,0,1,2 3 F1 6 0
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np, warnings
from scipy.optimize import linprog, minimize
from gen_lsf import Model
warnings.filterwarnings("ignore")


def strict_lp(M, lev, d, variant, F=None):
    nv = d + 1; T = d
    A, b = [], []
    def row(pairs, rhs):
        v = np.zeros(nv)
        for i, x in pairs: v[i] += x
        A.append(v); b.append(rhs)
    for j in range(1, d + 1):
        L = lev[j]; cj = j - 1
        row([(cj, 1)], L["rho"])                                  # survival
        if j >= 2: row([(cj, 1), (cj - 1, -1)], 0.0)              # nesting
        row([(cj, -1), (T, -1)], -L["H"])                         # list  H - c <= T
        if variant in ("F1", "F2"):
            ex = 0.0
            if variant == "F2":
                r12, r1, r2, ex = M.filter_terms(L, F[j - 1])
                row([(cj, -1), (T, -1)], -(L["H"] + r12 - r1))   # entries
                row([(cj, -1), (T, -1)], -(L["H"] + r12 - r2))
            # merge of level-j lists: 2H_j - c_j - c_{j-1} + ex <= T
            pr = [(cj, -1), (T, -1)]; rhs = -(2 * L["H"] + ex)
            if j == 1: rhs += 1.0
            else: pr.append((cj - 1, -1))
            row(pr, rhs)
    if variant in ("F0L", "F1", "F2"):
        row([(T, -1)], -0.5 * lev[d]["H"])                        # leaf build
    bb = np.array(b)
    if not np.all(np.isfinite(bb)):
        return 9.0, None
    res = linprog(np.eye(nv)[T], A_ub=np.array(A), b_ub=bb, bounds=[(0, 1)] * d + [(0, 2)], method="highs")
    return (res.fun, res.x) if res.status == 0 else (9.0, None)


def evaluate(M, z, d, variant):
    ns, nf = M.nsplit, M.nfilt
    P = z[:d * ns].reshape(d, ns) if ns else np.zeros((d, 0))
    F = [z[d * ns + nf * j: d * ns + nf * (j + 1)] for j in range(d)] if variant in ("F2", "B2") else None
    if variant in ("B1", "B2"):
        T, x, lev = M.lp(P, F)
        return T, x, lev, P, F
    lev = M.tree(P)
    T, x = strict_lp(M, lev, d, variant, F)
    return T, x, lev, P, F


def optimise(D, d, variant, restarts=6, seed=0):
    M = Model(D); rng = np.random.default_rng(seed)
    ns, nf = M.nsplit, M.nfilt
    nz = d * ns + (d * nf if variant in ("F2", "B2") else 0)
    f = lambda z: evaluate(M, z, d, variant)[0]
    if nz == 0:
        return f(np.zeros(0)), np.zeros(0), M
    best = (9.0, None)
    for r in range(restarts):
        z = np.concatenate([rng.normal(-2 + r * 0.5, 1.0, d * ns), rng.normal(0, 0.5, nz - d * ns)])
        for _ in range(2):
            res = minimize(f, z, method="Powell", options=dict(maxiter=20000, xtol=1e-7, ftol=1e-11))
            res = minimize(f, res.x, method="Nelder-Mead", options=dict(maxiter=8000, xatol=1e-8, fatol=1e-12))
            z = res.x
        if res.fun < best[0]:
            best = (res.fun, res.x)
    return best[0], best[1], M


def describe(M, z, d, variant):
    T, x, lev, P, F = evaluate(M, z, d, variant)
    out = [f"T = {T:.5f}"]
    if x is None:
        return "\n".join(out)
    if variant in ("B1", "B2"):
        c = [1.0] + list(x[:d]); Ls = list(x[d:2 * d])
    else:
        c = [1.0] + list(x[:d]); Ls = [lev[j]["H"] - c[j] for j in range(1, d + 1)]
    for j in range(1, d + 1):
        ch = lev[j]["child"]
        dig = " ".join(f"{k}:{ch[k]:.4f}" for k in M.D if ch[k] > 5e-5)
        mg = 2 * Ls[j - 1] - (c[j - 1] - c[j])
        out.append(f"  level {j}: [{dig}]  H {lev[j]['H']:.4f} rho {lev[j]['rho']:.4f} c {c[j]:.4f} "
                   f"list {Ls[j-1]:.4f} merge-pairs {mg:.4f}")
    out.append(f"  leaf H_d/2 {lev[d]['H'] / 2:.4f}")
    return "\n".join(out)


if __name__ == "__main__":
    D = [int(t) for t in sys.argv[1].split(",")]; d = int(sys.argv[2]); variant = sys.argv[3]
    restarts = int(sys.argv[4]) if len(sys.argv) > 4 else 6; seed = int(sys.argv[5]) if len(sys.argv) > 5 else 0
    T, z, M = optimise(D, d, variant, restarts, seed)
    tag = f"D={sys.argv[1]} d={d} {variant}"
    print(f"{tag}: best T = {T:.5f}", flush=True)
    print(describe(M, z, d, variant), flush=True)
    os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), "runs"), exist_ok=True)
    np.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "runs",
                         f"rf_{sys.argv[1].replace(',', '_')}_d{d}_{variant}.npy"), z)

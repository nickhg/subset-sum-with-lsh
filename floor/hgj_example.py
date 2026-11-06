"""Worked example for the introduction: the top HGJ merge, x0 of weight 1/2 split into x + y of
weight 1/4 with disjoint supports.
(a) pattern waste p = H(sigma) - 2 H(delta);  the 'hard' two-label filter (1 of x -> L, 1 of y -> R, (0,0) -> L w.p. a),
    its information terms and saving, for a = 1/2 and the a minimising the entry cost;
(b) the HGJ depth-3 optima of the model (BBSS accounting), unfiltered (B1) and filtered (B2): per merge pairs, p_j,
    I(XY;L), I(X;L), I(Y;L), saving, entries, passing.
usage: python3 floor/hgj_example.py
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
import numpy as np
from scipy.optimize import minimize_scalar
from gen_lsf import Model

H = lambda *p: -sum(x * np.log2(x) for x in p if x > 0)
h = lambda x: H(x, 1 - x)
sig = {(1, 0): .25, (0, 1): .25, (0, 0): .5}
print(f"(a) p = H(sigma) - 2H(delta) = {H(*sig.values()) - 2 * h(.25):.4f}   (3/4)h(1/3) - h(1/4) = {.75 * h(1/3) - h(.25):.4f}")

def hard(a):
    J = {((1, 0), 'L'): .25, ((0, 1), 'R'): .25, ((0, 0), 'L'): .5 * a, ((0, 0), 'R'): .5 * (1 - a)}
    def marg(f):
        o = {}
        for k, v in J.items(): o[f(k)] = o.get(f(k), 0) + v
        return list(o.values())
    HL = H(*marg(lambda k: k[1])); IXY = H(*marg(lambda k: k[0])) + HL - H(*J.values())
    IX = h(.25) + HL - H(*marg(lambda k: (k[0][0], k[1]))); IY = h(.25) + HL - H(*marg(lambda k: (k[0][1], k[1])))
    return IXY, IX, IY
for a in (0.5, minimize_scalar(lambda a: hard(a)[0] - min(hard(a)[1:]), bounds=(1e-6, 1 - 1e-6), method="bounded").x):
    IXY, IX, IY = hard(a)
    print(f"    hard filter a = {a:.3f}: I_XY {IXY:.4f} I_X {IX:.4f} I_Y {IY:.4f} saving {IX + IY - IXY:.4f}  entries gap {IXY - min(IX, IY):.4f}")

M = Model([0, 1])
for v in ("B1", "B2"):
    z = np.load(os.path.join(HERE, "runs", f"rf_0_1_d3_{v}.npy")); d = 3
    F = [z[M.nfilt * j:M.nfilt * (j + 1)] for j in range(d)] if v == "B2" else None
    P = np.zeros((d, 0)); T, x, lev = M.lp(P, F); c = [1.0] + list(x[:d]); L = list(x[d:2 * d])
    print(f"(b) HGJ depth 3, {v}: T = {T:.4f}")
    for j in range(1, d + 1):
        pairs = 2 * L[j - 1] - (c[j - 1] - c[j]); pj = lev[j]["Hpar"] + lev[j]["rho"] - 2 * lev[j]["H"]
        s = f"    merge {j}: list {L[j-1]:.4f} pairs {pairs:.4f} p {pj:+.4f}"
        if F is not None:
            r12, r1, r2, ex = M.filter_terms(lev[j], F[j - 1])
            s += f" | I_XY {r12:.4f} I_X {r1:.4f} I_Y {r2:.4f} saving {-ex:.4f} entries {L[j-1] + r12 - min(r1, r2):.4f} passing {pairs + ex:.4f}"
        print(s)
    print(f"    leaves {lev[d]['H'] / 2:.4f}")

"""Independent re-cost of a saved {-1,0,1,2} filtered point (wc handoff21).  Written separately from gen_lsf: only the
parameter layout (the order of logits) is shared; tree, information terms and LP are re-derived here.

Layout of a point z (depth d): d rows of split logits, then d rows of filter logits.
  split row: for each parent digit (ascending), logits of its unordered splits after the first, softmax with the first
             fixed at 0.  Splits of a parent p: pairs (x, y), x >= y, x + y = p, x, y in D, ordered with pairs
             containing 0 first, then by decreasing |x - y|.
  filter row: [pi logit (ignored: we use pi = Q_Lambda)], one logit per symmetric type (x, x) for (N vs R, L = R),
             two per asymmetric type x > y for (N, L) vs R; the mirrored type (y, x) gets labels L <-> R.
Costs (per n, log 2), BBSS accounting, filtered merges:
  level j: sigma_j = law of the ordered pair, delta_j its marginal, p_j = H(sigma_j) - 2 H(delta_j)
  lists:  l_d + c_d = H_d;  l_j + c_j <= H_j;  l_{j-1} = 2 l_j - (c_{j-1} - c_j) + p_j  (j >= 2);
          root 2 l_1 - (1 - c_1) + p_1 >= 0;  1 >= c_1 >= ... >= c_d >= 0
  T >= H_d / 2,  l_j,  l_j + I(XY;L) - I(X;L),  l_j + I(XY;L) - I(Y;L),
       P_j + I(XY;L) - I(X;L) - I(Y;L)  with P_j = 2 l_j - (c_{j-1} - c_j)
usage: recost.py point.npy d
"""
import sys, itertools
import numpy as np
from scipy.optimize import linprog

D = [-1, 0, 1, 2]


def H(p):
    p = np.asarray(p, float).ravel(); p = p[p > 0]; return float(-(p * np.log2(p)).sum())


def softmax(v):
    v = np.asarray(v, float); e = np.exp(v - v.max()); return e / e.sum()


def splits(p):
    s = [(x, p - x) for x in D if (p - x) in D and x >= p - x]
    return sorted(s, key=lambda q: (0 if 0 in q else 1, -abs(q[0] - q[1])))


SPL = {p: splits(p) for p in D}
NS = sum(len(v) - 1 for v in SPL.values())
OT = [t for p in D for (x, y) in SPL[p] for t in ([(x, y)] if x == y else [(x, y), (y, x)])]   # ordered types
SYM = [t for t in OT if t[0] == t[1]]; ASYM = [t for t in OT if t[0] > t[1]]
NF = 1 + len(SYM) + 2 * len(ASYM)


def decode(z, d):
    P = z[:d * NS].reshape(d, NS); F = z[d * NS:d * (NS + NF)].reshape(d, NF)
    levels = []; par = {0: 0.5, 1: 0.5}
    for j in range(d):
        sig = {}; i = 0
        for p in D:
            nl = len(SPL[p]) - 1; q = softmax(np.concatenate([[0.0], P[j, i:i + nl]])); i += nl
            for (x, y), w in zip(SPL[p], q):
                m = par.get(p, 0.0) * w
                if x == y:
                    sig[(x, y)] = sig.get((x, y), 0) + m
                else:
                    sig[(x, y)] = sig.get((x, y), 0) + m / 2; sig[(y, x)] = sig.get((y, x), 0) + m / 2
        child = {}
        for (x, y), m in sig.items():
            child[x] = child.get(x, 0) + m
        kap = {}; i = 1                                       # label law given the ordered pair, labels (N, L, R)
        for t in SYM:
            kap[t] = softmax([F[j, i], 0.0, 0.0]); i += 1
        for t in ASYM:
            k = softmax([F[j, i], F[j, i + 1], 0.0]); kap[t] = k; kap[(t[1], t[0])] = k[[0, 2, 1]]; i += 2
        levels.append(dict(sig=sig, child=child, par=dict(par), kap=kap)); par = child
    return levels


def info(lv):
    """I(XY;L), I(X;L), I(Y;L) from the joint law of (X, Y, L) under the valid-pair law sigma"""
    J = {}
    for t, m in lv["sig"].items():
        for l in range(3):
            J[(t[0], t[1], l)] = m * lv["kap"][t][l]
    def marg(keyf):
        out = {}
        for k, v in J.items():
            out[keyf(k)] = out.get(keyf(k), 0) + v
        return np.array(list(out.values()))
    HL = H(marg(lambda k: k[2])); HXY = H(marg(lambda k: (k[0], k[1]))); HXYL = H(np.array(list(J.values())))
    HX = H(marg(lambda k: k[0])); HY = H(marg(lambda k: k[1]))
    HXL = H(marg(lambda k: (k[0], k[2]))); HYL = H(marg(lambda k: (k[1], k[2])))
    return HXY + HL - HXYL, HX + HL - HXL, HY + HL - HYL


def recost(z, d):
    lv = decode(z, d)
    Hj = [H(list(l["child"].values())) for l in lv]
    pj = [H(list(l["sig"].values())) - 2 * Hj[j] for j, l in enumerate(lv)]
    I = [info(l) for l in lv]
    # variables: c_1..c_d, l_1..l_d, T
    nv = 2 * d + 1; c = lambda j: j - 1; L = lambda j: d + j - 1; T = 2 * d
    A, b, Ae, be = [], [], [], []
    def le(terms, rhs, eq=False):
        v = np.zeros(nv)
        for k, x in terms: v[k] += x
        (Ae if eq else A).append(v); (be if eq else b).append(rhs)
    le([(L(d), 1), (c(d), 1)], Hj[d - 1], eq=True)
    for j in range(1, d):
        le([(L(j), 1), (c(j), 1)], Hj[j - 1])
        le([(c(j + 1), 1), (c(j), -1)], 0)
        # l_j = 2 l_{j+1} - (c_j - c_{j+1}) + p_{j+1}
        le([(L(j), 1), (L(j + 1), -2), (c(j), 1), (c(j + 1), -1)], pj[j], eq=True)
    le([(L(1), -2), (c(1), -1)], pj[0] - 1)                   # root: 2 l_1 - 1 + c_1 + p_1 >= 0
    for j in range(1, d + 1):
        IXY, IX, IY = I[j - 1]
        le([(L(j), 1), (T, -1)], 0)
        le([(L(j), 1), (T, -1)], -(IXY - IX)); le([(L(j), 1), (T, -1)], -(IXY - IY))
        pr = [(L(j), 2), (c(j), 1), (T, -1)] + ([] if j == 1 else [(c(j - 1), -1)])
        le(pr, (1.0 if j == 1 else 0.0) - (IXY - IX - IY))
    le([(T, -1)], -Hj[d - 1] / 2)
    r = linprog(np.eye(nv)[T], A_ub=np.array(A), b_ub=np.array(b), A_eq=np.array(Ae), b_eq=np.array(be),
                bounds=[(0, 1)] * d + [(-1, 1)] * d + [(0, 1)], method="highs")
    x = r.x; cc = [1.0] + list(x[:d]); ll = list(x[d:2 * d])
    rows = []
    for j in range(1, d + 1):
        IXY, IX, IY = I[j - 1]; Pj = 2 * ll[j - 1] - (cc[j - 1] - cc[j])
        rows.append(dict(j=j, H=Hj[j - 1], p=pj[j - 1], c=cc[j], l=ll[j - 1], P=Pj, IXY=IXY, IX=IX, IY=IY,
                         entries=ll[j - 1] + IXY - min(IX, IY), passing=Pj + IXY - IX - IY))
    # corner flags: tiny digit masses, tiny type classes carrying non-trivial labels
    flags = []
    for j, l in enumerate(lv, 1):
        for dg, m in l["child"].items():
            if 0 < m < 1e-4:
                flags.append(f"level {j}: digit {dg} mass {m:.2e}")
        for t, m in l["sig"].items():
            if 0 < m < 1e-4:
                flags.append(f"merge {j}: pair type {t} mass {m:.2e}")
    return r.fun, rows, flags, lv


if __name__ == "__main__":
    z = np.load(sys.argv[1]); d = int(sys.argv[2]); T, rows, flags, _ = recost(z, d)
    print(f"independent T = {T:.6f}")
    for r in rows:
        print("  j {j}: H {H:.4f} p {p:+.4f} c {c:.4f} l {l:.4f} | pairs {P:.4f} I_XY {IXY:.4f} I_X {IX:.4f} "
              "I_Y {IY:.4f} entries {entries:.4f} passing {passing:.4f}".format(**r))
    print("  flags:", "; ".join(flags) if flags else "none")

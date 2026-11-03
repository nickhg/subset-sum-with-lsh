"""Independent re-cost of a saved Meet-LWE tree point (meetlwe_model.py), written without gen_lsf / meetlwe_model.
Only the parameter layout is shared (same conventions as floor/recost.py, digit set D a parameter).

Root: ternary key, relative weight omega (omega/2 each sign).  May accounting (ePrint 2021/216, Sec. 7.4):
  c_j <= rho_j,  c_j <= c_{j-1},  lists l_j = H_j - c_j
  root merge (Odlyzko, 1 bit per coordinate)   P_1 = 2 l_1 - 1
  merge of level-j lists (j >= 2)              P_j = 2 l_j - (c_{j-1} - c_j)
  leaves H_d / 2
Filters as in the subset-sum paper (pi = Q_Lambda):  entries l_j + I(XY;L) - I(X;L) (and Y), passing P_j + I(XY;L) - I(X;L) - I(Y;L).
T = max of leaves, lists, and per merge the passing and entry terms (filtered) or P_j (unfiltered).
usage: ml_recost.py point.npy DIGITS d omega [f]
"""
import sys
import numpy as np
from scipy.optimize import linprog


def H(p):
    p = np.asarray(p, float).ravel(); p = p[p > 0]; return float(-(p * np.log2(p)).sum())


def softmax(v):
    v = np.asarray(v, float); e = np.exp(v - v.max()); return e / e.sum()


def layout(D):
    spl = {}
    for p in D:
        s = [(x, p - x) for x in D if (p - x) in D and x >= p - x]
        spl[p] = sorted(s, key=lambda q: (0 if 0 in q else 1, -abs(q[0] - q[1])))
    ns = sum(len(v) - 1 for v in spl.values())
    ot = [t for p in D for (x, y) in spl[p] for t in ([(x, y)] if x == y else [(x, y), (y, x)])]
    sym = [t for t in ot if t[0] == t[1]]; asym = [t for t in ot if t[0] > t[1]]
    return spl, ns, sym, asym, 1 + len(sym) + 2 * len(asym)


def levels(z, D, d, omega, filt):
    spl, ns, sym, asym, nf = layout(D)
    P = z[:d * ns].reshape(d, ns); F = z[d * ns:d * (ns + nf)].reshape(d, nf) if filt else None
    par = {-1: omega / 2, 0: 1 - omega, 1: omega / 2}; out = []
    for j in range(d):
        sig = {}; i = 0
        for p in D:
            nl = len(spl[p]) - 1; q = softmax(np.concatenate([[0.0], P[j, i:i + nl]])); i += nl
            for (x, y), w in zip(spl[p], q):
                m = par.get(p, 0.0) * w
                if m <= 0:
                    continue
                if x == y:
                    sig[(x, y)] = sig.get((x, y), 0) + m
                else:
                    sig[(x, y)] = sig.get((x, y), 0) + m / 2; sig[(y, x)] = sig.get((y, x), 0) + m / 2
        child = {}
        for (x, y), m in sig.items():
            child[x] = child.get(x, 0) + m
        I = (0.0, 0.0, 0.0)
        if filt:
            kap = {}; i = 1
            for t in sym:
                kap[t] = softmax([F[j, i], 0.0, 0.0]); i += 1
            for t in asym:
                k = softmax([F[j, i], F[j, i + 1], 0.0]); kap[t] = k; kap[(t[1], t[0])] = k[[0, 2, 1]]; i += 2
            J = {(t[0], t[1], l): m * kap[t][l] for t, m in sig.items() for l in range(3)}
            def mg(f):
                o = {}
                for k, v in J.items(): o[f(k)] = o.get(f(k), 0) + v
                return list(o.values())
            HL = H(mg(lambda k: k[2]))
            I = (H(mg(lambda k: k[:2])) + HL - H(list(J.values())), H(mg(lambda k: k[0])) + HL - H(mg(lambda k: (k[0], k[2]))),
                 H(mg(lambda k: k[1])) + HL - H(mg(lambda k: (k[1], k[2]))))
        Hp, Hc = H(list(par.values())), H(list(child.values()))
        out.append(dict(H=Hc, rho=H(list(sig.values())) - Hp, p=H(list(sig.values())) - 2 * Hc, I=I, child=child))
        par = child
    return out


def cost(z, D, d, omega, filt):
    lv = levels(z, D, d, omega, filt)
    nv = d + 1; T = d; A, b = [], []
    def le(terms, rhs):
        v = np.zeros(nv)
        for k, x in terms: v[k] += x
        A.append(v); b.append(rhs)
    for j in range(1, d + 1):
        Hj, (IXY, IX, IY) = lv[j - 1]["H"], lv[j - 1]["I"]
        le([(j - 1, 1)], lv[j - 1]["rho"])                    # c_j <= rho_j
        if j >= 2:
            le([(j - 1, 1), (j - 2, -1)], 0.0)                # nesting
        # list l_j = H_j - c_j <= T
        le([(j - 1, -1), (T, -1)], -Hj)
        if filt:
            le([(j - 1, -1), (T, -1)], -(Hj + IXY - min(IX, IY)))
        sav = IXY - IX - IY if filt else 0.0
        # P_j = 2 H_j - 2 c_j - (c_{j-1} - c_j)  (c_0 replaced by the Odlyzko bit at the root)
        if j == 1:
            le([(0, -2), (T, -1)], -(2 * Hj - 1 + sav))
        else:
            le([(j - 1, -1), (j - 2, -1), (T, -1)], -(2 * Hj + sav))
    le([(T, -1)], -lv[d - 1]["H"] / 2)
    r = linprog(np.eye(nv)[T], A_ub=np.array(A), b_ub=np.array(b), bounds=[(0, 3)] * d + [(0, 3)], method="highs")
    return r.fun, r.x, lv


if __name__ == "__main__":
    z = np.load(sys.argv[1]); D = [int(x) for x in sys.argv[2].split(",")]; d = int(sys.argv[3]); om = float(sys.argv[4])
    filt = len(sys.argv) > 5 and sys.argv[5] == "f"
    T, x, lv = cost(z, D, d, om, filt)
    print(f"independent T = {T:.6f}")
    for j, l in enumerate(lv, 1):
        print(f"  j{j} H {l['H']:.4f} rho {l['rho']:.4f} c {x[j-1]:.4f} l {l['H']-x[j-1]:.4f} p {l['p']:+.4f} "
              f"I_XY {l['I'][0]:.4f} I_X {l['I'][1]:.4f}  child " + " ".join(f"{k}:{v:.4f}" for k, v in sorted(l['child'].items())))

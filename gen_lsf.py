"""Representation trees over a general digit set D (e.g. {-2,-1,0,1,2}), BBSS accounting,
with optional type-class LSF at each merge.  Exponents /n, log base 2, standard heuristics.

Split law: for every parent digit d, a distribution over unordered pairs {x,y} in D with
x + y = d (ordered versions split equally).  sigma_j = joint law of the ordered child pair.
  child type = marginal of sigma,  reps rho = H(sigma) - H(parent),  valid pair type tau* = sigma
BBSS accounting (lp2): lists may be random subsets; L_j + c_j <= H_j; final E[#solutions] >= 1.
LSF (labels N,L,R, mirror-symmetric): worst case over all pair types in closed form
  passing = pairs + r12 + H(A) + H(B) - H(Q_lambda) - CE(Q_lambda, pi) - 2H
  entries = L + r12 - r1  (and r2)
"""
import numpy as np
from scipy.optimize import linprog


def Hv(v):
    v = np.asarray(v, float); v = v[v > 1e-300]
    return float(-(v * np.log2(v)).sum())


def sm(v):
    v = np.asarray(v, float); e = np.exp(v - v.max()); return e / e.sum()


def kl(p, q):
    m = p > 1e-300
    return float((p[m] * np.log2(p[m] / q[m])).sum())


class Model:
    def __init__(self, D):
        self.D = sorted(D)
        # unordered pairs per parent digit; first listed = "trivial" split (d,0) if possible
        self.upairs = {}
        for d in self.D:
            ps = []
            for x in self.D:
                y = d - x
                if y in self.D and x >= y:
                    ps.append((x, y))
            ps.sort(key=lambda p: (0 if 0 in p else 1, -abs(p[0] - p[1])))
            self.upairs[d] = ps
        self.nsplit = sum(len(v) - 1 for v in self.upairs.values())   # free logits per level
        # ordered types
        self.types = []
        for d in self.D:
            for (x, y) in self.upairs[d]:
                self.types.append((x, y))
                if x != y:
                    self.types.append((y, x))
        self.T = len(self.types)
        self.mir = [self.types.index((y, x)) for (x, y) in self.types]
        self.sym = [t for t, (x, y) in enumerate(self.types) if x == y]
        self.asym = [t for t, (x, y) in enumerate(self.types) if x > y]
        self.nfilt = 1 + len(self.sym) + 2 * len(self.asym)

    # ---------------- tree ----------------
    def tree(self, P):
        """P: array (k, nsplit) of logits."""
        par = {d: 0.0 for d in self.D}; par[0] = 0.5; par[1] = 0.5
        lev = [None]
        for row in P:
            sig = np.zeros(self.T); i = 0
            for d in self.D:
                ups = self.upairs[d]; nl = len(ups) - 1
                pr = sm(np.concatenate([[0.0], row[i:i + nl]])); i += nl
                if par[d] <= 0:
                    continue
                for (x, y), q in zip(ups, pr):
                    if x == y:
                        sig[self.types.index((x, y))] += par[d] * q
                    else:
                        sig[self.types.index((x, y))] += par[d] * q / 2
                        sig[self.types.index((y, x))] += par[d] * q / 2
            child = {d: 0.0 for d in self.D}
            for t, (x, y) in enumerate(self.types):
                child[x] += sig[t]
            Hp, Hc = Hv(list(par.values())), Hv(list(child.values()))
            lev.append(dict(H=Hc, Hpar=Hp, rho=Hv(sig) - Hp, tau=sig, child=dict(child)))
            par = child
        return lev

    # ---------------- filters ----------------
    def filt(self, z):
        pi = sm([z[0], 0.0, 0.0]); cond = np.zeros((self.T, 3)); i = 1
        for t in self.sym:
            cond[t] = sm([z[i], 0.0, 0.0]); i += 1
        for t in self.asym:
            c = sm([z[i], z[i + 1], 0.0]); i += 2
            cond[t] = c; cond[self.mir[t]] = c[[0, 2, 1]]
        return pi, cond

    def filter_terms(self, L, z):
        pi, cond = self.filt(z); tau = L["tau"]; nd = len(self.D)
        Q = tau[:, None] * cond
        r12 = sum(tau[t] * kl(cond[t], pi) for t in range(self.T) if tau[t] > 0)
        A = np.zeros((3, nd)); B = np.zeros((3, nd))
        for t, (x, y) in enumerate(self.types):
            A[:, self.D.index(x)] += Q[t]; B[:, self.D.index(y)] += Q[t]
        def rate(Mg):
            r = 0.0
            for d in range(nd):
                s = Mg[:, d].sum()
                if s > 1e-300:
                    r += s * kl(Mg[:, d] / s, pi)
            return r
        r1, r2 = rate(A), rate(B)
        Ql = Q.sum(0); ce = float(-(Ql * np.log2(pi)).sum())
        extra = r12 + Hv(A.ravel()) + Hv(B.ravel()) - Hv(Ql) - ce - 2 * L["H"]
        return r12, r1, r2, extra

    # ---------------- BBSS-accounting LP ----------------
    def lp(self, P, F=None):
        lev = self.tree(P); k = len(P)
        C = lambda j: j - 1; Lv = lambda j: k + j - 1; T = 2 * k; nv = 2 * k + 1
        Aub, bub, Aeq, beq = [], [], [], []
        def row(ub, d, rhs):
            v = np.zeros(nv)
            for i, x in d: v[i] += x
            (Aub if ub else Aeq).append(v); (bub if ub else beq).append(rhs)
        pv = lambda j: lev[j]["Hpar"] + lev[j]["rho"] - 2 * lev[j]["H"]
        row(False, [(Lv(k), 1), (C(k), 1)], lev[k]["H"])
        for j in range(1, k):
            row(False, [(Lv(j), 1), (Lv(j + 1), -2), (C(j), 1), (C(j + 1), -1)], pv(j + 1))
            row(True, [(Lv(j), 1), (C(j), 1)], lev[j]["H"])
            row(True, [(C(j + 1), 1), (C(j), -1)], 0)
        row(True, [(Lv(1), -2), (C(1), -1)], pv(1) - 1)
        for j in range(1, k + 1):
            row(True, [(Lv(j), 1), (T, -1)], 0)
            extra = 0.0
            if F is not None and F[j - 1] is not None:
                r12, r1, r2, extra = self.filter_terms(lev[j], F[j - 1])
                row(True, [(Lv(j), 1), (T, -1)], -(r12 - r1))
                row(True, [(Lv(j), 1), (T, -1)], -(r12 - r2))
            d = [(Lv(j), 2), (C(j), 1), (T, -1)]; rhs = -extra
            if j == 1: rhs += 1.0
            else: d.append((C(j - 1), -1))
            row(True, d, rhs)
        row(True, [(T, -1)], -0.5 * lev[k]["H"])
        bb = np.array(bub + beq)
        if not np.all(np.isfinite(bb)):
            return 9.0, None, lev
        res = linprog(np.eye(nv)[T], A_ub=np.array(Aub), b_ub=np.array(bub), A_eq=np.array(Aeq),
                      b_eq=np.array(beq), bounds=[(0, 1)] * k + [(-1, 1)] * k + [(0, 1)], method="highs")
        return (res.fun, res.x, lev) if res.status == 0 else (9.0, None, lev)

    def report(self, P, F=None):
        T, x, lev = self.lp(P, F); k = len(P); c = [1.0] + list(x[:k]); L = list(x[k:2 * k])
        out = [f"T = {T:.5f}"]
        for j in range(1, k + 1):
            ch = lev[j]["child"]
            out.append(f" level {j}: digits " + " ".join(f"{d}:{ch[d]:.4f}" for d in self.D)
                       + f" | reps {lev[j]['rho']:.4f} c {c[j]:.4f} list {L[j-1]:.4f}")
        for j in range(1, k + 1):
            pairs = 2 * L[j - 1] - (c[j - 1] - c[j]); s = f" merge of level-{j} lists: pairs {pairs:.4f}"
            if F is not None:
                r12, r1, r2, ex = self.filter_terms(lev[j], F[j - 1])
                s += f" | LSF entries {L[j-1] + r12 - min(r1, r2):.4f} passing {pairs + ex:.4f}"
            out.append(s)
        out.append(f" base {0.5 * lev[k]['H']:.4f}")
        return "\n".join(out)

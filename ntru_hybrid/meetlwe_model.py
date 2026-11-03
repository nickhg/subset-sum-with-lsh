"""handoff16c: May's Meet-LWE (ePrint 2021/216, Sections 7-8) as a representation-tree LP, with optional type-class
filters (gen_lsf.filter_terms) and the survival-recursion accounting.  Exponents per n, asymptotic, guessing T_g ignored
(as in May's Tables 5 and 7).

Root: ternary key of relative weight omega (omega/2 of each sign).  Levels j = 1..d with digit set D, split laws as in
gen_lsf.Model (parent digit -> unordered pair, symmetric).  Exact matching on r^(j) = log_q R^(j) = o(n) q-ary
coordinates gives c_j n bits; nested c_j <= c_{j-1} (j >= 2).  May's run time (Sec. 7.4):
    T^(j) = 2 L^(j+1) - (c_j - c_{j+1})   (j = 1..d-1),     T^(0) = 2 L^(1) - 1   (Odlyzko: 1 bit/coordinate),
    leaves H_d / 2,   lists L^(j) = H_j - c_j.
Accountings:  'may'  c_j = rho_j at the optimum (strict: c_j <= rho_j),   'surv'  survival recursion
    s_d = 0, s_j = min(0, rho_{j+1} - c_{j+1} + 2 s_{j+1}), root rho_1 - c_1 + 2 s_1 >= 0, lists H_j - c_j + s_j.
Filters (F given): each merge's pairs P become P + extra, entries L + r12 - r1 (gen_lsf), as in the subset-sum paper.
usage: meetlwe_model.py check            reproduce May Tables 5 (Rep-1) and 7 (Rep-2) at depth 4
       meetlwe_model.py DIGITS d omega ACC [filt] [restarts]
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np, warnings
from scipy.optimize import linprog, minimize
from gen_lsf import Model, Hv
warnings.filterwarnings("ignore")


class TModel(Model):
    def __init__(self, D, omega):
        super().__init__(D); self.omega = omega

    def tree(self, P):
        w = self.omega; par = {d: 0.0 for d in self.D}; par[-1] = w / 2; par[1] = w / 2; par[0] = 1 - w
        lev = [None]
        for row in P:
            sig = np.zeros(self.T); i = 0
            for d in self.D:
                ups = self.upairs[d]; nl = len(ups) - 1
                e = np.exp(np.concatenate([[0.0], row[i:i + nl]]) - max(0.0, *row[i:i + nl]) if nl else np.zeros(1))
                pr = e / e.sum(); i += nl
                if par[d] <= 0:
                    continue
                for (x, y), qq in zip(ups, pr):
                    if x == y:
                        sig[self.types.index((x, y))] += par[d] * qq
                    else:
                        sig[self.types.index((x, y))] += par[d] * qq / 2
                        sig[self.types.index((y, x))] += par[d] * qq / 2
            child = {d: 0.0 for d in self.D}
            for t, (x, y) in enumerate(self.types):
                child[x] += sig[t]
            Hp, Hc = Hv(list(par.values())), Hv(list(child.values()))
            lev.append(dict(H=Hc, Hpar=Hp, rho=Hv(sig) - Hp, tau=sig, child=dict(child)))
            par = child
        return lev


def lp(M, lev, d, acc, F=None):
    """min T for fixed split/filter laws.  Variables c_1..c_d, [s_1..s_{d-1}], T."""
    ns_ = d - 1 if acc == "surv" else 0; nv = d + ns_ + 1; T = nv - 1
    C = lambda j: j - 1; S = lambda j: d + j - 1
    ex = [0.0] * (d + 1); ent = [None] * (d + 1)
    if F is not None:
        for j in range(1, d + 1):
            r12, r1, r2, ex[j] = M.filter_terms(lev[j], F[j - 1]); ent[j] = max(r12 - r1, r12 - r2)
    best = (9.0, None)
    for pat in range(2 ** ns_):
        Aub, bub, Aeq, beq = [], [], [], []
        def row(ub, pairs, rhs):
            v = np.zeros(nv)
            for i, x in pairs: v[i] += x
            (Aub if ub else Aeq).append(v); (bub if ub else beq).append(rhs)
        sv = lambda j: [(S(j), 1)] if (acc == "surv" and j < d) else []
        if acc == "may":
            for j in range(1, d + 1):
                row(True, [(C(j), 1)], lev[j]["rho"])                                   # c_j <= rho_j
        else:
            for j in range(1, d):
                e = [(C(j + 1), -1)] + [(i, 2 * x) for i, x in sv(j + 1)]
                if pat >> (j - 1) & 1:
                    row(False, [(S(j), 1)] + [(i, -x) for i, x in e], lev[j + 1]["rho"])
                else:
                    row(False, [(S(j), 1)], 0.0); row(True, [(i, -x) for i, x in e], lev[j + 1]["rho"])
            row(True, [(C(1), 1)] + [(i, -2 * x) for i, x in sv(1)], lev[1]["rho"])   # root survival
        for j in range(2, d + 1):
            row(True, [(C(j), 1), (C(j - 1), -1)], 0.0)                                 # nesting
        for j in range(1, d + 1):
            Lj = [(C(j), -1)] + sv(j)
            row(True, Lj + [(T, -1)], -lev[j]["H"])                                     # list
            if ent[j] is not None:
                row(True, Lj + [(T, -1)], -(lev[j]["H"] + ent[j]))                      # filter entries
            pr = [(i, 2 * x) for i, x in Lj] + [(T, -1)]; rhs = -(2 * lev[j]["H"] + ex[j])
            if j == 1:
                rhs += 1.0                                                              # root: 2 L_1 - 1
            else:
                pr += [(C(j - 1), -1), (C(j), 1)]                                       # 2 L_j - (c_{j-1} - c_j)
            row(True, pr, rhs)
        row(True, [(T, -1)], -0.5 * lev[d]["H"])                                        # leaves
        if not np.all(np.isfinite(bub)):
            return 9.0, None
        res = linprog(np.eye(nv)[T], A_ub=np.array(Aub), b_ub=np.array(bub),
                      A_eq=np.array(Aeq) if Aeq else None, b_eq=np.array(beq) if beq else None,
                      bounds=[(0, 3)] * d + [(-2, 0)] * ns_ + [(0, 3)], method="highs")
        if res.status == 0 and res.fun < best[0]:
            best = (res.fun, res.x)
    return best


def optimise(D, d, omega, acc, filt=False, restarts=6, seed=0, init=None):
    M = TModel(D, omega); ns, nf = M.nsplit, M.nfilt; nz = d * ns + (d * nf if filt else 0)
    def f(z):
        P = z[:d * ns].reshape(d, ns); F = [z[d * ns + nf * j:d * ns + nf * (j + 1)] for j in range(d)] if filt else None
        return lp(M, M.tree(P), d, acc, F)[0]
    rng = np.random.default_rng(seed); best = (9.0, None)
    if init is not None:
        best = (f(init), init)
    for r in range(restarts):
        z = (best[1] + rng.normal(0, 0.3, nz)) if (best[1] is not None and r % 2) else \
            np.concatenate([rng.normal(-2 + 0.4 * r, 1.0, d * ns), rng.normal(0, 0.5, nz - d * ns)])
        for _ in range(2):
            res = minimize(f, z, method="Powell", options=dict(maxiter=20000, xtol=1e-7, ftol=1e-11))
            res = minimize(f, res.x, method="Nelder-Mead", options=dict(maxiter=8000, xatol=1e-8, fatol=1e-12))
            z = res.x
        if res.fun < best[0]:
            best = (res.fun, res.x)
    return best[0], best[1], M


if __name__ == "__main__":
    if sys.argv[1] == "check":
        may5 = {0.3: 0.298, 0.375: 0.323, 0.441: 0.340, 0.5: 0.356, 0.62: 0.389, 0.667: 0.407}
        may7 = {0.3: 0.295, 0.375: 0.318, 0.441: 0.334, 0.5: 0.348, 0.62: 0.371, 0.667: 0.379}
        for om in may5:
            T1 = optimise([-1, 0, 1], 4, om, "may", restarts=4)[0]
            T2 = optimise([-2, -1, 0, 1, 2], 4, om, "may", restarts=4)[0]
            print(f"omega {om}: Rep-1 d=4 ours {T1:.4f} (May {may5[om]})   Rep-2 d=4 ours {T2:.4f} (May {may7[om]})",
                  flush=True)
        sys.exit()
    D = [int(x) for x in sys.argv[1].split(",")]; d = int(sys.argv[2]); om = float(sys.argv[3]); acc = sys.argv[4]
    filt = len(sys.argv) > 5 and sys.argv[5] == "filt"; rs = int(sys.argv[6]) if len(sys.argv) > 6 else 6
    T, z, M = optimise(D, d, om, acc, filt, rs)
    print(f"D={D} d={d} omega={om} acc={acc} filters={filt}: T = {T:.5f}", flush=True)
    os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), "runs"), exist_ok=True)
    np.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "runs",
                         f"ml_{sys.argv[1].replace(',', '_')}_d{d}_w{om}_{acc}_{'f' if filt else 'p'}.npy"), z)

"""wc handoff4: K-symbol label alphabets for the type-class filters, on the deep {-1,0,1,2} B2 optima.

Invariant form (pi = Q_Lambda; pi cancels, see handoff2 reply B.1), per merge with pair-type law tau and label laws
cond[t] in Delta^K (most general: every ordered pair type its own law, no mirror constraint):
    r12 = I(T;Lambda),  r1 = I(X;Lambda),  r2 = I(Y;Lambda)
    entries gap = r12 - r1 (and r12 - r2),   extra (saving on passing pairs) = r12 - r1 - r2 + I(X;Y|...)-free form:
    extra = I(T;Lambda) - I(X;Lambda) - I(Y;Lambda)          (equals gen_lsf.filter_terms' extra at pi = Q_Lambda)
Digit laws fixed at the warm start; the filters are re-optimised (step 1).  Optional step 2 re-optimises everything.
usage: klabel.py START.npy depth K [joint]
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np, warnings
from scipy.optimize import minimize
from gen_lsf import Model, Hv, sm, kl
warnings.filterwarnings("ignore")


class KModel(Model):
    def __init__(self, D, K):
        super().__init__(D); self.K = K

    def cond_of(self, v):
        K = self.K
        return np.array([sm(np.concatenate([v[t * (K - 1):(t + 1) * (K - 1)], [0.0]])) for t in range(self.T)])

    def filter_terms(self, L, v):
        cond = self.cond_of(v); tau = L["tau"]; Q = tau[:, None] * cond; Ql = Q.sum(0)
        r12 = sum(tau[t] * kl(cond[t], Ql) for t in range(self.T) if tau[t] > 0)
        nd = len(self.D); A = np.zeros((self.K, nd)); B = np.zeros((self.K, nd))
        for t, (x, y) in enumerate(self.types):
            A[:, self.D.index(x)] += Q[t]; B[:, self.D.index(y)] += Q[t]
        def mi(Mg):
            r = 0.0
            for d in range(nd):
                s = Mg[:, d].sum()
                if s > 1e-300:
                    r += s * kl(Mg[:, d] / s, Ql)
            return r
        r1, r2 = mi(A), mi(B)
        return r12, r1, r2, r12 - r1 - r2


def embed3(M3, K, F):
    """3-label gen_lsf filter row -> K-label logits (extra labels at log-mass -6)."""
    _, cond = M3.filt(F); out = []
    for t in range(M3.T):
        c = np.concatenate([cond[t], np.full(K - 3, np.exp(-6.0))]); c /= c.sum()
        lg = np.log(np.maximum(c, 1e-300)); out.append(lg[:-1] - lg[-1])
    return np.concatenate(out)


if __name__ == "__main__":
    src, k, K = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]); joint = len(sys.argv) > 4
    D = [-1, 0, 1, 2]; M3 = Model(D); MK = KModel(D, K); ns, nf3 = M3.nsplit, M3.nfilt; nfk = M3.T * (K - 1)
    z = np.load(src); P = z[:k * ns].reshape(k, ns); F3 = [z[k * ns + nf3 * j:k * ns + nf3 * (j + 1)] for j in range(k)]
    T3 = M3.lp(P, F3)[0]
    v0 = np.concatenate([embed3(M3, K, F) for F in F3])
    unpackF = lambda v: [v[nfk * j:nfk * (j + 1)] for j in range(k)]
    TK0 = MK.lp(P, unpackF(v0))[0]
    print(f"d={k} 3-label T = {T3:.6f};  embedded in K={K}: T = {TK0:.6f}", flush=True)
    rng = np.random.default_rng(K)
    f = lambda v: MK.lp(P, unpackF(v))[0]
    best = (TK0, v0)
    for r in range(4):
        v = best[1] + (rng.normal(0, 0.5, len(v0)) if r else 0)
        res = minimize(f, v, method="Powell", options=dict(maxiter=60000, xtol=1e-7, ftol=1e-11))
        res = minimize(f, res.x, method="Nelder-Mead", options=dict(maxiter=20000, xatol=1e-8, fatol=1e-12))
        if res.fun < best[0] - 1e-9:
            best = (res.fun, res.x)
        print(f"  filters-only restart {r}: {res.fun:.6f}  best {best[0]:.6f}", flush=True)
    if joint:
        g = lambda w: MK.lp(w[:k * ns].reshape(k, ns), unpackF(w[k * ns:]))[0]
        w = np.concatenate([P.ravel(), best[1]])
        for r in range(3):
            res = minimize(g, w, method="Powell", options=dict(maxiter=60000, xtol=1e-7, ftol=1e-11))
            w = res.x
            print(f"  joint round {r}: {res.fun:.6f}", flush=True)
        if res.fun < best[0]:
            P = w[:k * ns].reshape(k, ns); best = (res.fun, w[k * ns:])
    lev = M3.tree(P); TK, x, _ = MK.lp(P, unpackF(best[1]))
    print(f"RESULT d={k} K={K}: T = {TK:.6f}  (3-label {T3:.6f}, change {TK - T3:+.6f})")
    lev3 = M3.tree(z[:k * ns].reshape(k, ns))
    for j in range(1, k + 1):
        a = M3.filter_terms(lev3[j], F3[j - 1]); b = MK.filter_terms(lev[j], unpackF(best[1])[j - 1])
        cond = MK.cond_of(unpackF(best[1])[j - 1]); Ql = (lev[j]["tau"][:, None] * cond).sum(0)
        print(f"  level {j}: 3-label entries gap {a[0] - min(a[1], a[2]):.5f} extra {a[3]:+.5f} | K={K} entries gap "
              f"{b[0] - min(b[1], b[2]):.5f} extra {b[3]:+.5f}  Q_lambda {np.round(Ql, 3)}")
    np.save(src.replace(".npy", f"_K{K}.npy"), np.concatenate([P.ravel(), best[1]]))

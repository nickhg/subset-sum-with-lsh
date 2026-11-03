"""handoff17 step 1 (go/no-go): at May's own optimum (split laws fixed), how much do filters cut the binding cost?
Reports per merge: pattern waste p_j = H(sigma_j) - 2 H_j (log fraction of matched pairs that are valid splits),
unfiltered cost, and the filtered cost with only the filter laws optimised (May accounting, c_j <= rho_j).
usage: gonogo.py POINT.npy DIGITS d omega
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np, warnings
from scipy.optimize import minimize
from meetlwe_model import TModel, lp
from gen_lsf import Hv
warnings.filterwarnings("ignore")

src, D, d, om = sys.argv[1], [int(x) for x in sys.argv[2].split(",")], int(sys.argv[3]), float(sys.argv[4])
M = TModel(D, om); ns, nf = M.nsplit, M.nfilt
z = np.load(src)[:d * ns]; P = z.reshape(d, ns); lev = M.tree(P)


def costs(x, F):
    c = [None] + list(x[:d]); L = [None] + [lev[j]["H"] - c[j] for j in range(1, d + 1)]
    out = []
    for j in range(1, d + 1):
        pairs = 2 * L[j] - 1 if j == 1 else 2 * L[j] - (c[j - 1] - c[j])
        ex = M.filter_terms(lev[j], F[j - 1])[3] if F is not None else 0.0
        out.append((pairs, pairs + ex))
    return c, L, out


T0, x0 = lp(M, lev, d, "may")
rng = np.random.default_rng(0); best = (T0, None)
f = lambda v: lp(M, lev, d, "may", [v[nf * j:nf * (j + 1)] for j in range(d)])[0]
for r in range(int(os.environ.get("RESTARTS", "2"))):
    v0 = rng.normal(0, 1.0, d * nf)
    res = minimize(f, v0, method="Powell", options=dict(maxiter=20000, xtol=1e-7, ftol=1e-11))
    res = minimize(f, res.x, method="Nelder-Mead", options=dict(maxiter=8000))
    if res.fun < best[0]:
        best = (res.fun, res.x)
T1, v = best; F = [v[nf * j:nf * (j + 1)] for j in range(d)] if v is not None else None
_, x1 = lp(M, lev, d, "may", F) if F is not None else (T0, x0)
c0, L0, k0 = costs(x0, None); c1, L1, k1 = costs(x1, F)
print(f"{os.path.basename(src)}  D={D} d={d} omega={om}: unfiltered T = {T0:.5f}, filters only (split laws fixed) T = {T1:.5f}")
print(f"  leaves H_d/2 = {lev[d]['H'] / 2:.4f}")
for j in range(1, d + 1):
    p = Hv(lev[j]["tau"]) - 2 * lev[j]["H"]
    print(f"  merge of level-{j} lists: waste 2^{p:+.4f}  list {L0[j]:.4f}  pairs {k0[j - 1][0]:.4f}"
          f"   | filtered: pairs passing {k1[j - 1][1]:.4f} (list {L1[j]:.4f})")

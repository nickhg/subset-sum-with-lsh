"""handoff16b items 1 and 3: re-cost the logged HKLS optima with type-class filters on the representation coordinates.

HKLS level cost (estimator.py, lsh_cost):  log R_lsh + log lsh_dim + log2(S + N_col),  N_col = S^2 p_col / 2
(value near-collisions, weight-checked afterwards).  Product bucket (value-LSH bucket x type-class label filter):
    log R_lsh + log lsh_dim + log2( S * 2^{a d} + N_col * 2^{-b d} )
    a = I(XY;L) - min(I(X;L), I(Y;L))   (filters per vector),   b = I(X;L) + I(Y;L) - I(XY;L)   (saving on pairs)
in per-coordinate units from gen_lsf.filter_terms, times the guessing dimension d.  Valid pairs keep Theta(1)
common filters (amplify by a poly factor, ignored here).
Split law at a merge (HKLS Lemma 1, written additively x + y = z with y = -s'_r): parent weight w (w/2 of each sign)
into children of weight w': nonzero parent digits go to x or to y with probability 1/2 each; (w' - w/2) parent zeros
become (1,-1) or (-1,1).
CAVEAT: the lists have only 5-26 nonzeros in d ~ 2000-6600 coordinates, so the asymptotic type-class exponents are
optimistic at these sizes. Fixed-parameter re-costing only: no re-optimisation over beta, d, w (that needs the
estimator's full search).
usage: filtered_hkls.py logs/16_1450_64_2.txt [...]
"""
import sys, os, re, ast
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np, warnings
from scipy.optimize import minimize
from gen_lsf import Model, Hv
warnings.filterwarnings("ignore")
M = Model([-1, 0, 1]); NF = M.nfilt
_cache = {}


def lev_for(d, w, wn):
    c = wn - w / 2
    tau = np.zeros(M.T)
    for t, (x, y) in enumerate(M.types):
        if (x, y) in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            tau[t] = w / (4 * d)
        elif (x, y) in ((1, -1), (-1, 1)):
            tau[t] = c / (2 * d)
        elif (x, y) == (0, 0):
            tau[t] = 1 - w / d - c / d
    child = np.array([wn / (2 * d), 1 - wn / d, wn / (2 * d)])
    return dict(tau=tau, H=Hv(child))


def best_filter(d, w, wn, delta):
    """min over filters of log2(2^{a d} + 2^{delta - b d}) where delta = log N_col - log S."""
    key = (d, w, wn, round(delta, 1))
    if key in _cache:
        return _cache[key]
    L = lev_for(d, w, wn)
    def f(z):
        r12, r1, r2, ex = M.filter_terms(L, z)
        a = (r12 - min(r1, r2)) * d; b = -ex * d
        return np.logaddexp2(a, delta - b), a, b
    best = (np.logaddexp2(0, delta), 0.0, 0.0, None)        # no filter
    rng = np.random.default_rng(0)
    for s in range(6):
        z0 = rng.normal(0, 1.5, NF)
        r = minimize(lambda z: f(z)[0], z0, method="Nelder-Mead", options=dict(maxiter=4000, xatol=1e-6, fatol=1e-8))
        v, a, b = f(r.x)
        if v < best[0]:
            best = (v, a, b, r.x)
    _cache[key] = best
    return best


def parse(path):
    txt = open(path).read()
    final = float(re.search(r"Final Cost: ([\d.]+)", txt).group(1))
    lat = ast.literal_eval(re.search(r"'lat': (\{.*?\})", txt).group(1))
    vals = {}
    for k in ("w", "R_lsh", "lsh_dim", "log_S", "log_p_col", "log_cost_list", "log_cost_lsh", "log_p_sp", "log_p_ncf"):
        m = re.search(r"- '" + k + r"': (\[.*?\])", txt)
        vals[k] = ast.literal_eval(m.group(1).replace("-inf", "None").replace("'-'", "None")) if m else None
    guess = float(re.search(r"'guess_cost': ([\d.]+)", txt).group(1))
    p_hw = float(re.search(r"'log_p_hw': ([-\d.]+)", txt).group(1))
    return final, lat, vals, guess, p_hw


for path in sys.argv[1:]:
    final, lat, v, guess, p_hw = parse(path)
    d = lat["d"]; w = v["w"]; t = len(w) - 1
    print(f"== {os.path.basename(path)}: final {final}  lat {lat['cost']}  guess {guess}  d {d}  w {w}")
    tot_old, tot_new = [], []
    for i in range(1, t + 1):
        S = v["log_S"][i]; pc = v["log_p_col"][i]; Rl = v["R_lsh"][i]; dim = v["lsh_dim"][i]
        lst = v["log_cost_list"][i]; old = v["log_cost_lsh"][i]
        if pc is None:                                      # no near-collision step at this level (top, t=1)
            tot_old += [old, lst]; tot_new += [old, lst]
            print(f"  level {i}: no LSH collisions logged; unchanged ({old})"); continue
        logN = 2 * S + pc - 1
        val, a, b, _ = best_filter(d, w[i - 1], w[i], logN - S)
        new = np.log2(Rl) + np.log2(dim) + S + val
        tot_old += [old, lst]; tot_new += [new, lst]
        print(f"  merge {i}->{i - 1}: weights {w[i]}->{w[i - 1]}  log S {S:.2f}  log N_col {logN:.2f}  "
              f"cost {old:.2f} -> {new:.2f}  (filters/vector 2^{a:.2f}, pair saving 2^-{b:.2f})")
    logp = sum(x for x in v["log_p_ncf"][1:] if x is not None) + sum(x for x in v["log_p_sp"][1:] if x is not None)
    g_old = np.log2(sum(2.0 ** x for x in tot_old)) - logp
    g_new = np.log2(sum(2.0 ** x for x in tot_new)) - logp
    print(f"  guess cost {g_old:.2f} (logged {guess}) -> {g_new:.2f};  final at fixed params "
          f"{max(lat['cost'], g_old) - p_hw:.2f} -> {max(lat['cost'], g_new) - p_hw:.2f} (lattice side {lat['cost']})")

"""Optimise the {-1,0,1,2} tree under BBSS accounting (lp2), with ('f') or without ('p') LSF.
usage: bbss2_opt.py seed p|f [bcj]"""
import sys; sys.path.insert(0, '/home/claude/work')
import numpy as np, warnings; warnings.filterwarnings("ignore")
from scipy.optimize import minimize
from bbss_lsf import *

k = 3; seed = int(sys.argv[1]); use_f = sys.argv[2] == 'f'; mask = np.ones((k, 3))
tag = sys.argv[2] + (sys.argv[3] if len(sys.argv) > 3 else '')
if len(sys.argv) > 3 and sys.argv[3] == 'bcj':
    mask[:, 1:] = 0
rng = np.random.default_rng(seed)


def to_raw(efg):
    lev = tree(efg, raw=False); par = {0: .5, 1: .5}; raw = []
    lg = lambda p: np.log(max(p, 1e-9) / max(1 - p, 1e-9))
    for j, (e, f, g) in enumerate(efg):
        raw += [lg(e / (par.get(0, 0) / 2)),
                lg(f / (par.get(1, 0) / 2)) if par.get(1, 0) > 0 else -20,
                lg(g / par.get(2, 0)) if par.get(2, 0) > 0 else -20]
        par = lev[j + 1]['child']
    return np.array(raw)


def f(z):
    p = np.where(mask > 0, z[:3 * k].reshape(k, 3), -60.0)
    fl = [z[3 * k + NPAR * j:3 * k + NPAR * (j + 1)] for j in range(k)] if use_f else None
    return lp2([tuple(r) for r in p], fl)[0]


z0 = to_raw(efg_from_types([(0.0340, 0.0041, 1 / 4), (0.0311, 0.0006, 1 / 8), (0.0202, 0.0001, 1 / 16)]))
z0 = z0 + rng.normal(0, 0.3, 3 * k) * (seed > 0)
if use_f:
    z0 = np.concatenate([z0, rng.normal(0, 0.3, NPAR * k)])
best = (f(z0), z0); print("start", round(best[0], 5), flush=True)
for t in range(80):
    z = best[1] + (np.concatenate([rng.normal(0, 0.1, 3 * k), rng.normal(0, 0.3, len(z0) - 3 * k)]) if t > 0 else 0)
    r = minimize(f, z, method='Powell', options=dict(maxiter=30000, xtol=1e-7, ftol=1e-11))
    r = minimize(f, r.x, method='Nelder-Mead', options=dict(maxiter=10000, xatol=1e-8, fatol=1e-12))
    if r.fun < best[0] - 1e-9:
        best = (r.fun, r.x); np.save(f'bbss2_{tag}_{seed}.npy', best[1])
    print(t, round(r.fun, 5), "best", round(best[0], 5), flush=True)

"""Filters added to the best unfiltered Meet-LWE point at fixed split laws (only the filter laws optimised).
usage: ml_fixed_law.py omega d [restarts]     (point from points/w{omega}_d{d}_p.npy)"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, warnings; warnings.filterwarnings("ignore")
from scipy.optimize import minimize
from meetlwe_model import TModel
from ml_worker import T_of
from ml_recost import cost
om, d = sys.argv[1], int(sys.argv[2]); R = int(sys.argv[3]) if len(sys.argv) > 3 else 8
M = TModel([-1, 0, 1], float(om)); zp = np.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "points", f"w{om}_d{d}_p.npy"))[:d * M.nsplit]
f = lambda F: T_of(M, np.concatenate([zp, F]), d, True); rng = np.random.default_rng(0)
b = (f(np.zeros(d * M.nfilt)), np.zeros(d * M.nfilt))
for r in range(R):
    x = minimize(f, rng.normal(0, 1, d * M.nfilt), method="Powell", options=dict(maxiter=20000))
    x = minimize(f, x.x, method="Nelder-Mead", options=dict(maxiter=10000))
    if x.fun < b[0]: b = (x.fun, x.x)
    print(f"restart {r}: {x.fun:.6f} best {b[0]:.6f}", flush=True)
Tr = cost(np.concatenate([zp, b[1]]), [-1, 0, 1], d, float(om), True)[0]
print(f"omega {om} d {d}: unfiltered {T_of(M, zp, d, False):.6f}  filters at fixed split laws {b[0]:.6f}  (recost {Tr:.6f})")

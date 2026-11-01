import warnings; warnings.filterwarnings('ignore')
import sys; sys.path.insert(0, '..')
import numpy as np
from bcj_lsf import lp, opt_filters, opt_eps
rng = np.random.default_rng(1)
eps = [0.0274, 0.0203, 0.0053]
print("plain at wc eps", round(lp(eps, None)[0], 5), flush=True)
filters = [rng.normal(0, 0.1, 8) for _ in range(3)]
for it in range(4):
    filters = opt_filters(eps, filters, rng, rounds=2)
    T, eps = opt_eps(3, filters, starts=[eps])
    print(it, "T with LSF", round(T, 5), "eps", np.round(eps, 4), flush=True)

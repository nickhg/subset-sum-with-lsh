"""May's Rep-1 (ePrint 2021/216, Sec. 7) costed directly from his formulas in eps notation, independent of our tree model.
  w_j = w_{j-1}/2 + eps_j (per sign),  R_j = 2 w_{j-1} + (1 - 2 w_{j-1}) H(eps_j/z, eps_j/z, .),  S_j = H(w_j, w_j, .)
  L_j = S_j - R_j (r_j = log_q R_j),  T^(0) = 2 L_1 - 1,  T^(j) = 2 L_{j+1} - (R_j - R_{j+1}),  leaves S_d / 2
usage: may_rep1.py omega   (optimises 3, 4, 5 constrained levels = May depths 4, 5, 6)"""
import sys
import numpy as np
from scipy.optimize import minimize

def H(*p):
    p = np.array([x for x in p if x > 0]); return float(-(p * np.log2(p)).sum())

def may(om, eps):
    w = [om / 2]; R = [None]; S = [None]
    for e in eps:
        wp = w[-1]; z = 1 - 2 * wp
        R.append(2 * wp + z * H(e / z, e / z, 1 - 2 * e / z)); wj = wp / 2 + e; w.append(wj); S.append(H(wj, wj, 1 - 2 * wj))
    d = len(eps); L = [None] + [S[j] - R[j] for j in range(1, d + 1)]
    return max([2 * L[1] - 1] + [2 * L[j + 1] - (R[j] - R[j + 1]) for j in range(1, d)] + [S[d] / 2] + L[1:])

if __name__ == "__main__":
    om = float(sys.argv[1]); rng = np.random.default_rng(1)
    for k in (3, 4, 5):
        best = (9, None)
        for r in range(40):
            x0 = np.sort(rng.uniform(0, 0.1, k))[::-1]
            res = minimize(lambda e: may(om, list(np.clip(e, 1e-9, 0.24))), x0, method="Nelder-Mead",
                           options=dict(maxiter=20000, xatol=1e-10, fatol=1e-12))
            if res.fun < best[0]: best = (res.fun, np.clip(res.x, 1e-9, 0.24))
        print(f"omega {om}: May depth {k + 1}: T = {best[0]:.5f}  eps {np.round(best[1], 4)}", flush=True)

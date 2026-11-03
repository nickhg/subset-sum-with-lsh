"""Adaptive basin-hopping worker for the filtered {-1,0,1,2} tree (gen_lsf.Model, BBSS accounting, filters on).

Many workers share one results directory.  Each worker owns one depth d and loops until its time limit:
  start = the best point known for depth d (any worker), or, with probability GRAFT, the best depth-(d-1) point
          grafted to depth d (a copy of one level inserted; the best insertion position is used)
  start is canonicalised (logits re-expressed with bounded magnitude, same probabilities up to 1e-12) and jittered
  with a scale drawn from JIT; then Powell + Nelder-Mead as in gen_opt.py.
A strict improvement on the worker's own best is saved as  RES/d{d}_T{T:.6f}_w{worker}.npy  (T in the name, so the
best for a depth is found by listing files).  Seed points can be dropped into RES with the same naming.
usage: polish_worker.py RES depth worker_id hours [seed]
"""
import sys, os, glob, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np, warnings
from scipy.optimize import minimize
from gen_lsf import Model
warnings.filterwarnings("ignore")

D = [-1, 0, 1, 2]; M = Model(D); NS, NF = M.nsplit, M.nfilt
GRAFT = 0.25; JIT = (0.1, 0.3, 0.6, 1.0, 2.0); CLIP = 1e-12


def T_of(z, d):
    P = z[:d * NS].reshape(d, NS); F = list(z[d * NS:d * (NS + NF)].reshape(d, NF))
    return M.lp(P, F)[0]


def _logits(p, ref):
    p = np.maximum(p, CLIP); p = p / p.sum(); return np.log(p / p[ref])


def canon(z, d):
    """same split and filter laws, logits of bounded size (|logit| <= log(1/CLIP) ~ 27.6)"""
    P = z[:d * NS].reshape(d, NS).copy(); F = z[d * NS:d * (NS + NF)].reshape(d, NF).copy()
    for j in range(d):
        i = 0
        for dg in M.D:
            nl = len(M.upairs[dg]) - 1
            if nl:
                row = np.concatenate([[0.0], P[j, i:i + nl]]); e = np.exp(row - row.max())
                P[j, i:i + nl] = _logits(e / e.sum(), 0)[1:]; i += nl
        pi, cond = M.filt(F[j]); F[j, 0] = _logits(pi, 2)[0]; i = 1
        for t in M.sym:
            F[j, i] = _logits(cond[t], 2)[0]; i += 1
        for t in M.asym:
            F[j, i:i + 2] = _logits(cond[t], 2)[:2]; i += 2
    return np.concatenate([P.ravel(), F.ravel()])


def graft(z, d0):
    """depth d0 -> d0+1 by duplicating one level; returns the best of the d0 insertion positions"""
    P = z[:d0 * NS].reshape(d0, NS); F = z[d0 * NS:d0 * (NS + NF)].reshape(d0, NF); best = (9.0, None)
    for j in range(d0):
        z1 = np.concatenate([np.insert(P, j, P[j], 0).ravel(), np.insert(F, j, F[j], 0).ravel()])
        T = T_of(z1, d0 + 1)
        if T < best[0]:
            best = (T, z1)
    return best


def best_known(res, d):
    fs = glob.glob(os.path.join(res, f"d{d}_T*.npy"))
    if not fs:
        return 9.0, None
    f = min(fs, key=lambda s: float(s.split("_T")[1].split("_")[0]))
    try:
        z = np.load(f); return T_of(z, d), z
    except Exception:
        return 9.0, None


if __name__ == "__main__":
    res, d, wid, hours = sys.argv[1], int(sys.argv[2]), sys.argv[3], float(sys.argv[4])
    seed = int(sys.argv[5]) if len(sys.argv) > 5 else abs(hash(wid)) % 2 ** 31
    rng = np.random.default_rng(seed); t_end = time.time() + 3600 * hours; mine = 9.0; it = 0
    f = lambda z: T_of(z, d)
    while time.time() < t_end:
        Tb, zb = best_known(res, d); src = "best"
        if (zb is None or rng.random() < GRAFT) and d > 1:
            Tg, zg = best_known(res, d - 1)
            if zg is not None:
                Tg, zg = graft(zg, d - 1)
                if zb is None or rng.random() < 0.5 or Tg < Tb:
                    Tb, zb, src = Tg, zg, "graft"
        if zb is None:
            time.sleep(60); continue
        mine = min(mine, Tb) if src == "best" else mine
        s = JIT[rng.integers(len(JIT))]
        z = canon(zb, d); z = z + rng.normal(0, s, len(z)) * (rng.random(len(z)) < 0.5)   # jitter half the coords
        r = minimize(f, z, method="Powell", options=dict(maxiter=40000, xtol=1e-7, ftol=1e-11))
        r = minimize(f, r.x, method="Nelder-Mead", options=dict(maxiter=10000, xatol=1e-8, fatol=1e-12))
        it += 1
        print(f"{time.strftime('%H:%M:%S')} d{d} w{wid} it {it} from {src} {Tb:.6f} jit {s}: {r.fun:.6f}", flush=True)
        if r.fun < min(mine, Tb) - 1e-7:
            mine = r.fun
            np.save(os.path.join(res, f"d{d}_T{r.fun:.6f}_w{wid}.npy"), r.x)
            print(f"   NEW d{d} {r.fun:.6f}", flush=True)

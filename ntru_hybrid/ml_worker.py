"""Shared-directory basin-hopping worker for the Meet-LWE tree (wc handoff25); cf. cloud/polish_worker.py.
Rep-1-type ternary root of weight omega, digit set {-1,0,1}, May accounting (c_j <= rho_j), asymptotic, guessing ignored.

Each worker owns one key (omega, d, p|f) and loops until its time limit.  Start points (best over all workers, read
from RES/w{omega}_d{d}_{p|f}_T{T}_w{id}.npy):
  own key best;  trivial extension of the (omega, d-1, same) best (exact copy);  nested seed = (omega, d-1) best plus a
  bottom level copied from its last level with split probabilities scaled by 0.5/1/1.5;  for f: the (omega, d, p) best
  with all-zero filter logits (exact copy).  The lowest-T start is used with prob. 0.75, otherwise a random other one.
Then canonicalise, jitter (scale from JIT, half the coordinates), Powell + Nelder-Mead; save strict improvements.
usage: ml_worker.py RES omega d p|f worker_id hours [seed]
"""
import sys, os, glob, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np, warnings
from scipy.optimize import minimize
from meetlwe_model import TModel, lp
from ml_hop import canon
warnings.filterwarnings("ignore")
JIT = tuple(float(x) for x in os.environ.get("JIT", "0.1,0.3,0.6,1.0,2.0,3.0").split(","))


def key(om, d, f):
    return f"w{om}_d{d}_{'f' if f else 'p'}"


def T_of(M, z, d, filt):
    ns, nf = M.nsplit, M.nfilt; P = z[:d * ns].reshape(d, ns)
    F = [z[d * ns + nf * j:d * ns + nf * (j + 1)] for j in range(d)] if filt else None
    try:
        return lp(M, M.tree(P), d, "may", F)[0]
    except Exception:
        return 9.0


def best_file(res, k):
    fs = glob.glob(os.path.join(res, k + "_T*.npy"))
    if not fs:
        return None
    return min(fs, key=lambda s: float(s.split("_T")[1].split("_")[0]))


def starts(M, res, om, d, filt, rng):
    ns, nf = M.nsplit, M.nfilt; out = []
    def load(k):
        f = best_file(res, k)
        return np.load(f) if f else None
    z = load(key(om, d, filt))
    if z is not None:
        out.append(z)
    zp = load(key(om, d - 1, filt)) if d > 1 else None
    if zp is not None:
        P = zp[:(d - 1) * ns].reshape(d - 1, ns); F = zp[(d - 1) * ns:].reshape(d - 1, nf) if filt else None
        out.append(np.concatenate([np.vstack([P, np.full((1, ns), -27.6)]).ravel()] +
                                  ([np.vstack([F, np.zeros((1, nf))]).ravel()] if filt else [])))
        sc = rng.choice([0.5, 1.0, 1.5]); pr = 1 / (1 + np.exp(-P[-1])); row = np.log(np.clip(pr * sc, 1e-12, 1 - 1e-12) /
                                                                                        np.clip(1 - pr * sc, 1e-12, 1))
        out.append(np.concatenate([np.vstack([P, row]).ravel()] + ([np.vstack([F, F[-1:]]).ravel()] if filt else [])))
    if filt:
        zu = load(key(om, d, False))
        if zu is not None:
            out.append(np.concatenate([zu[:d * ns], np.zeros(d * nf)]))
    return out


if __name__ == "__main__":
    res, om, d, filt, wid, hours = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]), sys.argv[4] == "f", sys.argv[5], float(sys.argv[6])
    rng = np.random.default_rng(int(sys.argv[7]) if len(sys.argv) > 7 else abs(hash(wid)) % 2 ** 31)
    M = TModel([-1, 0, 1], om); f = lambda z: T_of(M, z, d, filt); k = key(om, d, filt)
    t_end = time.time() + 3600 * hours; mine = 9.0; it = 0
    while time.time() < t_end:
        cand = [(f(z), z) for z in starts(M, res, om, d, filt, rng)]
        if not cand:                                            # nothing yet: random start
            z = np.concatenate([rng.normal(-2, 1.0, d * M.nsplit)] + ([rng.normal(0, 0.5, d * M.nfilt)] if filt else []))
            cand = [(f(z), z)]
        cand.sort(key=lambda c: c[0]); Tb, zb = cand[0] if rng.random() < 0.75 or len(cand) == 1 else cand[rng.integers(1, len(cand))]
        if Tb < mine - 1e-7:                                    # a copy/extension beats our best: record it
            mine = Tb; np.save(os.path.join(res, f"{k}_T{Tb:.6f}_w{wid}.npy"), zb)
        s = JIT[rng.integers(len(JIT))]; z = canon(M, zb, d, filt)
        z = z + rng.normal(0, s, len(z)) * (rng.random(len(z)) < 0.5)
        r = minimize(f, z, method="Powell", options=dict(maxiter=40000, xtol=1e-7, ftol=1e-11))
        r = minimize(f, r.x, method="Nelder-Mead", options=dict(maxiter=10000, xatol=1e-8, fatol=1e-12)); it += 1
        print(f"{time.strftime('%H:%M:%S')} {k} w{wid} it {it} from {Tb:.6f} jit {s}: {r.fun:.6f}", flush=True)
        if r.fun < min(mine, Tb) - 1e-7:
            mine = r.fun; np.save(os.path.join(res, f"{k}_T{r.fun:.6f}_w{wid}.npy"), r.x)
            print(f"   NEW {k} {r.fun:.6f}", flush=True)

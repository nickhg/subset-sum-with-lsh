"""Basin hopping for the Meet-LWE tree (meetlwe_model, May accounting), as cloud/polish_worker.py for subset sum:
canonicalise the logits (same laws, bounded size), jitter, Powell + Nelder-Mead; seeds from runs/ml_* and from trivial
bottom-level extensions of the depth-(d-1) best.  Writes runs/hop_w{omega}_d{d}_{p|f}.npy and prints improvements.
usage: ml_hop.py omega d p|f hours [seed]
"""
import sys, os, glob, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np, warnings
from scipy.optimize import minimize
from meetlwe_model import TModel, lp
warnings.filterwarnings("ignore")
D = [-1, 0, 1]; CLIP = 1e-12; JIT = (0.1, 0.3, 0.6, 1.0, 2.0, 3.0)
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "runs")


def T_of(M, z, d, filt):
    ns, nf = M.nsplit, M.nfilt; P = z[:d * ns].reshape(d, ns)
    F = [z[d * ns + nf * j:d * ns + nf * (j + 1)] for j in range(d)] if filt else None
    return lp(M, M.tree(P), d, "may", F)[0]


def lg(p, ref):
    p = np.maximum(p, CLIP); p = p / p.sum(); return np.log(p / p[ref])


def canon(M, z, d, filt):
    ns, nf = M.nsplit, M.nfilt; P = z[:d * ns].reshape(d, ns).copy()
    for j in range(d):
        i = 0
        for dg in M.D:
            nl = len(M.upairs[dg]) - 1
            if nl:
                row = np.concatenate([[0.0], P[j, i:i + nl]]); e = np.exp(row - row.max())
                P[j, i:i + nl] = lg(e / e.sum(), 0)[1:]; i += nl
    out = [P.ravel()]
    if filt:
        F = z[d * ns:d * (ns + nf)].reshape(d, nf).copy()
        for j in range(d):
            pi, cond = M.filt(F[j]); F[j, 0] = lg(pi, 2)[0]; i = 1
            for t in M.sym:
                F[j, i] = lg(cond[t], 2)[0]; i += 1
            for t in M.asym:
                F[j, i:i + 2] = lg(cond[t], 2)[:2]; i += 2
        out.append(F.ravel())
    return np.concatenate(out)


def seeds(M, om, d, filt):
    ns, nf = M.nsplit, M.nfilt; n = d * ns + (d * nf if filt else 0); out = []
    for f in glob.glob(os.path.join(R, f"*_w{om}_*.npy")):
        b = os.path.basename(f)
        if "-2" in b: continue
        try:
            dd = int(b.split("_d")[1].split("_")[0]); z = np.load(f); ff = b.endswith("_f.npy")
        except Exception:
            continue
        if dd not in (d, d - 1): continue
        P = z[:dd * ns].reshape(dd, ns); F = z[dd * ns:dd * (ns + nf)].reshape(dd, nf) if ff else np.zeros((dd, nf))
        if dd == d - 1:                                    # trivial bottom level
            P = np.vstack([P, np.full((1, ns), -27.6)]); F = np.vstack([F, np.zeros((1, nf))])
        zz = np.concatenate([P.ravel()] + ([F.ravel()] if filt else []))
        if len(zz) == n:
            out.append(zz)
    return out


if __name__ == "__main__":
    om, d, filt, hours = float(sys.argv[1]), int(sys.argv[2]), sys.argv[3] == "f", float(sys.argv[4])
    rng = np.random.default_rng(int(sys.argv[5]) if len(sys.argv) > 5 else 0); M = TModel(D, om)
    f = lambda z: T_of(M, z, d, filt); best = (9.0, None)
    for z in seeds(M, om, d, filt):
        T = f(z)
        if T < best[0]: best = (T, z)
    if best[1] is None:                                    # no saved point: random start
        z = np.concatenate([rng.normal(-2, 1.0, d * M.nsplit)] + ([rng.normal(0, 0.5, d * M.nfilt)] if filt else []))
        best = (f(z), z)
    tag = f"hop_w{om}_d{d}_{'f' if filt else 'p'}"; print(tag, "start", round(best[0], 6), flush=True)
    t_end = time.time() + 3600 * hours; it = 0
    while time.time() < t_end and best[1] is not None:
        s = JIT[rng.integers(len(JIT))]; z = canon(M, best[1], d, filt)
        z = z + rng.normal(0, s, len(z)) * (rng.random(len(z)) < 0.5)
        r = minimize(f, z, method="Powell", options=dict(maxiter=40000, xtol=1e-7, ftol=1e-11))
        r = minimize(f, r.x, method="Nelder-Mead", options=dict(maxiter=10000, xatol=1e-8, fatol=1e-12)); it += 1
        if r.fun < best[0] - 1e-7:
            best = (r.fun, r.x); np.save(os.path.join(R, tag + ".npy"), r.x)
        print(f"{it} jit {s} {r.fun:.6f} best {best[0]:.6f}", flush=True)

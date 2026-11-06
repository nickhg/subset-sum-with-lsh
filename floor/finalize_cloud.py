"""Post-run check of the cloud polish bests: per depth 4..9 the best point over cloud/results/*/res
and cloud/seed, made monotone by trivial extension (bottom level z -> (z,0), unfiltered; an exact copy), then
  gen_lsf B2 (polish_worker.T_of)  ==  floor/recost.py (independent)  ==  S2 (survival recursion), plus corner flags.
Filters whose saving is <= 0 (they do not reduce the pairs examined) are replaced by trivial ones (zero logits: labels
independent of the digits, I = 0) when T is unchanged.
Passing points are copied to floor/runs/polish/gen_m4_{d}_f_cloud.npy for make_numbers.py.
usage: python3 floor/finalize_cloud.py
"""
import sys, os, glob
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(ROOT, "cloud"))
import numpy as np
from polish_worker import T_of, NS, NF, M
from recost import recost
from recursive_floor import evaluate

def triv(z, d):
    P = z[:d * NS].reshape(d, NS); F = z[d * NS:d * (NS + NF)].reshape(d, NF)
    return np.concatenate([np.vstack([P, np.full((1, NS), -27.6)]).ravel(), np.vstack([F, np.zeros((1, NF))]).ravel()])

def tidy(z, d):
    """trivial filter at every merge whose saving is <= 0, if T does not change"""
    T0 = T_of(z, d); z = z.copy()
    for j in range(d):
        P = z[:d * NS].reshape(d, NS); lev = M.tree(P); i0 = d * NS + j * NF
        r12, r1, r2, ex = M.filter_terms(lev[j + 1], z[i0:i0 + NF])
        if -ex <= 1e-9:
            z1 = z.copy(); z1[i0:i0 + NF] = 0.0
            if T_of(z1, d) <= T0 + 1e-9:
                z = z1; print(f"    d{d} merge {j+1}: saving {-ex:+.5f} -> trivial filter")
    return z

prev = None; ok_all = True
for d in range(4, 10):
    fs = glob.glob(os.path.join(ROOT, "cloud", "results", "*", "res", f"d{d}_T*.npy")) + \
         glob.glob(os.path.join(ROOT, "cloud", "seed", f"d{d}_T*.npy")) + \
         glob.glob(os.path.join(HERE, "runs", "polish", f"gen_m4_{d}_f_cloud.npy"))   # stored best (so never worse)
    best = min(((T_of(np.load(f), d), np.load(f), os.path.relpath(f, ROOT)) for f in fs), key=lambda c: c[0])
    if prev is not None:
        zt = triv(prev[1], d - 1); Tt = T_of(zt, d)
        if Tt < best[0] - 1e-9:
            best = (Tt, zt, f"trivial extension of d{d-1}")
    zt = tidy(best[1], d); best = (T_of(zt, d), zt, best[2])
    T, z, src = best; Tr, rows, flags, _ = recost(z, d); Ts = evaluate(M, z, d, "S2")
    Ts = Ts[0] if isinstance(Ts, tuple) else Ts
    ok = abs(T - Tr) < 1e-6 and abs(T - Ts) < 1e-6; ok_all &= ok
    print(f"d{d}: B2 {T:.6f}  recost {Tr:.6f}  S2 {Ts:.6f}  {'OK' if ok else 'MISMATCH'}  from {src}  flags: {'; '.join(flags) or 'none'}", flush=True)
    if ok:
        np.save(os.path.join(HERE, "runs", "polish", f"gen_m4_{d}_f_cloud.npy"), z)
    prev = best
print("all OK" if ok_all else "SOME MISMATCH")

"""wc handoff11b: digit masses and the splits that create -2 / 2, per level, for saved {-2,...,2} B2 points.
usage: digit_mass.py POINT.npy depth [POINT.npy depth ...]"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
from gen_lsf import Model
M = Model([-2, -1, 0, 1, 2]); ns, nf = M.nsplit, M.nfilt
args = sys.argv[1:]
for src, d in zip(args[::2], map(int, args[1::2])):
    z = np.load(src); P = z[:d * ns].reshape(d, ns); F = [z[d * ns + nf * j:d * ns + nf * (j + 1)] for j in range(d)]
    T, x, lev = M.lp(P, F); c = [1.0] + list(x[:d])
    s = [0.0] * (d + 1)
    for j in range(d - 1, 0, -1):
        s[j] = min(0.0, lev[j + 1]["rho"] - c[j + 1] + 2 * s[j + 1])
    print(f"== {os.path.basename(src)}  d={d}  T={T:.5f}  root excess {lev[1]['rho'] - c[1]:+.4f}  2s_1 {2 * s[1]:+.4f}")
    for j in range(1, d + 1):
        ch = lev[j]["child"]; tau = lev[j]["tau"]
        gen = {}
        for t, (a, b) in enumerate(M.types):
            if tau[t] > 1e-7 and (a in (-2, 2) or b in (-2, 2)):
                key = f"{a + b}->({max(a, b)},{min(a, b)})"; gen[key] = gen.get(key, 0) + tau[t]
        g = "  ".join(f"{k}:{v:.5f}" for k, v in sorted(gen.items(), key=lambda kv: -kv[1]))
        print(f"  level {j}: delta(-2) {ch[-2]:.5f}  delta(2) {ch[2]:.5f}  delta(-1) {ch[-1]:.4f}  | splits with +-2: {g}")

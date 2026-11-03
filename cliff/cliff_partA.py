"""wc handoff15 Part A: does the cliff work?  Babai on the reduced knapsack block, given the correct rest x_R.

Block lattice (dimension k+1), rows  (K q, 0, ..., 0)  and  (K a_i, e_i)  for i = 1..k,  q = 2^n, K = scale forcing
exact sums.  A planted x_B in {0,1}^k with residual target t' = <a_B, x_B> mod q gives the lattice vector (K t', x_B);
the target (K t', 1/2, ..., 1/2) is at distance sqrt(k)/2 (error x_B - 1/2 in {+-1/2}^k).  Babai's nearest plane on a
BKZ-b reduced basis succeeds iff the error lies in the GS parallelepiped.
Reports, per (n, k, b): log2 of the smallest GS length (dimensions 1..k, i.e. excluding the scaled sum coordinate),
mean log2 GS (= n/(k+1) + ...), and the Babai success rate over instances.
usage: cliff_partA.py n k_list b [instances] [seed]      e.g.  cliff_partA.py 128 8,16,24,32 20 20
"""
import sys, time
import numpy as np
from fpylll import IntegerMatrix, LLL, BKZ, GSO, FPLLL
from fpylll.algorithms.bkz2 import BKZReduction

n = int(sys.argv[1]); ks = [int(x) for x in sys.argv[2].split(",")]; b = int(sys.argv[3])
inst = int(sys.argv[4]) if len(sys.argv) > 4 else 20; seed = int(sys.argv[5]) if len(sys.argv) > 5 else 0
rng = np.random.default_rng(seed); q = 1 << n
FPLLL.set_precision(n + 64)          # targets are ~2^n with +-1 offsets: 53-bit mpfr loses them


def rand_int(bits):
    return int.from_bytes(rng.bytes((bits + 7) // 8), "little") % (1 << bits)


for k in ks:
    K = 2 * k                      # sum coordinate weighted so that any nonzero sum error dominates
    ok = 0; gs_min = []; gs_mean = []; t_red = 0.0
    for _ in range(inst):
        a = [rand_int(n) for _ in range(k)]
        B = IntegerMatrix(k + 1, k + 1)
        B[0, 0] = K * q
        for i in range(k):
            B[i + 1, 0] = K * a[i]; B[i + 1, i + 1] = 2          # scale by 2 so the centred target is integral
        t0 = time.time()
        LLL.reduction(B)
        if b > 2:
            BKZReduction(B)(BKZ.EasyParam(min(b, k + 1), max_loops=4))
        t_red += time.time() - t0
        M = GSO.Mat(B, float_type="mpfr"); M.update_gso()
        r = [M.get_r(i, i) for i in range(k + 1)]                # squared GS norms
        lg = 0.5 * np.log2(np.array(r, dtype=float))
        gs_min.append(lg.min()); gs_mean.append(lg.mean())
        xB = rng.integers(0, 2, k); tp = sum(int(a[i]) * int(xB[i]) for i in range(k)) % q
        target = [K * tp] + [1] * k                               # (K t', 2 * 1/2, ...)
        v = B.multiply_left([int(c) for c in M.babai(target)])
        ok += int(v[0] == K * tp and all(v[i + 1] == 2 * xB[i] for i in range(k)))
    print(f"n={n} k={k} beta={k / n:.3f} BKZ-{b}: log2 GS_min {np.mean(gs_min):6.2f}  log2 GS_mean {np.mean(gs_mean):6.2f}"
          f"  Babai success {ok}/{inst}  reduction {t_red / inst:.2f}s", flush=True)

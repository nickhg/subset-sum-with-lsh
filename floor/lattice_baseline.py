"""Task 3: lattice baseline at density 1 (centred CJLOSS embedding, fpylll progressive BKZ; no G6K).

Instance (integer, density 1): a_i uniform in [0, 2^n), planted x of weight n/2, t = <a,x> over the integers.
(A modular instance with an extra row (0 | K 2^n) is WRONG here: it puts (0 | K gcd(2t - sum a, 2^n)) and hence
the vectors (2e_i | 0) into the lattice.)
Basis (n+1 rows, integer, centred and scaled by 2):
    row i   = ( 2 e_i      | K a_i )      i = 1..n
    row t   = ( 1 ... 1    | K t   )
sum_i x_i row_i - row_t = (2x - 1 | 0): a {+-1}-vector of norm sqrt(n), the target.
BKZ-30 preprocessing, then enumeration of ALL lattice vectors with norm^2 <= n (the target norm): at density 1
the target lies just beyond the Gaussian heuristic, so SVP alone returns decoys. Counts short vectors by parity.
usage: lattice_baseline.py n [instances] [seed] [max_beta]
"""
import sys, time
import numpy as np
from fpylll import IntegerMatrix, LLL, BKZ, GSO, Enumeration, EnumerationError
from fpylll.algorithms.bkz2 import BKZReduction

n = int(sys.argv[1]); inst = int(sys.argv[2]) if len(sys.argv) > 2 else 5
seed = int(sys.argv[3]) if len(sys.argv) > 3 else 0; max_beta = int(sys.argv[4]) if len(sys.argv) > 4 else 50
rng = np.random.default_rng(seed); N = 1 << n; K = n * 4
BKZ_BETA = 30; MAX_SOLS = 200000


def solved(B, a, t):
    for r in range(B.nrows):
        row = [B[r, j] for j in range(n + 1)]
        if row[n] != 0 or any(abs(v) != 1 for v in row[:n]):
            continue
        for sgn in (1, -1):
            x = [(sgn * v + 1) // 2 for v in row[:n]]
            if sum(ai * xi for ai, xi in zip(a, x)) == t:
                return True
    return False


for i in range(inst):
    a = [int(v) for v in rng.integers(0, 2 ** min(n, 62), n)] if n <= 62 else \
        [int.from_bytes(rng.bytes((n + 7) // 8), "little") % N for _ in range(n)]
    xs = rng.choice(n, n // 2, replace=False); t = sum(a[j] for j in xs)
    B = IntegerMatrix(n + 1, n + 1)
    for r in range(n):
        B[r, r] = 2; B[r, n] = K * a[r]
    for j in range(n):
        B[n, j] = 1
    B[n, n] = K * t
    t0 = time.time(); LLL.reduction(B)
    bkz = BKZReduction(B); beta = min(BKZ_BETA, B.nrows)
    bkz(BKZ.EasyParam(beta, max_loops=8)); t1 = time.time()
    # enumerate every lattice vector with norm^2 <= n (the target has norm^2 = n exactly)
    Mg = GSO.Mat(B); Mg.update_gso()
    enum = Enumeration(Mg, nr_solutions=MAX_SOLS)
    try:
        sols = enum.enumerate(0, B.nrows, n * 1.0001, 0)
    except EnumerationError:
        sols = []
    found = False; by_lam = {}
    for _, coeffs in sols:
        v = B.multiply_left([int(round(c)) for c in coeffs])
        if v[n] != 0:
            continue
        odd = v[0] % 2 != 0
        if odd and all(abs(e) == 1 for e in v[:n]):
            for sgn in (1, -1):
                x = [(sgn * e + 1) // 2 for e in v[:n]]
                if sum(ai * xi for ai, xi in zip(a, x)) == t:
                    found = True
        key = "odd(lam=+-1,..)" if odd else "even(lam=0,+-2,..)"
        by_lam[key] = by_lam.get(key, 0) + 1
    print(f"n={n} inst={i}: BKZ-{beta} {t1 - t0:.1f}s, enum {time.time() - t1:.1f}s  short vectors (up to sign) "
          f"{len(sols)} {by_lam}  solution found: {found}", flush=True)

"""Task 4 model: build a representation-tree node list by lattice enumeration of its coset instead of merging.

Node list = {x in {0,1}^n of weight p n : <a,x> = tau mod M},  log2 M = m n.  As a lattice problem: all points of the
coset lattice {y : <a,y> = tau mod M} (det 2^{mn}, full dimension n) within centred radius^2 = p(1-p) n of p*1.
  true list         2^{(h(p) - m) n}
  lattice points    2^{(max(GH, MO) - m) n}: GH = 1/2 log2(2 pi e p(1-p)); MO = Mazo-Odlyzko count of Z^n points
                                  in the ball (dominates for sparse p, where GH undercounts)
  ball / GH radius  2^{(1/2 log2(2 pi e p(1-p)) - m)}     (> 1 whenever the list is exponentially large)
Cost of option (b) >= max(sieve preprocessing in dimension n, number of lattice points in the ball):
  classical sieve (BDGL): 2^{0.292 n} time, 2^{0.2075 n} memory.
A node is only worth building by (b) if that beats merging AND the tree target (0.2793 / BCJ 0.291 / HGJ 0.337).
"""
import numpy as np
from scipy.optimize import minimize_scalar


def mazo_odlyzko(p):
    """(1/n) log2 #{y in Z^n : |y - p*1|^2 <= p(1-p) n}, saddle point min_t [t r^2 + log theta_p(t)]."""
    r2 = p * (1 - p); ks = np.arange(-30, 31)
    f = lambda t: (t * r2 + np.log(np.exp(-t * (ks - p) ** 2).sum())) / np.log(2)
    return minimize_scalar(f, bounds=(1e-6, 200), method="bounded").fun

h = lambda p: -p * np.log2(p) - (1 - p) * np.log2(1 - p)
SIEVE_T, SIEVE_M = 0.292, 0.2075
print(f"{'p':>6} {'h(p)':>7} {'lattice exp':>12} {'decoy excess':>13}   cost(b) = max(0.292, latt - m) for m = 0.3 .. 0.7")
for p in (1 / 2, 1 / 4, 1 / 5, 1 / 8, 1 / 16):
    lat = max(0.5 * np.log2(2 * np.pi * np.e * p * (1 - p)), mazo_odlyzko(p))   # GH vs Z^n point count
    row = "  ".join(f"m={m:.1f}:{max(SIEVE_T, lat - m):.3f}" for m in (0.3, 0.4, 0.5, 0.6, 0.7))
    print(f"{p:6.4f} {h(p):7.4f} {lat:12.4f} {lat - h(p):13.4f}   {row}")
print("\nEvery option-(b) cost is >= 0.292 > 0.2793 (BBSS + filters) and > 0.2909 (BCJ): a full-dimension lattice step "
      "cannot appear in a tree that beats the current best, whatever level or modulus.")
print("A gain would need a lattice step in dimension beta*n < n (a block hybrid): sieve cost 0.292*beta.")
for beta in (0.5, 0.75, 0.9, 0.95):
    print(f"  beta = {beta}: sieve cost {0.292 * beta:.4f} n")

# ---- Block hybrid (wc handoff2 C): guess (1-beta)n coordinates, batch-CVPP on the beta*n block -------------------
# Block lattice {y in Z^m : <a_B,y> = 0 mod 2^n}, m = beta n, det 2^n.  Centred target distance sqrt(m)/2, so
#   target / GH = sqrt(2 pi e)/2 * 2^{-1/beta} = 2.066 * 2^{-1/beta}      (1.033 at beta = 1; < 1 for beta < 0.954)
# Ducas-Laarhoven-van Woerden, randomized slicer (PKC 2020, ePrint 2020/120), Heuristic claim 4:
#   a batch of >= 2^{0.058 m} CVP instances on one lattice costs 2^{0.292 m} time, 2^{0.208 m} memory in total
#   (amortised 2^{0.234 m} each; preprocessing = one sieve, 2^{0.292 m}).
# Guesses: all 2^{(1-beta) n} completions of the guessed block (no constraint to exploit) -> one CVP each.
#   T(beta) = max(0.292 beta, (1 - beta) + 0.234 beta); for (1-beta) < 0.058 beta the batch is too small for the
#   0.234 amortisation but the whole batch still fits in the one 2^{0.292 m} run, so T = 0.292 beta there.
print("\nBlock hybrid (guess (1-beta)n coords, batch-CVPP on beta*n block; DLvW 2020 slicer):")
for beta in (0.90, 0.93, 0.9452, 0.95, 0.97, 1.0):
    T = max(0.292 * beta, (1 - beta) + 0.234 * beta); ratio = np.sqrt(2 * np.pi * np.e) / 2 * 2 ** (-1 / beta)
    print(f"  beta {beta:.4f}: T {T:.4f}  memory {0.208 * beta:.4f}  target/GH {ratio:.3f}  "
          f"batch ok {(1 - beta) >= 0.058 * beta - 1e-4}")
b = 1 / 1.058
print(f"  optimum beta = 1/1.058 = {b:.4f}: T = 0.292/1.058 = {0.292 * b:.4f}, memory {0.208 * b:.4f}"
      "  (beats BBSS 0.2829, not BBSS + deep filters 0.2734)")

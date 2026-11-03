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

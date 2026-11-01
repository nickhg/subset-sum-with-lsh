"""HGJ-style representation tree of depth k, asymptotic exponents (all /n).

Level j (1..k): 2^j lists of x in {0,1}^n with weight w_j = 2^-(j+1),
constrained on the low l_j*n bits of <a,x> (nested: l_k <= ... <= l_1 <= l_0 = 1).

  list size        s_j = h(w_j) - l_j
  rep condition    l_j <= 2 w_j          (log C(2w_j n, w_j n)/n = 2 w_j)
  merge output     o_j = 2 s_j - (l_{j-1} - l_j)   pairs matching parent constraint
  disjoint share   p_j = log Pr[two random weight-w_j vectors are disjoint]
  base lists       Schroeppel-Shamir/MITM over position halves: 0.5 h(w_k)

Modes for the cost of the merge at level j:
  'plain'  : max(s_j, o_j)                (HGJ: enumerate all matching pairs)
  'oracle' : max(s_j, o_j + p_j)          (perfect disjointness filter: only pay for
                                           disjoint pairs - a LOWER bound on any LSH)
"""
import numpy as np
from scipy.optimize import linprog
from math import log2


def h(x):
    return 0.0 if x <= 0 or x >= 1 else -x * log2(x) - (1 - x) * log2(1 - x)


def logp_disjoint(w):
    # log2 [C(n-wn, wn) / C(n, wn)] / n
    return (1 - w) * h(w / (1 - w)) - h(w)


def solve(k, mode):
    w = [2.0 ** -(j + 1) for j in range(k + 1)]  # w[0]=1/2 is the solution weight
    nv = k + 1  # vars: l_1..l_k, T  (index j-1 for l_j, k for T)
    T = k
    A, b = [], []

    def row(coeffs, rhs):  # sum coeffs*vars <= rhs
        r = np.zeros(nv)
        for i, c in coeffs:
            r[i] += c
        A.append(r); b.append(rhs)

    L = lambda j: j - 1  # var index of l_j
    for j in range(1, k + 1):
        # nesting l_j <= l_{j-1}
        if j >= 2:
            row([(L(j), 1), (L(j - 1), -1)], 0)
        row([(L(j), 1)], 2 * w[j])                       # reps
        # T >= s_j = h(w_j) - l_j   ->  -l_j - T <= -h(w_j)
        row([(L(j), -1), (T, -1)], -h(w[j]))
        # o_j = 2h(w_j) - 2l_j - l_{j-1} + l_j = 2h - l_j - l_{j-1}
        extra = logp_disjoint(w[j]) if mode == "oracle" else 0.0
        coeffs = [(L(j), -1), (T, -1)]
        rhs = -(2 * h(w[j]) + extra)
        if j == 1:
            rhs += 1.0  # l_0 = 1 is a constant
        else:
            coeffs.append((L(j - 1), -1))
        row(coeffs, rhs)
    # base MITM
    row([(T, -1)], -0.5 * h(w[k]))
    bounds = [(0, 1)] * k + [(0, 1)]
    c = np.zeros(nv); c[T] = 1
    res = linprog(c, A_ub=np.array(A), b_ub=np.array(b), bounds=bounds, method="highs")
    return res.fun, res.x[:k]


if __name__ == "__main__":
    for k in range(1, 8):
        tp, lp = solve(k, "plain")
        to, lo = solve(k, "oracle")
        print(f"depth {k}:  plain {tp:.4f}   perfect-filter {to:.4f}   "
              f"l(plain)={np.round(lp,3)}  l(oracle)={np.round(lo,3)}")

"""Li's TER (ternary representation tree, depth 3), re-optimised with honest 3-list merge cost.

Exactly the paper's model (Information 2025, 16, 887, Sec. 3.1, pp. 12-14):
  l1 = H(1/6+w1, w1) - r1,   l2 = H(1/18+w2, w2) - r2,   l3 = H(1/18+w2, w2)/2
  w1 = e1 + 2 e0,            w2 = e1/3 + 2 e0/3 + E-1 + E1 + 2 E0     (E = level-2 eps)
  2 r1 = log R1,  2 r2 = log R2   (paper's choice r = 1/2 log R;  'relaxed' allows r <= 1/2 log R)
Paper's time (output-size costing):
  max( l3, 2 l3 - r2, 3 l2 - (r1 - r2), 3 l1 - (1 - r1) )
Honest time: a 3-list modular merge must enumerate pairs from two lists and look up the third,
so each 3-way merge costs max(2 l, 3 l - new bits):
  max( l3, 2 l3 - r2, 2 l2, 3 l2 - (r1 - r2), 2 l1, 3 l1 - (1 - r1) )
"""
import numpy as np
from math import log2
from scipy.optimize import minimize


def Hm(*p):  # multinomial entropy with remainder
    p = list(p); p.append(1 - sum(p))
    if min(p) < -1e-12:
        return None
    return -sum(x * log2(x) for x in p if x > 1e-15)


def model(z, relaxed=False):
    e1, e0, E1, E0, Em1 = np.abs(z[:5])
    w1 = e1 + 2 * e0
    w2 = e1 / 3 + 2 * e0 / 3 + Em1 + E1 + 2 * E0
    a = Hm(2 * e1, 2 * e1, 2 * e1, 1 / 3 - 2 * e1, 1 / 3 - 2 * e1)          # 1-coords of e, scaled to n/2
    b = Hm(*([2 * e0] * 6))
    if a is None or b is None:
        return None
    logR1 = a / 2 + b / 2
    A = 1 / 6 + w1; B = 5 / 6 - 2 * w1
    if A <= 0 or B <= 0 or w1 <= 0:
        return None
    c1 = Hm(E1 / A, E1 / A, E1 / A, 1 / 3 - E1 / A, 1 / 3 - E1 / A)
    c0 = Hm(*([E0 / B] * 6))
    cm = Hm(Em1 / w1, Em1 / w1, Em1 / w1, 1 / 3 - Em1 / w1, 1 / 3 - Em1 / w1)
    if None in (c1, c0, cm):
        return None
    logR2 = c1 * A + c0 * B + cm * w1
    H1 = Hm(1 / 6 + w1, w1); H2 = Hm(1 / 18 + w2, w2)
    if H1 is None or H2 is None:
        return None
    if relaxed:
        r1 = min(logR1 / 2, max(0.0, z[5])); r2 = min(logR2 / 2, max(0.0, z[6]))
    else:
        r1, r2 = logR1 / 2, logR2 / 2
    if r2 > r1:
        return None
    l1, l2, l3 = H1 - r1, H2 - r2, H2 / 2
    paper = max(l3, 2 * l3 - r2, 3 * l2 - (r1 - r2), 3 * l1 - (1 - r1))
    honest = max(paper, 2 * l2, 2 * l1)
    return dict(paper=paper, honest=honest, l=(l1, l2, l3), r=(r1, r2), R=(logR1, logR2), w=(w1, w2))


def opt(key, relaxed, starts):
    best = (9, None)
    f = lambda z: (model(z, relaxed) or {key: 9})[key]
    for s in starts:
        r = minimize(f, s, method="Nelder-Mead", options=dict(maxiter=20000, xatol=1e-9, fatol=1e-12))
        if r.fun < best[0]:
            best = (r.fun, r.x)
    return best


if __name__ == "__main__":
    paper_pt = np.array([0.0024, 0.0066, 0.0001, 0.0004, 0.0000])
    m = model(paper_pt)
    print("paper's parameters:  paper-cost %.4f   honest cost %.4f" % (m["paper"], m["honest"]),
          " l =", np.round(m["l"], 4), " logR =", np.round(m["R"], 4))
    rng = np.random.default_rng(0)
    starts = [paper_pt] + [np.abs(rng.normal(0, 0.01, 5)) for _ in range(60)]
    b = opt("paper", False, starts)
    print("re-optimised, paper's costing:   %.4f" % b[0])
    b = opt("honest", False, starts)
    mm = model(b[1])
    print("re-optimised, honest costing:    %.4f   l = %s  eps = %s" % (b[0], np.round(mm["l"], 4), np.round(np.abs(b[1]), 4)))
    starts2 = [np.concatenate([s, [0.3, 0.1]]) for s in starts] + \
              [np.concatenate([np.abs(rng.normal(0, 0.01, 5)), rng.uniform(0, .6, 2)]) for _ in range(60)]
    b = opt("honest", True, starts2)
    mm = model(b[1], True)
    print("honest costing, r <= 1/2 log R:  %.4f   l = %s  r = %s" % (b[0], np.round(mm["l"], 4), np.round(mm["r"], 4)))

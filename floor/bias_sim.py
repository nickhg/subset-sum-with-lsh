"""Does a type-class filter bias which parents survive?  Small-n filtered merge, n = 32.

Shape of the d=4 optimum's level-2 merge (BBSS digits, one (+1,-1) cancellation), at integer sizes:
  children A, B: one -1 and five +1 (exact type)       parent: one -1 and nine +1 (exact type)
  valid pair: no same-sign overlap, exactly one (+1,-1) cross overlap (the cancellation)
  reps per parent R = 2 * 22 * C(9,4) = 5544;  modulus M = R / c  (c = 2 consistent reps per parent)
Lists are complete cosets: L_A = {x : <a,x> = u mod M}, L_B = {y : <a,y> = r - u mod M}, r = <a,S> for a planted
parent S of the exact type.
Filter: codewords lambda in {N,L,R}^n iid pi = (0.657, 0.172, 0.172) (level-2 Q_lambda of the d=4 optimum).
  x in bucket(lambda) iff labels on x's five +1 coords have counts (N,L,R) = (3,2,0) and its -1 coord is labelled R
  (integer rounding of the optimum's A-side conditional laws); B side mirrored (L <-> R).  Zeros unconstrained.
  The rule depends only on the joint (digit, label) counts, i.e. it is permutation invariant, like the real filter.
  K codewords with K * p_pair = 1 (p_pair measured on typical valid pairs).
Measured per draw: sigma = |output| / E[#valid parents with residue r], planted survival, and the class of each
passing pair (which child carries the parent's -1) against the unfiltered split; filter off is the control.
usage: bias_sim.py [draws] [seed]
"""
import sys, itertools
from math import comb
import numpy as np

draws = int(sys.argv[1]) if len(sys.argv) > 1 else 100; seed = int(sys.argv[2]) if len(sys.argv) > 2 else 0
n = 32; R = 2 * 22 * comb(9, 4); Mod = R // 2
PI = np.array([0.6566, 0.1717, 0.1717]); N_, L_, R_ = 0, 1, 2
rng = np.random.default_rng(seed)

plus_c = np.array(list(itertools.combinations(range(n), 5)), dtype=np.int64)          # (201376, 5)
comp = np.array([[i for i in range(n) if i not in set(r)] for r in plus_c], dtype=np.int64)  # (201376, 27)
plus_mask_c = (np.int64(1) << plus_c).sum(1)
E_valid = comb(n, 9) * 23 / Mod                                                       # E #valid parents per residue


def coset(a, res):
    """all children (plus mask, plus idx, minus pos) with <a,x> = res mod Mod."""
    s = (a[plus_c].sum(1)[:, None] - a[comp]) % Mod
    i, k = np.nonzero(s == res)
    return plus_mask_c[i], plus_c[i], comp[i, k]


def pairs_valid(pmA, mA, pmB, mB):
    """boolean matrix (|A|,|B|) of valid pairs and the class (True = A carries the cancellation's +1)."""
    pa, pb = pmA[:, None], pmB[None, :]
    bitA, bitB = (np.int64(1) << mA)[:, None], (np.int64(1) << mB)[None, :]
    same = ((pa & pb) != 0) | (mA[:, None] == mB[None, :])
    crossA = (pa & bitB) != 0            # B's -1 sits on an A +1 (cancellation, A carries +1)
    crossB = (pb & bitA) != 0
    return ~same & (crossA ^ crossB), crossA


def parent_key(pmA, mA, pmB, mB, crossA):
    """encode the parent as (plus mask) * 64 + minus pos."""
    plus = np.where(crossA, (pmA | pmB) & ~(np.int64(1) << mB), (pmA | pmB) & ~(np.int64(1) << mA))
    minus = np.where(crossA, mA, mB)
    return plus * 64 + minus


def member(lab, pidx, mpos, side):
    """membership (K, |L|): +1 coords counts (N,L,R) = (3,2,0) [A] / (3,0,2) [B]; -1 coord labelled R [A] / L [B]."""
    lp = lab[:, pidx]                                       # (K, |L|, 5)
    cN = (lp == N_).sum(2); cL = (lp == L_).sum(2); cR = (lp == R_).sum(2)
    if side == "A":
        return (cN == 3) & (cL == 2) & (cR == 0) & (lab[:, mpos] == R_)
    return (cN == 3) & (cL == 0) & (cR == 2) & (lab[:, mpos] == L_)


# calibrate p_pair on random typical valid pairs (one random parent, all its reps)
def random_parent():
    perm = rng.permutation(n); return np.sort(perm[:9]), perm[9]


lab = rng.choice(3, size=(200000, n), p=PI).astype(np.int8)
ones, m = random_parent(); zeros = [i for i in range(n) if i not in set(ones) and i != m]
hits = 0; tot = 0
for z in zeros[:6]:
    for sub in list(itertools.combinations(ones, 4))[:20]:
        rest = [o for o in ones if o not in sub]
        # class 1: A = parent -1 at m, ones sub + z ; B = ones rest, -1 at z
        a_in = member(lab, np.array([list(sub) + [z]]), np.array([m]), "A")[:, 0]
        b_in = member(lab, np.array([rest]), np.array([z]), "B")[:, 0]
        hits += int((a_in & b_in).sum()); tot += lab.shape[0]
p_pair = hits / tot; K = max(1, int(round(1 / p_pair)))
print(f"n={n} R={R} M={Mod} E|V_parent|/M={E_valid:.0f}  p_pair={p_pair:.3e} -> K={K} codewords", flush=True)

res = []
for dr in range(draws):
    a = rng.integers(0, 2 ** 30, n, dtype=np.int64)
    ones, m = random_parent()
    S_key = int((np.int64(1) << ones.astype(np.int64)).sum()) * 64 + int(m)
    r = int((a[ones].sum() - a[m]) % Mod); u = int(rng.integers(0, Mod))
    pmA, pA, mA = coset(a, u); pmB, pB, mB = coset(a, (r - u) % Mod)
    V, cA = pairs_valid(pmA, mA, pmB, mB)
    ia, ib = np.nonzero(V)
    keys_u = np.unique(parent_key(pmA[ia], mA[ia], pmB[ib], mB[ib], cA[ia, ib]))
    frac_cls_u = cA[ia, ib].mean()
    lab = rng.choice(3, size=(K, n), p=PI).astype(np.int8)
    inA = member(lab, pA, mA, "A"); inB = member(lab, pB, mB, "B")
    out = []; cls = []
    for k in range(K):
        xa = np.nonzero(inA[k])[0]; xb = np.nonzero(inB[k])[0]
        if len(xa) == 0 or len(xb) == 0:
            continue
        Vk = V[np.ix_(xa, xb)]
        if not Vk.any():
            continue
        i2, j2 = np.nonzero(Vk); ga, gb = xa[i2], xb[j2]
        out.append(parent_key(pmA[ga], mA[ga], pmB[gb], mB[gb], cA[ga, gb])); cls.append(cA[ga, gb])
    keys_f = np.unique(np.concatenate(out)) if out else np.zeros(0, np.int64)
    cls = np.concatenate(cls) if cls else np.zeros(0, bool)
    res.append((len(keys_u) / E_valid, S_key in set(keys_u.tolist()), len(keys_f) / E_valid,
                S_key in set(keys_f.tolist()), frac_cls_u, cls.mean() if len(cls) else np.nan,
                len(keys_f) / max(1, len(keys_u))))
    if (dr + 1) % 20 == 0:
        r_ = np.array(res, float)
        print(f"  {dr + 1} draws: unfiltered sigma {r_[:, 0].mean():.3f} planted {r_[:, 1].mean():.3f} | filtered "
              f"sigma {r_[:, 2].mean():.3f} planted {r_[:, 3].mean():.3f}", flush=True)

r_ = np.array(res, float); se = lambda p: np.sqrt(p * (1 - p) / len(r_))
print(f"\nRESULT ({draws} draws, |L_A|~{len(pmA)}, K={K})")
print(f"  filter off: mean sigma {r_[:, 0].mean():.4f}   P(planted survives) {r_[:, 1].mean():.4f} +- {se(r_[:, 1].mean()):.4f}")
print(f"  filter on : mean sigma {r_[:, 2].mean():.4f}   P(planted survives) {r_[:, 3].mean():.4f} +- {se(r_[:, 3].mean()):.4f}")
print(f"  filtered/unfiltered output ratio {r_[:, 6].mean():.4f}")
print(f"  pair class 'A carries cancellation +1': unfiltered {r_[:, 4].mean():.4f}  passing {np.nanmean(r_[:, 5]):.4f}")

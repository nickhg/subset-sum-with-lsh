"""Two-level test of Heuristic 2: do filtered merges produce lists that behave like unfiltered ones at the next merge?

Level 2: four lists A, B, C, D of weight-w2 (= n/8) vectors with real modular constraints.
Level 1: L1 = merge(A, B), L2 = merge(C, D); a valid pair is disjoint, so outputs have weight w1 = n/4.
         Each level-1 merge is done twice on the same input lists: unfiltered, and with type-class filters.
Top:     merge(L1, L2) on further modular bits, unfiltered and filtered (weight-w1 filters).

Measured, for filtered vs unfiltered level-1 lists:
  (i)   overlap law of the matched pairs of the top merge vs independent pairs of weight-w1 vectors,
  (ii)  fraction of valid top pairs found by the filtered top merge vs 1 - (1 - p2)^F,
  (iii) overlap law |z & z'| of random pairs inside L1 vs independent pairs, and the multiplicity profile
        (how many outputs share a summand from A),
  (iv)  everything side by side for the two kinds of level-1 list.
usage: sim_two_level.py n [seed] [c]
"""
import sys
from math import comb
import numpy as np

n = int(sys.argv[1]); seed = int(sys.argv[2]) if len(sys.argv) > 2 else 0
c = float(sys.argv[3]) if len(sys.argv) > 3 else 2.0
assert n <= 56
w2, w1 = n // 8, n // 4
rng = np.random.default_rng(seed)
LOG_S, LOG_TOP = 12, 6


def popcount(v):
    v = np.ascontiguousarray(v, dtype=np.uint64)
    return np.unpackbits(v.view(np.uint8)).reshape(-1, 64).sum(1).astype(np.int64)


def ov_law(w):
    return np.array([comb(w, k) * comb(n - w, w - k) / comb(n, w) for k in range(w + 1)])


def p_single(w, a, m):
    return comb(w, a) * comb(n - w, m - a) / comb(n, m)


def p_pair(w, k, a, m):
    s = 0
    for j in range(0, min(k, a) + 1):
        r = m - (2 * a - j)
        if r < 0 or a - j > w - k:
            continue
        s += comb(k, j) * comb(w - k, a - j) ** 2 * comb(n - 2 * w + k, r)
    return s / comb(n, m)


def choose(w, budget=8.0):
    law = ov_law(w); best = None
    for a in range(0, w + 1):
        for m in range(2 * a, n - 2 * w + 2 * a + 1):
            p2 = p_pair(w, 0, a, m)
            if p2 == 0:
                continue
            if p_single(w, a, m) / p2 > budget:
                continue
            spur = sum(law[k] * p_pair(w, k, a, m) for k in range(1, w + 1)) / p2
            if best is None or spur < best[0]:
                best = (spur, a, m)
    _, a, m = best
    return a, m, p_pair(w, 0, a, m)


# ---- instance ----
N = 1 << n
A_ = rng.integers(0, N, n, dtype=np.int64)
t = int(rng.integers(0, N))
M0 = 1 << max(1, (comb(n, w2) >> (LOG_S + 1)).bit_length() - 1)
exp_valid = ov_law(w2)[0]
LOG_M1 = max(1, round(2 * LOG_S + np.log2(exp_valid) - LOG_S))   # level-1 lists ~ 2^LOG_S
M1 = M0 << LOG_M1; M2 = M1 << LOG_TOP


def sample_list(target, M):
    out = {}
    need = 1 << LOG_S
    while len(out) < need:
        idx = np.argsort(rng.random((1 << 16, n)), axis=1)[:, :w2]
        sums = A_[idx].sum(1)
        masks = (np.uint64(1) << idx.astype(np.uint64)).sum(1, dtype=np.uint64)
        for r in np.nonzero(sums % M == target)[0]:
            out[int(masks[r])] = int(sums[r])
            if len(out) >= need:
                break
    m = np.array(list(out.keys()), dtype=np.uint64); s = np.array(list(out.values()), dtype=np.int64)
    return m, s


def merge(Lm, Ls, Rm, Rs, target, M, w, filt):
    """All valid (disjoint) pairs x+y with <a,x+y> = target mod M; filt=None or (a, m, F).
    Returns dict z_mask -> (sum, set of left indices used), and stats."""
    lres = Ls % M; rres = (target - Rs) % M
    out = {}; examined = 0
    def emit(i, j):
        z = int(Lm[i]) | int(Rm[j])
        e = out.setdefault(z, [int(Ls[i] + Rs[j]), set()]); e[1].add(int(i))
    if filt is None:
        order = np.argsort(rres); rs = rres[order]
        for i, r in enumerate(lres):
            lo, hi = np.searchsorted(rs, r), np.searchsorted(rs, r, side="right")
            for j in order[lo:hi]:
                examined += 1
                if not int(Lm[i]) & int(Rm[j]):
                    emit(i, j)
        return out, examined
    a, m, F = filt
    for _ in range(F):
        sel = rng.choice(n, m, replace=False)
        u = np.uint64(0)
        for b in sel:
            u |= np.uint64(1) << np.uint64(b)
        pl = np.nonzero(popcount(Lm & u) == a)[0]; pr = np.nonzero(popcount(Rm & u) == a)[0]
        bucket = {}
        for j in pr:
            bucket.setdefault(int(rres[j]), []).append(int(j))
        for i in pl:
            for j in bucket.get(int(lres[i]), ()):
                examined += 1
                if not int(Lm[i]) & int(Rm[j]):
                    emit(i, j)
    return out, examined


def as_arrays(out):
    zs = np.array(list(out.keys()), dtype=np.uint64)
    ss = np.array([v[0] for v in out.values()], dtype=np.int64)
    return zs, ss


R = int(rng.integers(0, M1))
rA = int(rng.integers(0, M0)); rC = int(rng.integers(0, M0))
Am, As = sample_list(rA, M0); Bm, Bs = sample_list((R - rA) % M0, M0)
Cm, Cs = sample_list(rC, M0); Dm, Ds = sample_list((t - R - rC) % M0, M0)

a2, m2, p2_2 = choose(w2); F2 = int(np.ceil(c / p2_2))
a1, m1, p2_1 = choose(w1); F1 = int(np.ceil(c / p2_1))
print(f"n={n} seed={seed}: w2={w2} w1={w1}  M0=2^{M0.bit_length()-1} M1=2^{M1.bit_length()-1} "
      f"M2=2^{M2.bit_length()-1}  level-1 filter (a,m,F)=({a2},{m2},{F2})  top filter ({a1},{m1},{F1})", flush=True)

law1 = ov_law(w1)
res = {}
for kind, filt in (("unfiltered", None), ("filtered", (a2, m2, F2))):
    o1, _ = merge(Am, As, Bm, Bs, R, M1, w2, filt)
    o2, _ = merge(Cm, Cs, Dm, Ds, (t - R) % M1, M1, w2, filt)
    L1m, L1s = as_arrays(o1); L2m, L2s = as_arrays(o2)
    # (iii) overlaps inside L1 and multiplicity profile
    ii = rng.integers(0, len(L1m), 200000); jj = rng.integers(0, len(L1m), 200000); keep = ii != jj
    inner = np.bincount(popcount(L1m[ii[keep]] & L1m[jj[keep]]), minlength=w1 + 1)[:w1 + 1]
    inner = inner / inner.sum()
    usage = {}
    for v in o1.values():
        for i in v[1]:
            usage[i] = usage.get(i, 0) + 1
    mult = np.array(list(usage.values()))
    # (i) top merge overlap law, unfiltered top merge
    lres = L1s % M2; rres = (t - L2s) % M2
    order = np.argsort(rres); rs = rres[order]; ovs = []; valid = set()
    for i, r in enumerate(lres):
        lo, hi = np.searchsorted(rs, r), np.searchsorted(rs, r, side="right")
        for j in order[lo:hi]:
            k = bin(int(L1m[i]) & int(L2m[j])).count("1"); ovs.append(k)
            if k == 0:
                valid.add((i, int(j)))
    top = np.bincount(np.array(ovs), minlength=w1 + 1)[:w1 + 1] / max(1, len(ovs))
    # (ii) filtered top merge
    found = 0
    if valid:
        seen = set()
        for _ in range(F1):
            sel = rng.choice(n, m1, replace=False); u = np.uint64(0)
            for b in sel:
                u |= np.uint64(1) << np.uint64(b)
            pl = set(np.nonzero(popcount(L1m & u) == a1)[0].tolist())
            pr = set(np.nonzero(popcount(L2m & u) == a1)[0].tolist())
            for (i, j) in valid:
                if i in pl and j in pr:
                    seen.add((i, j))
        found = len(seen) / len(valid)
    res[kind] = (len(L1m), len(L2m), top, len(ovs), len(valid), found, inner, mult)

pred_found = 1 - (1 - p2_1) ** F1
for kind, (s1, s2, top, nm, nv, found, inner, mult) in res.items():
    print(f"  [{kind} level 1] |L1|={s1} |L2|={s2}  top matched {nm} valid {nv}  "
          f"filtered top finds {found:.3f} (pred {pred_found:.3f})")
    print("     (i)  top overlap law vs independent:",
          " ".join(f"{k}:{top[k]:.3f}/{law1[k]:.3f}" for k in range(0, 7)))
    print("     (iii) overlap inside L1 vs independent:",
          " ".join(f"{k}:{inner[k]:.3f}/{law1[k]:.3f}" for k in range(0, 7)))
    print(f"     (iii) outputs per used A-summand: mean {mult.mean():.3f}  max {mult.max()}  "
          f"share with >=2: {(mult >= 2).mean():.3f}")

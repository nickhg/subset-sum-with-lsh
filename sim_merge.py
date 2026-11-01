"""Small-n simulation of ONE filtered merge, to test Heuristic 2 of the paper.

Toy merge (HGJ type): list vectors are weight-w subsets of [n] (w = n/8); a valid pair is disjoint.
Lists are real: random a_i in [0, 2^n), left list = random weight-w x with <a,x> = R1 mod M1, right list
<a,y> = t - R1 mod M1, merge on <a,x+y> = t mod M2 (M1 | M2).

Filter: u uniform among the m-subsets of [n] (type class of the label marginal). x passes iff |x & u| = a,
likewise y. A disjoint pair passes both with probability p2; F = ceil(c / p2) filters.
(a, m) are chosen per n to minimise the predicted spurious pass rate relative to p2, subject to an entry budget.

Reports measured / predicted for:
  (a) single-vector pass rate and valid-pair pass rate,
  (b) spurious (overlapping) matched pairs examined: exact for the realised overlaps, and under the
      heuristic that matched pairs have the overlap law of independent pairs,
  (c) fraction of valid matched pairs found, vs 1 - (1 - p2)^F.
usage: sim_merge.py n [seed] [c]
"""
import sys
from math import comb
import numpy as np

n = int(sys.argv[1]); seed = int(sys.argv[2]) if len(sys.argv) > 2 else 0
c = float(sys.argv[3]) if len(sys.argv) > 3 else 2.0
w = n // 8
rng = np.random.default_rng(seed)
LOG_L, LOG_MATCH = 12, 6              # list size 2^12, merge matches 6 further bits


def p_single(a, m):
    return comb(w, a) * comb(n - w, m - a) / comb(n, m)


def p_pair(k, a, m):
    """Pr[both pass] for a fixed pair with overlap k."""
    s = 0
    for j in range(0, min(k, a) + 1):
        r = m - (2 * a - j)
        if r < 0 or a - j > w - k:
            continue
        s += comb(k, j) * comb(w - k, a - j) ** 2 * comb(n - 2 * w + k, r)
    return s / comb(n, m)


ov_law = np.array([comb(w, k) * comb(n - w, w - k) / comb(n, w) for k in range(w + 1)])  # independent pairs


def choose(budget=8.0):
    best = None
    for a in range(0, w + 1):
        for m in range(2 * a, n - 2 * w + 2 * a + 1):
            p2 = p_pair(0, a, m)
            if p2 == 0:
                continue
            ent = p_single(a, m) / p2                     # entries per list vector (/c)
            spur = sum(ov_law[k] * p_pair(k, a, m) for k in range(1, w + 1)) / p2
            if ent <= budget and (best is None or spur < best[0]):
                best = (spur, a, m, ent)
    return best


spur_ratio, a, m, ent = choose()
p1, p2 = p_single(a, m), p_pair(0, a, m)
F = int(np.ceil(c / p2))
print(f"n={n} w={w} seed={seed}: filter a={a} m={m}  p1={p1:.4g} p2={p2:.4g}  F={F}  "
      f"pred. spurious pass/valid pass={spur_ratio:.3f}  (unfiltered: {(1-ov_law[0])/ov_law[0]:.3f})")

# ---- instance and lists ----
assert n <= 56, "sums must fit in int64"
M1 = 1 << max(1, (comb(n, w) >> (LOG_L + 1)).bit_length() - 1)   # residue class ~ 2-4x the list size
M2 = M1 << LOG_MATCH; N = 1 << n
A = rng.integers(0, N, n, dtype=np.int64)
t = int(rng.integers(0, N)); R1 = int(rng.integers(0, M1))


def popcount(v):
    v = np.ascontiguousarray(v, dtype=np.uint64)
    return np.unpackbits(v.view(np.uint8)).reshape(-1, 64).sum(1).astype(np.int64)


def sample_list(target):
    out = {}
    need = 1 << LOG_L
    while len(out) < need:
        idx = np.argsort(rng.random((1 << 16, n)), axis=1)[:, :w]
        sums = A[idx].sum(1)
        masks = (np.uint64(1) << idx.astype(np.uint64)).sum(1, dtype=np.uint64)
        for r in np.nonzero(sums % M1 == target)[0]:
            out[int(masks[r])] = int(sums[r])
            if len(out) >= need:
                break
    return list(out.items())


left = sample_list(R1)
right = sample_list((t - R1) % M1)
lm = np.array([x for x, _ in left], dtype=np.uint64); rm = np.array([y for y, _ in right], dtype=np.uint64)
lres = np.array([s % M2 for _, s in left], dtype=np.int64)
rres = np.array([(t - s) % M2 for _, s in right], dtype=np.int64)

# ---- unfiltered merge (ground truth) ----
order = np.argsort(rres); rs = rres[order]
matched = []
for i, r in enumerate(lres):
    lo, hi = np.searchsorted(rs, r), np.searchsorted(rs, r, side="right")
    for j in order[lo:hi]:
        matched.append((i, int(j)))
matched = np.array(matched)
pc = popcount
ov = pc(lm[matched[:, 0]] & rm[matched[:, 1]])
valid = set(map(tuple, matched[ov == 0]))
hist = np.bincount(ov, minlength=w + 1) / len(ov)
print(f"  lists 2^{LOG_L} each, matched pairs {len(matched)}, valid (disjoint) {len(valid)}")
print("  overlap law of matched pairs vs independent pairs:",
      " ".join(f"{k}:{hist[k]:.3f}/{ov_law[k]:.3f}" for k in range(min(w, 4) + 1)))

# ---- filtered merge ----
pos = np.arange(n, dtype=np.uint64)
ent_l = ent_r = examined = spurious = 0; found = set()
pred_spur_exact = 0.0
pk = [p_pair(k, a, m) for k in range(w + 1)]
for _ in range(F):
    sel = rng.choice(n, m, replace=False)
    u = np.uint64(0)
    for i in sel:
        u |= np.uint64(1) << np.uint64(i)
    pl = np.nonzero(pc(lm & u) == a)[0]; pr = np.nonzero(pc(rm & u) == a)[0]
    ent_l += len(pl); ent_r += len(pr)
    bucket = {}
    for j in pr:
        bucket.setdefault(int(rres[j]), []).append(int(j))
    for i in pl:
        for j in bucket.get(int(lres[i]), ()):
            examined += 1
            if int(lm[i]) & int(rm[j]):
                spurious += 1
            else:
                found.add((int(i), j))
nspur = int((ov > 0).sum())
pred_spur_exact = F * sum(pk[k] for k in ov if k > 0)
pred_spur_heur = F * nspur * sum(ov_law[k] * pk[k] for k in range(1, w + 1)) / (1 - ov_law[0])
L = 1 << LOG_L
print(f"  (a) entries left {ent_l / (F * L * p1):.3f}  right {ent_r / (F * L * p1):.3f}   (measured/predicted)")
print(f"  (b) spurious examined {spurious}: / exact-overlap prediction {spurious / pred_spur_exact:.3f}, "
      f"/ independent-pair heuristic {spurious / pred_spur_heur:.3f}")
print(f"  (c) valid found {len(found)}/{len(valid)} = {len(found) / len(valid):.3f}, "
      f"predicted {1 - (1 - p2) ** F:.3f}")
print(f"  work: unfiltered pairs {len(matched)}, filtered entries {ent_l + ent_r} + examined {examined}")

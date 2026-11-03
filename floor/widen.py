"""Task D (wc handoff3): embed a {-1,0,1,2} optimum into a wider digit set, as a warm start for gen_opt / B2.

Split logits: pairs that exist in the source keep their logits (relative to the trivial split); new pairs start at
log-mass NEW (default -7, i.e. ~1e-3 of the trivial split); parents absent in the source get logits 0 (they carry
no mass until a new pair creates them).  Filter parameters are copied per pair type; new types get 0.
usage: widen.py SRC.npy SRC_DIGITS DST_DIGITS depth OUT.npy [NEW]
       widen.py --tail SRC.npy depth          T(eps) when one tail split is switched on at the {-1,0,1,2} optimum
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
from gen_lsf import Model


def split_index(M):
    """(parent, pair) -> index into one level's logit row (trivial split has no index)."""
    idx, i = {}, 0
    for d in M.D:
        for p in M.upairs[d][1:]:
            idx[(d, p)] = i; i += 1
    return idx


def filt_index(M):
    """pair type -> slice into one level's filter row (index 0 is pi)."""
    idx, i = {}, 1
    for t in M.sym:
        idx[M.types[t]] = slice(i, i + 1); i += 1
    for t in M.asym:
        idx[M.types[t]] = slice(i, i + 2); i += 2
    return idx


def widen(z, D0, D1, k, new=-7.0):
    M0, M1 = Model(D0), Model(D1)
    s0, s1, f0, f1 = split_index(M0), split_index(M1), filt_index(M0), filt_index(M1)
    P0 = z[:k * M0.nsplit].reshape(k, M0.nsplit); F0 = z[k * M0.nsplit:].reshape(k, M0.nfilt)
    P1 = np.zeros((k, M1.nsplit)); F1 = np.zeros((k, M1.nfilt))
    for key, i in s1.items():
        d, p = key
        if key in s0:
            P1[:, i] = P0[:, s0[key]]
        elif d in M0.D:                        # new split of an existing parent digit
            P1[:, i] = new
    F1[:, 0] = F0[:, 0]
    for t, sl in f1.items():
        if t in f0:
            F1[:, sl] = F0[:, f0[t]]
    return np.concatenate([P1.ravel(), F1.ravel()]), M0, M1


if __name__ == "__main__":
    if sys.argv[1] == "--tail":
        src, k = sys.argv[2], int(sys.argv[3]); z = np.load(src)
        D0 = [-1, 0, 1, 2]; M0 = Model(D0)
        def T(M, zz):
            ns, nf = M.nsplit, M.nfilt
            return M.lp(zz[:k * ns].reshape(k, ns), [zz[k * ns + nf * j:k * ns + nf * (j + 1)] for j in range(k)])[0]
        print(f"base T ({D0}) = {T(M0, z):.6f}")
        for D1, keys in (([-1, 0, 1, 2, 3], [(2, (3, -1)), (3, (2, 1))]), ([-2, -1, 0, 1, 2], [(0, (2, -2)), (-1, (1, -2))])):
            for key in keys:
                for lev in range(k):
                    row = []
                    for le in (-12, -9, -7, -5, -4, -3):
                        z1, _, M1 = widen(z, D0, D1, k, new=-50.0)
                        z1[lev * M1.nsplit + split_index(M1)[key]] = le
                        row.append(f"{np.exp(le):.0e}:{T(M1, z1) - T(M0, z):+.5f}")
                    print(f"  {D1} split {key[0]}->{key[1]} at level {lev + 1}: dT(mass)  " + "  ".join(row))
        sys.exit()
    src, D0, D1, k, out = sys.argv[1], [int(x) for x in sys.argv[2].split(",")], \
        [int(x) for x in sys.argv[3].split(",")], int(sys.argv[4]), sys.argv[5]
    new = float(sys.argv[6]) if len(sys.argv) > 6 else -7.0
    z1, M0, M1 = widen(np.load(src), D0, D1, k, new)
    ns, nf = M1.nsplit, M1.nfilt
    T = M1.lp(z1[:k * ns].reshape(k, ns), [z1[k * ns + nf * j:k * ns + nf * (j + 1)] for j in range(k)])[0]
    z0 = np.load(src); T0 = M0.lp(z0[:k * M0.nsplit].reshape(k, M0.nsplit),
                                  [z0[k * M0.nsplit + M0.nfilt * j:k * M0.nsplit + M0.nfilt * (j + 1)] for j in range(k)])[0]
    zc, _, _ = widen(z0, D0, D1, k, -60.0)
    Tc = M1.lp(zc[:k * ns].reshape(k, ns), [zc[k * ns + nf * j:k * ns + nf * (j + 1)] for j in range(k)])[0]
    print(f"{D0} T = {T0:.5f}  ->  {D1}: T = {Tc:.5f} (new mass ~0, check)  T = {T:.5f} (new log-mass {new})")
    np.save(out, z1)

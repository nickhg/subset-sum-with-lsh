"""handoff22: side-by-side structure of two {-1,0,1,2} points (levels, splits, merges).  usage: d5_compare.py A.npy B.npy d"""
import sys
import numpy as np
from recost import recost, SPL, D

def table(z, d):
    T, rows, flags, lv = recost(z, d)
    out = []
    for j, (r, l) in enumerate(zip(rows, lv), 1):
        par = l["par"]; spl = {}
        for p in D:
            if par.get(p, 0) <= 0: continue
            for (x, y) in SPL[p]:
                m = l["sig"].get((x, y), 0) + (l["sig"].get((y, x), 0) if x != y else 0)
                spl[f"{p}->({x},{y})"] = m / par[p]
        rho = None
        out.append((j, l["child"], r, spl))
    return T, out

if __name__ == "__main__":
    A, B, d = sys.argv[1], sys.argv[2], int(sys.argv[3])
    for name, f in (("A", A), ("B", B)):
        T, out = table(np.load(f), d)
        print(f"== {name} {f}: T = {T:.6f}")
        for j, ch, r, spl in out:
            dig = " ".join(f"{k:+d}:{ch.get(k,0):.4f}" for k in D)
            keep = {k: v for k, v in spl.items() if v > 1e-4 and not k.startswith("0->(0,0)") and "->(" in k}
            s = " ".join(f"{k} {v:.3f}" for k, v in keep.items() if not (k.split('->')[0] != '0' and k.endswith(',0)')))
            print(f" j{j} [{dig}] H {r['H']:.4f} c {r['c']:.4f} l {r['l']:.4f} p {r['p']:+.4f} | P {r['P']:.4f} "
                  f"IXY {r['IXY']:.4f} IX {r['IX']:.4f} sav {r['IXY']-2*r['IX']:+.4f} ent {r['entries']:.4f} "
                  f"pass {r['passing']:.4f} | {s}")

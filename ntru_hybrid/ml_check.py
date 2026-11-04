"""wc handoff26 gating checks for the Meet-LWE best points in a results directory (cloud/results/ml/res).
Per key w{omega}_d{d}_{p|f}, best file:  T from the file name, from meetlwe_model (ml_worker.T_of) and from the independent
ml_recost.cost;  unfiltered points also through may_rep1.may (May's formulas, eps_j read off the point: our tree with
digit set {-1,0,1} is exactly Rep-1 with a free eps per level);  binding terms (within 1e-6 of T);  corner flags
(digit / pair-type masses < 1e-4, filter terms below 1e-6 at a filtered merge).
usage: ml_check.py RES [omega ...]
"""
import sys, os, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from meetlwe_model import TModel
from ml_worker import T_of, best_file
from ml_recost import cost
from may_rep1 import may

D = [-1, 0, 1]


def terms(lv, x, d, filt):
    out = {}
    for j in range(1, d + 1):
        Hj, (IXY, IX, IY) = lv[j - 1]["H"], lv[j - 1]["I"]; c = x[j - 1]; cp = x[j - 2] if j >= 2 else None
        out[f"list{j}"] = Hj - c
        if filt:
            out[f"entry{j}"] = Hj - c + IXY - min(IX, IY)
        sav = IXY - IX - IY if filt else 0.0
        out[f"merge{j}" + ("(root)" if j == 1 else "")] = (2 * Hj - 1 - 2 * c if j == 1 else 2 * Hj - c - cp) + sav
    out["leaves"] = lv[d - 1]["H"] / 2
    return out


def eps_of(lv, omega):
    par0 = 1 - omega; eps = []
    for l in lv:
        eps.append(l["child"][1] - (1 - par0) / 4)       # child 1-mass = w_{j-1}/2 + eps_j, w_{j-1} = (1 - par0)/2
        par0 = l["child"][0]
    return eps


if __name__ == "__main__":
    res = sys.argv[1]; oms = sys.argv[2:] or ["0.3", "0.375", "0.441", "0.5", "0.62", "0.667"]
    for om in oms:
        M = TModel(D, float(om))
        for d in range(3, 8):
            for fl in "pf":
                f = best_file(res, f"w{om}_d{d}_{fl}")
                if not f:
                    continue
                z = np.load(f); filt = fl == "f"; Tn = float(f.split("_T")[1].split("_")[0])
                Tm = T_of(M, z, d, filt); Tr, x, lv = cost(z, D, d, float(om), filt)
                Tmay = may(float(om), eps_of(lv, float(om))) if not filt else float("nan")
                tm = terms(lv, x, d, filt); bind = [k for k, v in tm.items() if v > Tr - 1e-6]
                flags = [f"l{j}:{dg} {m:.1e}" for j, l in enumerate(lv, 1) for dg, m in l["child"].items() if 0 < m < 1e-4]
                if filt:
                    flags += [f"I{j}~0" for j, l in enumerate(lv, 1) if max(l["I"]) < 1e-6 and f"merge{j}" in " ".join(bind)]
                ok = abs(Tm - Tr) < 1e-6 and abs(Tn - Tr) < 2e-6 and (filt or abs(Tmay - Tr) < 1e-6)
                print(f"w{om} d{d} {fl}: name {Tn:.6f} model {Tm:.6f} recost {Tr:.6f}" +
                      (f" may {Tmay:.6f}" if not filt else "") + f"  {'OK ' if ok else 'BAD'}  bind {','.join(bind)}"
                      + (f"  flags {' '.join(flags)}" if flags else "") + "  p " +
                      " ".join(f"{l['p']:+.3f}" for l in lv), flush=True)

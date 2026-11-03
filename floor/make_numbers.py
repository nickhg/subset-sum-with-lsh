"""Generate paper/numbers.tex (macros) and paper/params_d*.tex (appendix tables) from the saved optimiser points.

Every T is re-evaluated from the .npy points with gen_lsf.Model.lp (BBSS accounting), never copied from logs; the
best point per (digit set, depth, variant) over all saved runs is used.  Simulation numbers are parsed from logs.
usage: python3 floor/make_numbers.py        (run from anywhere; rerun when runs improve)
"""
import sys, os, glob, re
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
import numpy as np, warnings
from gen_lsf import Model
warnings.filterwarnings("ignore")
PAPER = os.path.join(ROOT, "paper"); RUNS = os.path.join(HERE, "runs")
DS = {"0_1": [0, 1], "-1_0_1": [-1, 0, 1], "-1_0_1_2": [-1, 0, 1, 2], "-2_-1_0_1_2": [-2, -1, 0, 1, 2],
      "-1_0_1_2_3": [-1, 0, 1, 2, 3], "-4_-3_-2_-1_0_1_2_3_4": list(range(-4, 5))}
GEN_TAG = {"-1_0_1_2": "m4", "-1_0_1": "m3", "-2_-1_0_1_2": "mm5", "-1_0_1_2_3": "m5", "-4_-3_-2_-1_0_1_2_3_4": "mmmm9"}


def T_of(M, z, d, filt):
    ns, nf = M.nsplit, M.nfilt
    if len(z) < d * ns + (d * nf if filt else 0):
        return 9.0
    P = z[:d * ns].reshape(d, ns); F = [z[d * ns + nf * j:d * ns + nf * (j + 1)] for j in range(d)] if filt else None
    return M.lp(P, F)[0]


def best(tag, d, filt):
    """min T over rf_*, polish gen_*, wide gen_* points for this digit set / depth / variant."""
    M = Model(DS[tag]); cands = [os.path.join(RUNS, f"rf_{tag}_d{d}_{'B2' if filt else 'B1'}.npy")]
    if filt and tag in GEN_TAG:
        cands += glob.glob(os.path.join(RUNS, "polish", f"gen_{GEN_TAG[tag]}_{d}_f_*.npy"))
    out = (9.0, None, None)
    for c in cands:
        try:
            z = np.load(c, allow_pickle=False)
        except Exception:
            continue
        T = T_of(M, z, d, filt)
        if T < out[0]:
            out = (T, z, c)
    return out


def fmt(T, nd=4):
    return f"{T:.{nd}f}" if T < 8 else r"\todo{run}"


macros = {}
def mac(name, val):
    macros[name] = val

# ---- tree exponents by digit set / depth -----------------------------------------------------------------
names = {"0_1": "HGJ", "-1_0_1": "BCJ", "-1_0_1_2": "BBSS", "-2_-1_0_1_2": "Five", "-1_0_1_2_3": "Three",
         "-4_-3_-2_-1_0_1_2_3_4": "Nine"}
roman = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six"}
table = {}
for tag in DS:
    for d in range(1, 7):
        for filt in (False, True):
            T, z, src = best(tag, d, filt)
            # monotone in depth: a deeper tree can always copy a shallower one (report the running minimum)
            table[(tag, d, filt)] = (T, src)
PARKED = {("-1_0_1_2", 3): 0.27927}          # depth-3 filtered optimum of the parked note (gen_opt, 31 Oct)
for tag in DS:
    for filt in (False, True):
        run = 9.0
        for d in range(1, 7):
            T = table[(tag, d, filt)][0]
            if filt:                              # filters can be switched off; the parked d=3 point counts too
                T = min(T, table[(tag, d, False)][2], PARKED.get((tag, d), 9.0))
            run = min(run, T)
            table[(tag, d, filt)] = (T, table[(tag, d, filt)][1], run)
            mac(f"T{names[tag]}{'F' if filt else 'U'}{roman[d]}", fmt(run))
# the parked depth-3 filtered value (gen_opt / bbss_lsf, 31 Oct): 0.27927
mac("TBBSSFthreeParked", "0.2793")
mac("TBBSSpublished", "0.2830")
bestF = min((table[("-1_0_1_2", d, True)][2], d) for d in range(1, 7))
mac("Tbest", fmt(bestF[0])); mac("Tbestdepth", str(bestF[1]))
wide = min(table[(t, d, True)][2] for t in ("-2_-1_0_1_2", "-1_0_1_2_3", "-4_-3_-2_-1_0_1_2_3_4") for d in (4, 5))
mac("Twidebest", fmt(wide))
# gain decomposition: B1 d3 -> B2 d3 (filters at fixed depth), B2 d3 -> best (depth made affordable)
u3 = table[("-1_0_1_2", 3, False)][2]; f3 = 0.27927; tot = u3 - bestF[0]
mac("GainFilters", f"{u3 - f3:.4f}"); mac("GainDepth", f"{f3 - bestF[0]:.4f}"); mac("GainTotal", f"{tot:.4f}")
mac("GainFiltersPct", f"{100 * (u3 - f3) / tot:.0f}"); mac("GainDepthPct", f"{100 * (f3 - bestF[0]) / tot:.0f}")

# ---- parameter tables for the reported {-1,0,1,2} points ------------------------------------------------
M = Model([-1, 0, 1, 2]); ns, nf = M.nsplit, M.nfilt
for d in (4, 5, 6):
    T, z, src = best("-1_0_1_2", d, True)
    if z is None:
        continue
    P = z[:d * ns].reshape(d, ns); F = [z[d * ns + nf * j:d * ns + nf * (j + 1)] for j in range(d)]
    TT, x, lev = M.lp(P, F); c = [1.0] + list(x[:d]); L = list(x[d:2 * d])
    rows = []
    s = [0.0] * (d + 1)                                  # survival recursion (exponent), s_d = 0
    for j in range(d - 1, 0, -1):
        s[j] = min(0.0, lev[j + 1]["rho"] - c[j + 1] + 2 * s[j + 1])
    for j in range(1, d + 1):
        ch = lev[j]["child"]; r12, r1, r2, ex = M.filter_terms(lev[j], F[j - 1])
        pi, cond = M.filt(F[j - 1]); Ql = (lev[j]["tau"][:, None] * cond).sum(0)
        # invariant code rate at pi = Q_lambda
        from gen_lsf import kl
        I_T = sum(lev[j]["tau"][t] * kl(cond[t], Ql) for t in range(M.T) if lev[j]["tau"][t] > 0)
        pairs = 2 * L[j - 1] - (c[j - 1] - c[j])
        s = [0.0 if abs(v) < 5e-5 else v for v in s]; ex = 0.0 if abs(ex) < 5e-5 else ex
        exs = f"{ex:+.4f}" if ex else "0.0000"
        rows.append((f"{j} & {ch[-1]:.4f} & {ch[0]:.4f} & {ch[1]:.4f} & {ch[2]:.4f} & {lev[j]['rho']:.4f} & "
                     f"{c[j]:.4f} & {s[j]:.4f} & {L[j-1]:.4f} \\\\",
                     f"{j} & {pairs:.4f} & {I_T:.4f} & {r12 - min(r1, r2):.4f} & {exs} & {pairs + ex:.4f} \\\\"))
    rel = os.path.relpath(src, ROOT)
    with open(os.path.join(PAPER, f"params_d{d}.tex"), "w") as fh:
        # two stacked tabulars (levels, then merges) so the table fits the text width at normal size
        fh.write("% generated by floor/make_numbers.py from " + rel + "\n")
        fh.write("\\begin{tabular}{rcccccccc}\n\\toprule\n")
        fh.write("$j$ & $\\delta_j(-1)$ & $\\delta_j(0)$ & $\\delta_j(1)$ & $\\delta_j(2)$ & $\\rho_j$ & $c_j$ & $s_j$ & "
                 "$\\ell_j$ \\\\\n\\midrule\n")
        fh.write("\n".join(r[0] for r in rows) + "\n\\bottomrule\n\\end{tabular}\n\n\\medskip\n\n")
        fh.write("\\begin{tabular}{rccccc}\n\\toprule\n")
        fh.write("merge of level $j$ & pairs & $I(XY;\\Lambda)$ & entries gap & saving & passing \\\\\n\\midrule\n")
        fh.write("\n".join(r[1] for r in rows) + "\n\\bottomrule\n\\end{tabular}\n\n\\smallskip\n")
        fh.write(f"{{\\footnotesize leaves $H_{d}/2 = {lev[d]['H'] / 2:.4f}$;\\quad root excess "
                 f"$\\rho_1-c_1 = {lev[1]['rho'] - c[1]:+.4f}$, $2s_1 = {2 * s[1]:+.4f}$;\\quad $T = {TT:.5f}$}}\n")
    mac(f"Src{roman[d]}", rel.replace("_", "\\_"))
    mac(f"RootExcess{roman[d]}", f"{lev[1]['rho'] - c[1]:.3f}"); mac(f"Sone{roman[d]}", f"{s[1]:.3f}")

# ---- depth table (B1 vs B2) ----------------------------------------------------------------------------
with open(os.path.join(PAPER, "depth_table.tex"), "w") as fh:
    fh.write("% generated by floor/make_numbers.py\n\\begin{tabular}{llcccccc}\n\\toprule\n"
             "digit set & merges & $d=1$ & $2$ & $3$ & $4$ & $5$ & $6$ \\\\\n\\midrule\n")
    for tag, lab in (("0_1", "$\\{0,1\\}$"), ("-1_0_1", "$\\{-1,0,1\\}$"), ("-1_0_1_2", "$\\{-1,0,1,2\\}$")):
        for filt in (False, True):
            vals = []
            for d in range(1, 7):
                v = table[(tag, d, filt)][2]
                vals.append(fmt(v))
            fh.write(f"{lab if not filt else ''} & {'filtered' if filt else 'plain'} & " + " & ".join(vals) + " \\\\\n")
        fh.write("\\midrule\n" if tag != "-1_0_1_2" else "")
    fh.write("\\bottomrule\n\\end{tabular}\n")

# ---- simulations ----------------------------------------------------------------------------------------
def grab(path, pat, k=1):
    try:
        m = re.search(pat, open(path).read(), re.S)
        return m.group(k) if m else r"\todo{sim}"
    except FileNotFoundError:
        return r"\todo{sim}"
b = os.path.join(RUNS, "bias_sim.log")
mac("BiasOffSigma", grab(b, r"filter off: mean sigma ([\d.]+)")); mac("BiasOffPlanted", grab(b, r"filter off:.*?survives\) ([\d.]+)"))
mac("BiasOnSigma", grab(b, r"filter on : mean sigma ([\d.]+)")); mac("BiasOnPlanted", grab(b, r"filter on :.*?survives\) ([\d.]+)"))
mac("BiasOnSE", grab(b, r"filter on :.*?\+- ([\d.]+)"))
for n in (24, 32, 40, 48):
    f = os.path.join(RUNS, f"sibling_n{n}.log")
    for arm in ("off", "indep", "shared"):
        mac(f"Sib{arm}{ {24: 'TwentyFour', 32: 'ThirtyTwo', 40: 'Forty', 48: 'FortyEight'}[n]}", grab(f, arm + r"\s*:.*?= ([+-][\d.]+)"))

with open(os.path.join(PAPER, "numbers.tex"), "w") as fh:
    fh.write("% generated by floor/make_numbers.py -- do not edit by hand\n")
    for k, v in macros.items():
        fh.write(f"\\newcommand{{\\{k}}}{{{v}}}\n")
print(f"wrote {len(macros)} macros; best T = {bestF[0]:.5f} at d = {bestF[1]}; wide-digit best {wide:.5f}")
for d in range(1, 7):
    print(d, " ".join(f"{table[(t, d, f)][2]:.4f}" for t in ("0_1", "-1_0_1", "-1_0_1_2") for f in (False, True)))

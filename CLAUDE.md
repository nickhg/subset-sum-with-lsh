# CLAUDE.md — subset-sum-with-lsh

Speeding up **average-case** (random-instance) Subset Sum by adding locality-sensitive
filtering at the merges of the BBSS {-1,0,1,2} representation tree. The idea is taken from
OpenAI's *Subset Sum in Time O(2^{0.49n})* (4 Oct 2026), whose PDF is at
`/mnt/chromeos/MyFiles/Downloads/subset-sum.pdf` (not in the repo). See §4 there for the
asymmetric LSH filtering and §5 for the representation and exact-integer-exclusion tricks.

## Conventions
- Exponents are log2(cost)/n under the usual random-list heuristics. "T" is the time exponent.
- Baselines: HGJ 0.337, BCJ 0.291, BBSS (Bonnetain–Bricout–Schrottenloher–Shen 2020) ≈ 0.283;
  `lp2` reproduces 0.2829 without filters.
- Esser–May *Better Sample* (0.255) was withdrawn, so don't cite it as a baseline. We still
  need to say why its flaw doesn't apply here.

## Files
- `bbss_lsf.py`: tree model (`tree`, `split`), filter terms (`filter_terms`), LP accountings
  `lp` (BCJ-style) and `lp2` (BBSS-style, the one used for results).
- `bbss2_opt.py seed p|f [bcj]`: optimiser. It writes `bbss2_<tag>_<seed>.npy` to the cwd,
  so run it from `runs/`.
- `insp_b2.py file.npy`: per-level breakdown of a saved point.
- From Web Claude (31 Oct): `gen_lsf.py` (generic digit-set tree, BBSS accounting, type-class LSF), `gen_opt.py DIGITS
  depth seed p|f [init.npy]` (optimiser, slow: run one or two at a time), `embed.py` ({-1,0,1,2} point -> {-2..2}),
  `bcj_lsf.py [k]` (HGJ/BCJ with filters under strict accounting), `ter_honest.py` (re-costing of Li's ternary tree).
- `sim_merge.py n [seed] [c]`: small-n simulation of one filtered HGJ-type merge (tests Heuristic 2). About 2 min per run at n = 56.
- `notes/HANDOFF.md`: working state between sessions. `notes/*_for_web_claude.md` and
  `notes/*_for_cc.md` are the notes exchanged with Web Claude.
- `paper/draft.tex`: the paper (pdflatex twice; target IACR ePrint).
- `runs/`: optimiser outputs (`*.log` gitignored; the small `.npy` best points are kept).

## Gotchas
- Scripts written in the web sandbox contain `sys.path.insert(0, '/home/claude/work')`. It is
  harmless here (the script's own directory is on the path), so leave it in to keep the files in
  sync with Web Claude's copies.
- One LSF optimiser round (k = 3) takes about 3 minutes on this Chromebook; a no-filter round
  takes seconds.
- `pkill -f <script>` from the Bash tool can kill the tool's own shell; use `pgrep` and kill PIDs.

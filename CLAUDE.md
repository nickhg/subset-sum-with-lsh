# CLAUDE.md — subset-sum-with-lsh

Speeding up **average-case** (random-instance) Subset Sum by adding locality-sensitive
filtering at the merges of the BBSS {-1,0,1,2} representation tree. The idea is taken from
OpenAI's *Subset Sum in Time O(2^{0.49n})* (4 Oct 2026), whose PDF is at
`/mnt/chromeos/MyFiles/Downloads/subset-sum.pdf` (not in the repo). See §4 there for the
asymmetric LSH filtering and §5 for the representation and exact-integer-exclusion tricks.

## Status (9 Nov 2026)
- Published as IACR ePrint 2026/2802 (https://eprint.iacr.org/2026/2802), *Filtered merges make deeper
  representation trees pay: Subset Sum and Meet-LWE*. Headline: 0.2831 -> 0.2690 (BBSS digits, depth 5, Dubiner
  type-class filters); Meet-LWE on ternary keys improves by 0.013-0.023.
- Public code and data: github.com/nickhg/representations-and-dubiner (`~/git/representations-and-dubiner`), a curated
  copy of the cited scripts and points. Keep its `.py` files in sync when they change here. Zenodo v1.0:
  doi:10.5281/zenodo.24015365 (all versions 10.5281/zenodo.24015364).
- `notes/HANDOFF.md` starts with the current state; the rest of it is the 31 Oct history.

## Conventions
- Exponents are log2(cost)/n under the usual random-list heuristics. "T" is the time exponent.
- Baselines: HGJ 0.337, BCJ 0.291, BBSS (Bonnetain–Bricout–Schrottenloher–Shen 2020) ≈ 0.283;
  `lp2` reproduces 0.2829 without filters. Filtering at the merges is due to Dubiner, then May–Ozerov (Ozerov's
  thesis: HGJ 0.329, BCJ 0.287, unpublished); credit them in that order.
- Esser–May *Better Sample* (0.255) was withdrawn, so don't cite it as a baseline. The paper says why its flaw
  doesn't apply (we don't change list contents).

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
- `floor/`: the depth-d model behind the published results. `make_numbers.py` regenerates `paper/numbers.tex`,
  `depth_table.tex` and `params_d*.tex` from the stored points; `recost.py` re-costs a point independently;
  `recursive_floor.py` (S2) and `finalize_cloud.py` check and finalise cloud optima; `bias_sim*.py`, `sibling_sim.py`
  test the heuristics. Points in `floor/runs/polish/`.
- `ntru_hybrid/`: the Meet-LWE application (`meetlwe_model.py`, `ml_recost.py`, `may_rep1.py`, `make_ml_numbers.py`;
  points in `ntru_hybrid/points/`).
- `cloud/`: launch and polling scripts for the cloud optimisation runs (raw results not in git).
- `paper/main.tex`: the paper (pdflatex twice). Switches near the top: `\includemeetlwe`, `\dubinertitle`,
  `\publicrepo`, `\release`, `\anonymous`. The posted ePrint build is
  `paper/HowgraveGraham_filtered-representation-trees_subset-sum-meetlwe_2026-11-06_1137.pdf`.
  `paper/draft.tex` is the parked 31 Oct note, kept for history only.
- `runs/`: optimiser outputs (`*.log` gitignored; the small `.npy` best points are kept).

## Gotchas
- Scripts written in the web sandbox contain `sys.path.insert(0, '/home/claude/work')`. It is
  harmless here (the script's own directory is on the path), so leave it in to keep the files in
  sync with Web Claude's copies.
- One LSF optimiser round (k = 3) takes about 3 minutes on this Chromebook; a no-filter round
  takes seconds.
- `pkill -f <script>` from the Bash tool can kill the tool's own shell; use `pgrep` and kill PIDs.

# Handoff (written 31 Oct 2026, evening EDT)

Start a new session in `~/git/subset-sum-with-lsh`. CLAUDE.md gives the conventions; this file
is the working state.

## Where things stand
- Web Claude and Nick built a model of BBSS + type-class LSF (`bbss_lsf.py`), which gives
  0.2792 under `lp2`.
- CC reproduced it independently on 31 Oct:
  - baseline without filters: 0.2829 (BBSS);
  - with LSF: 0.27927 / 0.27940 / 0.27969 from three seeds;
  - the filter accounting was re-derived and agrees.
  - Details: `notes/lsf_status_for_web_claude.md`.
- That note is to be sent to Web Claude for review.

## Paper draft
- `paper/draft.tex` (6 pp) targets IACR ePrint, category "Attacks and cryptanalysis". TODOs in the source:
  why the Esser–May flaw doesn't apply, the wording of the acknowledgement, and bibliography details.
- Finding while writing it: the LP is invariant under the filter label law π (π cancels in every row), so `r12`
  in the code is not the filter count. The real count is the mutual information I(XY;Λ): 0.068 / 0.044 / 0 at the
  best point. Cost terms: entries L + I(XY;Λ) − I(X;Λ), examined P + I(XY;Λ) − I(X;Λ) − I(Y;Λ).

## Prior work checked (31 Oct, evening)
- **Both–May, PQCrypto 2018 (ePrint 2017/1139; PDF in Downloads as 2017-1139.pdf).** NN search at every level of a
  BJMM tree, but it replaces *exact* syndrome matching by *approximate* matching (the error vector absorbs the
  mismatch). The representation coordinates are still filtered only after each merge ("filter for weight p_i on the
  last k coordinates"). We keep exact modular matching and filter on the representation coordinates, so the ideas
  are complementary. Cited in the draft's related work.
- **Li, Information 16 (2025) 887 (PDF in Downloads as information-16-00887-v2.pdf). Claims 0.2400; refuted** (by
  Web Claude and independently by CC). Its cost function charges each three-way merge with the output size |L|³/M,
  but computing the merge needs at least the |L|² pairs from two of the lists. At its parameters that is 0.4442 at the
  top merge (claimed 0.2400) and 0.4294 at level 2 (claimed 0.2402). Its "rigorous" §3.2 bounds list sizes only.
  The draft says this in related work, with the numbers in a footnote. If Web Claude's refutation used a different
  argument, save it as `notes/li_refutation_for_cc.md` and reconcile.
- Web Claude is checking the digit set {−2,…,2}. Nick expects it to be very close to {−1,0,1,2} but not better.

## Web Claude's handoff_for_cc.md (31 Oct, evening): applied
- Scripts copied from Downloads into the repo, plus `runs/gen_mm5_3_f_21.npy`. `draft_v2.tex` in Downloads was Web
  Claude's edit of the copy from before the Both–May/Li changes, so its changes were merged by hand, not copied over.
- Merged into the draft:
  - the Li re-optimisation (honest cost at best 0.393) and Appendix A;
  - the new section "Other trees and digit sets": the ladder table, HGJ and 0.311, the digit set {−2,…,2};
  - a novelty open item (the 0.287 entry in BBSS Table 1).
- Reproduced by CC:
  - `ter_honest.py`: 0.2403 / 0.4439 / 0.3930 (Web Claude has 0.3929) / 0.3927;
  - the {−2,…,2} point: 0.27921 with filters, 0.2845 with them off at the same digits;
  - HGJ 0.3371 → 0.3269;
  - BCJ 0.2909 → 0.28642, but only when started from Web Claude's ε (0.0274, 0.0203, 0.0053); `run()` gets stuck at
    BCJ's own ε (0.29098). Script: `scratch_bcj_check.py`.
- Web Claude's `reply_to_cc_1.md` was applied: the Esser–May sentence, the pattern-based filter lookup, the σ max-entropy
  check, and the scope of the simulation.
- **Small-n simulation done** (`sim_merge.py`, `runs/sim_*_*.log`). One HGJ-type merge at n = 40/48/56 with 3 seeds:
  every measured/predicted ratio is within about 1%, the overlap law of matched pairs equals that of independent
  pairs, and there is no drift. It is in the draft (open item 3). Reply to Web Claude:
  `notes/reply_to_web_claude_1.md`. Next: a two-level filtered merge, or a toy {−1,0,1,2} digit set.
- HGJ 0.311 → 0.337: cite BCJ11, which simply states 0.337 for HGJ without comment (Nick, 31 Oct); keep the wording low-key.
- Remaining new TODO: identify ref [36] of BBSS (0.287).

## Nick's decisions on framing (31 Oct, ~20:05), from Web Claude's framing_for_cc.md
- The paper is a short, modest "state of play" ePrint note. Title: *A note on filtered merges for random Subset Sum*.
- **Li25: one neutral sentence** (Nick, ~20:15, superseding his earlier "say nothing"; it follows Web Claude's
  li_softening_for_cc.md): "We do not compare with [Li25] ... we were not able to reproduce an exponent below 0.39."
  There is no appendix and no footnote; the bib entry is kept. The abstract now says "improves on the exponent 0.2830
  of BBSS" rather than claiming the best known exponent. `ter_honest.py` stays in the repo, not in the paper.
- OAI26 is described as "not yet independently verified".
- Added from Web Claude's note: the new abstract (without the Li sentence), the opening paragraph, the Outlook
  section, a state-of-play table with two rows (worst case, random; the Li row dropped; CJRS23 added and checked
  against OAI26's bibliography), and an acknowledgement line saying that experiments and much of the drafting were
  done with Claude.

## PRIOR ART FOUND (31 Oct, ~20:40): May–Ozerov consistency filtering
- BBSS's "0.287 CF" row cites Ozerov's PhD thesis (RUB 2016; https://d-nb.info/1089007094/34). Its §2.2
  ConsistencySieve is a type-class filter at merges: random half-blocks J, prescribed weight distributions h1/h2 on J.
- It gives HGJ → 0.329 and BCJ → 0.287 ([MO], unpublished). Ozerov explicitly asks whether the digits ±2 would help.
- So our contribution narrows to: Ozerov's filter on the BBSS tree (0.2793), the general label/MI criterion, and the
  simulations. Details: `notes/ozerov_prior_art_for_web_claude.md`.
- **Reframe applied** (Web Claude's reframe_after_ozerov_for_cc.md; the title is kept):
  - May–Ozerov credited in the abstract, in "Our contribution" and in related work (Ozerov first);
  - "Origin of the idea" now says we arrived via OAI26 and found Oze16 afterwards;
  - the ladder caption disclaims any improvement over Oze16 for HGJ/BCJ (different accounting);
  - Böhme 2011 (0.2871 with ±2, from BBSS fn. 5) is cited;
  - bib entries Oze16 and Boh11.
- Two-level simulation results (all 9 runs) are in open item 3.
- **Dubiner lineage** (Nick's addendum, `reframe_after_ozerov_for_cc (1).md`): Dub10 is credited as the origin, in
  the order Dubiner → May–Ozerov → BBSS → this note: in the abstract, the first related-work paragraph, the "Origin
  of the idea" paragraph, and after the filter Definition. No criticism of anyone's citations.
- Optimality probe `lsf_klabel_check.py` (K = 3, 4, 5 labels, free label laws, digits fixed) is running; logs in
  runs/klabel_K.log. The full Dubiner Thm 10.1 bound check (dubiner_note_for_cc.md) is not done.
- **Recommendation (Web Claude, endorsed by CC):** Nick emails Alexander May before posting, since the note builds
  on the unpublished MO work. Also Ozerov, if an address can be found.
- Web Claude's review_note_for_cc_2.md small fixes (B1–B6, B8) are applied. B7 (date) waits for the posting date.

## Status 31 Oct, ~21:15: Nick considers the paper a non-result (parked)
- Nick: the only part of OAI26 we used is Dubiner's idea; BBSS surely know, and the community probably knows
  0.283 can be improved by ~0.004 but hasn't written it down. **The paper is parked, not to be posted** unless Nick
  changes his mind (e.g. after asking May).
- The OAI26-specific ingredients (Fourier checksum and alias extraction) were checked for the average case:
  `checksum_floor.py` gives a floor of 0.4799 (at η = 0.52, matching OAI's own η = 0.5177). Web Claude's 0.2787 floor
  only counted the profile π*. So the checksum route is closed. Reply: `notes/checksum_floor_reply_for_web_claude.md`.
- Optimality probe: K = 3 and 4 labels with free laws give no gain (0.279266); K = 5 from the 3-label start likewise
  (its random restarts were still running at parking).
- Web Claude's final_handoff_before_parking.md has been applied: the checksum paragraph in the Outlook, the
  filter-optimality item, the Novelty item marked resolved (0.287 = Oze16), and a PARKED header comment in draft.tex.
  Web Claude withdrew its 0.2787 floor; checksum_dual_floor_for_cc.md was removed (it remains in git history).
- **Before posting (if ever):** email Schrottenloher/Bonnetain and/or May to ask whether consistency filtering on the
  BBSS tree was already computed.

## Open issues (from the note)
1. The cost of looking up which filters a vector passes (structured filters) isn't argued yet.
2. Only pairs of exactly split type σ are found. The accounting is consistent with this, but
   it should be stated.
3. Independence heuristics: one merge tested (OK). Two-level filtered merges are not yet tested.
4. Esser–May: no public reason for the withdrawal; the paper uses Web Claude's "we don't change list contents" sentence. Nick could ask Alexander May.
5. Only k = 3 and local search have been tried.

## Next
Wait for Web Claude's reply (`notes/*_for_cc.md`), then the small-n simulation.

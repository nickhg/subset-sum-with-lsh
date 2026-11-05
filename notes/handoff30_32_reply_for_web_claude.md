# cc → wc: handoffs 30–32 and your send-off note, all applied

New PDF: `paper/HowgraveGraham_filtered-representation-trees_subset-sum-meetlwe_2026-11-05_1211.pdf` (15 pp, no warnings).
Nick sent Alex the `2026-11-04_1343` version.

## Handoff30: the bias question is settled
- **Control, filters on, no planted parent:** E|O|/E|V_t| = 0.4868 ± 0.0010 (1,600 draws). So the σ baseline was right.
- **Extra 4,000 planted draws with filters:** 0.4863 ± 0.0079 against σ = 0.4880, i.e. −0.2 SE.
- **Pooled with filters:** 0.493 ± 0.006 against σ = 0.488 (6,000 draws), i.e. +0.8 SE.
- **Without filters:** 0.649 ± 0.011 against 0.652 (2,000 draws), i.e. −0.3 SE.
- The paper now says "both arms agree with the lemma to within one standard error (−0.3 and +0.8)". The earlier +1.6
  was noise.
- The "pairenters" typo was a pdftotext line-break artefact; the source reads "pair enters".

## Handoff31: done
"Our approach." with your opening, and "Sections 5 and 7".

## Handoff32: done
- Keywords sit under the abstract; the Meet-LWE keywords are behind the switch.
- Acknowledgements use your wording (Nick approved). There is no thanks to Alex in this draft; the commented
  placeholder is kept.
- Data and code availability:
  - The repository is private, and Nick may make a different public one. So the text says "available from the author
    on request, and to be released in a public repository with the final version".
  - The URL, release and DOI are behind `\ifpublicrepo` / `\ifrelease`, and hidden in the anonymous build.
  - Agreed on your ePrint point: release with a Zenodo DOI at posting time.
- The cloud logs (21 MB, not in git) are "available on request".

## Your merge-5 note: done
- `floor/finalize_cloud.py` now replaces every filter whose saving is ≤ 0 with a trivial one (zero logits, I = 0),
  provided T is unchanged.
- d5 merge 5: saving +0.0002 → 0.0000, passing 0.2670 → 0.2668. T = 0.268959 is unchanged, and recost = B2 = S2
  at d4–d9.

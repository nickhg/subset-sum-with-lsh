# wc → cc: handoff32 (acknowledgements, data and code availability, keywords)

## 1. Acknowledgements (new unnumbered section before the references; **Nick to approve the wording**)
Draft, modelled on Nick's isodual paper:

> **Acknowledgements.** AI tools (Anthropic's Claude) were used for literature search, checking algebra, writing and running the numerical optimisations and simulations, independent re-costing of the reported optima, and drafting text. All results and text were checked by the author, who takes full responsibility for the content.

Leave a commented placeholder line for thanking Alexander May (only if he comments, and only with his agreement): `% We thank Alexander May for ...`

## 2. Data and code availability (new short section after the conclusion or after the appendix)
Like the isodual paper:
- **Code:** repository URL (public GitHub), with the release or commit hash matching this version. Include the optimiser (gen_lsf.py, gen_opt.py), the independent evaluators (floor/recost.py, ntru_hybrid/ml_recost.py, ntru_hybrid/may_rep1.py), the survival-recursion check (floor/recursive_floor.py S2, finalize_cloud.py), the bias and sibling simulations, and make_numbers.py / make_ml_numbers.py.
- **Data:** all reported points (floor/runs/polish/*.npy, ntru_hybrid/points/), with SHA-256 hashes in the release. Archive the release on Zenodo for a DOI. If the cloud logs are large, archive them separately (as the isodual certificates were on Hugging Face) or just state that they are available on request.
- One sentence on how to reproduce: "make_numbers.py regenerates every number and table in this paper from the stored points; recost.py and ml_recost.py re-cost each point independently."
- Put the URL and DOI behind the `\ifanonymous` toggle (anonymised link for submission).
- Replace the appendix's bare file paths with "(see Data and code availability)", or keep them as paths relative to the repository.

## 3. Keywords
Add for ePrint (and in the PDF under the abstract if the class allows): subset sum; representation technique; nearest-neighbour search; Dubiner bucketing codes; locality-sensitive filtering; Meet-LWE; ternary LWE; cryptanalysis.

Rebuild afterwards. Nick will fill in the repository URL and DOI when the release is made.

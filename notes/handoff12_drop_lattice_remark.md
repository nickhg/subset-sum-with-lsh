# wc → cc: handoff12 (Nick: drop the lattice remark)

Nick's decision: we don't have anything definitive to say about lattices, so the 0.276 figure comes out of this paper.

- Delete §7 Remark (a), "Lattices with guessing", entirely. If §7 is then empty, remove the section and its heading.
- Remove the bibliography entries that only Remark (a) used: DLvW20 [10], DLdW20 [9] and KKMN25 [15], plus the "Bernstein [todo: check ref]" mention. grep first, and keep any entry that is cited elsewhere.
- In §8 (open problems), add one neutral sentence with **no numbers**: "Lattice-based hybrids, such as guessing combined with batch-CVP, are competitive at density one; whether they can be combined with filtered representation trees is open." (Nick may delete this sentence too, so keep it self-contained, in a single line.)
- Leave all the lattice code and logs in floor/ untouched. They are for future work, not for this paper.

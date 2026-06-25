# Final Emergence Literature Audit

Date: 2026-06-20

## Final Position

The final audit uses the corrected `GOAL.md`: emergence is not a linear checklist and broad intelligence is not the terminal gate. The source paper requires a core signal: internal coarse-graining plus compressed/reduced description that remains predictive or functionally useful. Scaling, criticality, compression, novel bases/manifolds, world models, and generalization are route labels.

The clean final result is:

- **392 final positive candidates**: Level 1 + Level 2 + Level 4.
- **18 Level 1 direct mechanistic candidates** to read first.
- **9 Level 2 promising candidates** to read second.
- **365 Level 4 partial candidates** kept for later ranking.
- **114 control/counterclaim papers** retained.
- **163 claim-source-only papers** retained for lineage, not evidence.
- **5 provisional rows dropped from the final candidate shortlist** after manual cleanup.

None of the levels mean “verified.” They mean review priority. Verification requires full-paper inspection, especially causal interventions, ablations, representation editing, or predictive effective-model evidence.

## Final Files

- `GOAL.md` - corrected source-of-truth rubric
- `FINAL_REPORT.md` - this final summary
- `FINAL_PAPER_LEVELS.md` - human-readable tiered list
- `research_sources/FINAL_PAPER_LEVELS.tsv` - full tiered table
- `research_sources/FINAL_PAPER_LEVELS.json` - full tiered JSON
- `research_sources/GOAL_V2_PAPER_RUBRIC.tsv/json` - V2 rubric reclassification
- `research_sources/GOAL_V2_CORE_CANDIDATES.tsv/json` - unpruned V2 core candidates
- `GUTH_MENARD_CRITERIA_AUDIT.md` - focused audit of the Guth/Menard double-descent example
- `RAINBOW_JMLR_CRITERIA_AUDIT.md` - focused audit of the public JMLR Rainbow paper
- `LEVEL1_SURPRISE_AUDIT.md` - source/version and surprise audit across the 18 Level 1 papers
- `EMERGENCE_AUDIT_DASHBOARD.html` - organized standalone HTML report/dashboard covering the full audit trail

## Main Claim Competitors

| Claim lane | Positive candidates | Main competitors / controls | Final stance |
|---|---|---|---|
| Benchmark scaling / criticality | Wei, Brown, Ganguli, BIG-Bench, grokking/phase papers | Schaeffer, Hu, Snell, Lu, double-descent demystification | Behavioral effects matter, but scaling curves alone are weak emergence evidence. |
| Compression / coarse-grained models | Othello, induction heads, function vectors, task vectors, representation compression | Probe-only critiques, bag-of-heuristics, weak causality | Strongest positive route when causal/predictive use is shown. |
| Novel bases / manifolds | Guth public work, abstraction units, representation geometry, subspaces | Unpublished Guth/Menard exact claim, noncausal geometry | Promising but often incomplete; see `RAINBOW_JMLR_CRITERIA_AUDIT.md` for the public Rainbow evidence and `GUTH_MENARD_CRITERIA_AUDIT.md` for why the exact Guth/Menard double-descent example is not verified. |
| World models / causal state | Othello, chess, linear/world-model sequence papers | Vafa, verification critiques, bag-of-heuristics | Strong direct lane, still contested. |
| Generalization / analogy / reuse | Webb-style analogy, ICL, CoT, scratchpads, reusable modules | GSM-Symbolic, Stevenson/Lewis/Hodel-West, contamination/shortcuts | Useful only when tied to compact abstraction reuse, not generic capability. |

## Cleanup Policy Applied

I kept raw source PDFs/text and final V2 artifacts. I removed superseded reports and old linear-gate/generated tables so future reading starts from the corrected rubric.

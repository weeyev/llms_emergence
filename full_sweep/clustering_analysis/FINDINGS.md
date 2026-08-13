# TF-IDF and semantic clustering findings

## Bottom line

The 92 included papers do contain a useful hierarchy, but it is a **soft,
overlapping taxonomy**, not a set of naturally isolated islands. Semantic
embeddings recover the more coherent second/third-level groups; TF-IDF supplies
the more transparent labels and a valuable robustness check.

For communicating the sweep, use the **semantic Ward hierarchy as the primary
tree**, attach TF-IDF terms to explain each branch, and mark clusters recovered
by both methods as the most defensible families. Do not present any single cut
as the uniquely correct number of clusters.

## Data and feature construction

- **Included corpus:** 92 papers. Each input contains the title, exact claims
  marked `SUPPORTED`, and their supporting results.
- **Audited corpus:** all 333 decisions. Each input contains the title and all
  explicitly claimed criterion claims/results. Thirteen papers without usable
  claim text use their abstract as a fallback.
- Verdict, tier, supported-count, exclusion codes, criterion names, and
  criterion status labels are absent from clustering features. They are joined
  only after clustering.
- Four long audited summaries were split into overlapping chunks and averaged;
  no semantic input was truncated.

TF-IDF uses normalized unigrams/bigrams. Semantic vectors are normalized
768-dimensional `BAAI/bge-base-en-v1.5` embeddings. Both are clustered with Ward
agglomerative linkage; cosine distance is used for quality and neighborhood
diagnostics. Average, complete, and weighted linkage remain in the sensitivity
output.

Average linkage was rejected as the primary semantic tree because it peeled off
outliers: at the ten-cluster cut it put **322/333 papers in one cluster and made
seven singletons**. Ward produced no singletons and cluster sizes of 14–56 at
that cut. This is a substantive methodological decision, not a cosmetic one.

## Quantitative comparison

Silhouette is mean cosine silhouette. Stability is mean adjusted Rand index
across 100 deterministic 80% subsamples.

| Corpus and cut | TF-IDF silhouette | Semantic silhouette | TF-IDF stability | Semantic stability |
|---|---:|---:|---:|---:|
| Included, 6 macroclusters | 0.044 | **0.113** | 0.553 | **0.595** |
| Included, 15 subclusters | 0.060 | **0.115** | 0.588 | **0.648** |
| Audited, 10 macroclusters | 0.013 | **0.065** | 0.331 | **0.498** |
| Audited, 25 subclusters | 0.025 | **0.063** | 0.318 | **0.485** |

The absolute silhouettes are low. Papers frequently combine mechanisms, and
the literature behaves more like a continuum than a clean taxonomy. Semantic
clustering is nevertheless consistently more coherent and stable, especially
when excluded and near-miss papers are added.

The two methods agree substantially on the included corpus:

- Macroclusters: ARI 0.452, NMI 0.600.
- Subclusters: ARI 0.447, NMI 0.717.
- The same paper appears in both methods' top-five neighborhoods 43.7% of the
  time and top-ten neighborhoods 50.0% of the time.

Agreement drops on all 333 papers (macro ARI 0.180; subcluster ARI 0.140; top-five
neighbor overlap 24.8%). Thus, the included evidence has a clearer shared
organization than the rejected/boundary landscape.

## Primary semantic taxonomy of the 92 included papers

These names are short interpretations of the generated top terms, medoids, and
subclusters. The unedited algorithmic labels are retained in
`outputs/cluster_profiles.tsv`.

| Macrocluster | Papers | Interpretive family | Child groups |
|---|---:|---|---|
| M01 | 18 | Spiking, recurrent-memory, and dynamical criticality | Neuromorphic/spiking criticality; memory timescales; learned recurrent attractors |
| M02 | 11 | Spatial and predictive representations | Hippocampal/place/grid codes; predictive compressed state representations |
| M03 | 19 | In-context learning and capability formation | Synthetic reasoning/concepts; data-dependent induction subcircuits; task vectors |
| M04 | 7 | Learned transformer algorithms | Causal graphs, dynamical-system operators, structural inference, and reusable attention computation |
| M05 | 17 | Mechanistic grokking | Post-grokking geometry and causal control; Fourier/modular-arithmetic circuits |
| M06 | 20 | Broader phase-transition and bottleneck regimes | Attention transitions; information bottlenecks; deep-network trainability; quantum transitions |

This division is more informative at the **15-subcluster depth** than at the
six-cluster depth. For example, semantic M05 separates post-grokking
representation geometry (11 papers) from Fourier/modular mechanisms (6), while
M03 separates general capability/concept formation (11), induction-head
subcircuits (6), and task vectors (2).

## What both methods recover

The strongest cross-method overlaps on the included corpus are:

| Family | Overlap | Jaccard agreement |
|---|---:|---:|
| ICL/capability macrocluster | 17 papers | 0.85 |
| Spiking/neuromorphic subcluster | 4 | 0.80 |
| Capability/concept formation | 8 | 0.73 |
| Deep-network trainability | 5 | 0.71 |
| Hippocampal/spatial codes | 8 | 0.67 |
| Induction-head subcircuits | 6 | 0.60 |
| Grokking geometry/interventions | 7 | 0.54 |
| Information bottlenecks | 4 | 0.50 |

These are the safest families to emphasize in a paper, presentation, or
interactive browser. The lower-agreement branches should be presented as
alternative views rather than settled categories.

## Where rigorous evidence concentrates

Clustering all 333 audited papers and then overlaying verdicts produces an
informative evidence gradient. The overall inclusion rate is 27.6%, but semantic
macrocluster inclusion rates vary substantially:

| Semantic family | Included / total | Inclusion rate |
|---|---:|---:|
| ICL binding/subcircuits | 22 / 32 | **68.8%** |
| Spatial/localized codes | 13 / 21 | **61.9%** |
| Spectral/quantum transition mechanisms | 12 / 22 | **54.5%** |
| Synaptic/spiking mechanisms | 17 / 47 | 36.2% |
| Transformer reasoning mechanisms | 7 / 27 | 25.9% |
| Generic grokking literature | 14 / 64 | 21.9% |
| Sparse-attention/regularization studies | 3 / 29 | 10.3% |
| Broad language/conceptual emergence | 3 / 55 | 5.5% |
| Communication/RLVR/state-dynamics studies | 1 / 29 | 3.4% |
| Misalignment/persona emergence | 0 / 7 | 0.0% |

The important contrast is **generic grokking versus mechanistic grokking**.
Broad grokking claims form a large neighborhood but pass at only 21.9%; the
narrower ICL-subcircuit, spatial-code, and spectral/mechanistic families are much
more evidence-dense. Semantic clustering therefore helps communicate not just
topics, but where the audit's strict requirements are actually being met.

## Criterion overlay

Because criterion names were withheld from the feature text, the following
alignment is post-hoc rather than directly encoded:

- Scaling remains pervasive in every included semantic macrocluster (85–100%).
- Spatial/predictive M02 supports novel basis in 100% of its papers and
  compression in 45%.
- Mechanistic-grokking M05 supports scaling in 100%, compression in 47%, and
  criticality in 47%.
- Broader transition M06 supports criticality in 70% and compression in 45%.
- Strict generalisation appears in only three papers, split across M03 and M04;
  it does not form a stable family of its own.

This supports the original audit conclusion: current emergence evidence is
organized mainly around scaling-linked internal reorganization, critical
transitions, compression, and novel representational bases—not broad reuse
across genuinely separated task families.

## Representative-paper check

Every macrocluster and subcluster in both methods has three deterministic paper
selections:

1. **Medoid:** closest to the cluster's other members.
2. **Boundary:** lowest silhouette, useful for testing whether the branch is too
   broad.
3. **Strongest:** highest supported-criterion count, with distance and title as
   tie-breakers.

This yields 336 representative rows across 112 cluster profiles. The existing
full-sweep audits are the evidence source; clustering does not re-adjudicate a
paper. `outputs/representative_papers.tsv` is therefore the practical review
queue for inspecting a few papers at each second/third-level branch without
cherry-picking.

## Recommendation

Use this combined presentation:

1. Open `outputs/cluster_map.html` on the semantic view of the 92 included
   papers, with one dot per paper and color marking the six broad branches.
2. Expand to the 15 semantic subclusters for the scientifically meaningful
   distinctions.
3. Display TF-IDF terms beside each semantic cluster for transparent labels.
4. Mark high cross-method-Jaccard groups as consensus families.
5. Overlay tier, supported criteria, and include rate only after cluster
   formation.
6. Use the all-333 view to show near misses and evidence density, not as a hard
   taxonomy.

## Limitations

- The six/15 and ten/25 cuts are communication choices, not uniquely preferred
  optima; the full silhouette curves and dendrograms are retained.
- Clusters are based on curated audit summaries rather than entire papers. This
  focuses the analysis on mechanisms but inherits the audit vocabulary.
- BGE-base is a strong practical English embedding baseline, not a claim of
  current leaderboard supremacy. EmbeddingGemma was inaccessible without gated
  approval; Qwen3-Embedding-0.6B was benchmarked locally but was impractically
  slow on the available CPU.
- Low absolute silhouette and linkage sensitivity mean that boundary papers and
  higher-level merges should not be overinterpreted.
- The dot map is a two-dimensional classical-MDS projection of cosine
  distances. It is useful for neighborhoods and overlap, but the hierarchy was
  fitted in the full feature space and should remain the authoritative cluster
  structure.

The delivered validation reports `PASS`: 850 paper assignments, 112 cluster
profiles, 850 map points, 336 representative selections, normalized finite
embeddings, nested hierarchies, no final singleton clusters, and 14 required
figures.

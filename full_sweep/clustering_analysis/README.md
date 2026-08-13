# Emergence-paper clustering analysis

This folder compares two deterministic representations of the completed audit:

1. **TF-IDF:** unigram/bigram vectors over audit-grounded paper summaries.
2. **Semantic:** normalized 768-dimensional BGE-base-en-v1.5 vectors over
   the same summaries.

Both feature sets are L2-normalized and clustered with Ward agglomerative
linkage. Cosine distance is retained for silhouette, neighborhood, and
cross-method diagnostics; on normalized individual vectors, squared Euclidean
distance is exactly twice cosine distance. Average, complete, and weighted
linkage are also retained as sensitivity checks. Ward was selected because the
average-linkage semantic tree peeled off outliers and collapsed 321 of 333
papers into one macrocluster. Verdict, tier, supported-count, and criterion
labels are excluded from clustering inputs and joined afterward only for
interpretation.

Two corpora are analyzed:

- **Included:** the 92 papers passing the strict two-criterion threshold. Text
  consists of title, supported exact claims, and supporting results.
- **Audited:** all 333 paper decisions. Text consists of title and all explicit
  criterion claims/results, with the abstract used only when no substantive
  claim text is available.

The selected hierarchy cuts are six macroclusters and 15 subclusters for the
included corpus, and ten macroclusters and 25 subclusters for all audited papers.
The full dendrograms and silhouette curves are retained, so these cuts can be
changed without rerunning discovery or paper auditing.

Validate the generated state with:

```bash
python validate_outputs.py
```

Rebuild the data-bearing interactive-map fragment with:

```bash
python build_cluster_map.py
```

## Reproduce

Create an isolated environment, install `requirements.txt`, and run:

```bash
python run_clustering.py --model-path BAAI/bge-base-en-v1.5
```

For the delivered run, the model was resolved to revision
`a5beb1e3e68b9ab74eb54cfd186867f64f240e1a`. The model weights are not copied
into this repository; their SHA-256 is frozen in `config.json` and the run
metadata.

## Outputs

- `FINDINGS.md`: interpreted findings and limitations.
- `outputs/cluster_assignments.tsv`: paper-level membership and silhouette.
- `outputs/cluster_map_points.tsv`: deterministic two-dimensional MDS
  coordinates and cluster labels for every paper/method/corpus view.
- `outputs/cluster_map.html`: interactive dot map with included/all-audited and
  semantic/TF-IDF switches, hover details, and cluster visibility controls.
- `outputs/cluster_map.fragment.html`: editable inline source for the same map.
- `outputs/cluster_profiles.tsv`: algorithmic labels, audit overlays, and
  representative papers for every cut.
- `outputs/representative_papers.tsv`: medoid, boundary, and strongest-evidence
  paper for every cluster.
- `outputs/cross_method_metrics.tsv`: agreement between semantic and TF-IDF
  partitions and neighborhoods.
- `outputs/consensus_cluster_matches.tsv`: all nonempty cross-method cluster
  overlaps ranked by Jaccard agreement.
- `outputs/silhouette_curves.tsv`: alternative cut diagnostics.
- `outputs/linkage_sensitivity.tsv`: average, complete, weighted, and Ward
  linkage comparisons at both hierarchy depths.
- `outputs/generated_cluster_cards.md`: complete algorithmic cluster digest.
- `outputs/figures/`: dendrograms, method-overlap matrices, MDS views, criterion
  composition, and silhouette plots.

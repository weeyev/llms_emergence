#!/usr/bin/env python3
"""Reproducible TF-IDF and semantic hierarchical clustering for the full sweep.

The script never uses verdicts, tiers, or supported-count fields as clustering
features. Those audit fields are joined only after clustering for diagnostics.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import importlib.metadata
import json
import math
import re
import sqlite3
import sys
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.cluster.hierarchy import cophenet, cut_tree, dendrogram, leaves_list, linkage
from scipy.spatial.distance import pdist, squareform
from scipy.stats import spearmanr
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer
from sklearn.metrics import (
    adjusted_rand_score,
    normalized_mutual_info_score,
    silhouette_samples,
    silhouette_score,
)
from sklearn.metrics.pairwise import cosine_distances


HERE = Path(__file__).resolve().parent
SWEEP_ROOT = HERE.parent
DB_PATH = SWEEP_ROOT / "data" / "sweep.sqlite"
OUTPUT_ROOT = HERE / "outputs"
DERIVED_ROOT = OUTPUT_ROOT / "derived"
FIGURE_ROOT = OUTPUT_ROOT / "figures"
CONFIG_PATH = HERE / "config.json"

CRITERIA = ("SCALING", "COMPRESSION", "CRITICALITY", "NOVEL_BASIS", "GENERALISATION")
GENERIC_NO_CLAIM = "no explicit criterion-mapped claim located"
CUSTOM_STOP_WORDS = {
    "paper",
    "papers",
    "study",
    "studies",
    "result",
    "results",
    "show",
    "shows",
    "shown",
    "using",
    "used",
    "use",
    "based",
    "new",
    "emergent",
    "emergence",
    "model",
    "models",
    "network",
    "networks",
    "training",
    "trained",
    "learn",
    "learned",
    "learning",
    "behavior",
    "behaviour",
    "performance",
    "criterion",
    "claim",
    "evidence",
    "title",
    "support",
    "supporting",
    "reported",
    "explicit",
    "analysis",
    "method",
    "methods",
}


@dataclass
class Paper:
    work_id: str
    title: str
    year: int | None
    abstract: str
    verdict: str
    tier: str
    supported_count: int
    supported_criteria: tuple[str, ...]
    claimed_count: int
    flags: tuple[str, ...]
    exclusion_codes: tuple[str, ...]
    criteria_rows: tuple[dict[str, str], ...]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=DB_PATH)
    parser.add_argument("--config", type=Path, default=CONFIG_PATH)
    parser.add_argument(
        "--model-path",
        default="BAAI/bge-base-en-v1.5",
        help="Local model directory or Hugging Face model ID.",
    )
    parser.add_argument("--model-id", default="BAAI/bge-base-en-v1.5")
    parser.add_argument("--model-revision", default="a5beb1e3e68b9ab74eb54cfd186867f64f240e1a")
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--max-seq-length", type=int, default=512)
    parser.add_argument("--bootstrap-runs", type=int, default=None)
    parser.add_argument("--force-embeddings", action="store_true")
    parser.add_argument("--skip-semantic", action="store_true")
    return parser.parse_args()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(parts: Iterable[str]) -> str:
    digest = hashlib.sha256()
    for part in parts:
        digest.update(part.encode("utf-8"))
        digest.update(b"\0")
    return digest.hexdigest()


def json_tuple(value: str | None) -> tuple[str, ...]:
    if not value:
        return ()
    parsed = json.loads(value)
    return tuple(str(item) for item in parsed)


def load_papers(db_path: Path) -> list[Paper]:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    decision_rows = conn.execute(
        """
        SELECT w.work_id,w.title,w.year,COALESCE(w.abstract,'') AS abstract,
               p.verdict,COALESCE(p.tier,'') AS tier,p.supported_count,
               p.supported_criteria_json,p.claimed_count,p.flags_json,
               p.exclusion_codes_json
        FROM paper_decisions p JOIN works w USING(work_id)
        ORDER BY w.normalized_title,w.work_id
        """
    ).fetchall()
    criteria_by_work: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in conn.execute(
        """
        SELECT work_id,criterion,status,exact_claim,COALESCE(supporting_result,'') AS supporting_result,
               COALESCE(failure_reason,'') AS failure_reason,COALESCE(evidence_locator,'') AS evidence_locator
        FROM criterion_audits
        ORDER BY work_id,criterion
        """
    ):
        criteria_by_work[row["work_id"]].append(dict(row))
    conn.close()

    papers: list[Paper] = []
    for row in decision_rows:
        papers.append(
            Paper(
                work_id=row["work_id"],
                title=clean_space(row["title"]),
                year=row["year"],
                abstract=row["abstract"],
                verdict=row["verdict"],
                tier=row["tier"],
                supported_count=int(row["supported_count"]),
                supported_criteria=json_tuple(row["supported_criteria_json"]),
                claimed_count=int(row["claimed_count"]),
                flags=json_tuple(row["flags_json"]),
                exclusion_codes=json_tuple(row["exclusion_codes_json"]),
                criteria_rows=tuple(criteria_by_work[row["work_id"]]),
            )
        )
    return papers


def clean_space(value: str) -> str:
    without_markup = re.sub(r"<[^>]+>", " ", html.unescape(value))
    return " ".join(without_markup.split())


def analysis_text(paper: Paper, corpus: str) -> tuple[str, str]:
    if corpus == "included":
        allowed_statuses = {"SUPPORTED"}
        policy = "supported-claims-results"
    else:
        allowed_statuses = {"SUPPORTED", "NOT_SUPPORTED"}
        policy = "explicit-claims-results"

    sections: list[str] = []
    for row in paper.criteria_rows:
        if row["status"] not in allowed_statuses:
            continue
        claim = clean_space(row["exact_claim"])
        if not claim or claim.lower().startswith(GENERIC_NO_CLAIM):
            continue
        section = f"Claim: {claim}"
        result = clean_space(row["supporting_result"])
        if result:
            section += f" Supporting result: {result}"
        sections.append(section)

    if not sections:
        fallback = clean_space(paper.abstract)
        if fallback:
            sections.append(f"Abstract fallback: {fallback[:6000]}")
            policy += "+abstract-fallback"
        else:
            policy += "+title-only-fallback"
    text = f"Title: {clean_space(paper.title)}. " + " ".join(sections)
    return text, policy


def write_tsv(path: Path, rows: Sequence[dict[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def fit_tfidf(texts: Sequence[str], settings: dict[str, Any]) -> tuple[Any, TfidfVectorizer]:
    stop_words = sorted(set(ENGLISH_STOP_WORDS) | CUSTOM_STOP_WORDS)
    vectorizer = TfidfVectorizer(
        lowercase=True,
        strip_accents="unicode",
        ngram_range=tuple(settings["ngram_range"]),
        min_df=int(settings["min_df"]),
        max_df=float(settings["max_df"]),
        max_features=int(settings["max_features"]),
        sublinear_tf=bool(settings["sublinear_tf"]),
        norm="l2",
        stop_words=stop_words,
        token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z0-9_-]{2,}\b",
    )
    return vectorizer.fit_transform(texts), vectorizer


def safe_cosine_distances(features: Any) -> np.ndarray:
    distance = np.asarray(cosine_distances(features), dtype=np.float64)
    distance = (distance + distance.T) / 2.0
    np.fill_diagonal(distance, 0.0)
    return np.clip(distance, 0.0, 2.0)


def dense_features(features: Any) -> np.ndarray:
    return features.toarray() if hasattr(features, "toarray") else np.asarray(features)


def hierarchy(features: Any, distance: np.ndarray, method: str) -> np.ndarray:
    if method == "ward":
        return linkage(
            dense_features(features),
            method="ward",
            optimal_ordering=len(distance) <= 150,
        )
    condensed = squareform(distance, checks=False)
    return linkage(condensed, method=method, optimal_ordering=len(distance) <= 150)


def hierarchy_input_distances(features: Any, distance: np.ndarray, method: str) -> np.ndarray:
    if method == "ward":
        return pdist(dense_features(features), metric="euclidean")
    return squareform(distance, checks=False)


def renumber_by_leaf_order(labels: np.ndarray, tree: np.ndarray) -> np.ndarray:
    order = leaves_list(tree)
    mapping: dict[int, int] = {}
    next_label = 1
    for index in order:
        old = int(labels[index])
        if old not in mapping:
            mapping[old] = next_label
            next_label += 1
    return np.asarray([mapping[int(value)] for value in labels], dtype=int)


def exact_partition(tree: np.ndarray, k: int) -> np.ndarray:
    raw = cut_tree(tree, n_clusters=[k]).reshape(-1)
    return renumber_by_leaf_order(raw, tree)


def partition_metrics(distance: np.ndarray, labels: np.ndarray) -> dict[str, float | int]:
    counts = Counter(int(item) for item in labels)
    samples = silhouette_samples(distance, labels, metric="precomputed")
    return {
        "clusters": len(counts),
        "silhouette": float(np.mean(samples)),
        "min_cluster_size": min(counts.values()),
        "max_cluster_size": max(counts.values()),
        "singleton_clusters": sum(size == 1 for size in counts.values()),
    }


def silhouette_curve(distance: np.ndarray, tree: np.ndarray, max_k: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for k in range(2, min(max_k, len(distance) - 1) + 1):
        labels = exact_partition(tree, k)
        metric = partition_metrics(distance, labels)
        rows.append({"k": k, **metric})
    return rows


def linkage_sensitivity_rows(
    corpus: str,
    method_name: str,
    features: Any,
    distance: np.ndarray,
    macro_k: int,
    sub_k: int,
    linkage_methods: Sequence[str],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for linkage_method in linkage_methods:
        tree = hierarchy(features, distance, linkage_method)
        for level, k in (("macro", macro_k), ("subcluster", sub_k)):
            labels = exact_partition(tree, k)
            rows.append(
                {
                    "corpus": corpus,
                    "method": method_name,
                    "linkage": linkage_method,
                    "level": level,
                    **partition_metrics(distance, labels),
                }
            )
    return rows


def bootstrap_stability(
    features: Any,
    distance: np.ndarray,
    full_labels: np.ndarray,
    k: int,
    runs: int,
    fraction: float,
    seed: int,
    linkage_method: str,
) -> dict[str, float | int]:
    rng = np.random.default_rng(seed)
    n = len(distance)
    subset_size = max(k + 2, int(round(n * fraction)))
    scores: list[float] = []
    for _ in range(runs):
        subset = np.sort(rng.choice(n, size=subset_size, replace=False))
        subdistance = distance[np.ix_(subset, subset)]
        subfeatures = features[subset]
        subtree = hierarchy(subfeatures, subdistance, linkage_method)
        sublabels = exact_partition(subtree, k)
        scores.append(float(adjusted_rand_score(full_labels[subset], sublabels)))
    values = np.asarray(scores, dtype=float)
    return {
        "runs": runs,
        "subsample_fraction": fraction,
        "mean_ari": float(values.mean()),
        "std_ari": float(values.std(ddof=1)) if len(values) > 1 else 0.0,
        "p10_ari": float(np.quantile(values, 0.10)),
        "min_ari": float(values.min()),
    }


def distinct_terms(
    tfidf_matrix: Any,
    feature_names: np.ndarray,
    labels: np.ndarray,
    cluster_id: int,
    limit: int = 10,
) -> list[str]:
    inside = np.flatnonzero(labels == cluster_id)
    outside = np.flatnonzero(labels != cluster_id)
    mean_inside = np.asarray(tfidf_matrix[inside].mean(axis=0)).ravel()
    if len(outside):
        mean_outside = np.asarray(tfidf_matrix[outside].mean(axis=0)).ravel()
    else:
        mean_outside = np.zeros_like(mean_inside)
    score = mean_inside * np.log2((mean_inside + 1e-5) / (mean_outside + 1e-5))
    score[mean_inside <= 0] = -np.inf
    candidates = np.argsort(score)[::-1]
    terms: list[str] = []
    for index in candidates:
        if not np.isfinite(score[index]) or score[index] <= 0:
            continue
        term = str(feature_names[index])
        if term in CUSTOM_STOP_WORDS:
            continue
        terms.append(term)
        if len(terms) >= limit:
            break
    return terms


def representative_indices(
    papers: Sequence[Paper], distance: np.ndarray, labels: np.ndarray, cluster_id: int
) -> dict[str, int]:
    members = np.flatnonzero(labels == cluster_id)
    within = distance[np.ix_(members, members)]
    medoid = int(members[int(np.argmin(within.mean(axis=1)))])
    if len(set(labels)) > 1 and len(members) > 1:
        samples = silhouette_samples(distance, labels, metric="precomputed")
        boundary = int(members[int(np.argmin(samples[members]))])
    else:
        boundary = medoid
    strongest = sorted(
        (int(index) for index in members),
        key=lambda index: (-papers[index].supported_count, distance[medoid, index], papers[index].title.lower()),
    )[0]
    return {"medoid": medoid, "boundary": boundary, "strongest": strongest}


def cluster_profile_rows(
    corpus: str,
    method: str,
    level: str,
    papers: Sequence[Paper],
    labels: np.ndarray,
    distance: np.ndarray,
    tfidf_matrix: Any,
    feature_names: np.ndarray,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    profiles: list[dict[str, Any]] = []
    representatives: list[dict[str, Any]] = []
    prefix = "M" if level == "macro" else "S"
    for cluster_id in sorted(set(int(item) for item in labels)):
        members = np.flatnonzero(labels == cluster_id)
        cluster_papers = [papers[index] for index in members]
        terms = distinct_terms(tfidf_matrix, feature_names, labels, cluster_id)
        reps = representative_indices(papers, distance, labels, cluster_id)
        criterion_counts = Counter(
            criterion for paper in cluster_papers for criterion in paper.supported_criteria
        )
        verdict_counts = Counter(paper.verdict for paper in cluster_papers)
        tier_counts = Counter(paper.tier or "UNTIERED" for paper in cluster_papers)
        cluster_name = f"{prefix}{cluster_id:02d}"
        profiles.append(
            {
                "corpus": corpus,
                "method": method,
                "level": level,
                "cluster": cluster_name,
                "size": len(members),
                "algorithmic_label": " / ".join(terms[:3]),
                "top_terms": " | ".join(terms),
                "mean_supported_count": round(
                    float(np.mean([paper.supported_count for paper in cluster_papers])), 3
                ),
                "include_count": verdict_counts.get("INCLUDE", 0),
                "exclude_count": verdict_counts.get("EXCLUDE", 0),
                "tier_1": tier_counts.get("TIER_1", 0),
                "tier_2": tier_counts.get("TIER_2", 0),
                "tier_3": tier_counts.get("TIER_3", 0),
                "untiered": tier_counts.get("UNTIERED", 0),
                **{
                    f"{criterion.lower()}_count": criterion_counts.get(criterion, 0)
                    for criterion in CRITERIA
                },
                "medoid_work_id": papers[reps["medoid"]].work_id,
                "medoid_title": papers[reps["medoid"]].title,
                "boundary_work_id": papers[reps["boundary"]].work_id,
                "boundary_title": papers[reps["boundary"]].title,
                "strongest_work_id": papers[reps["strongest"]].work_id,
                "strongest_title": papers[reps["strongest"]].title,
            }
        )
        for role, index in reps.items():
            representatives.append(
                {
                    "corpus": corpus,
                    "method": method,
                    "level": level,
                    "cluster": cluster_name,
                    "algorithmic_label": " / ".join(terms[:3]),
                    "role": role,
                    "work_id": papers[index].work_id,
                    "title": papers[index].title,
                    "verdict": papers[index].verdict,
                    "tier": papers[index].tier,
                    "supported_count": papers[index].supported_count,
                    "supported_criteria": ",".join(papers[index].supported_criteria),
                }
            )
    return profiles, representatives


def assignment_rows(
    corpus: str,
    method: str,
    papers: Sequence[Paper],
    macro_labels: np.ndarray,
    sub_labels: np.ndarray,
    distance: np.ndarray,
) -> list[dict[str, Any]]:
    macro_sil = silhouette_samples(distance, macro_labels, metric="precomputed")
    sub_sil = silhouette_samples(distance, sub_labels, metric="precomputed")
    rows: list[dict[str, Any]] = []
    for index, paper in enumerate(papers):
        rows.append(
            {
                "corpus": corpus,
                "method": method,
                "work_id": paper.work_id,
                "title": paper.title,
                "year": paper.year or "",
                "verdict": paper.verdict,
                "tier": paper.tier,
                "claimed_count": paper.claimed_count,
                "supported_count": paper.supported_count,
                "supported_criteria": ",".join(paper.supported_criteria),
                "macro_cluster": f"M{int(macro_labels[index]):02d}",
                "subcluster": f"S{int(sub_labels[index]):02d}",
                "macro_silhouette": round(float(macro_sil[index]), 6),
                "subcluster_silhouette": round(float(sub_sil[index]), 6),
            }
        )
    return rows


def nearest_neighbor_overlap(first: np.ndarray, second: np.ndarray, k: int) -> float:
    overlaps: list[float] = []
    for index in range(len(first)):
        first_order = [item for item in np.argsort(first[index]) if item != index][:k]
        second_order = [item for item in np.argsort(second[index]) if item != index][:k]
        overlaps.append(len(set(first_order) & set(second_order)) / k)
    return float(np.mean(overlaps))


def coassignment_agreement(first: np.ndarray, second: np.ndarray) -> float:
    upper = np.triu_indices(len(first), k=1)
    first_same = first[upper[0]] == first[upper[1]]
    second_same = second[upper[0]] == second[upper[1]]
    return float(np.mean(first_same == second_same))


def cross_method_metrics(
    tfidf_distance: np.ndarray,
    semantic_distance: np.ndarray,
    tfidf_labels: np.ndarray,
    semantic_labels: np.ndarray,
) -> dict[str, float]:
    upper = np.triu_indices(len(tfidf_distance), k=1)
    rho = spearmanr(tfidf_distance[upper], semantic_distance[upper]).statistic
    return {
        "adjusted_rand_index": float(adjusted_rand_score(tfidf_labels, semantic_labels)),
        "normalized_mutual_information": float(
            normalized_mutual_info_score(tfidf_labels, semantic_labels)
        ),
        "coassignment_agreement": coassignment_agreement(tfidf_labels, semantic_labels),
        "pairwise_distance_spearman": float(rho),
        "top_5_neighbor_overlap": nearest_neighbor_overlap(tfidf_distance, semantic_distance, 5),
        "top_10_neighbor_overlap": nearest_neighbor_overlap(tfidf_distance, semantic_distance, 10),
    }


def consensus_match_rows(
    corpus: str,
    level: str,
    papers: Sequence[Paper],
    tfidf_labels: np.ndarray,
    semantic_labels: np.ndarray,
) -> list[dict[str, Any]]:
    prefix = "M" if level == "macro" else "S"
    tfidf_sets = {
        cluster_id: set(np.flatnonzero(tfidf_labels == cluster_id))
        for cluster_id in sorted(set(int(item) for item in tfidf_labels))
    }
    semantic_sets = {
        cluster_id: set(np.flatnonzero(semantic_labels == cluster_id))
        for cluster_id in sorted(set(int(item) for item in semantic_labels))
    }
    candidates: list[dict[str, Any]] = []
    for tfidf_id, tfidf_members in tfidf_sets.items():
        for semantic_id, semantic_members in semantic_sets.items():
            overlap = tfidf_members & semantic_members
            if not overlap:
                continue
            union = tfidf_members | semantic_members
            candidates.append(
                {
                    "corpus": corpus,
                    "level": level,
                    "tfidf_cluster": f"{prefix}{tfidf_id:02d}",
                    "semantic_cluster": f"{prefix}{semantic_id:02d}",
                    "overlap_papers": len(overlap),
                    "tfidf_size": len(tfidf_members),
                    "semantic_size": len(semantic_members),
                    "jaccard": len(overlap) / len(union),
                    "overlap_work_ids": ",".join(papers[index].work_id for index in sorted(overlap)),
                }
            )
    return sorted(
        candidates,
        key=lambda row: (-float(row["jaccard"]), -int(row["overlap_papers"]), row["tfidf_cluster"]),
    )


def classical_mds(distance: np.ndarray) -> np.ndarray:
    n = len(distance)
    centering = np.eye(n) - np.ones((n, n)) / n
    gram = -0.5 * centering @ (distance**2) @ centering
    eigenvalues, eigenvectors = np.linalg.eigh(gram)
    order = np.argsort(eigenvalues)[::-1]
    positive = [index for index in order if eigenvalues[index] > 0][:2]
    if len(positive) < 2:
        return np.zeros((n, 2))
    coordinates = eigenvectors[:, positive] * np.sqrt(eigenvalues[positive])
    # Eigenvector signs are mathematically arbitrary. Fix each axis orientation
    # so regenerated maps do not flip despite identical inputs.
    for axis in range(coordinates.shape[1]):
        anchor = int(np.argmax(np.abs(coordinates[:, axis])))
        if coordinates[anchor, axis] < 0:
            coordinates[:, axis] *= -1
    return coordinates


def plot_dendrogram(
    path: Path,
    tree: np.ndarray,
    papers: Sequence[Paper],
    macro_k: int,
    method: str,
    corpus: str,
    linkage_method: str,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    n = len(papers)
    if n <= 120:
        fig_height = max(14, n * 0.24)
        labels = [paper.title[:75] for paper in papers]
        kwargs: dict[str, Any] = {"labels": labels, "leaf_font_size": 6}
    else:
        fig_height = 15
        kwargs = {
            "truncate_mode": "lastp",
            "p": 45,
            "show_contracted": True,
            "leaf_font_size": 7,
        }
    fig, axis = plt.subplots(figsize=(14, fig_height))
    n_rows = len(tree)
    lower_index = n - macro_k - 1
    upper_index = n - macro_k
    if 0 <= lower_index < n_rows and 0 <= upper_index < n_rows:
        threshold = float((tree[lower_index, 2] + tree[upper_index, 2]) / 2)
    else:
        threshold = None
    dendrogram(tree, orientation="right", ax=axis, color_threshold=threshold, **kwargs)
    axis.set_title(f"{corpus.title()} corpus — {method.upper()} {linkage_method}-linkage hierarchy")
    if linkage_method == "ward":
        axis.set_xlabel("Ward merge distance (Euclidean on L2-normalized vectors)")
    else:
        axis.set_xlabel("Cosine distance")
    axis.set_ylabel("Paper" if n <= 120 else "Contracted branch (paper count in parentheses)")
    axis.grid(axis="x", alpha=0.18)
    fig.tight_layout()
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def plot_silhouette_curves(path: Path, rows: Sequence[dict[str, Any]], corpus: str) -> None:
    fig, axis = plt.subplots(figsize=(9, 5.5))
    for method, marker in (("tfidf", "o"), ("semantic", "s")):
        subset = [row for row in rows if row["method"] == method]
        axis.plot(
            [row["k"] for row in subset],
            [row["silhouette"] for row in subset],
            marker=marker,
            markersize=3,
            linewidth=1.5,
            label=method.upper(),
        )
    axis.set_title(f"{corpus.title()} corpus — silhouette across hierarchy cuts")
    axis.set_xlabel("Number of clusters (k)")
    axis.set_ylabel("Mean silhouette (cosine)")
    axis.grid(alpha=0.2)
    axis.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def plot_comparison_map(
    path: Path,
    papers: Sequence[Paper],
    distances: dict[str, np.ndarray],
    labels: dict[str, np.ndarray],
    corpus: str,
) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(14, 6.5))
    for axis, method in zip(axes, ("tfidf", "semantic")):
        coords = classical_mds(distances[method])
        cluster_labels = labels[method]
        axis.scatter(
            coords[:, 0],
            coords[:, 1],
            c=cluster_labels,
            cmap="tab20",
            s=28 if len(papers) <= 120 else 14,
            alpha=0.82,
            edgecolors="none",
        )
        for cluster_id in sorted(set(int(item) for item in cluster_labels)):
            members = np.flatnonzero(cluster_labels == cluster_id)
            within = distances[method][np.ix_(members, members)]
            medoid = int(members[int(np.argmin(within.mean(axis=1)))])
            axis.annotate(
                f"M{cluster_id:02d}",
                (coords[medoid, 0], coords[medoid, 1]),
                fontsize=8,
                fontweight="bold",
            )
        axis.set_title(method.upper())
        axis.set_xlabel("Classical MDS axis 1")
        axis.set_ylabel("Classical MDS axis 2")
        axis.grid(alpha=0.12)
    fig.suptitle(f"{corpus.title()} corpus — cosine-distance views (colors are macroclusters)")
    fig.tight_layout()
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def plot_contingency(
    path: Path, first: np.ndarray, second: np.ndarray, corpus: str, level: str
) -> None:
    first_ids = sorted(set(int(item) for item in first))
    second_ids = sorted(set(int(item) for item in second))
    matrix = np.zeros((len(first_ids), len(second_ids)), dtype=int)
    first_map = {value: index for index, value in enumerate(first_ids)}
    second_map = {value: index for index, value in enumerate(second_ids)}
    for left, right in zip(first, second):
        matrix[first_map[int(left)], second_map[int(right)]] += 1
    fig_width = max(7, len(second_ids) * 0.45)
    fig_height = max(5.5, len(first_ids) * 0.42)
    fig, axis = plt.subplots(figsize=(fig_width, fig_height))
    image = axis.imshow(matrix, cmap="viridis", aspect="auto")
    for row in range(matrix.shape[0]):
        for column in range(matrix.shape[1]):
            if matrix[row, column]:
                axis.text(column, row, str(matrix[row, column]), ha="center", va="center", fontsize=7)
    prefix = "M" if level == "macro" else "S"
    axis.set_xticks(range(len(second_ids)), [f"{prefix}{item:02d}" for item in second_ids], rotation=45)
    axis.set_yticks(range(len(first_ids)), [f"{prefix}{item:02d}" for item in first_ids])
    axis.set_xlabel("Semantic clusters")
    axis.set_ylabel("TF-IDF clusters")
    axis.set_title(f"{corpus.title()} corpus — {level} cluster overlap")
    fig.colorbar(image, ax=axis, label="Papers")
    fig.tight_layout()
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def plot_criterion_heatmap(
    path: Path,
    papers: Sequence[Paper],
    method_labels: dict[str, np.ndarray],
    corpus: str,
) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(14, 7), layout="constrained")
    for axis, method in zip(axes, ("tfidf", "semantic")):
        labels = method_labels[method]
        cluster_ids = sorted(set(int(item) for item in labels))
        matrix = np.zeros((len(cluster_ids), len(CRITERIA)), dtype=float)
        for row_index, cluster_id in enumerate(cluster_ids):
            members = np.flatnonzero(labels == cluster_id)
            for col_index, criterion in enumerate(CRITERIA):
                matrix[row_index, col_index] = np.mean(
                    [criterion in papers[index].supported_criteria for index in members]
                )
        image = axis.imshow(matrix, vmin=0, vmax=1, cmap="magma", aspect="auto")
        axis.set_xticks(
            range(len(CRITERIA)),
            [criterion.replace("_", " ").title() for criterion in CRITERIA],
            rotation=35,
            ha="right",
        )
        axis.set_yticks(range(len(cluster_ids)), [f"M{item:02d}" for item in cluster_ids])
        axis.set_title(method.upper())
        axis.set_xlabel("Supported criterion (overlay only)")
        axis.set_ylabel("Macrocluster")
    fig.colorbar(
        image,
        ax=axes.ravel().tolist(),
        label="Share of papers supporting criterion",
        shrink=0.78,
        fraction=0.035,
        pad=0.035,
    )
    fig.suptitle(f"{corpus.title()} corpus — criterion composition after clustering")
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def semantic_embeddings(
    texts_by_corpus: dict[str, list[str]],
    args: argparse.Namespace,
    semantic_config: dict[str, Any],
) -> tuple[dict[str, np.ndarray], dict[str, list[int]], dict[str, Any]]:
    from sentence_transformers import SentenceTransformer

    prompt = semantic_config["prompt"]
    model_path = Path(args.model_path)
    weight_hash = "remote-or-unresolved"
    weight_file = model_path / "model.safetensors"
    if weight_file.exists():
        weight_hash = sha256_file(weight_file)

    model = SentenceTransformer(args.model_path, device="cpu")
    model.max_seq_length = args.max_seq_length
    tokenizer_limit = model.tokenizer.model_max_length
    model.tokenizer.model_max_length = 10**9
    all_texts: list[str] = []
    slices: dict[str, slice] = {}
    raw_token_counts: dict[str, list[int]] = {}
    start = 0
    for corpus, texts in texts_by_corpus.items():
        counts = [
            len(model.tokenizer.encode(prompt + text, add_special_tokens=True, truncation=False))
            for text in texts
        ]
        raw_token_counts[corpus] = counts
        all_texts.extend(texts)
        slices[corpus] = slice(start, start + len(texts))
        start += len(texts)

    prompt_tokens = len(
        model.tokenizer.encode(prompt, add_special_tokens=False, truncation=False)
    )
    chunk_size = args.max_seq_length - prompt_tokens - 2
    if chunk_size < 64:
        raise ValueError("The semantic prompt leaves fewer than 64 tokens for paper text")
    chunk_overlap = min(64, chunk_size // 4)
    chunk_stride = chunk_size - chunk_overlap
    encoded_texts: list[str] = []
    chunk_to_original: list[int] = []
    chunked_originals = 0
    for original_index, text in enumerate(all_texts):
        raw_count = len(
            model.tokenizer.encode(prompt + text, add_special_tokens=True, truncation=False)
        )
        if raw_count <= args.max_seq_length:
            encoded_texts.append(text)
            chunk_to_original.append(original_index)
            continue
        chunked_originals += 1
        token_ids = model.tokenizer.encode(text, add_special_tokens=False, truncation=False)
        for chunk_start in range(0, len(token_ids), chunk_stride):
            chunk_ids = token_ids[chunk_start : chunk_start + chunk_size]
            encoded_texts.append(
                model.tokenizer.decode(
                    chunk_ids,
                    skip_special_tokens=True,
                    clean_up_tokenization_spaces=True,
                )
            )
            chunk_to_original.append(original_index)
            if chunk_start + chunk_size >= len(token_ids):
                break
    model.tokenizer.model_max_length = tokenizer_limit

    cache_digest = sha256_text(
        [
            args.model_id,
            args.model_revision,
            weight_hash,
            str(args.max_seq_length),
            prompt,
            f"overlap={chunk_overlap}",
            *all_texts,
        ]
    )
    cache_path = DERIVED_ROOT / "semantic_embeddings.npy"
    cache_meta_path = DERIVED_ROOT / "semantic_embeddings.meta.json"
    embeddings: np.ndarray | None = None
    if not args.force_embeddings and cache_path.exists() and cache_meta_path.exists():
        cache_meta = json.loads(cache_meta_path.read_text(encoding="utf-8"))
        if cache_meta.get("cache_digest") == cache_digest:
            embeddings = np.load(cache_path)

    started = time.time()
    if embeddings is None:
        chunk_embeddings = model.encode(
            encoded_texts,
            prompt=prompt,
            batch_size=args.batch_size,
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=False,
        ).astype(np.float32)
        embeddings = np.zeros((len(all_texts), chunk_embeddings.shape[1]), dtype=np.float32)
        chunk_counts = np.zeros(len(all_texts), dtype=np.int32)
        for chunk_index, original_index in enumerate(chunk_to_original):
            embeddings[original_index] += chunk_embeddings[chunk_index]
            chunk_counts[original_index] += 1
        embeddings /= np.maximum(chunk_counts[:, None], 1)
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        embeddings = embeddings / np.maximum(norms, 1e-12)
        DERIVED_ROOT.mkdir(parents=True, exist_ok=True)
        np.save(cache_path, embeddings)
        cache_meta_path.write_text(
            json.dumps(
                {
                    "cache_digest": cache_digest,
                    "model_id": args.model_id,
                    "model_revision": args.model_revision,
                    "model_weight_sha256": weight_hash,
                    "max_sequence_length": args.max_seq_length,
                    "prompt": prompt,
                    "chunk_overlap_tokens": chunk_overlap,
                    "chunked_papers": chunked_originals,
                    "encoded_chunks": len(encoded_texts),
                    "shape": list(embeddings.shape),
                },
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
    elapsed = time.time() - started
    result = {corpus: embeddings[span] for corpus, span in slices.items()}
    metadata = {
        "model_id": args.model_id,
        "model_revision": args.model_revision,
        "model_weight_sha256": weight_hash,
        "prompt": prompt,
        "max_sequence_length": args.max_seq_length,
        "chunk_overlap_tokens": chunk_overlap,
        "chunked_papers": chunked_originals,
        "encoded_chunks": len(encoded_texts),
        "embedding_dimensions": int(embeddings.shape[1]),
        "encoding_or_cache_load_seconds": round(elapsed, 3),
        "cache_digest": cache_digest,
    }
    return result, raw_token_counts, metadata


def markdown_cluster_cards(profile_rows: Sequence[dict[str, Any]]) -> str:
    lines = [
        "# Generated cluster cards",
        "",
        "Labels are the three most distinctive TF-IDF terms for each partition. Semantic",
        "clusters are labeled post hoc with the same keyword diagnostic; no generative model",
        "was used to form or label clusters.",
        "",
    ]
    grouped: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in profile_rows:
        grouped[(row["corpus"], row["method"], row["level"])].append(row)
    for key in sorted(grouped):
        corpus, method, level = key
        lines.extend([f"## {corpus.title()} · {method.upper()} · {level}", ""])
        for row in sorted(grouped[key], key=lambda item: item["cluster"]):
            lines.extend(
                [
                    f"### {row['cluster']} — {row['algorithmic_label']}",
                    "",
                    f"- Size: {row['size']}; mean supported criteria: {row['mean_supported_count']}",
                    f"- Medoid: {row['medoid_title']}",
                    f"- Boundary case: {row['boundary_title']}",
                    f"- Strongest-evidence member: {row['strongest_title']}",
                    f"- Terms: {row['top_terms']}",
                    "",
                ]
            )
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    if args.bootstrap_runs is not None:
        config["bootstrap_runs"] = args.bootstrap_runs
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    DERIVED_ROOT.mkdir(parents=True, exist_ok=True)
    FIGURE_ROOT.mkdir(parents=True, exist_ok=True)

    all_papers = load_papers(args.db)
    corpora: dict[str, list[Paper]] = {
        "included": [paper for paper in all_papers if paper.verdict == "INCLUDE"],
        "audited": list(all_papers),
    }
    for corpus, papers in corpora.items():
        expected = int(config["corpora"][corpus]["papers"])
        if len(papers) != expected:
            raise RuntimeError(f"{corpus} corpus has {len(papers)} papers; expected {expected}")

    texts_by_corpus: dict[str, list[str]] = {}
    policies_by_corpus: dict[str, list[str]] = {}
    for corpus, papers in corpora.items():
        pairs = [analysis_text(paper, corpus) for paper in papers]
        texts_by_corpus[corpus] = [pair[0] for pair in pairs]
        policies_by_corpus[corpus] = [pair[1] for pair in pairs]

    tfidf_features: dict[str, Any] = {}
    feature_matrices: dict[str, dict[str, Any]] = defaultdict(dict)
    vectorizers: dict[str, TfidfVectorizer] = {}
    distances: dict[str, dict[str, np.ndarray]] = defaultdict(dict)
    trees: dict[str, dict[str, np.ndarray]] = defaultdict(dict)
    for corpus in corpora:
        matrix, vectorizer = fit_tfidf(texts_by_corpus[corpus], config["tfidf"])
        tfidf_features[corpus] = matrix
        feature_matrices[corpus]["tfidf"] = matrix
        vectorizers[corpus] = vectorizer
        distances[corpus]["tfidf"] = safe_cosine_distances(matrix)
        trees[corpus]["tfidf"] = hierarchy(
            matrix, distances[corpus]["tfidf"], config["linkage"]
        )

    raw_token_counts: dict[str, list[int]] = {corpus: [0] * len(papers) for corpus, papers in corpora.items()}
    semantic_meta: dict[str, Any] = {"status": "skipped"}
    if not args.skip_semantic:
        embedding_features, raw_token_counts, semantic_meta = semantic_embeddings(
            texts_by_corpus, args, config["semantic"]
        )
        for corpus in corpora:
            feature_matrices[corpus]["semantic"] = embedding_features[corpus]
            distances[corpus]["semantic"] = safe_cosine_distances(embedding_features[corpus])
            trees[corpus]["semantic"] = hierarchy(
                embedding_features[corpus], distances[corpus]["semantic"], config["linkage"]
            )

    text_rows: list[dict[str, Any]] = []
    for corpus, papers in corpora.items():
        for index, paper in enumerate(papers):
            token_count = raw_token_counts[corpus][index]
            text_rows.append(
                {
                    "corpus": corpus,
                    "work_id": paper.work_id,
                    "title": paper.title,
                    "verdict": paper.verdict,
                    "text_policy": policies_by_corpus[corpus][index],
                    "characters": len(texts_by_corpus[corpus][index]),
                    "semantic_tokens_before_truncation": token_count,
                    "semantic_chunked": int(token_count > args.max_seq_length) if token_count else "",
                    "semantic_truncated": 0 if token_count else "",
                    "analysis_text": texts_by_corpus[corpus][index],
                }
            )
    write_tsv(OUTPUT_ROOT / "paper_texts.tsv", text_rows)

    metrics: dict[str, Any] = {
        "run": {
            "database": str(args.db.resolve()),
            "database_sha256": sha256_file(args.db),
            "config": config,
            "semantic": semantic_meta,
            "versions": {
                package: importlib.metadata.version(package)
                for package in (
                    "numpy",
                    "scipy",
                    "scikit-learn",
                    "matplotlib",
                    "sentence-transformers",
                    "torch",
                    "transformers",
                )
                if not (args.skip_semantic and package in {"sentence-transformers", "torch", "transformers"})
            },
            "python": sys.version,
        },
        "corpora": {},
    }
    silhouette_rows: list[dict[str, Any]] = []
    cross_rows: list[dict[str, Any]] = []
    consensus_rows: list[dict[str, Any]] = []
    profile_rows: list[dict[str, Any]] = []
    representative_rows: list[dict[str, Any]] = []
    assignment_rows_all: list[dict[str, Any]] = []
    cluster_map_rows: list[dict[str, Any]] = []
    sensitivity_rows: list[dict[str, Any]] = []
    partitions: dict[str, dict[str, dict[str, np.ndarray]]] = defaultdict(dict)

    methods = ("tfidf",) if args.skip_semantic else ("tfidf", "semantic")
    for corpus, papers in corpora.items():
        corpus_config = config["corpora"][corpus]
        macro_k = int(corpus_config["macro_clusters"])
        sub_k = int(corpus_config["subclusters"])
        metrics["corpora"][corpus] = {}
        partitions[corpus] = {}
        for method_index, method in enumerate(methods):
            distance = distances[corpus][method]
            tree = trees[corpus][method]
            macro_labels = exact_partition(tree, macro_k)
            sub_labels = exact_partition(tree, sub_k)
            partitions[corpus][method] = {"macro": macro_labels, "subcluster": sub_labels}
            cophenetic = float(
                cophenet(
                    tree,
                    hierarchy_input_distances(
                        feature_matrices[corpus][method], distance, config["linkage"]
                    ),
                )[0]
            )
            method_metrics: dict[str, Any] = {"cophenetic_correlation": cophenetic}
            profile_labels: dict[str, dict[str, str]] = {}
            method_sensitivity = linkage_sensitivity_rows(
                corpus,
                method,
                feature_matrices[corpus][method],
                distance,
                macro_k,
                sub_k,
                config["linkage_sensitivity"],
            )
            sensitivity_rows.extend(method_sensitivity)
            method_metrics["linkage_sensitivity"] = method_sensitivity
            for level_index, (level, labels, k) in enumerate(
                (("macro", macro_labels, macro_k), ("subcluster", sub_labels, sub_k))
            ):
                level_metrics = partition_metrics(distance, labels)
                level_metrics["bootstrap_stability"] = bootstrap_stability(
                    feature_matrices[corpus][method],
                    distance,
                    labels,
                    k,
                    int(config["bootstrap_runs"]),
                    float(config["bootstrap_subsample_fraction"]),
                    int(config["random_seed"]) + method_index * 1000 + level_index * 100 + len(papers),
                    config["linkage"],
                )
                method_metrics[level] = level_metrics
                profiles, reps = cluster_profile_rows(
                    corpus,
                    method,
                    level,
                    papers,
                    labels,
                    distance,
                    tfidf_features[corpus],
                    vectorizers[corpus].get_feature_names_out(),
                )
                profile_rows.extend(profiles)
                representative_rows.extend(reps)
                profile_labels[level] = {
                    row["cluster"]: row["algorithmic_label"] for row in profiles
                }
            metrics["corpora"][corpus][method] = method_metrics
            current_assignments = assignment_rows(
                corpus, method, papers, macro_labels, sub_labels, distance
            )
            assignment_rows_all.extend(current_assignments)
            coordinates = classical_mds(distance)
            for index, assignment in enumerate(current_assignments):
                macro_cluster = assignment["macro_cluster"]
                subcluster = assignment["subcluster"]
                cluster_map_rows.append(
                    {
                        "corpus": corpus,
                        "method": method,
                        "work_id": assignment["work_id"],
                        "title": assignment["title"],
                        "year": assignment["year"],
                        "verdict": assignment["verdict"],
                        "tier": assignment["tier"],
                        "supported_count": assignment["supported_count"],
                        "supported_criteria": assignment["supported_criteria"],
                        "macro_cluster": macro_cluster,
                        "macro_label": profile_labels["macro"][macro_cluster],
                        "subcluster": subcluster,
                        "subcluster_label": profile_labels["subcluster"][subcluster],
                        "macro_silhouette": assignment["macro_silhouette"],
                        "subcluster_silhouette": assignment["subcluster_silhouette"],
                        "mds_x": round(float(coordinates[index, 0]), 8),
                        "mds_y": round(float(coordinates[index, 1]), 8),
                    }
                )
            for row in silhouette_curve(distance, tree, int(corpus_config["silhouette_scan_max_k"])):
                silhouette_rows.append({"corpus": corpus, "method": method, **row})

            plot_dendrogram(
                FIGURE_ROOT / f"{corpus}_{method}_dendrogram.png",
                tree,
                papers,
                macro_k,
                method,
                corpus,
                config["linkage"],
            )

        if not args.skip_semantic:
            for level in ("macro", "subcluster"):
                comparison = cross_method_metrics(
                    distances[corpus]["tfidf"],
                    distances[corpus]["semantic"],
                    partitions[corpus]["tfidf"][level],
                    partitions[corpus]["semantic"][level],
                )
                metrics["corpora"][corpus][f"cross_method_{level}"] = comparison
                cross_rows.append({"corpus": corpus, "level": level, **comparison})
                consensus_rows.extend(
                    consensus_match_rows(
                        corpus,
                        level,
                        papers,
                        partitions[corpus]["tfidf"][level],
                        partitions[corpus]["semantic"][level],
                    )
                )
                plot_contingency(
                    FIGURE_ROOT / f"{corpus}_{level}_method_overlap.png",
                    partitions[corpus]["tfidf"][level],
                    partitions[corpus]["semantic"][level],
                    corpus,
                    level,
                )
            plot_comparison_map(
                FIGURE_ROOT / f"{corpus}_method_comparison_map.png",
                papers,
                distances[corpus],
                {
                    "tfidf": partitions[corpus]["tfidf"]["macro"],
                    "semantic": partitions[corpus]["semantic"]["macro"],
                },
                corpus,
            )
            plot_criterion_heatmap(
                FIGURE_ROOT / f"{corpus}_criterion_composition.png",
                papers,
                {
                    "tfidf": partitions[corpus]["tfidf"]["macro"],
                    "semantic": partitions[corpus]["semantic"]["macro"],
                },
                corpus,
            )

    for corpus in corpora:
        plot_silhouette_curves(
            FIGURE_ROOT / f"{corpus}_silhouette_curves.png",
            [row for row in silhouette_rows if row["corpus"] == corpus],
            corpus,
        )

    write_tsv(OUTPUT_ROOT / "cluster_assignments.tsv", assignment_rows_all)
    write_tsv(OUTPUT_ROOT / "cluster_map_points.tsv", cluster_map_rows)
    write_tsv(OUTPUT_ROOT / "cluster_profiles.tsv", profile_rows)
    write_tsv(OUTPUT_ROOT / "representative_papers.tsv", representative_rows)
    write_tsv(OUTPUT_ROOT / "silhouette_curves.tsv", silhouette_rows)
    write_tsv(OUTPUT_ROOT / "linkage_sensitivity.tsv", sensitivity_rows)
    if cross_rows:
        write_tsv(OUTPUT_ROOT / "cross_method_metrics.tsv", cross_rows)
        write_tsv(OUTPUT_ROOT / "consensus_cluster_matches.tsv", consensus_rows)
    (OUTPUT_ROOT / "metrics.json").write_text(
        json.dumps(metrics, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (OUTPUT_ROOT / "generated_cluster_cards.md").write_text(
        markdown_cluster_cards(profile_rows), encoding="utf-8"
    )
    print(json.dumps(metrics, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

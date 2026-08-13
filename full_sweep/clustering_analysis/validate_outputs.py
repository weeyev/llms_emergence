#!/usr/bin/env python3
"""Fail-closed validation for the delivered clustering outputs."""

from __future__ import annotations

import csv
import json
import sqlite3
from collections import defaultdict
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "outputs"
DB = HERE.parent / "data" / "sweep.sqlite"


def read_tsv(name: str) -> list[dict[str, str]]:
    with (OUTPUT / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def main() -> int:
    failures: list[str] = []
    config = json.loads((HERE / "config.json").read_text(encoding="utf-8"))
    assignments = read_tsv("cluster_assignments.tsv")
    map_points = read_tsv("cluster_map_points.tsv")
    profiles = read_tsv("cluster_profiles.tsv")
    representatives = read_tsv("representative_papers.tsv")
    paper_texts = read_tsv("paper_texts.tsv")
    cross_metrics = read_tsv("cross_method_metrics.tsv")
    sensitivity = read_tsv("linkage_sensitivity.tsv")
    consensus = read_tsv("consensus_cluster_matches.tsv")
    metrics = json.loads((OUTPUT / "metrics.json").read_text(encoding="utf-8"))

    conn = sqlite3.connect(DB)
    db_total = conn.execute("SELECT COUNT(*) FROM paper_decisions").fetchone()[0]
    db_included = conn.execute(
        "SELECT COUNT(*) FROM paper_decisions WHERE verdict='INCLUDE'"
    ).fetchone()[0]
    db_ids = {row[0] for row in conn.execute("SELECT work_id FROM paper_decisions")}
    conn.close()
    require(db_total == 333, f"database has {db_total} decisions, expected 333", failures)
    require(db_included == 92, f"database has {db_included} includes, expected 92", failures)

    expected_assignment_rows = 2 * (db_total + db_included)
    require(
        len(assignments) == expected_assignment_rows,
        f"assignment rows={len(assignments)}, expected {expected_assignment_rows}",
        failures,
    )
    assignment_keys = {
        (row["corpus"], row["method"], row["work_id"]) for row in assignments
    }
    require(
        len(assignment_keys) == len(assignments),
        "duplicate paper assignment within a corpus/method",
        failures,
    )
    require(
        {row["work_id"] for row in assignments if row["corpus"] == "audited"} == db_ids,
        "audited assignment IDs differ from database decisions",
        failures,
    )
    map_keys = {(row["corpus"], row["method"], row["work_id"]) for row in map_points}
    require(
        len(map_points) == expected_assignment_rows,
        f"map point rows={len(map_points)}, expected {expected_assignment_rows}",
        failures,
    )
    require(map_keys == assignment_keys, "map point IDs differ from cluster assignments", failures)
    require(
        all(
            np.isfinite(float(row[axis]))
            for row in map_points
            for axis in ("mds_x", "mds_y")
        ),
        "map points contain non-finite coordinates",
        failures,
    )
    require(
        all(row["macro_label"] and row["subcluster_label"] for row in map_points),
        "map points contain unlabeled clusters",
        failures,
    )
    assignment_by_key = {
        (row["corpus"], row["method"], row["work_id"]): row for row in assignments
    }
    require(
        all(
            row["macro_cluster"] == assignment_by_key[key]["macro_cluster"]
            and row["subcluster"] == assignment_by_key[key]["subcluster"]
            for row in map_points
            for key in [(row["corpus"], row["method"], row["work_id"])]
        ),
        "map cluster memberships differ from assignments",
        failures,
    )

    for corpus, corpus_config in config["corpora"].items():
        expected_n = int(corpus_config["papers"])
        for method in ("tfidf", "semantic"):
            rows = [
                row
                for row in assignments
                if row["corpus"] == corpus and row["method"] == method
            ]
            require(
                len(rows) == expected_n,
                f"{corpus}/{method} has {len(rows)} rows, expected {expected_n}",
                failures,
            )
            require(
                len({row["macro_cluster"] for row in rows})
                == int(corpus_config["macro_clusters"]),
                f"{corpus}/{method} macrocluster count mismatch",
                failures,
            )
            require(
                len({row["subcluster"] for row in rows})
                == int(corpus_config["subclusters"]),
                f"{corpus}/{method} subcluster count mismatch",
                failures,
            )
            parent_by_subcluster: dict[str, set[str]] = defaultdict(set)
            for row in rows:
                parent_by_subcluster[row["subcluster"]].add(row["macro_cluster"])
            require(
                all(len(parents) == 1 for parents in parent_by_subcluster.values()),
                f"{corpus}/{method} hierarchy is not nested",
                failures,
            )
            require(
                all(np.isfinite(float(row["macro_silhouette"])) for row in rows),
                f"{corpus}/{method} has non-finite silhouettes",
                failures,
            )
            point_rows = [
                row
                for row in map_points
                if row["corpus"] == corpus and row["method"] == method
            ]
            for axis in ("mds_x", "mds_y"):
                coordinates = np.asarray([float(row[axis]) for row in point_rows])
                require(
                    float(np.ptp(coordinates)) > 0,
                    f"{corpus}/{method} {axis} is degenerate",
                    failures,
                )

    expected_profile_rows = 2 * ((6 + 15) + (10 + 25))
    require(
        len(profiles) == expected_profile_rows,
        f"profile rows={len(profiles)}, expected {expected_profile_rows}",
        failures,
    )
    require(
        len(representatives) == 3 * len(profiles),
        "representative rows must contain medoid, boundary, and strongest for each cluster",
        failures,
    )
    roles_by_cluster: dict[tuple[str, str, str, str], set[str]] = defaultdict(set)
    for row in representatives:
        roles_by_cluster[
            (row["corpus"], row["method"], row["level"], row["cluster"])
        ].add(row["role"])
    require(
        all(roles == {"medoid", "boundary", "strongest"} for roles in roles_by_cluster.values()),
        "one or more clusters lack a representative role",
        failures,
    )
    require(len(paper_texts) == db_total + db_included, "paper text row count mismatch", failures)
    require(
        all(row["semantic_truncated"] in {"", "0"} for row in paper_texts),
        "a semantic input was truncated rather than chunked",
        failures,
    )
    require(len(cross_metrics) == 4, "cross-method metrics row count mismatch", failures)
    require(len(sensitivity) == 32, "linkage sensitivity row count mismatch", failures)
    require(bool(consensus), "consensus cluster match output is empty", failures)

    embeddings = np.load(OUTPUT / "derived" / "semantic_embeddings.npy")
    require(
        embeddings.shape == (db_total + db_included, 768),
        f"embedding shape={embeddings.shape}, expected {(db_total + db_included, 768)}",
        failures,
    )
    require(np.isfinite(embeddings).all(), "semantic embeddings contain NaN/Inf", failures)
    norms = np.linalg.norm(embeddings, axis=1)
    require(np.allclose(norms, 1.0, atol=1e-4), "semantic embeddings are not L2-normalized", failures)

    for corpus in ("included", "audited"):
        for method in ("tfidf", "semantic"):
            current = metrics["corpora"][corpus][method]
            for level in ("macro", "subcluster"):
                require(
                    current[level]["singleton_clusters"] == 0,
                    f"{corpus}/{method}/{level} has singleton clusters",
                    failures,
                )
                require(
                    current[level]["bootstrap_stability"]["runs"] == config["bootstrap_runs"],
                    f"{corpus}/{method}/{level} bootstrap run count mismatch",
                    failures,
                )

    required_figures = {
        f"{corpus}_{name}.png"
        for corpus in ("included", "audited")
        for name in (
            "tfidf_dendrogram",
            "semantic_dendrogram",
            "method_comparison_map",
            "criterion_composition",
            "macro_method_overlap",
            "subcluster_method_overlap",
            "silhouette_curves",
        )
    }
    existing_figures = {path.name for path in (OUTPUT / "figures").glob("*.png")}
    require(required_figures <= existing_figures, "one or more required figures are missing", failures)

    if failures:
        print("FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("PASS")
    print(
        f"Validated {len(assignments)} assignments, {len(profiles)} cluster profiles, "
        f"{len(map_points)} map points, {len(representatives)} representatives, "
        f"and {len(required_figures)} figures."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

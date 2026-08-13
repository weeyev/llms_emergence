#!/usr/bin/env python3
"""Build the self-contained paper-cluster map fragment from audited outputs."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "outputs"
DEFAULT_POINTS = OUTPUT / "cluster_map_points.tsv"
DEFAULT_TEMPLATE = HERE / "cluster_map_template.html"
DEFAULT_FRAGMENT = OUTPUT / "cluster_map.fragment.html"

COLUMNS = (
    "corpus",
    "method",
    "work_id",
    "title",
    "year",
    "verdict",
    "tier",
    "supported_count",
    "supported_criteria",
    "macro_cluster",
    "macro_label",
    "subcluster",
    "subcluster_label",
    "macro_silhouette",
    "subcluster_silhouette",
    "mds_x",
    "mds_y",
)
INTEGER_COLUMNS = {"year", "supported_count"}
FLOAT_COLUMNS = {"macro_silhouette", "subcluster_silhouette", "mds_x", "mds_y"}
PLACEHOLDER = "__CLUSTER_MAP_DATA__"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--points", type=Path, default=DEFAULT_POINTS)
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE)
    parser.add_argument("--fragment", type=Path, default=DEFAULT_FRAGMENT)
    parser.add_argument(
        "--inline-path",
        type=Path,
        help="Optional second fragment path for the conversation visualization.",
    )
    return parser.parse_args()


def parse_value(column: str, value: str) -> Any:
    if column in INTEGER_COLUMNS:
        return int(value) if value else None
    if column in FLOAT_COLUMNS:
        return float(value)
    return value


def load_payload(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if tuple(reader.fieldnames or ()) != COLUMNS:
            raise RuntimeError(
                "Unexpected cluster-map schema: "
                + ", ".join(reader.fieldnames or ())
            )
        rows = [
            [parse_value(column, row[column]) for column in COLUMNS]
            for row in reader
        ]
    return {"columns": list(COLUMNS), "rows": rows}


def write_fragment(path: Path, fragment: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(fragment, encoding="utf-8")


def main() -> int:
    args = parse_args()
    template = args.template.read_text(encoding="utf-8")
    if template.count(PLACEHOLDER) != 1:
        raise RuntimeError("Cluster-map template must contain exactly one data placeholder")
    payload = json.dumps(
        load_payload(args.points),
        ensure_ascii=False,
        separators=(",", ":"),
    ).replace("</", "<\\/")
    fragment = template.replace(PLACEHOLDER, payload)
    encoded_size = len(fragment.encode("utf-8"))
    if encoded_size >= 1_000_000:
        raise RuntimeError(f"Visualization fragment is {encoded_size} bytes; limit is 1 MB")
    write_fragment(args.fragment, fragment)
    if args.inline_path:
        write_fragment(args.inline_path, fragment)
    print(f"Wrote {len(json.loads(payload)['rows'])} paper-map points ({encoded_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

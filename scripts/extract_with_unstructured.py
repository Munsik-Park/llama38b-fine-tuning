#!/usr/bin/env python3
"""Extract text blocks from documents using Unstructured.

This script reads files from ``data/raw`` and outputs filtered JSON
files under ``data/extracted``. Only ``NarrativeText`` and ``Title``
blocks are kept. ``metadata['page_number']`` is preserved when
available.
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path

try:
    from unstructured.partition.auto import partition
except ImportError as e:  # pragma: no cover - dependency might be missing in CI
    raise SystemExit("unstructured package is required: pip install 'unstructured[all-docs]'") from e


INPUT_DIR = Path("data/raw")
OUTPUT_DIR = Path("data/extracted")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def filter_elements(elements: list) -> list[dict]:
    """Return dict representations of desired elements."""
    filtered: list[dict] = []
    for el in elements:
        if getattr(el, "category", None) not in {"NarrativeText", "Title"}:
            continue
        data = el.to_dict()
        meta = data.get("metadata") or {}
        # keep only page_number if present
        if "page_number" in meta:
            data["metadata"] = {"page_number": meta["page_number"]}
        else:
            data["metadata"] = {}
        filtered.append(data)
    return filtered


def main() -> None:
    for file_path in INPUT_DIR.glob("*.*"):
        doc_id = f"{file_path.stem}_{uuid.uuid4().hex[:8]}"
        elements = partition(filename=str(file_path))
        data = filter_elements(elements)

        out_path = OUTPUT_DIR / f"{doc_id}.json"
        with out_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ {file_path.name} -> {out_path}")


if __name__ == "__main__":
    main()

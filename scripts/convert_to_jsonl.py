#!/usr/bin/env python3
"""Convert extracted Unstructured JSON files to simple JSONL format."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

PROMPT = "다음 문단을 요약하라"


def process_file(json_path: Path, output_dir: Path) -> None:
    data = json.loads(json_path.read_text(encoding="utf-8"))
    records = []
    for block in data:
        text = (block.get("text") or "").strip()
        if not text:
            continue
        records.append({"prompt": PROMPT, "completion": text})

    if not records:
        return

    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / f"{json_path.stem}.jsonl"
    with out_path.open("w", encoding="utf-8") as f:
        for rec in records:
            json.dump(rec, f, ensure_ascii=False)
            f.write("\n")
    print(f"✅ {out_path} ({len(records)} lines)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert Unstructured JSON files to JSONL")
    parser.add_argument("--input", default="data/extracted", help="Input directory")
    parser.add_argument("--output", default="data/jsonl", help="Output directory")
    args = parser.parse_args()

    input_dir = Path(args.input)
    output_dir = Path(args.output)
    if not input_dir.exists():
        print(f"Input directory not found: {input_dir}")
        return

    for json_file in input_dir.glob("*.json"):
        process_file(json_file, output_dir)


if __name__ == "__main__":
    main()

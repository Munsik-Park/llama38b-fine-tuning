#!/usr/bin/env python3
"""Convert split text files to JSONL dataset."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def count_tokens(text: str) -> int:
    try:
        import tiktoken

        enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(text))
    except Exception:
        return len(text)


def build_records(chunks: list[str], doc_id: str, source: str) -> list[dict]:
    records = []
    for idx, chunk in enumerate(chunks, start=1):
        record = {
            "document_id": doc_id,
            "chunk_id": f"{idx:04d}",
            "text": chunk,
            "source": source,
            "token_count": count_tokens(chunk),
            "metadata": {
                "created_at": "",
                "tags": [],
                "origin": "사내 문서",
            },
        }
        records.append(record)
    return records


def read_splits(file_path: Path) -> list[str]:
    if file_path.suffix.lower() == ".json":
        return json.loads(file_path.read_text(encoding="utf-8"))
    text = file_path.read_text(encoding="utf-8")
    return [p for p in text.splitlines() if p.strip()]


def process_file(file_path: Path, output_dir: Path, source: str) -> None:
    chunks = read_splits(file_path)
    records = build_records(chunks, file_path.stem, source)
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / f"{file_path.stem}.jsonl"
    with out_path.open("w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"✅ jsonl: {out_path} ({len(records)} records)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert split files to JSONL")
    parser.add_argument("--input", default="data/splits", help="Input directory")
    parser.add_argument("--output", default="data/json", help="Output directory")
    parser.add_argument("--source", default="txt", help="Source label")
    args = parser.parse_args()

    input_dir = Path(args.input)
    output_dir = Path(args.output)

    if not input_dir.exists():
        print(f"Input directory not found: {input_dir}")
        return

    for file_path in input_dir.glob("*"):
        if file_path.is_file():
            process_file(file_path, output_dir, args.source)


if __name__ == "__main__":
    main()

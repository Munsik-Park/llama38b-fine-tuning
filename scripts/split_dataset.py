#!/usr/bin/env python3
"""Split cleaned text into paragraphs or fixed-size chunks."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def split_paragraphs(text: str, min_length: int) -> list[str]:
    parts = [p.strip() for p in text.split("\n\n") if p.strip()]
    if min_length > 0:
        parts = [p for p in parts if len(p) >= min_length]
    return parts


def split_chunks(text: str, chunk_size: int, stride: int, min_length: int) -> list[str]:
    if stride <= 0:
        stride = chunk_size
    chunks = []
    i = 0
    while i < len(text):
        chunk = text[i:i + chunk_size]
        if len(chunk.strip()) >= max(1, min_length):
            chunks.append(chunk)
        i += stride
    return chunks


def process_file(file_path: Path, output_dir: Path, chunk_size: int | None, stride: int | None, min_length: int) -> None:
    text = file_path.read_text(encoding="utf-8")
    if chunk_size:
        if stride is None:
            stride = chunk_size
        parts = split_chunks(text, chunk_size, stride, min_length)
    else:
        parts = split_paragraphs(text, min_length)
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / f"{file_path.stem}.json"
    out_path.write_text(json.dumps(parts, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ split: {out_path} ({len(parts)} parts)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Split cleaned text files")
    parser.add_argument("--input", default="data/cleaned", help="Input directory")
    parser.add_argument("--output", default="data/splits", help="Output directory")
    parser.add_argument("--chunk-size", type=int, default=None, help="Chunk size in characters")
    parser.add_argument("--stride", type=int, default=None, help="Stride for overlapping chunks")
    parser.add_argument("--min-length", type=int, default=0, help="Minimum length of paragraph or chunk")
    args = parser.parse_args()

    input_dir = Path(args.input)
    output_dir = Path(args.output)

    if not input_dir.exists():
        print(f"Input directory not found: {input_dir}")
        return

    for file_path in input_dir.glob("*.txt"):
        process_file(file_path, output_dir, args.chunk_size, args.stride, args.min_length)


if __name__ == "__main__":
    main()

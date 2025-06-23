#!/usr/bin/env python3
"""Clean text files extracted from documents."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

SPECIAL_CHARS = ['■', '※', '▣', '●', '▪', '▲']


def clean_text(text: str) -> str:
    """Apply basic cleaning rules to raw text."""
    # unify newlines
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # remove special characters
    pattern = "[" + re.escape("".join(SPECIAL_CHARS)) + "]"
    text = re.sub(pattern, "", text)
    # normalize tabs and multiple spaces
    text = re.sub(r"[ \t]+", " ", text)
    # collapse multiple newlines to at most two
    text = re.sub(r"\n{3,}", "\n\n", text)
    # strip trailing spaces per line
    lines = [line.strip() for line in text.splitlines()]
    cleaned_lines = []
    for line in lines:
        # remove page numbers or header/footer style lines
        if re.match(r"^\s*\d+\s*$", line):
            continue
        if re.match(r"^\s*Page\s*\d+", line, re.IGNORECASE):
            continue
        cleaned_lines.append(line)
    return "\n".join(cleaned_lines).strip() + "\n"


def process_file(file_path: Path, output_dir: Path) -> None:
    text = file_path.read_text(encoding="utf-8", errors="ignore")
    cleaned = clean_text(text)
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / file_path.name
    out_path.write_text(cleaned, encoding="utf-8")
    print(f"✅ cleaned: {out_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Clean extracted text files")
    parser.add_argument("--input", default="data/extracted", help="Input directory")
    parser.add_argument("--output", default="data/cleaned", help="Output directory")
    args = parser.parse_args()

    input_dir = Path(args.input)
    output_dir = Path(args.output)

    if not input_dir.exists():
        print(f"Input directory not found: {input_dir}")
        return

    for file_path in input_dir.glob("*.txt"):
        process_file(file_path, output_dir)


if __name__ == "__main__":
    main()

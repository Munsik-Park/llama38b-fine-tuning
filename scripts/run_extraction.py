from __future__ import annotations

import argparse
from pathlib import Path

from extractors.factory import get_extractor


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract text from documents")
    parser.add_argument("file", help="Path to the document file")
    parser.add_argument("--output", help="Output text file", default=None)
    args = parser.parse_args()

    extractor = get_extractor(args.file)
    text = extractor.extract_text()

    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        print(text)


if __name__ == "__main__":
    main()

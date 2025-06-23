#!/usr/bin/env python3
"""Split cleaned text into paragraphs or fixed-size chunks with UUID naming."""

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


def load_metadata(cleaned_file: Path) -> dict:
    """Load metadata from the corresponding .meta.json file."""
    meta_file = cleaned_file.with_suffix('.txt.meta.json')
    if meta_file.exists():
        return json.loads(meta_file.read_text(encoding="utf-8"))
    return {}


def process_file(file_path: Path, output_dir: Path, chunk_size: int | None, stride: int | None, min_length: int) -> tuple[bool, str]:
    """Process a single file and return success status and message."""
    try:
        text = file_path.read_text(encoding="utf-8")
        
        # 실패한 추출 파일 건너뛰기
        if text.startswith("Extraction failed:") or text.startswith("Extraction skipped:"):
            return False, f"건너뜀: 추출 실패/건너뜀 파일"
        
        # 빈 텍스트 건너뛰기
        if not text.strip():
            return False, f"건너뜀: 빈 텍스트"
        
        if chunk_size:
            if stride is None:
                stride = chunk_size
            parts = split_chunks(text, chunk_size, stride, min_length)
        else:
            parts = split_paragraphs(text, min_length)
        
        # 분할 결과가 없으면 건너뛰기
        if not parts:
            return False, f"건너뜀: 분할 결과 없음"
        
        # Load metadata
        metadata = load_metadata(file_path)
        
        # Create output data with metadata
        output_data = {
            "chunks": parts,
            "metadata": metadata,
            "split_info": {
                "chunk_size": chunk_size,
                "stride": stride,
                "min_length": min_length,
                "total_chunks": len(parts)
            }
        }
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Use same UUID base name for consistency
        uuid_base = file_path.stem  # e.g., "uuid-1283b42e"
        out_path = output_dir / f"{uuid_base}.json"
        out_path.write_text(json.dumps(output_data, ensure_ascii=False, indent=2), encoding="utf-8")
        
        return True, f"split: {out_path} ({len(parts)} parts)"
        
    except Exception as e:
        return False, f"오류: {str(e)}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Split cleaned text files with UUID naming")
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

    success_count = 0
    skipped_count = 0
    error_count = 0

    for file_path in input_dir.glob("uuid-*.txt"):
        success, message = process_file(file_path, output_dir, args.chunk_size, args.stride, args.min_length)
        if success:
            print(f"✅ {message}")
            success_count += 1
        else:
            print(f"⏭️  {file_path.name}: {message}")
            if "오류" in message:
                error_count += 1
            else:
                skipped_count += 1

    print(f"\n📊 분할 완료: 성공 {success_count}개, 건너뜀 {skipped_count}개, 오류 {error_count}개")


if __name__ == "__main__":
    main()

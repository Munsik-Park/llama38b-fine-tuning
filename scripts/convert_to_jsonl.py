#!/usr/bin/env python3
"""Convert split text files to JSONL dataset with UUID naming and metadata preservation."""

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


def build_records(chunks: list[str], doc_id: str, source: str, metadata: dict, split_info: dict) -> list[dict]:
    records = []
    for idx, chunk in enumerate(chunks, start=1):
        record = {
            "document_id": doc_id,
            "chunk_id": f"{idx:04d}",
            "text": chunk,
            "source": source,
            "token_count": count_tokens(chunk),
            "metadata": {
                "original_filename": metadata.get("original_filename", ""),
                "text_hash": metadata.get("text_hash", ""),
                "text_length": metadata.get("text_length", 0),
                "split_info": split_info,
                "created_at": metadata.get("created_at", ""),
                "tags": metadata.get("tags", []),
                "origin": metadata.get("origin", "사내 문서"),
            },
        }
        records.append(record)
    return records


def read_splits(file_path: Path) -> tuple[list[str], dict, dict]:
    """Read split file and return chunks, metadata, and split_info."""
    if file_path.suffix.lower() == ".json":
        data = json.loads(file_path.read_text(encoding="utf-8"))
        
        # Handle new format with metadata
        if isinstance(data, dict) and "chunks" in data:
            chunks = data["chunks"]
            metadata = data.get("metadata", {})
            split_info = data.get("split_info", {})
        else:
            # Handle old format (just list of chunks)
            chunks = data
            metadata = {}
            split_info = {}
        
        return chunks, metadata, split_info
    
    # Fallback for text files
    text = file_path.read_text(encoding="utf-8")
    chunks = [p for p in text.splitlines() if p.strip()]
    return chunks, {}, {}


def process_file(file_path: Path, output_dir: Path, source: str) -> tuple[bool, str]:
    """Process a single file and return success status and message."""
    try:
        chunks, metadata, split_info = read_splits(file_path)
        
        # 실패한 추출 파일 건너뛰기
        if chunks and len(chunks) == 1 and (chunks[0].startswith("Extraction failed:") or chunks[0].startswith("Extraction skipped:")):
            return False, f"건너뜀: 추출 실패/건너뜀 파일"
        
        # 빈 청크 건너뛰기
        if not chunks:
            return False, f"건너뜀: 빈 청크"
        
        records = build_records(chunks, file_path.stem, source, metadata, split_info)
        
        # 빈 레코드 건너뛰기
        if not records:
            return False, f"건너뜀: 빈 레코드"
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Use same UUID base name for consistency
        uuid_base = file_path.stem  # e.g., "uuid-1283b42e"
        out_path = output_dir / f"{uuid_base}.jsonl"
        
        with out_path.open("w", encoding="utf-8") as f:
            for rec in records:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        
        return True, f"jsonl: {out_path} ({len(records)} records)"
        
    except Exception as e:
        return False, f"오류: {str(e)}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert split files to JSONL with UUID naming")
    parser.add_argument("--input", default="data/splits", help="Input directory")
    parser.add_argument("--output", default="data/jsonl", help="Output directory")
    parser.add_argument("--source", default="txt", help="Source label")
    args = parser.parse_args()

    input_dir = Path(args.input)
    output_dir = Path(args.output)

    if not input_dir.exists():
        print(f"Input directory not found: {input_dir}")
        return

    success_count = 0
    skipped_count = 0
    error_count = 0

    for file_path in input_dir.glob("uuid-*.json"):
        success, message = process_file(file_path, output_dir, args.source)
        if success:
            print(f"✅ {message}")
            success_count += 1
        else:
            print(f"⏭️  {file_path.name}: {message}")
            if "오류" in message:
                error_count += 1
            else:
                skipped_count += 1

    print(f"\n📊 JSONL 변환 완료: 성공 {success_count}개, 건너뜀 {skipped_count}개, 오류 {error_count}개")


if __name__ == "__main__":
    main()

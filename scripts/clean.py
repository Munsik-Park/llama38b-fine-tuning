#!/usr/bin/env python3
"""Clean extracted text files with UUID-based safe filenames."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from unicodedata import normalize


def clean_text(text: str) -> str:
    """Clean text by removing special characters and normalizing."""
    # Unicode normalize (NFC)
    text = normalize("NFC", text)
    
    # Remove page numbers (e.g., "1", "2", "3" at start of lines)
    text = re.sub(r'^\d+\s*$', '', text, flags=re.MULTILINE)
    
    # Remove excessive whitespace and normalize line breaks
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    
    # Remove special characters but keep Korean and English
    text = re.sub(r'[^\w\s가-힣ㄱ-ㅎㅏ-ㅣ.,!?;:()\[\]{}"\'-]', '', text)
    
    return text.strip()


def generate_safe_filename(text: str, original_name: str) -> tuple[str, str]:
    """Generate UUID-based safe filename and metadata."""
    # Generate hash from text content for consistent naming
    text_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()[:12]
    safe_name = f"uuid-{text_hash}.txt"
    
    # Create metadata
    metadata = {
        "original_filename": original_name,
        "text_hash": text_hash,
        "text_length": len(text),
        "created_at": "",
        "tags": [],
        "origin": "사내 문서"
    }
    
    return safe_name, metadata


def process_file(file_path: Path, output_dir: Path) -> tuple[bool, str]:
    """Process a single file and return success status and message."""
    try:
        text = file_path.read_text(encoding="utf-8", errors="ignore")
        
        # 실패한 추출 파일 건너뛰기
        if text.startswith("Extraction failed:") or text.startswith("Extraction skipped:"):
            return False, f"건너뜀: 추출 실패/건너뜀 파일"
        
        # 빈 텍스트 건너뛰기
        if not text.strip():
            return False, f"건너뜀: 빈 텍스트"
        
        cleaned = clean_text(text)
        
        # 빈 텍스트 건너뛰기
        if not cleaned.strip():
            return False, f"건너뜀: 정제 후 빈 텍스트"
        
        # Generate safe filename and metadata
        safe_name, metadata = generate_safe_filename(cleaned, file_path.name)
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save cleaned text
        out_path = output_dir / safe_name
        out_path.write_text(cleaned, encoding="utf-8")
        
        # Save metadata
        meta_path = output_dir / f"{safe_name}.meta.json"
        meta_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
        
        return True, f"cleaned: {out_path} (원본: {file_path.name})"
        
    except Exception as e:
        return False, f"오류: {str(e)}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Clean extracted text files with UUID naming")
    parser.add_argument("--input", default="data/extracted", help="Input directory")
    parser.add_argument("--output", default="data/cleaned", help="Output directory")
    args = parser.parse_args()

    input_dir = Path(args.input)
    output_dir = Path(args.output)

    if not input_dir.exists():
        print(f"Input directory not found: {input_dir}")
        return

    success_count = 0
    skipped_count = 0
    error_count = 0

    for file_path in input_dir.glob("*.txt"):
        success, message = process_file(file_path, output_dir)
        if success:
            print(f"✅ {message}")
            success_count += 1
        else:
            print(f"⏭️  {file_path.name}: {message}")
            if "오류" in message:
                error_count += 1
            else:
                skipped_count += 1

    print(f"\n📊 정제 완료: 성공 {success_count}개, 건너뜀 {skipped_count}개, 오류 {error_count}개")


if __name__ == "__main__":
    main()

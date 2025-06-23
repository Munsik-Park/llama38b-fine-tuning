from __future__ import annotations

import argparse
from pathlib import Path

from extractors.factory import get_extractor


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract text from documents")
    parser.add_argument("file", help="Path to the document file")
    parser.add_argument("--output", help="Output text file", default=None)
    parser.add_argument("--output-dir", help="Output directory", default="data/extracted")
    args = parser.parse_args()

    extractor = get_extractor(args.file)
    text = extractor.extract_text()

    if args.output:
        # 사용자가 지정한 출력 파일
        output_path = Path(args.output)
    else:
        # 기본 출력 디렉토리에 저장
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 원본 파일명에서 확장자만 .txt로 변경
        file_name = Path(args.file).stem
        output_path = output_dir / f"{file_name}.txt"

    # 텍스트 저장
    output_path.write_text(text, encoding="utf-8")
    print(f"✅ 추출 완료: {output_path}")


if __name__ == "__main__":
    main()

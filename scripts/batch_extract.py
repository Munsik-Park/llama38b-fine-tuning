#!/usr/bin/env python3
"""
배치 문서 추출 스크립트
doc-source 디렉토리의 모든 파일을 추출하여 data/extracted/ 디렉토리에 저장합니다.
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# scripts 디렉토리를 Python 경로에 추가
sys.path.append(str(Path(__file__).parent))

from extractors.factory import get_extractor


def get_supported_extensions() -> List[str]:
    """지원되는 파일 확장자 목록"""
    return [".pdf", ".docx", ".doc", ".pptx", ".ppt", ".xlsx", ".xls", ".hwp"]


def find_documents(source_dir: str = "data/raw") -> Dict[str, List[str]]:
    """지원되는 문서 파일들을 찾아서 형식별로 분류"""
    documents = {
        "pdf": [],
        "docx": [],
        "doc": [],
        "pptx": [],
        "ppt": [],
        "xlsx": [],
        "xls": [],
        "hwp": []
    }
    
    if not os.path.exists(source_dir):
        print(f"⚠️  {source_dir} 디렉토리가 존재하지 않습니다.")
        return documents
    
    supported_exts = get_supported_extensions()
    
    for file_path in Path(source_dir).rglob("*"):
        if file_path.is_file():
            ext = file_path.suffix.lower()
            if ext in supported_exts:
                file_type = ext[1:]  # .pdf -> pdf
                documents[file_type].append(str(file_path))
    
    return documents


def extract_and_save(file_path: str, output_dir: str = "data/extracted") -> Tuple[bool, str]:
    """단일 파일을 추출하여 저장"""
    try:
        # 추출기 생성 및 텍스트 추출
        extractor = get_extractor(file_path)
        text = extractor.extract_text()
        
        # 파일명 생성 (확장자를 .txt로 변경)
        file_name = Path(file_path).stem
        output_file = Path(output_dir) / f"{file_name}.txt"
        
        # 출력 디렉토리 생성
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # 텍스트 저장
        output_file.write_text(text, encoding="utf-8")
        
        return True, str(output_file)
        
    except Exception as e:
        return False, str(e)


def main():
    print("🚀 배치 문서 추출 시작")
    print("=" * 50)
    
    # 문서 파일 찾기
    documents = find_documents()
    
    total_files = sum(len(files) for files in documents.values())
    if total_files == 0:
        print("❌ 추출할 문서를 찾을 수 없습니다.")
        return
    
    print(f"📁 발견된 문서 수: {total_files}")
    for file_type, files in documents.items():
        if files:
            print(f"  - {file_type.upper()}: {len(files)}개")
    print()
    
    # 배치 추출 실행
    success_count = 0
    failed_count = 0
    skipped_count = 0
    
    for file_type, files in documents.items():
        if not files:
            continue
            
        print(f"📄 {file_type.upper()} 파일 처리 중...")
        
        for file_path in files:
            file_name = os.path.basename(file_path)
            print(f"  🔍 {file_name}")
            
            success, result = extract_and_save(file_path)
            
            if success:
                if "Extraction skipped" in result:
                    print(f"    ⏭️  건너뜀: {result}")
                    skipped_count += 1
                else:
                    print(f"    ✅ 성공: {result}")
                    success_count += 1
            else:
                print(f"    ❌ 실패: {result}")
                failed_count += 1
    
    # 결과 요약
    print("\n📊 배치 추출 완료")
    print("=" * 50)
    print(f"✅ 성공: {success_count}개")
    print(f"⏭️  건너뜀: {skipped_count}개")
    print(f"❌ 실패: {failed_count}개")
    print(f"📁 저장 위치: data/extracted/")
    
    if success_count > 0:
        print(f"\n💾 추출된 파일들은 'data/extracted/' 디렉토리에 저장되었습니다.")
        print("다음 단계: 텍스트 정제 및 JSONL 변환을 진행하세요.")


if __name__ == "__main__":
    main() 
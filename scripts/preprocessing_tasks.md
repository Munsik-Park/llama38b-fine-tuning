# 📌 Codex 작업 지시서: 전처리 파이프라인 스크립트 개발

이 문서는 `data/extracted/` 디렉토리에 있는 `.txt` 문서들을 정제(Cleaning), 분할(Splitting), JSONL 구조화로 이어지는 전처리 작업을 자동화하기 위한 스크립트를 작성하는 작업 지시서입니다.

## 📁 디렉토리 구조 기준


data/
extracted/ ← 1차 텍스트 추출 결과 (.txt)
cleaned/ ← 정제된 텍스트 저장소
splits/ ← 문단/청크 단위로 분할된 데이터 저장소
json/ ← 최종 JSONL 형태 데이터 저장소

scripts/
clean.py ← 정제 스크립트
split_dataset.py ← 문단/청크 분할 스크립트
convert_to_jsonl.py← JSONL 변환 스크립트




---

## 1️⃣ `clean.py` 작업 지시서

**목적**: `data/extracted/*.txt` 파일들을 불필요한 기호, 공백, 특수문자 등을 정제하고 `data/cleaned/`에 저장

### 작업 내용
- 입력: `data/extracted/*.txt`
- 출력: `data/cleaned/<같은_파일명>.txt`
- 처리 항목:
  - 이중 공백 → 단일 공백으로 정규화
  - 모든 탭, 개행 → 통일된 형식 유지 (`\n` 단락 유지)
  - 특수문자 제거 (예: `■`, `※`, `▣`, `●`, `▪`, `▲`)
  - 페이지 번호/헤더/푸터 제거 시도 (단순 패턴 기반)

### 예시
```txt
정제 전:
■ HPC 시스템의 주요 요소
    ● Interconnect
※ 이 문서는 2021년에 작성된 보고서입니다.

정제 후:
HPC 시스템의 주요 요소
Interconnect
이 문서는 2021년에 작성된 보고서입니다.


2️⃣ split_dataset.py 작업 지시서

목적: 정제된 텍스트(data/cleaned/*.txt)를 문단 혹은 일정 길이의 청크로 분할하여 data/splits/에 저장

작업 내용
입력: data/cleaned/*.txt
출력: data/splits/<같은_파일명>.txt 또는 .json (List[str])
처리 방식:
기본 분할 기준: 문단 (\n\n)
선택 옵션:
--chunk-size (문자 수 기준, 예: 512자)
--stride (청크 간 중첩, 예: 256자)
--min-length (최소 단락 길이 필터링)
예시 옵션
python split_dataset.py --input data/cleaned --output data/splits --chunk-size 512 --stride 256


3️⃣ convert_to_jsonl.py 작업 지시서

목적: 분할된 텍스트 조각을 JSONL 형태로 변환하여 data/json/*.jsonl에 저장

작업 내용
입력: data/splits/*.txt 또는 List[str] 형태
출력: data/json/<같은_파일명>.jsonl
각 JSON 객체 구조:

{
  "document_id": "파일명",
  "chunk_id": "0001",
  "text": "청크 내용",
  "source": "hwp/pdf/doc/etc",
  "token_count": 123,
  "metadata": {
    "created_at": "자동/수동 입력",
    "tags": [],
    "origin": "사내 문서"
  }
}


요구 기능
파일명에서 document_id 자동 추출
chunk_id는 4자리 고정
token_count는 tiktoken 또는 길이 기준 대체 가능
✅ 개발 순서 제안

clean.py → 정제된 텍스트 확인
split_dataset.py → 문단/청크 분리 테스트
convert_to_jsonl.py → 벡터화 준비용 JSONL 생성


💡 확장 아이디어 (선택)

로그 기록 (log.txt)
처리 요약 보고서 자동 출력 (성공/실패/청크 수 등)
에러 발생 시 .error/ 디렉토리에 로그 저장
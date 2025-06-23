이 지시서는 특히 다음을 목표로 합니다:

✅ 기존 파일명에서 안전한 UUID 기반으로 리네이밍
✅ 메타 정보는 내부 JSON에 포함
✅ 전처리 파이프라인 통일 (Clean → Split → JSONL)
✅ 수십만 개 파일에서도 자동화 가능

# 📌 Codex 작업 지시서: 전처리 자동화 및 안전한 파일명 관리

이 문서는 `data/extracted/*.txt` 형태로 추출된 텍스트를 다음 처리 단계로 연결하고, 파일명이 macOS 유니코드 등으로 인한 문제를 방지하도록 **UUID 기반 안전 파일명**을 사용하는 전처리 방식을 정의합니다.

---

## ✅ 전체 전처리 파이프라인 요약

```mermaid
graph TD
A[data/extracted] --> B[clean.py]
B --> C[data/cleaned]
C --> D[split_dataset.py]
D --> E[data/splits]
E --> F[convert_to_jsonl.py]
F --> G[data/json]



🔁 파일명 리네이밍 정책

항목	내용
기존 파일명	예: 여의시스템.1. 연구개발계획서_v1.txt
변환 후	uuid-1283b42e.txt 형식
매핑 방식	original_filename 필드를 JSON 내부 metadata에 저장
UUID 생성	uuid.uuid4() 또는 hashlib.sha256(text).hexdigest()[:12]
📂 디렉토리 구조

경로	설명
data/extracted/	추출된 원시 텍스트
data/cleaned/	정제 후 텍스트
data/splits/	문단 또는 청크 단위로 분할
data/json/	최종 JSONL 파일 저장 위치
🧹 Step 1: clean.py

기능: 특수문자 제거, 다중 공백/줄바꿈 정규화, 페이지 번호 제거
출력: data/cleaned/uuid-xxxx.txt
내부 코드 개선 제안:
정규식으로 NFD Unicode normalize
UUID 변환 + 메타 구성

from unicodedata import normalize
import uuid

cleaned_text = normalize("NFC", original_text)
safe_name = f"uuid-{uuid.uuid4().hex[:12]}.txt"


📗 Step 2: split_dataset.py

기능: \n\n 기준 문단 분할
옵션: --min-length, --chunk-size, --stride
출력: data/splits/uuid-xxxx.json
📄 Step 3: convert_to_jsonl.py

기능: split된 조각들을 JSONL로 저장
출력 예:
{
  "document_id": "uuid-1283b42e",
  "chunk_id": "0001",
  "text": "문단 내용",
  "source": "txt",
  "token_count": 152,
  "metadata": {
    "original_filename": "여의시스템.1. 연구개발계획서_v1.txt",
    "created_at": "",
    "tags": [],
    "origin": "사내 문서"
  }
}


주의사항:
chunk_id는 0001, 0002... 형식
token_count는 tiktoken 기반 계산 (cl100k_base)
전체 결과는 data/json/uuid-xxxx.jsonl로 저장
✅ 추가 고려 사항

향후 ML 학습에서 Trainer 또는 trl 사용 시, text 필드만 추출해 finetune_ready/로 구성 가능
로그 저장 또는 오류 기록을 위해 logs/ 디렉토리 구조 설계 고려
✅ 요약

항목	작업 목적
파일명 안전화	macOS/NFD 문제, 중복 방지
메타 보존	원본 추적 가능성 확보
자동화 지원	batch 처리에 용이한 UUID 기반 저장
파인튜닝 연계	JSONL 구조 통일 → LLaMA3/TinyLlama 사용 가능
이 지시서를 기반으로 각 스크립트를 리팩토링 또는 작성해 주세요. 
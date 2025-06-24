# 🛠️ 작업 지시서: Unstructured 기반 문서 전처리 파이프라인 적용

## 🎯 목적
현재 파인튜닝용 데이터 전처리 파이프라인에 Unstructured.io를 도입하여 다음 문서 포맷에 대해 자동화된 파싱 및 JSONL 변환을 지원합니다:

- PPT (.pptx)
- PDF (.pdf)
- Excel (.xlsx, .xls)
- Word (.docx)
- HWP (.hwp, .hwpx)

---

## 📁 프로젝트 내 수정 대상 디렉토리

- `scripts/extractors/` → 삭제 또는 리팩터링
- `scripts/extract_with_unstructured.py` → 신규 생성
- `scripts/convert_to_jsonl.py` → 로직 간소화
- `data/` → 구조 유지
- `README.md` → 변경사항 반영

---

## 🧩 단계별 작업 내용

### 1. 📦 Unstructured 설치

```bash
pip install "unstructured[all-docs]"
```

---

### 2. 🧠 추출 스크립트: `extract_with_unstructured.py`

#### ✅ 역할
- 각 문서 형식을 Unstructured로 파싱
- 결과를 `data/extracted/{doc_id}.json` 형태로 저장

#### ✅ 예시 구조

```python
from unstructured.partition.auto import partition
from pathlib import Path
import json, uuid

input_dir = Path("data/raw")
output_dir = Path("data/extracted")
output_dir.mkdir(exist_ok=True, parents=True)

for file_path in input_dir.glob("*.*"):
    doc_id = file_path.stem + "_" + str(uuid.uuid4())[:8]
    elements = partition(filename=str(file_path))

    output_json = output_dir / f"{doc_id}.json"
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump([el.to_dict() for el in elements], f, ensure_ascii=False, indent=2)
```

---

### 3. 🧹 정제(clean) 및 필터링

- `NarrativeText`, `Title` 블록만 선택
- `metadata["page_number"]`가 존재할 경우 유지

---

### 4. 📄 JSONL 변환 로직 수정

- `scripts/convert_to_jsonl.py` 내부에서 Unstructured JSON을 받아 다음 구조로 변환:

```json
{"prompt": "다음 문단을 요약하라", "completion": "<본문 블록>"}
```

---

### 5. 📄 HWP 처리 전략

- `.hwp → .hwpx` 변환 후 네이버 클라우드 문서변환 OpenAPI를 통해 `.docx` 또는 `.pdf`로 변환
- 이후 위와 동일한 흐름으로 처리

---

### 6. 🧪 테스트

- `test_extractors.py`에서 샘플 PDF, DOCX, PPTX 문서 테스트
- 추출된 JSON 블록 수, 블록 타입, 텍스트 유무 검증

---

## ✅ 기대 효과

- 문서별 파서 없이 통합 처리 가능
- 블록 단위의 의미 기반 fine-tuning 데이터 생성
- 추출 품질 향상 및 유지보수 간소화

---

## 📌 추가 참고

- https://github.com/Unstructured-IO/unstructured
- https://unstructured-io.github.io/unstructured/

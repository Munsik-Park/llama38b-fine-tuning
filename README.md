# llama38b-fine-tuning

# LLM Fine-tuning Pipeline (LLaMA 3 기반)

이 프로젝트는 사내 문서(약 16GB)를 활용하여 LLaMA 3 8B 모델을 파인튜닝하는 파이프라인을 구축하는 것을 목표로 합니다.  
MVP 단계에서는 RTX 2080 환경에서 경량 모델을 사용하여 전체 흐름을 검증합니다.

---

## 🔥 프로젝트 목표

- 다양한 문서 포맷에서 텍스트 추출 및 정제
- JSONL 기반 데이터셋 구축
- 경량 모델 기반 파인튜닝 검증 (MVP)
- A100 2기를 이용한 LLaMA 3 8B 튜닝
- 파인튜닝 + 추론 자동화 파이프라인 구축
- 궁극적으로는 RAG 시스템을 통합한 제품화

---

## 📁 프로젝트 디렉토리 구조

llama38b-fine-tuning/
├── data/
│ ├── raw/ # 원본 문서
│ ├── extracted/ # 추출된 텍스트
│ ├── cleaned/ # 정제된 텍스트
│ ├── jsonl/ # 학습용 JSONL 파일
│ └── splits/ # train/val/test 분할
├── models/
│ ├── lightweight/ # 경량 모델 튜닝 결과
│ └── llama3-8b/ # A100 기반 튜닝 결과
├── scripts/
│ ├── extract.py # 문서 추출
│ ├── clean.py # 텍스트 정제
│ ├── convert_to_jsonl.py # JSONL 변환
│ ├── split_dataset.py # 학습셋 분할
│ ├── train_mvp.py # 경량 모델 학습
│ └── train_llama3.py # LLaMA3 학습
├── README.md
└── 작업지시서.md



---

## 🧩 1단계 개발 범위

- 문서 추출 스크립트 개발 (PDF, DOCX, PPTX, XLSX 중심)
- 정제 스크립트 개발
- JSONL 생성 및 분할
- QLoRA 기반 튜닝 테스트 (TinyLLaMA 등)

---

## 📌 개발 도구 및 환경

- Python 3.10+
- PyTorch, HuggingFace Transformers, PEFT, TRL
- CUDA 11.x (RTX 2080 / A100)
- MLflow, Weights & Biases (선택)

---

## 📦 향후 계획

- LLaMA3 8B 튜닝 스크립트 개발
- Airflow/n8n 연동을 통한 자동화
- RAG 시스템과의 통합 및 배포 도구화




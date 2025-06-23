✅ 작업 지시서: 디렉토리 구조 리팩토링

📌 목적
현재 llama38b-fine-tuning 프로젝트 디렉토리를 다양한 모델 및 하드웨어 환경에서 재사용 가능하도록 리팩토링합니다. 학습 결과, 설정 파일, 로그를 모델 및 실행 환경별로 명확하게 구분하고, 데이터셋 가공 흐름도 버전 관리될 수 있도록 구조화합니다.

🧱 목표 디렉토리 구조

llama-fine-tuning/
├── data/
│   ├── raw/                    # 원본 문서
│   ├── extracted/              # 텍스트 추출 결과
│   ├── cleaned/                # 정제된 문장
│   ├── splits/                 # 학습/평가 분리
│   └── jsonl/                  # 모델용 포맷
│
├── datasets/
│   └── v1_preprocessed/       # 전처리 버전 관리
│
├── models/
│   ├── tinyllama/
│   │   └── rtx2080_run1/       # GPU 및 실험 이름 기준
│   │       ├── config.yaml
│   │       ├── checkpoint-*/   # Huggingface 포맷
│   │       └── logs/
│   └── llama3_8b/
│       └── a100_run1/
│           ├── config.yaml
│           ├── checkpoint-*/
│           └── logs/
│
├── configs/                  # 모델/환경별 학습 config
│   ├── tinyllama.yaml
│   ├── llama3_8b_a100.yaml
│   └── solar10b_fp16.yaml
│
├── scripts/
│   ├── extract/               # 문서 추출기
│   ├── preprocess/            # 클리닝 및 포맷 변환
│   ├── train/
│   │   └── finetune.py        # 공통 학습 엔트리포인트
│   └── infer/
│       └── cli_infer.py       # CLI 기반 추론 테스트
│
├── outputs/                   # 선택적: 통합 결과 디렉토리
│
└── README.md



🔧 세부 작업 목록
scripts/ 하위 스크립트 분리
finetune.py → scripts/train/finetune.py
추론 스크립트(cli)가 있으면 scripts/infer/cli_infer.py로 이동 예정
모델별 학습 결과 분리
outputs/tinyllama-finetune → models/tinyllama/rtx2080_run1/로 이동
checkpoint-*, trainer_state.json, adapter_config.json 등 전체 포함
config 위치 정리
tinyllama_config.yaml → configs/tinyllama.yaml로 이동
각 모델 config를 configs/에서 통합 관리
데이터 가공 결과 재구성
data/cleaned, splits, jsonl → 유지
향후 전처리 버전 별로 datasets/v1_preprocessed/ 구조로 복사 가능성 고려
README 및 setup.md 업데이트
새로운 디렉토리 구조를 문서화
실험 수행 방법 명시 (python scripts/train/finetune.py --config models/tinyllama/rtx2080_run1/config.yaml)
✅ 리팩토링 완료 후 검토 기준
 models/<모델명>/<실험명>/ 구조에 체크포인트, 로그, config.yaml 이 포함되었는가?
 configs/ 폴더에서 모델별 YAML 설정이 정리되었는가?
 기존 outputs/ 하위 구조는 제거 혹은 백업되었는가?
 scripts/train/finetune.py 는 이전 경로 없이 실행 가능한가?
 
작업 완료 후 README.md에 새로운 구조에 따라 사용법을 문서화해 주세요.
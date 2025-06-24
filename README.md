# llama-fine-tuning

## 프로젝트 목적
- 다양한 LLM 모델 및 하드웨어 환경에서 재사용 가능한 파인튜닝/추론 파이프라인 구축
- 데이터, 모델, 실험 결과, 설정 파일, 로그를 명확하게 분리하여 관리

## 디렉토리 구조

```
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
│       ├── stats.json         # 데이터 통계
│       ├── sample.jsonl       # 데이터 샘플
│       └── preprocess.log     # 전처리 로그
│
├── models/
│   ├── tinyllama/
│   │   └── rtx2080_run1/      # GPU 및 실험 이름 기준
│   │       ├── config.yaml
│   │       ├── checkpoint-*/
│   │       ├── logs/
│   │       └── meta.json      # 실험 메타데이터
│   └── llama3_8b/
│       └── a100_run1/
│           ├── config.yaml
│           ├── checkpoint-*/
│           ├── logs/
│           └── meta.json
│
├── configs/                  # 모델/환경별 학습 config
│   ├── tinyllama.yaml
│   ├── llama3_8b_a100.yaml
│   └── solar10b_fp16.yaml
│
├── scripts/
│   ├── extract_with_unstructured.py  # 문서 파싱 스크립트
│   ├── convert_to_jsonl.py            # JSONL 변환 스크립트
│   ├── train/
│   │   └── finetune.py
│   └── infer/
│       └── cli_infer.py
│
├── outputs/                  # 통합 결과 디렉토리(선택적)
│
├── README.md
└── setup.md
```

## 문서 파싱 및 JSONL 생성

1. `data/raw/` 디렉토리에 문서를 배치합니다.
2. Unstructured 패키지가 필요합니다. 다음 명령으로 설치 후 추출을 진행합니다.

```bash
pip install "unstructured[all-docs]"
python scripts/extract_with_unstructured.py
```

3. 추출된 JSON을 JSONL 포맷으로 변환합니다.

```bash
python scripts/convert_to_jsonl.py
```


## 실험 실행 예시

```bash
python scripts/train/finetune.py --config models/tinyllama/rtx2080_run1/config.yaml
```

## 실험 메타데이터/데이터 통계 자동 기록
- 각 실험 디렉토리(`models/<모델명>/<실험명>/meta.json`)에 실행 정보, 커밋 해시, 하이퍼파라미터, 환경 정보 자동 저장
- 데이터셋 전처리 시 통계(stats.json), 샘플(sample.jsonl), 로그(preprocess.log) 자동 저장

## 실험 결과/데이터 확인
- 모델별 실험 결과: `models/<모델명>/<실험명>/`
- 데이터셋 통계/샘플: `datasets/v1_preprocessed/`

## 협업 및 확장성
- 실험, 데이터, 코드, 설정이 명확히 분리되어 협업과 유지보수에 용이
- 다양한 모델/환경/실험을 동시에 관리 가능

---

> **리팩토링 및 자동화 코드 샘플은 scripts/train/finetune.py, 전처리 스크립트 등에서 확인/적용할 수 있습니다.**




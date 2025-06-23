# Python 가상환경 설정 가이드

## 가상환경 구성 완료

이 프로젝트를 위한 Python 가상환경이 성공적으로 구성되었습니다.

### 설치된 주요 패키지

- **PyTorch**: 2.7.1+cu126 (CUDA 12.6 지원)
- **Transformers**: 4.52.4
- **Datasets**: 3.6.0
- **Accelerate**: 1.8.1
- **문서 처리 라이브러리들**:
  - PyMuPDF (PDF 처리)
  - python-docx (DOCX 처리)
  - python-pptx (PPTX 처리)
  - pandas, openpyxl, xlrd (Excel 처리)

### 가상환경 사용법

#### 1. 가상환경 활성화
```bash
# 방법 1: 직접 활성화
source venv/bin/activate

# 방법 2: 스크립트 사용
./activate_venv.sh
```

#### 2. 가상환경 비활성화
```bash
deactivate
```

#### 3. 패키지 설치 확인
```bash
pip list
```

#### 4. Python 버전 확인
```bash
python --version
```

### CUDA 지원 확인

PyTorch가 CUDA를 지원하는지 확인:
```python
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"CUDA version: {torch.version.cuda}")
```

### 주의사항

1. **가상환경 활성화**: 작업을 시작하기 전에 반드시 가상환경을 활성화하세요.
2. **패키지 설치**: 새로운 패키지가 필요하면 가상환경이 활성화된 상태에서 설치하세요.
3. **프로젝트 이동**: 다른 환경으로 프로젝트를 이동할 때는 `venv` 폴더를 제외하고 이동하세요.

### 문제 해결

#### 가상환경이 활성화되지 않는 경우
```bash
# 가상환경 재생성
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 패키지 설치 오류가 발생하는 경우
```bash
# pip 업그레이드
pip install --upgrade pip

# 캐시 클리어 후 재설치
pip cache purge
pip install -r requirements.txt
``` 
#!/bin/bash
# 가상환경 활성화 스크립트

echo "가상환경을 활성화합니다..."
source venv/bin/activate

echo "설치된 패키지 확인:"
pip list

echo ""
echo "가상환경이 활성화되었습니다. (venv)"
echo "가상환경을 비활성화하려면 'deactivate' 명령어를 사용하세요." 
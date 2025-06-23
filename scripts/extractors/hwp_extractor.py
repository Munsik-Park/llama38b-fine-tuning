from __future__ import annotations

import subprocess
import os

from .base_extractor import BaseExtractor


class HWPExtractor(BaseExtractor):
    """Extract text from HWP files using the hwp5txt CLI tool."""

    def extract_text(self) -> str:
        try:
            # hwp5txt 명령어가 있는지 확인
            result = subprocess.run(
                ["which", "hwp5txt"],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                # hwp5txt가 없어도 현재 진행을 계속
                return f"Extraction skipped: HWP 파일 '{os.path.basename(self.file_path)}' - hwp5txt 도구가 설치되지 않아 추출을 건너뜁니다."
            
            # 텍스트 추출 시도
            result = subprocess.run(
                ["hwp5txt", self.file_path],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Extraction failed: hwp5txt 실행 오류 - {e.stderr}"
        except Exception as e:
            return f"Extraction failed: {e}"

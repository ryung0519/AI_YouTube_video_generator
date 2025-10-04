import json
from pathlib import Path

def load_input():
    """
    프로젝트 루트의 input.json 파일 불러오기
    반환: dict (질문, 선택지, 결과)
    """
    input_path = Path(__file__).parent.parent / "input.json"
    with open(input_path, "r", encoding="utf-8") as f:
        return json.load(f)

    return
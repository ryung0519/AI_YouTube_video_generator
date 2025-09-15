import json
from pathlib import Path

def load_input():
    input_path = Path(__file__).parent.parent / "input.json"
    with open(input_path, "r", encoding="utf-8") as f:
        return json.load(f)

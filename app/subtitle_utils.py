# app/subtitle_utils.py
from pathlib import Path
import textwrap

def _sec_to_timestamp(sec: float) -> str:
    ms = int(round((sec - int(sec)) * 1000))
    s = int(sec) % 60
    m = (int(sec) // 60) % 60
    h = int(sec) // 3600
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def add_subtitles(texts, durations, out_path: str, wrap: int = 52):
    """
    texts: 자막 문장 리스트
    durations: 각 장면 길이(sec) 리스트
    out_path: 저장할 SRT 경로
    """
    assert len(texts) == len(durations), "texts와 durations 길이가 같아야 합니다."
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)

    cur = 0.0
    blocks = []
    for i, (txt, dur) in enumerate(zip(texts, durations), start=1):
        start = _sec_to_timestamp(cur)
        end = _sec_to_timestamp(cur + float(dur))
        wrapped = "\n".join(textwrap.wrap(txt, width=wrap)) if wrap else txt
        blocks.append(f"{i}\n{start} --> {end}\n{wrapped}\n")
        cur += float(dur)

    Path(out_path).write_text("\n".join(blocks), encoding="utf-8")
    return str(Path(out_path))

import pyttsx3
from pathlib import Path

def _pick_english_voice(engine):
    """가능한 경우 영어 보이스를 선택"""
    try:
        voices = engine.getProperty("voices")
        for v in voices:
            name = (v.name or "").lower()
            if "english" in name:   # 이름에 'english' 들어간 보이스 선택
                return v.id
    except Exception:
        pass
    return None   # 못 찾으면 None 반환

def tts_save(text: str, out_path: str, rate: int = 165, volume: float = 0.9):
    """
    하나의 텍스트를 음성으로 변환하여 WAV 파일로 저장
    - text: 변환할 텍스트
    - out_path: 저장할 경로
    - rate: 말하기 속도 (작을수록 느림)
    - volume: 음량 (0~1)
    """
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)  # 저장 폴더 없으면 생성(.mkdir = 폴더생성명령어, parents=True : 상위 폴더가 없으면 같이 생성)
    engine = pyttsx3.init()  # 텍스트를 음성으로 변환하는 모듈 (pyttsx3 : 로컬에서 TTS(Text to Speech, 음성합성)를 해주는 파이썬 라이브러리)
    engine.setProperty("rate", rate) # .setProperty : pyttsx3 라이브러리에서 음성 합성 엔진의 속성을 바꾸는 메서드
    engine.setProperty("volume", volume)

    # 영어 보이스 있으면 그걸로 세팅
    vid = _pick_english_voice(engine)
    if vid:
        engine.setProperty("voice", vid)

    # 음성 파일로 저장
    engine.save_to_file(text, out_path)
    engine.runAndWait()

def tts_batch(texts, out_dir: str, prefix: str):
    """
    여러 개의 텍스트를 순차적으로 음성으로 변환
    - texts: 변환할 문자열 리스트
    - out_dir: 출력 폴더
    - prefix: 파일명 앞에 붙일 문자열
    반환: 생성된 오디오 파일 경로 리스트
    """
    out_paths = []
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    for i, t in enumerate(texts, start=1):
        p = Path(out_dir) / f"{prefix}_{i:03d}.wav"  # scene_001.wav 형식
        tts_save(t, str(p))
        out_paths.append(str(p))
    return out_paths
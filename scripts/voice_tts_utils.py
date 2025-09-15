import pyttsx3

def tts_save(text: str, out_path: str, rate: int = 165, volume: float = 0.9):
    engine = pyttsx3.init()
    engine.setProperty("rate", rate)
    engine.setProperty("volume", volume)

    # 영어 보이스 우선 선택
    try:
        voices = engine.getProperty("voices")
        picked = None
        for v in voices:
            name = (v.name or "").lower()
            if "english" in name:
                picked = v.id
                break
        if picked:
            engine.setProperty("voice", picked)
    except Exception:
        pass

    engine.save_to_file(text, out_path)
    engine.runAndWait()

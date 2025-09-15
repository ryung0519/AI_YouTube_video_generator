from pathlib import Path
from data_utils import load_input
from voice_tts_utils import tts_save # from voice(tts)_utils
from video_utils import make_shorts_video

IMG_PATH = "assets/images/moon_test.jpg"
AUDIO_PATH = "assets/audio/question.wav"
OUTPUT_PATH = "assets/output/shorts_scene1.mp4"

if __name__ == "__main__":
    data = load_input()
    question_text = data["question"]

    print("🔊 TTS 생성 중…")
    tts_save(question_text, AUDIO_PATH)

    print("🎞️ 영상 합성 중…")
    make_shorts_video(IMG_PATH, AUDIO_PATH, OUTPUT_PATH)

    print(f"✅ 완료! 파일: {OUTPUT_PATH}")

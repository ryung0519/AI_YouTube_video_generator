from pathlib import Path
from .data_utils import load_input
from .voice_tts_utils import tts_batch
from .video_utils import make_scene, concat_scenes, add_bgm_to_video
from .subtitle_utils import add_subtitles
import subprocess
from imageio_ffmpeg import get_ffmpeg_exe  # ffmpeg 경로 확보용

# === 경로 설정 ==
IMG_PATH = "assets/images/moon_test.jpg"   # 배경 이미지 (파일 존재 확인)
AUDIO_DIR = "assets/audio"
OUTPUT_DIR = "assets/output"
SRT_DIR = "assets/srt"
BGM_PATH = "assets/audio/bgm.mp3"          # 없으면 건너뜀

SHORTS_RAW = f"{OUTPUT_DIR}/shorts_raw.mp4"           # 장면 연결본
SHORTS_WITH_SUBS = f"{OUTPUT_DIR}/shorts_with_subs.mp4"  # 자막 번인본
SHORTS_FINAL = f"{OUTPUT_DIR}/shorts_final.mp4"       # (선택) BGM 믹스 최종본
SRT_PATH = f"{SRT_DIR}/shorts.srt"

if __name__ == "__main__":
    data = load_input()

    # 1) 텍스트 준비 (질문 → 선택지 → 결과)
    texts = [data["question"], *data["options"]]
    for r in data["results"]:
        texts.append(f"{r['title']}. {r['description']}")

    # 2) TTS 일괄 생성
    print("🔊 TTS batch 생성…")
    audio_paths = tts_batch(texts, AUDIO_DIR, prefix="scene")

    # 3) 각 장면 생성 (이미지+오디오)
    print("🎞️ 장면 생성…")
    scenes = [make_scene(IMG_PATH, p, fps=30) for p in audio_paths]

    # 4) 자막 타이밍(각 장면 길이)
    durations = [c.duration for c in scenes]

    # 5) 장면 결합 → 원본 쇼츠
    print("🧵 장면 결합…")
    concat_scenes(scenes, SHORTS_RAW, fps=30)

    # 6) SRT 생성 + FFmpeg 번인
    print("💬 자막 생성 & 번인…")
    srt_path =add_subtitles(texts, durations, SRT_PATH)
    ffmpeg = get_ffmpeg_exe()
    srt_escaped = srt_path.replace("\\", "/")  # Windows 경로 이스케이프

    #자막 스타일 커스터마이징
    cmd = [
        ffmpeg, "-y",
        "-i", SHORTS_RAW,
        "-vf", f"subtitles={srt_escaped}",
        "-c:a", "copy",
        SHORTS_WITH_SUBS,
    ]
    subprocess.run(cmd, check=True)

    # 7) BGM 믹스 (있을 때만)
    if Path(BGM_PATH).exists():
        print("🎼 BGM 믹스…")
        add_bgm_to_video(SHORTS_WITH_SUBS, BGM_PATH, SHORTS_FINAL, bgm_gain=0.15)
        print(f"✅ 완료! 파일: {SHORTS_FINAL}")
    else:
        print(f"✅ 완료! 파일: {SHORTS_WITH_SUBS} (BGM 없음)")

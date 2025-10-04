from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeAudioClip
from pathlib import Path

def make_scene(img_path: str, audio_path: str, fps: int = 30):
    """
    이미지 1장 + 오디오 1개 → 세로 화면(1080x1920) 클립 생성
    - img_path: 사용할 이미지 경로
    - audio_path: 오디오 파일 경로
    - fps: 초당 프레임 수
    """
    a = AudioFileClip(audio_path)                          # 오디오 불러오기
    base = ImageClip(img_path).resize(height=1920)         # 이미지를 세로 크기에 맞게 리사이즈
    clip = base.on_color(size=(1080, 1920), color=(0,0,0), pos="center")  # 검은 배경 캔버스 위 중앙 배치
    return clip.set_duration(a.duration).set_audio(a).set_fps(fps)        # 오디오 길이만큼 영상 길이 지정

def concat_scenes(clips, out_path: str, fps: int = 30):
    """
    여러 장면을 이어붙여 하나의 영상으로 출력
    - clips: make_scene으로 만든 클립 리스트
    - out_path: 최종 영상 파일 경로
    """
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    final = concatenate_videoclips(clips, method="compose")  # 클립들을 이어붙이기
    final.write_videofile(out_path, codec="libx264", audio_codec="aac", bitrate="7000k", fps=fps)

def add_bgm_to_video(video_path: str, bgm_path: str, out_path: str, bgm_gain: float = 0.15):
    """
    기존 영상에 BGM을 섞어서 최종 영상 생성
    - video_path: 원본 영상 경로
    - bgm_path: BGM 파일 경로
    - bgm_gain: BGM 볼륨 (1=100%, 0.15=15%)
    """
    from moviepy.editor import VideoFileClip, AudioFileClip
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)

    v = VideoFileClip(video_path)
    original_audio = v.audio                           # 원래 음성 (TTS)
    bgm = AudioFileClip(bgm_path).volumex(bgm_gain)    # BGM 불러오고 볼륨 낮춤

    # 영상 길이에 맞게 BGM 반복
    loops = int(v.duration // bgm.duration) + 1
    bgm_long = concatenate_videoclips([bgm] * loops).subclip(0, v.duration).audio

    # 오리지널 오디오 + BGM 믹스
    mixed = CompositeAudioClip([original_audio, bgm_long])
    v_out = v.set_audio(mixed)

    v_out.write_videofile(out_path, codec="libx264", audio_codec="aac", bitrate="7000k")

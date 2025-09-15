from moviepy.editor import ImageClip, AudioFileClip

def make_shorts_video(img_path: str, audio_path: str, out_path: str):
    audio = AudioFileClip(audio_path)
    base = ImageClip(img_path).resize(height=1920)
    clip = base.on_color(size=(1080, 1920), color=(0, 0, 0), pos="center")
    final = clip.set_duration(audio.duration).set_audio(audio).set_fps(30)
    final.write_videofile(out_path, codec="libx264", audio_codec="aac", bitrate="6000k")

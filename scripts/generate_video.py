import json
from pathlib import Path
from moviepy.editor import ImageClip, concatenate_videoclips
# from moviepy.editor import TextClip

print("🎬 영상 자동 생성 시작!")

# input.json 로드
input_path = Path(__file__).parent.parent / "input.json"
with open(input_path, "r") as f:
    data = json.load(f)

print(f"제목: {data['title']}")
print(f"질문: {data['question']}")
print("선택지:")
for opt in data['options']:
    print(f"- {opt}")
print("결과:")
for result in data['results']:
    print(f"[{result['title']}] {result['description']}")

print("\n🚧 실제 영상 생성 코드는 추후 추가 예정입니다.")


# # 이미지 생성용 코드 추가
# import os
# import openai
# from dotenv import load_dotenv
# import requests

# load_dotenv()
# openai.api_key = os.getenv("OPENAI_API_KEY")
# from pathlib import Path

# def generate_image(prompt: str, filename: str):
#     print(f"🎨 이미지 생성 중: {prompt}")
#     response = openai.images.generate(
#         model="dall-e-3",
#         prompt=prompt,
#         size="1024x1024",
#         quality="standard",
#         n=1
#     )
#     image_url = response.data[0].url
#     img_data = requests.get(image_url).content
#     img_path = Path("assets/images") / filename
#     with open(img_path, "wb") as f:
#         f.write(img_data)
#     print(f"✅ 이미지 저장 완료: {img_path}")
# 
# # 실제 실행
# generate_image(
#     "dreamy watercolor night sky with glowing full moon and soft clouds",
#     "moon_test.jpg"
# )



# 무료 이미지로 테스트 영상 만들기
img_path = "assets/images/moon_on_sea.jpg"  # 네가 넣은 이미지 파일 이름
output_path = "assets/output/test_output.mp4"

print("🎥 영상 생성 시작!")

clip = ImageClip(img_path, duration=5)  # 5초짜리 영상
clip = clip.set_fps(24)                 # 초당 24프레임
clip.write_videofile(output_path, codec="libx264")

print(f"✅ 영상 생성 완료: {output_path}")

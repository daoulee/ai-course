"""직접 해보기 7. VRAM 계산기

강의서 기준은 실습실 PC의 8GB.
내 장비는 Apple M4 Max 36GB 통합 메모리이고, GPU 사용 상한이 약 27GB다.
두 값을 같이 찍어서 비교한다.
"""

VRAM_LIST = [8.0, 27.0]  # 실습실 PC, 내 맥(GPU 사용 상한)

models = [
    ("qwen3:1.7b", 1.7),
    ("qwen3:4b", 4.0),
    ("qwen3:8b", 8.2),
    ("qwen3:14b", 14.8),
    ("qwen3:32b", 32.8),
    ("gpt-oss:120b", 117),
]

header = "  ".join(f"{v:.0f}GB에" for v in VRAM_LIST)
print(f"{'모델':14s} {'16비트':>8s} {'4비트':>8s}   {header}")
for name, b in models:
    fp16 = b * 2  # 파라미터 10억 개 × 2바이트 = 2GB
    q4 = b * 0.6  # 4비트 양자화는 파라미터 10억 개당 약 0.6GB
    # 1.5GB는 컨텍스트와 화면 출력 몫
    fits = "  ".join(
        f"{'들어감' if q4 + 1.5 <= v else '안 들어감':>9s}" for v in VRAM_LIST
    )
    print(f"{name:14s} {fp16:7.1f}GB {q4:7.1f}GB   {fits}")

print("\nqwen3:8b의 컨텍스트 메모리 (토큰당 147KB)")
for ctx in [4096, 8192, 16384, 32768]:
    f16 = ctx * 147 / 1024 / 1024
    print(
        f"  {ctx:6d} 토큰: 16비트 {f16:4.1f}GB, 8비트(q8_0) {f16 / 2:4.1f}GB, 모델 5.2GB와 합치면 {5.2 + f16:4.1f}GB / {5.2 + f16 / 2:4.1f}GB"
    )

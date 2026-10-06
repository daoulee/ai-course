"""도전. 1주차 실험을 내 GPU에서 (Apple Silicon 버전)

강의서는 NVIDIA의 cuda를 쓴다. 맥에는 cuda가 없고 Metal을 쓰는 mps가 그 자리다.
torch는 맥용 기본 패키지에 mps가 들어 있어서 따로 설치할 것이 없다.

주의. mps는 첫 연산에 셰이더를 컴파일하느라 시간이 더 걸린다.
워밍업을 한 번 돌리고 재지 않으면 GPU가 CPU보다 느리게 나온다.
"""

import time

import torch

device = "mps" if torch.backends.mps.is_available() else "cpu"
print("GPU(mps) 사용 가능:", torch.backends.mps.is_available())
print("GPU 이름: Apple Silicon (Metal)")

size = 4000  # 4000 x 4000 크기의 행렬
a = torch.rand(size, size)  # 무작위 숫자로 채운 행렬 두 개를 만든다
b = torch.rand(size, size)


def timeit(fn, n=5):
    """n번 돌린 평균 시간. 앞의 한 번은 워밍업이라 버린다."""
    fn()
    start = time.time()
    for _ in range(n):
        fn()
    return (time.time() - start) / n


# CPU에서 행렬 곱셈 시간 측정
cpu_time = timeit(lambda: a @ b)
print("CPU:", round(cpu_time, 4), "초")

# 같은 행렬을 GPU로 옮겨서 측정
a_gpu = a.to(device)  # cuda 자리에 mps가 들어간다
b_gpu = b.to(device)


def gpu_matmul():
    c = a_gpu @ b_gpu
    torch.mps.synchronize()  # GPU 계산이 끝날 때까지 대기


gpu_time = timeit(gpu_matmul)
print("GPU:", round(gpu_time, 4), "초")

print("GPU가 약", round(cpu_time / gpu_time, 1), "배 빠름")

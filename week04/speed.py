"""직접 해보기 9. 모델 크기와 속도

Ollama는 응답에 생성한 토큰 수(eval_count)와 걸린 시간(eval_duration, 나노초)을
같이 돌려준다. 이것으로 초당 토큰 수를 잰다.
"""

import subprocess

import ollama

prompt = "파이썬으로 1부터 100까지 소수를 출력하는 코드를 작성하고, 각 줄에 주석을 달아줘."
for model in ["qwen3:1.7b", "qwen3:8b"]:
    # 모델을 미리 올린다. 올리는 시간이 측정에 섞이지 않게 한다
    ollama.chat(model=model, think=False, messages=[{"role": "user", "content": "안녕"}])
    r = ollama.chat(
        model=model,
        think=False,
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0, "num_predict": 300},
    )
    speed = r.eval_count / (r.eval_duration / 1e9)
    ps = subprocess.run(["ollama", "ps"], capture_output=True, text=True).stdout.splitlines()
    line = next(l for l in ps if l.startswith(model))
    print(f"{model:11s} {r.eval_count}토큰, 초당 {speed:.1f}토큰 | {line}")

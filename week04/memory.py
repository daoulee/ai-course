"""직접 해보기 6. 대화 기억 확인

모델은 아무것도 기억하지 않는다. 매 요청이 백지에서 시작한다.
기억처럼 보이는 것은 프로그램이 이전 대화를 전부 다시 보내기 때문이다.
"""

import ollama


def chat(messages):
    r = ollama.chat(
        model="qwen3:8b", think=False, messages=messages, options={"temperature": 0}
    )
    return r.message.content.strip()


first = chat([{"role": "user", "content": "내 이름은 최민수야. 기억해 줘. 한 줄로 답해."}])
print("1:", first)

print("2 (이전 대화 없이):", chat([{"role": "user", "content": "내 이름이 뭐라고 했지? 한 줄로."}]))

print(
    "3 (이전 대화 포함):",
    chat(
        [
            {"role": "user", "content": "내 이름은 최민수야. 기억해 줘. 한 줄로 답해."},
            {"role": "assistant", "content": first},
            {"role": "user", "content": "내 이름이 뭐라고 했지? 한 줄로."},
        ]
    ),
)

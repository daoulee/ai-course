"""직접 해보기 7. 도구 호출

모델은 함수를 실행하지 않는다. "이 함수 불러 줘"라는 요청문만 쓰고 실행은 프로그램이 한다.
"""

import ollama, json, datetime

def get_time():
    """지금 시각을 돌려준다"""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

def calc(expression: str):
    """수식 문자열을 계산한다. 예: '17 * 24'"""
    return str(eval(expression, {"__builtins__": {}}))

def read_file(path: str):
    """파일 이름을 받아 그 파일의 내용을 돌려준다"""
    with open(path, encoding="utf-8") as f:
        return f.read()

functions = {"get_time": get_time, "calc": calc, "read_file": read_file}

messages = [{"role": "user", "content": "지금 몇 시야? 그리고 17 곱하기 24는?"}]

for step in range(5):
    r = ollama.chat(model="qwen3:8b", think=False, messages=messages,
                    tools=[get_time, calc, read_file])
    messages.append(r.message)

    if not r.message.tool_calls:
        print("답:", r.message.content)
        break

    for call in r.message.tool_calls:
        name, args = call.function.name, call.function.arguments
        result = functions[name](**args)
        print(f"  도구 호출: {name}({args}) -> {result[:80]}")
        messages.append({"role": "tool", "content": result, "tool_name": name})

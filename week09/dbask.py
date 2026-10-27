# week09/dbask.py

import sqlite3
import os
import ollama
import numpy as np
from openai import OpenAI


def row_to_text(row):
    """
    embeddb.py의 기준을 따름 (name, category, description, example, keywords)
    row index: 0:id, 1:name, 2:category, 3:description, 4:example, 5:keywords, 6:source_url, 7:embedding
    """
    return f"{row[1]} ({row[2]}): {row[3]} {row[4]} {row[5]}"


def search(question, k=3):
    db_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "security_concepts.db"
    )

    if not os.path.exists(db_path):
        raise FileNotFoundError(f"데이터베이스 파일을 찾을 수 없습니다: {db_path}")

    con = sqlite3.connect(db_path)
    cur = con.cursor()

    # 1. 데이터 로드 (명시적 SELECT)
    cur.execute(
        "SELECT id, name, category, description, example, keywords, source_url, embedding FROM security_concepts"
    )
    rows = cur.fetchall()

    if not rows:
        raise ValueError("데이터베이스가 비어있습니다.")

    # 2. 질문 임베딩 및 정규화
    res = ollama.embed(model="bge-m3", input=question)
    qv = np.array(res["embeddings"][0], dtype=np.float32)
    qv = qv / np.linalg.norm(qv)

    # 3. 유사도 검색
    candidates = []
    for row in rows:
        emb_blob = row[7]
        if emb_blob is None:
            continue

        qv_db = np.frombuffer(emb_blob, dtype=np.float32)
        qv_db = qv_db / np.linalg.norm(qv_db)

        score = np.dot(qv, qv_db)
        candidates.append((score, row))

    candidates.sort(key=lambda x: x[0], reverse=True)
    top_k = candidates[:k]

    con.close()
    return top_k


def answer(question, k=3):
    top_k = search(question, k)

    if not top_k:
        return [], "자료에 없습니다."

    print(f"\n질문: {question}")
    print("-" * 30)
    print(" [검색 결과 (Top 3)]")

    context_list = []
    for i, (score, row) in enumerate(top_k):
        name = row[1]
        print(f"{i+1}. (유사도: {score:.4f}) {name}")
        # row_to_text 재사용하여 context 생성
        context_list.append((row_to_text(row), score))

    # 4. 답변 생성 (Gemma4)
    client = OpenAI(
        base_url="https://krchoi.com/gemma4/v1", api_key="none", timeout=120, max_retries=0
    )
    context_text = "\n\n".join([f"[근거 자료]\n{c}" for c, s in context_list])

    prompt = f"""당신은 제공된 자료를 바탕으로 질문에 답하는 인공지능 비서입니다.
반드시 제공된 [근거 자료]만을 바탕으로 답변하세요.
만약 자료에 답을 찾을 수 없다면 "자료에 없습니다."라고 답하세요.
답변은 반드시 두 문장 이내로 간결하게 하세요.

[근거 자료]
{context_text}

질문: {question}
답변:"""

    try:
        r = client.chat.completions.create(
            model="gemma4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        ans = r.choices[0].message.content.strip()
    except Exception as e:
        ans = f"[API 호출 실패] {e}"

    print("\n [Gemma4 답변]")
    print(ans)
    print("-" * 30)

    return top_k, ans


def main():
    import sys

    DEFAULT_QUESTIONS = [
        "비밀번호 말고 지문이나 OTP를 같이 써서 확인하는 방법이 뭐야?",
        "입력창에 데이터베이스 명령어를 넣어서 정보를 빼가는 공격은?",
        "외부 인터넷과 내부망 사이에 격리된 구역을 뭐라고 불러?",
        "업무에 딱 필요한 만큼의 권한만 주는 원칙이 뭐야?",
        "해킹 사고가 터졌을 때 대응하는 절차를 무엇이라 해?",
        "사용자가 모르게 웹사이트에서 악성 스크립트가 실행되게 하는 건?",
        "데이터를 암호화할 때 똑같은 키로 잠그고 푸는 방식은?",
        "침입을 탐지만 하는 게 아니라 직접 차단까지 하는 장비는?",
        "가짜 이메일로 사람을 속여서 정보를 가져가는 수법은?",
        "한 번 로그인하고 연결된 여러 서비스를 다시 로그인하지 않고 이용하는 기술은?",
    ]

    if len(sys.argv) > 1:
        queries = sys.argv[1:]
    else:
        queries = DEFAULT_QUESTIONS

    for q in queries:
        answer(q)


if __name__ == "__main__":
    main()

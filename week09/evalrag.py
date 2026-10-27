# week09/evalrag.py

import sqlite3
import os
import numpy as np
import ollama


def eval_rag():
    db_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "security_concepts.db"
    )

    if not os.path.exists(db_path):
        print(f"Error: Database not found at {db_path}")
        return

    con = sqlite3.connect(db_path)
    cur = con.cursor()

    # 1. 데이터 로드
    cur.execute(
        "SELECT id, name, category, description, example, keywords, source_url, embedding FROM security_concepts"
    )
    rows = cur.fetchall()

    if not rows:
        print("Error: Database is empty.")
        con.close()
        return

    # 2. 테스트 데이터 (질문, 정답)
    TESTS = [
        ("비밀번호 말고 지문이나 OTP를 같이 써서 확인하는 방법이 뭐야?", "MFA"),
        (
            "입력창에 데이터베이스 명령어를 넣어서 정보를 빼가는 공격은?",
            "SQL Injection",
        ),
        ("외부 인터넷과 내부망 사이에 격리된 구역을 뭐라고 불러?", "DMZ"),
        ("업무에 딱 필요한 만큼의 권한만 주는 원칙이 뭐야?", "Least Privilege"),
        ("해킹 사고가 터졌을 때 대응하는 절차를 무엇이라 해?", "Incident Response"),
        ("사용자가 모르게 웹사이트에서 악성 스크립트가 실행되게 하는 건?", "XSS"),
        (
            "데이터를 암호화할 때 똑같은 키로 잠그고 푸는 방식은?",
            "Symmetric Encryption",
        ),
        ("침입을 탐지만 하는 게 아니라 직접 차단까지 하는 장비는?", "IPS"),
        ("가짜 이메일로 사람을 속여서 정보를 가져가는 수법은?", "Phishing"),
        (
            "한 번 로그인하고 연결된 여러 서비스를 다시 로그인하지 않고 이용하는 기술은?",
            "SSO",
        ),
    ]

    hit1 = 0
    hit3 = 0

    print(f"--- RAG 검색 적중률 평가 시작 (총 {len(TESTS)}개) ---")

    for q, want in TESTS:
        # 질문 임베딩
        res = ollama.embed(model="bge-m3", input=q)
        qv = np.array(res["embeddings"][0], dtype=np.float32)
        qv = qv / np.linalg.norm(qv)

        # 유사도 검색
        candidates = []
        for row in rows:
            emb_blob = row[7]
            if emb_blob is None:
                continue

            qv_db = np.frombuffer(emb_blob, dtype=np.float32)
            qv_db = qv_db / np.linalg.norm(qv_db)
            score = np.dot(qv, qv_db)
            candidates.append((score, row[1]))  # (score, name)

        candidates.sort(key=lambda x: x[0], reverse=True)
        top_3_data = candidates[:3]

        top_1 = top_3_data[0][1] if len(top_3_data) > 0 else ""
        top_3_names = [c[1] for c in top_3_data]

        # 결과 판정
        is_hit1 = top_1 == want
        is_hit3 = want in top_3_names

        if is_hit1:
            hit1 += 1
        if is_hit3:
            hit3 += 1

        status = "O" if is_hit1 else ("△" if is_hit3 else "X")
        print(f"{status} 질문: {q}")
        print(f"   -> 예측: {top_1} | 정답: {want} | Top3: {top_3_names}")

    print("-" * 40)
    print(f"결과: 1위 적중 {hit1}/{len(TESTS)}, 3위 안 적중 {hit3}/{len(TESTS)}")
    con.close()


if __name__ == "__main__":
    eval_rag()

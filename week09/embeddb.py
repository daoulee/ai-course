import sqlite3
import os
import ollama
import numpy as np

def row_to_text(row):
    # row 구조: (id, name, category, description, example, keywords, source_url, embedding)
    # 순서: example -> name -> category -> description -> keywords
    return f"{row[4]} {row[1]} ({row[2]}): {row[3]} {row[5]}"

def embed_db():
    # DB 경로는 스크립트 위치 기준
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "security_concepts.db")
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    # 모든 행 가져오기 (열을 명시하여 row_to_text 순서와 맞춤)
    # SELECT 순서: id(0), name(1), category(2), description(3), example(4), keywords(5), source_url(6), embedding(7)
    cur.execute("SELECT id, name, category, description, example, keywords, source_url, embedding FROM security_concepts")
    rows = cur.fetchall()

    processed_count = 0
    print(f"임베딩 시작 (총 {len(rows)}행)...\n")

    for row in rows:
        text = row_to_text(row)

        # 변환된 문장 예시 출력 (첫 번째 행만)
        if processed_count == 0:
            print(f"[문장 변환 예시]: {text}\n")

        # bge-m3 임베딩 호출
        res = ollama.embed(model="bge-m3", input=text)
        # float32 벡터로 변환
        vector = np.array(res.embeddings[0], dtype=np.float32)

        # float32 바이너리로 변환하여 embedding(BLOB)에 저장
        cur.execute(
            "UPDATE security_concepts SET embedding = ? WHERE id = ?",
            (vector.tobytes(), row[0])
        )

        processed_count += 1
        if processed_count % 10 == 0:
            print(f"{processed_count}행 처리 중...")

    con.commit()
    con.close()
    print(f"\n완료! 총 {processed_count}행을 다시 임베딩했습니다.")

if __name__ == "__main__":
    embed_db()

import sqlite3
import os

def sql_search(query):
    # DB 경로는 스크립트 위치 기준
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "security_concepts.db")
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    # LIKE 검색을 위해 % 를 붙임
    pattern = f"%{query}%"

    # name 또는 description에서 검색 (파라미터 사용)
    sql = "SELECT name, description FROM security_concepts WHERE name LIKE ? OR description LIKE ?"
    cur.execute(sql, (pattern, pattern))

    results = cur.fetchall()
    con.close()
    return results

if __name__ == "__main__":
    # 기본 검색어: 로그인, 암호, 스크립트, 차단
    search_terms = ["로그인", "암호", "스크립트", "차단"]

    for term in search_terms:
        print(f"--- '{term}' 검색 결과 ---")
        results = sql_search(term)
        if not results:
            print("검색 결과가 없습니다.")
        for name, desc in results:
            print(f"이름: {name} | 설명: {desc}")
        print()

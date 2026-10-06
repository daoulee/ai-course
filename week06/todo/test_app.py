import os
import tempfile

import app as todo_app

fd, path = tempfile.mkstemp(suffix=".db")
os.close(fd)
todo_app.app.config["DATABASE"] = path
todo_app.init_db()
client = todo_app.app.test_client()


def page():
    return client.get("/").get_data(as_text=True)


def rows():
    with todo_app.app.app_context():
        return [dict(r) for r in todo_app.get_db().execute("SELECT * FROM todos ORDER BY id")]


def reset():
    with todo_app.app.app_context():
        todo_app.get_db().execute("DELETE FROM todos")
        todo_app.get_db().commit()


results = []


def check(name, ok):
    results.append(ok)
    print("통과" if ok else "실패", name)


# 목록과 추가
r = client.get("/")
check("GET / (비어 있음) -> 200, 빈 목록 문구", r.status_code == 200 and "할 일이 없습니다." in page())

r = client.post("/add", data={"title": "공부하기"})
check("POST /add 공부하기 -> 302, 목록에 보임", r.status_code == 302 and "공부하기" in page())

reset()
r = client.post("/add", data={"title": "  테스트  "})
check("POST /add 앞뒤 공백 -> 302, 공백 없이 저장", r.status_code == 302 and rows()[-1]["title"] == "테스트")

reset()
client.post("/add", data={"title": "먼저"})
client.post("/add", data={"title": "나중"})
html = page()
check("두 개 추가 -> 나중에 추가한 것이 먼저", html.index("나중") < html.index("먼저"))

# 완료 표시와 해제
reset()
client.post("/add", data={"title": "완료할 일"})
tid = rows()[0]["id"]
r = client.post(f"/toggle/{tid}")
check("POST /toggle (있는 번호) -> 302, 완료로 바뀜", r.status_code == 302 and rows()[0]["done"] == 1)
r = client.post(f"/toggle/{tid}")
check("POST /toggle 한 번 더 -> 302, 미완료로 돌아옴", r.status_code == 302 and rows()[0]["done"] == 0)

# 삭제
r = client.post(f"/delete/{tid}")
check("POST /delete (있는 번호) -> 302, 목록에서 사라짐", r.status_code == 302 and rows() == [])

os.remove(path)
print(f"{sum(results)}/{len(results)} 통과")

# 진행 기록

## 끝난 단계
1. 목록과 추가: `app.py`, `templates/index.html`, `test_app.py`
2. 완료 표시와 해제: `/toggle/<id>`, 완료된 제목에 취소선
3. 삭제: `/delete/<id>`
4. 잘못된 입력: 빈 제목, 101자 이상은 400. 없는 번호는 404. `templates/error.html`
5. 리팩터링: 데이터베이스 코드를 `db.py`로 분리. `test_app.py`는 고치지 않음
6. 완료한 할 일을 목록 아래쪽에 모아 보기 (테스트 1줄 추가)
7. figma 로그인 화면의 색, 모서리, 글자 크기로 `static/style.css` 적용

## 스펙과 다르게 한 것
- 없음. 6번은 스펙 4절과 6절을 먼저 고친 뒤 구현했다.

## 남은 일
- 제목이 길면 목록에서 시각과 버튼 때문에 두 줄로 접힌다. 시각을 제목 아래 줄로 옮길지 정한다.

## 확인 방법
- `python test_app.py` → 15/15 통과
- `python app.py` → http://localhost:5001

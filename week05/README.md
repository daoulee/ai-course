# 5주차: LLM을 API로 다루기

- 학번: 202230136
- 이름 (영문): Daou Lee
- 실행 환경: Apple M4 Max, Ollama 0.34.4, qwen3:8b / qwen3:1.7b / bge-m3, 실습 서버 gemma4

---

## 1. Ollama는 서버다 (`raw.py`)

`ollama run`이나 `ollama.chat`은 전부 `localhost:11434`에 HTTP 요청을 보내는 클라이언트다.
`urllib`만으로 `/api/chat`에 JSON을 보내도 똑같이 답이 온다.

| 키 | 값 | 뜻 |
| --- | --- | --- |
| `prompt_eval_count` | 34 | 입력 토큰 |
| `eval_count` | 135 | 생성 토큰 |
| `eval_duration` | 2.09초 | 생성 시간 |
| `load_duration` | 3.82초 | 모델을 처음 올리는 데 걸린 시간 |

생성 속도는 `eval_count / eval_duration` = 초당 64.7토큰. 4주차 speed.py에서 잰 63.6과 거의 같다.
speed.py가 하던 계산이 결국 응답 JSON의 두 칸을 나눈 것이었다.

## 2. 같은 코드, 두 서버 (`twoservers.py`)

| 서버 | 답 | 입력 | 출력 |
| --- | --- | --- | --- |
| 내 PC (qwen3:8b) | **빈 문자열** | 28 | 200 |
| 실습 서버 (gemma4) | 리스트는 가변, 튜플은 불변 객체 | 31 | 40 |

주소와 모델 이름만 바꿔서 같은 코드가 두 서버에 다 붙었다. OpenAI 형식이 사실상 표준이라서다.

내 PC 쪽은 답이 아예 비어 있었다. 강의서 예시는 답이 잘린 정도였는데 여기서는 200토큰을 전부 생각(think)에 써서
본문까지 가지도 못했다. OpenAI 형식에는 `think=False`가 없어서 생긴 일이고, 그래서 로컬은 ollama 패키지를 쓴다.

## 3. 스트리밍 (`sse.py`)

```
조각 36개, 입력 27 토큰, 출력 80 토큰
```

조각 수(36)와 토큰 수(80)가 다르다. 서버가 토큰 두세 개를 한 `data:` 줄에 묶어 보내기 때문이다.
받는 쪽은 `delta.content`를 이어 붙이기만 하면 된다.

## 4. 콘솔 챗봇 (`chat.py`)

```
나: 내 이름은 최민수야
AI: 안녕하세요, 최민수님! 도움이 필요하시면 언제든지 말씀해주세요.
나: /history   → system, user, assistant 3개, 총 72자
나: 내 이름 뭐라고 했지?
AI: 당신의 이름은 최민수입니다.
나: /reset
나: 내 이름 뭐야?
AI: 저는 챗봇으로, 이름은 없어요. 어떻게 도와드릴까요?
```

챗봇은 이력 리스트를 매번 통째로 보내는 반복문이다. `/reset`으로 리스트를 지우면 기억도 같이 사라진다.
`/history`에 총 글자 수를 추가했는데, 대화할수록 이 숫자가 계속 커진다. 4주차 컨텍스트 상한에 다가가는 과정이다.

## 5. 구조화된 출력 (`jsonmode.py`)

```
원문: {"name": "김민수", "dept": "소프트웨어학부", "year": "2학년"}
파싱: 김민수 / 소프트웨어학부 / 2학년
```

`format="json"`은 JSON이 될 수 없는 토큰의 확률을 0으로 만든다. 그래서 앞뒤 설명이나 코드 블록 기호 없이 바로 `json.loads`가 된다.

## 6. 도구 호출 (`tools.py`)

```
  도구 호출: get_time({}) -> 2026-10-06 14:12
  도구 호출: calc({'expression': '17 * 24'}) -> 408
답: 지금은 2026년 10월 6일 14시 12분입니다. 그리고 17 곱하기 24는 408입니다.
```

4주차에 8b가 392로 틀린 17 × 24가 이번엔 408로 맞았다. 계산은 모델이 아니라 `calc`가 했다.
모델은 "이 함수를 이 인자로 불러 달라"는 요청문만 쓰고, 실행은 프로그램이 한다.

`read_file(path)`를 추가해서 "chat.py 파일의 첫 줄이 뭐야?"를 물어봤다.

| 모델 | 도구 호출 | 답 |
| --- | --- | --- |
| qwen3:8b | `read_file({'path': 'chat.py'})` | `"""직접 해보기 5. 콘솔 챗봇` (정답) |
| qwen3:1.7b | `read_file({'path': 'chat.py'})` | `import ollama` (오답) |
| qwen3:1.7b, 시각 질문 | `get_time`에 없는 인자 `type`을 넣음 | `TypeError`로 프로그램이 멈춤 |

1.7b는 파일 내용을 제대로 받아 놓고도 첫 줄을 지어냈다. 파이썬 파일이면 보통 import로 시작한다는 확률을 따라간 것 같다.
도구 형식을 지키는 능력은 모델 크기에 따라 다르고, 모델이 넘긴 인자를 그대로 믿고 실행하면 안 된다는 것도 확인했다.

## 7. RAG (`rag.py`)

| 질문 | 검색 1위 | 답 | 어디서 틀렸나 |
| --- | --- | --- | --- |
| 책 빌리는 곳 몇 시에 닫아? | 도서관은 오후 10시까지 연다 | 자료에 없습니다 | 생성 |
| 졸업하려면 뭐가 필요해? | 졸업 요건은 130학점... | 130학점 이상 이수와 졸업 작품 제출 | 정답 |
| 학식은 얼마야? | 졸업 요건은 130학점... | 자료에 없습니다 | 검색은 틀렸지만 생성이 막음 |

강의서 결과와 똑같이 나왔다. 검색은 관련 문서가 없어도 무조건 가장 가까운 걸 가져온다(2주차의 0.45 바닥값).
반대로 "10시까지 연다"를 "10시에 닫는다"로 연결하지 못한 건 검색이 아니라 생성 쪽 문제다.
틀린 결과가 나오면 검색과 생성 중 어디서 틀렸는지 나눠서 봐야 한다.

## 8. MCP: 토스페이먼츠 결제 연동 (`toss/`)

토스페이먼츠 MCP 서버를 `npx`로 띄우면 도구 세 개(`get-documents`, `get-glossary-documents`, `document-by-id`)가 나온다.
이 도구로 v2 SDK 문서와 결제 승인 문서를 검색해서, 그 내용대로 Flask 서버를 만들었다.

- 브라우저(`templates/index.html`): 클라이언트 키로 결제 UI를 그리고 `requestPayment`로 결제창을 띄운다
- 서버(`app.py`): `/success`로 돌아온 `paymentKey`, `orderId`, `amount`로 `/v1/payments/confirm`을 부른다.
  시크릿 키는 `auth=(secret_key, "")`로 넣는데, 이게 `Basic base64(시크릿키:)` 헤더를 만들어 준다

| 확인 | 넣은 값 | 결과 |
| --- | --- | --- |
| 가짜 paymentKey | `/success?paymentKey=aaa&orderId=bbb-123456&amount=1000` | 404 `NOT_FOUND_PAYMENT_SESSION` |
| 금액 조작 | `amount=999` | 승인 API를 부르지 않고 `AMOUNT_MISMATCH` |
| 결제 취소 | `/fail?code=PAY_PROCESS_CANCELED` | code, message 표시 |
| 시크릿 키 노출 | `/` 페이지 소스에서 `test_gsk` 검색 | 0건 |

가짜 값에 404가 온다는 건 서버가 실제로 토스 API를 부르고 있다는 뜻이다.
금액 검사를 빼면 구매자가 주소창에서 금액을 바꿔 결제할 수 있으니, 금액은 브라우저가 아니라 서버가 정해야 한다.

맥에서는 5000번 포트를 AirPlay 수신(ControlCenter)이 쓰고 있어서 Flask가 떠도 403이 나왔다.
`app.run(port=5001)`로 바꿔서 해결했다.

## 9. MCP: Figma 디자인 읽기 (`figma/index.html`)

`figma-developer-mcp`(0.13.2)를 등록하니 도구 두 개(`get_figma_data`, `download_figma_images`)가 나왔다.
`get_figma_data`가 돌려준 건 그림이 아니라 이런 텍스트였다.

```
[FRAME] "Login Screen" #1:2 layout={"mode":"column","padding":"72px 24px 40px","gap":"28px","designedWidth":"390px"}
  [TEXT] #1:4 fills=["#1C2430"] fontSize 26, fontWeight 700, text="다시 만나서 반갑습니다"
  [FRAME] "Input" padding 14px, fills #F7F7FA, strokes #DEE3E8, borderRadius 10px
  [FRAME] "Button / Primary" padding 16px 0, fills #2663EB, borderRadius 12px
```

모델은 이 텍스트만 보고 화면을 만든다. 3주차에 본 것처럼 모델이 다루는 건 토큰뿐이고,
MCP는 디자인을 토큰으로 바꿔 주는 통로다. Figma의 column, gap, padding이 CSS flex의 `flex-direction`, `gap`, `padding`으로 거의 1:1로 옮겨진다.

`download_figma_images`로 받은 원본 PNG와 만든 페이지를 390×844로 캡처해서 비교했다.
색, 간격, 버튼과 입력창 크기는 맞았다. 다른 건 한글 글꼴 하나다. Figma는 Inter에 없는 한글을 자체 글꼴로 대체하고
브라우저는 시스템 글꼴(Apple SD Gothic Neo)을 써서, 줄 높이가 달라 아래 요소가 3px 정도 밀렸다.

Cline(gemma4)에 강의서 요청문을 보냈을 때는 `get_figma_data`를 먼저 부르고 그 값대로 파일을 썼다.
색, 크기, 모서리는 맞았지만 두 군데가 디자인이나 요청과 달랐다.

| 문제 | 원인 |
| --- | --- |
| Google Fonts를 `<link>`로 불러옴 | "외부 CSS 없이"라고 했는데 Inter 글꼴을 쓰려고 어김 |
| 하단 "회원가입" 줄이 화면 맨 아래로 감 | 디자인에 없는 `margin-top: auto`를 넣음 |

두 가지를 한 번에 지적해서 다시 보내니 둘 다 고쳐졌다.
도구로 읽은 값은 잘 옮기지만, 읽은 것에 없는 부분은 모델이 흔한 방식으로 채운다.

Cline을 홈 폴더에서 실행했을 때는 `/Users/index.html`에 쓰려다 권한 오류가 나자 스스로 `~/projects/login-page`를 만들었다.
작업 폴더를 정해 주지 않으면 엉뚱한 곳에 파일을 만든다.

---

## 정리

- Ollama는 내 PC에서 계속 도는 서버고, 파이썬 패키지는 그 서버에 HTTP 요청을 대신 보내 주는 것뿐이다.
- OpenAI 형식이 표준이라 `base_url`만 바꾸면 로컬이든 실습 서버든 같은 코드로 부른다.
- 스트리밍은 `data:` 줄에 토큰 몇 개씩 담아 보내는 방식이고, 받는 쪽은 이어 붙이기만 한다.
- 모델은 기억하지 않는다. 챗봇의 기억은 프로그램이 들고 있는 리스트다.
- 도구 호출에서 모델은 요청문만 쓰고 실행은 프로그램이 한다. Cline도 결국 이 반복문을 도는 프로그램이다.
- RAG는 검색 결과를 프롬프트에 붙이는 것이 전부지만, 틀리는 지점이 두 군데라 따로 확인해야 한다.
- MCP는 tools.py의 `functions` 딕셔너리를 밖으로 꺼내 표준으로 만든 것이다. 서버가 도구를 내놓고 클라이언트가 모델에 잇는다.
- 결제는 브라우저 인증 → successUrl로 리다이렉트 → 서버 승인의 세 단계이고, 시크릿 키와 금액 검사는 서버에만 둔다.

import ollama
import numpy as np


def emb(text):
    return np.array(ollama.embed(model="bge-m3", input=text).embeddings[0])


# 직접 해보기 6: 나만의 도메인 문서 10개 (소프트웨어 개발 및 서비스 운영 지침)
docs = [
    "서버 정기 배포는 매주 목요일 오후 8시 점검 시간에 진행한다",
    "데이터베이스 일일 백업은 매일 새벽 3시에 자동으로 실행된다",
    "회원 탈퇴를 신청하면 개인 식별 데이터는 7일 후 완전히 영구 삭제된다",
    "사용자 비밀번호는 단방향 암호화 해시 알고리즘으로 안전하게 저장한다",
    "오류 발생 시 서버는 최대 3회까지 지수 백오프로 재시도한다",
    "로그인 세션의 유효 시간은 마지막 활동 기준 30분이다",
    "신규 기능 개발은 풀 리퀘스트를 통해 최소 1명 이상의 승인을 받아야 머지한다",
    "클라이언트와 서버 간의 모든 네트워크 통신은 HTTPS 보안 프로토콜을 사용한다",
    "API 호출 시 분당 요청 제한(Rate Limit)을 초과하면 429 상태 코드를 반환한다",
    "주요 인프라 모니터링 경보는 슬랙 알림 채널로 실시간 발송된다",
]
D = np.stack([emb(d) for d in docs])  # 문서 10개를 미리 벡터로 (10 x 1024)


def search(question, k=3):
    q = emb(question)
    sims = (
        D @ q / (np.linalg.norm(D, axis=1) * np.linalg.norm(q))
    )  # 문서 10개와의 코사인 유사도 일괄 계산
    results = []
    for i in np.argsort(-sims)[:k]:
        print(f"   {sims[i]:.3f}  {docs[i]}")
        results.append((sims[i], docs[i]))
    return results


# 겹치는 단어 없이 뜻으로만 묻는 질문 3개
questions = [
    "비번 어떻게 보관해?",
    "내 계정 지우면 기록 언제 다 없어져?",
    "새로운 버전 언제 릴리즈해?",
]

for question in questions:
    print(f"Q: {question}")
    search(question)
    print()

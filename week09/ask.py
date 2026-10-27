import ollama
import numpy as np
from openai import OpenAI


def load_index():
    """index.npz 파일을 로드합니다."""
    data = np.load("index.npz", allow_pickle=True)
    return data["V"], data["chunks"]


def search(query, V, chunks, k=3):
    """bge-m3를 사용하여 질문과 유사한 상위 k개 청크를 검색합니다."""
    # 질문 임베딩 (로컬 Ollama 사용)
    qv = np.array(
        ollama.embed(model="bge-m3", input=query)["embeddings"][0], dtype=np.float32
    )
    # 벡터 정규화
    qv = qv / np.linalg.norm(qv)

    # 유사도 계산 (내적)
    scores = V @ qv
    top_indices = np.argsort(-scores)[:k]

    results = []
    for idx in top_indices:
        results.append((chunks[idx], scores[idx]))
    return results


def ask_gemma(query, context_list):
    """교수님 서버의 OpenAI 호환 API를 사용하여 답변을 생성합니다."""
    client = OpenAI(
        base_url="https://krchoi.com/gemma4/v1",
        api_key="none",
        timeout=120,
        max_retries=0
    )

    # 검색된 청크들을 컨텍스트로 구성
    context_text = "\n\n".join([f"[근거 자료]\n{c}" for c, s in context_list])

    prompt = f"""당신은 제공된 자료를 바탕으로 질문에 답하는 인공지능 비서입니다.
반드시 제공된 [근거 자료]만을 바탕으로 답변하세요.
자료에서 추론할 수 있는 내용이라면 답변에 포함하되, 자료에 없는 내용은 반드시 "자료에 없습니다."라고 답해야 합니다.
답변은 반드시 두 문장 이내로 간결하게 하세요.

[근거 자료]
{context_text}

질문: {query}
답변:"""

    try:
        # 서버 혼잡을 고려하여 timeout을 120초로 설정
        r = client.chat.completions.create(
            model="gemma4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        return r.choices[0].message.content.strip()
    except Exception as e:
        # 요청 실패를 명확히 표시
        return f"[API 호출 실패] 오류 내용: {e}"


def main():
    import sys

    # 인덱스 로드
    try:
        V, chunks = load_index()
    except Exception as e:
        print(f"Error loading index: {e}")
        return

    # 기본 테스트 질문 리스트
    DEFAULT_TESTS = [
        "수강 철회는 언제까지 할 수 있어?",
        "결석 몇 번까지 괜찮아?",
        "학생증 잃어버리면 얼마 들어?",
        "휴학하고 나서 등록금 돌려받을 수 있어?",
        "기숙사비는 얼마야?",
    ]

    # 명령줄 인자가 있으면 해당 질문들을, 없으면 기본 질문들을 사용
    if len(sys.argv) > 1:
        queries = sys.argv[1:]
    else:
        queries = DEFAULT_TESTS

    for query in queries:
        print(f"\n질문: {query}")
        print("-" * 30)

        # 1. Retrieval (Local Embedding)
        top_results = search(query, V, chunks)

        print(" [검색 결과 (Top 3)]")
        for i, (text, score) in enumerate(top_results):
            print(f"{i+1}. (유사도: {score:.4f})")
            print(f"{text[:100].replace('\\n', ' ')}...")
            print("-" * 10)

        # 2. Generation (Remote API)
        print("\n [Gemma4 답변]")
        answer = ask_gemma(query, top_results)
        print(answer)
        print("-" * 30)


if __name__ == "__main__":
    main()

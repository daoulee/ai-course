import ollama
import numpy as np

def get_chunks():
    try:
        text = open("guide.txt", encoding="utf-8").read()
    except FileNotFoundError:
        print("Error: guide.txt를 찾을 수 없습니다.")
        return []

    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    current_title = ""
    for p in paragraphs:
        # 절 제목 판단 기준: 짧고 숫자로 시작함
        if len(p) < 30 and p[0].isdigit() and ('.' in p[:5] or p[0:2].isdigit()):
            current_title = p
            continue

        if current_title:
            chunks.append(f"{current_title}\n{p}")
        else:
            chunks.append(p)
    return chunks

chunks = get_chunks()
if not chunks:
    exit(1)

print(f"총 {len(chunks)}개의 청크를 생성했습니다.")

print("임베딩 중 (bge-m3)...")
embeddings = []
for chunk in chunks:
    res = ollama.embed(model="bge-m3", input=chunk)
    emb = res["embeddings"][0]
    embeddings.append(emb)

V = np.array(embeddings, dtype=np.float32)
# 정규화
V = V / np.linalg.norm(V, axis=1, keepdims=True)

# 저장 (chunks는 문자열 배열이므로 allow_pickle=True가 필요할 수 있음)
np.savez("index.npz", V=V, chunks=np.array(chunks, dtype=object))
print("index.npz 저장이 완료되었습니다.")

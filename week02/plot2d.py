import ollama
import numpy as np
import matplotlib.pyplot as plt

# macOS 환경 한글 폰트 설정 (Windows의 경우 "Malgun Gothic")
plt.rcParams["font.family"] = "AppleGothic"
plt.rcParams["axes.unicode_minus"] = False


def emb(text):
    return np.array(ollama.embed(model="bge-m3", input=text).embeddings[0])


groups = {
    "과일": ["사과", "배", "포도", "딸기"],
    "탈것": ["자동차", "버스", "기차", "비행기"],
    "직업": ["의사", "교사", "변호사", "요리사"],
    "동물": ["고양이", "강아지", "호랑이", "독수리"],
    "나라": ["한국", "일본", "프랑스", "브라질"],
}
words = [w for ws in groups.values() for w in ws]
X = np.stack([emb(w) for w in words])  # 20 x 1024

# 1024차원을 2차원으로: 분산이 가장 큰 두 방향만 남긴다 (주성분 분석)
Xc = X - X.mean(axis=0)
U, S, Vt = np.linalg.svd(Xc, full_matrices=False)
P = Xc @ Vt[:2].T  # 20 x 2

fig, ax = plt.subplots(figsize=(7.5, 6))
for group, ws in groups.items():
    for w in ws:
        x, y = P[words.index(w)]
        ax.scatter(x, y, s=60)
        ax.annotate(w, (x, y), xytext=(5, 4), textcoords="offset points", fontsize=12)

ax.set_title("단어 20개의 임베딩을 2차원으로 투영")
ax.set_xticks([])
ax.set_yticks([])
plt.tight_layout()
plt.savefig("week02/words2d.png", dpi=150)
plt.close()
print("week02/words2d.png 생성 완료!")

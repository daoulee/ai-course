text = open("guide.txt", encoding="utf-8").read()

# 1. Paragraph splitting
paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
print("--- 문단 단위 분할 ---")
print(f"문단 수: {len(paragraphs)}")
for i, p in enumerate(paragraphs[:6]):
    print(f"[{i}] {len(p)}자: {p[:40]}...")

# 2. 200-character splitting
size = 200
pieces = [text[i:i + size] for i in range(0, len(text), size)]
print("\n--- 200자 단위 분할 ---")
print(f"조각 수: {len(pieces)}")
print("[3]", repr(pieces[3][:60]))
print("[4]", repr(pieces[4][:60]))

# 3. Chunking with titles
print("\n--- 절 제목을 붙인 청크 생성 ---")
chunks = []
current_title = ""
for p in paragraphs:
    # If it looks like a section title (starts with digit and is short)
    if len(p) < 30 and p[0].isdigit() and ('.' in p[:5] or p[0:2].isdigit()):
        current_title = p
        continue

    if current_title:
        chunks.append(f"{current_title}\n{p}")
    else:
        chunks.append(p)

for i, c in enumerate(chunks[:5]):
    print(f"[{i}]\n{c[:100]}...")
    print("-" * 20)

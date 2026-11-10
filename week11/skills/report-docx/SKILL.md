---
name: report-docx
description: 보고서와 결과 정리처럼 글과 표가 포함된 Word 문서를 만들 때 사용한다. 스프레드시트나 PDF 작업에는 사용하지 않는다.
---

# 보고서 작성 규칙

- 파일명은 실행 당일을 사용해 report_YYYYMMDD.docx로 정한다.
- 문서 첫 단락은 Title 스타일로 제목을 표시한다.
- 제목 다음에 작성일: YYYY-MM-DD 형식으로 오늘 날짜를 적는다.
- 개요, 결과, 결론을 순서대로 배치하고 각 절 제목에는 Heading 1 스타일을 적용한다.
- 결과는 머리글 행이 있는 Table Grid 스타일 표로 나타낸다.
- 문서의 Normal 스타일은 맑은 고딕 11pt로 설정하며, 한글 글꼴에도 적용한다.
- 주어진 사실만 사용하고, 결론은 최대 두 문장으로 쓴다.
- 오늘 날짜는 기억에 의존하지 말고 파이썬 datetime으로 얻는다.

## 한글 글꼴 설정 예시

```python
from docx.shared import Pt
from docx.oxml.ns import qn

normal = doc.styles['Normal']
normal.font.name = '맑은 고딕'
normal.font.size = Pt(11)
normal.element.get_or_add_rPr().get_or_add_rFonts().set(qn('w:eastAsia'), '맑은 고딕')
```

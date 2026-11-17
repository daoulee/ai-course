import base64, json, re
from flask import Flask, render_template, request
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(base_url="https://krchoi.com/gemma4/v1", api_key="none")

def ask(prompt, image_bytes=None, mime="image/jpeg"):
    content = [{"type": "text", "text": prompt}]
    if image_bytes:
        url = f"data:{mime};base64," + base64.b64encode(image_bytes).decode()
        content.append({"type": "image_url", "image_url": {"url": url}})
    r = client.chat.completions.create(model="gemma4", messages=[{"role": "user", "content": content}])
    return r.choices[0].message.content

def parse_json(text):
    m = re.search(r"```(?:json)?\s*(.*?)```", text, re.S)
    try:
        return json.loads(m.group(1) if m else text)
    except (json.JSONDecodeError, TypeError):
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    per_person = None
    total_amount = None
    people_count = None
    remainder = None
    error = None
    items = None

    if request.method == 'POST':
        try:
            # 이미지 업로드 처리
            image_file = request.files.get('receipt_image')
            
            if image_file and image_file.filename != '':
                mime_type = image_file.content_type
                if mime_type not in ['image/jpeg', 'image/png']:
                    error = "JPEG 또는 PNG 이미지 파일만 업로드할 수 있습니다."
                else:
                    image_bytes = image_file.read()
                    prompt = "영수증을 분석해서 다음 JSON 형식으로 응답해줘: {\"items\": [{\"item\": \"항목명\", \"amount\": 금액}, ...], \"final_total\": 최종_결제_금액}. 주의사항: 1. final_total을 확실하게 읽을 수 없다면 반드시 null로 반환할 것. 2. 항목(items)의 금액 합계로 final_total을 추정하여 채우지 말 것."
                    response_text = ask(prompt, image_bytes=image_bytes, mime=mime_type)
                    parsed_result = parse_json(response_text)
                    
                    # 형식 검증 로직
                    is_valid_format = (
                        isinstance(parsed_result, dict) and
                        'items' in parsed_result and
                        'final_total' in parsed_result and
                        isinstance(parsed_result.get('items'), list) and
                        all(
                            isinstance(item, dict) and
                            isinstance(item.get('item'), str) and
                            isinstance(item.get('amount'), int) and
                            not isinstance(item.get('amount'), bool) and
                            item.get('amount') >= 0
                            for item in parsed_result.get('items')
                        ) and
                        (parsed_result.get('final_total') is None or 
                         (isinstance(parsed_result.get('final_total'), int) and not isinstance(parsed_result.get('final_total'), bool) and parsed_result.get('final_total') >= 0))
                    )

                    if not is_valid_format:
                        error = "영수증을 읽지 못했습니다."
                        items = None
                        total_amount = None
                    else:
                        items = parsed_result.get('items')
                        extracted_total = parsed_result.get('final_total')
                        
                        if extracted_total is not None:
                            total_amount = int(extracted_total)
                            # 이미지 분석 직후에는 나누기 계산을 수행하지 않음
                            per_person = None
                            remainder = None
                        else:
                            # final_total이 null인 경우
                            error = "최종 결제 금액을 확인할 수 없습니다. 직접 입력해주세요."
                            total_amount = None
            else:
                # 기존 수동 입력 로직
                total_amount = int(request.form.get('total_amount', 0))
                people_count = int(request.form.get('people_count', 0))

                if total_amount < 0:
                    error = "금액은 0원 이상이어야 합니다."
                elif people_count <= 0:
                    error = "인원수는 1명 이상이어야 합니다."
                else:
                    per_person = total_amount // people_count
                    remainder = total_amount % people_count
                    
        except ValueError:
            error = "숫자만 입력해 주세요."
        except Exception as e:
            error = f"오류가 발생했습니다: {str(e)}"

    return render_template('index.html', 
                           per_person=per_person, 
                           total_amount=total_amount, 
                           people_count=people_count, 
                           remainder=remainder,
                           error=error,
                           items=items)

if __name__ == '__main__':
    app.run(debug=True)

import flet as ft
from logic import generate_password

def main(page: ft.Page):
    page.title = "비밀번호 생성기"
    page.window.width = 360
    page.window.height = 440
    page.window.resizable = False

    # UI Components
    length_input = ft.TextField(label="길이")

    chk_upper = ft.Checkbox(label="대문자")
    chk_digits = ft.Checkbox(label="숫자")
    chk_special = ft.Checkbox(label="특수문자")
    chk_avoid = ft.Checkbox(label="헷갈리는 문자 제외")

    result_field = ft.TextField(label="결과", value="")
    error_text = ft.Text(value="", color=ft.Colors.RED)

    def handle_generate(e):
        # Get current values from UI
        length_val = length_input.value
        upper = chk_upper.value
        digits = chk_digits.value
        special = chk_special.value
        avoid = chk_avoid.value

        # Call logic.py
        password, error = generate_password(
            length_text=length_val,
            include_upper=upper,
            include_digits=digits,
            include_special=special,
            avoid_ambiguous=avoid
        )

        if error:
            result_field.value = ""
            error_text.value = error
        else:
            result_field.value = password
            error_text.value = ""

        page.update()

    # Buttons using ft.Button and Row
    btn_make = ft.Row(controls=[ft.Button(content="만들기", on_click=handle_generate)])
    btn_remake = ft.Row(controls=[ft.Button(content="다시 만들기", on_click=handle_generate)])

    # Add components to page in order
    page.add(
        length_input,
        chk_upper,
        chk_digits,
        chk_special,
        chk_avoid,
        btn_make,
        result_field,
        btn_remake,
        error_text
    )

if __name__ == "__main__":
    ft.run(main)

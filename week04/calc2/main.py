import flet as ft
from calc import Calculator

def main(page: ft.Page):
    page.title = "계산기"
    page.window.width = 340
    page.window.height = 520
    page.window.resizable = False

    calc = Calculator()

    display = ft.Text(value="0", size=40, text_align=ft.TextAlign.RIGHT)

    def on_button(e):
        key = e.control.data
        calc.press(key)
        display.value = calc.display
        page.update()

    def on_key(e: ft.KeyboardEvent):
        key_map = {
            "Enter": "=",
            "Backspace": "BS",
            "Escape": "C",
        }
        key = key_map.get(e.key, e.key)
        calc.press(key)
        display.value = calc.display
        page.update()

    page.on_keyboard_event = on_key

    def make_button(label, key, bgcolor):
        return ft.Button(
            content=label,
            data=key,
            on_click=on_button,
            expand=1,
            height=60,
            bgcolor=bgcolor,
            color=ft.Colors.WHITE
        )

    page.add(
        ft.Container(content=display, alignment=ft.Alignment.CENTER_RIGHT, padding=10, height=90),
        ft.Row(controls=[
            make_button("C", "C", ft.Colors.GREY_600),
            make_button("+/-", "+/-", ft.Colors.GREY_600),
            make_button("%", "%", ft.Colors.GREY_600),
            make_button("÷", "/", ft.Colors.ORANGE),
        ]),
        ft.Row(controls=[
            make_button("7", "7", ft.Colors.GREY_800),
            make_button("8", "8", ft.Colors.GREY_800),
            make_button("9", "9", ft.Colors.GREY_800),
            make_button("×", "*", ft.Colors.ORANGE),
        ]),
        ft.Row(controls=[
            make_button("4", "4", ft.Colors.GREY_800),
            make_button("5", "5", ft.Colors.GREY_800),
            make_button("6", "6", ft.Colors.GREY_800),
            make_button("−", "-", ft.Colors.ORANGE),
        ]),
        ft.Row(controls=[
            make_button("1", "1", ft.Colors.GREY_800),
            make_button("2", "2", ft.Colors.GREY_800),
            make_button("3", "3", ft.Colors.GREY_800),
            make_button("+", "+", ft.Colors.ORANGE),
        ]),
        ft.Row(controls=[
            make_button("0", "0", ft.Colors.GREY_800),
            make_button(".", ".", ft.Colors.GREY_800),
            make_button("⌫", "BS", ft.Colors.GREY_800),
            make_button("=", "=", ft.Colors.ORANGE),
        ]),
    )

ft.run(main)

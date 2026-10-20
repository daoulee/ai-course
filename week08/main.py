import flet as ft
from datetime import datetime
from calculator import ParkingCalculator


def main(page: ft.Page):
    # Page setup (Flet 1.0 syntax as per template)
    page.title = "주차 요금 계산기"
    page.window.width = 500
    page.window.height = 700
    page.window.resizable = False
    page.theme_mode = ft.ThemeMode.LIGHT

    calc = ParkingCalculator()
    today_str = datetime.now().strftime("%Y-%m-%d")

    # UI Components (Following template style)
    header_text = ft.Text(value="", size=16, weight=ft.FontWeight.BOLD)
    total_fee_text = ft.Text(value="", size=16, weight=ft.FontWeight.BOLD)

    entry_input = ft.TextField(label="입차 시각 (HH:MM)", width=180)
    exit_input = ft.TextField(label="출차 시각 (HH:MM)", width=180)

    error_text = ft.Text(value="", color=ft.Colors.RED_400, size=12)

    # Using ListView for records as seen in template
    record_list = ft.ListView(expand=True, spacing=10)

    def update_summary():
        """기준 날짜와 오늘 합계를 갱신하여 상단 표시"""
        current_today = datetime.now().strftime("%Y-%m-%d")
        header_text.value = f"기준 날짜: {current_today}"
        total_sum = calc.get_today_total(current_today)
        total_fee_text.value = f"오늘의 요금 합계: {total_sum:,.0f}원"
        page.update()

    def refresh_record_list():
        """기록 목록 UI를 새로 고침"""
        record_list.controls.clear()
        for i, rec in enumerate(calc.get_all_records()):
            # rec: (entry, exit, duration, fee, date_str)
            entry, exit_t, duration, fee, date_val = rec

            info_text = ft.Text(
                value=f"{entry}-{exit_t} ({duration}분) | {fee:,.0f}원", expand=True
            )

            def create_delete_handler(idx):
                def on_delete(e):
                    calc.delete_record(idx)
                    update_summary()
                    refresh_record_list()

                return on_delete

            delete_btn = ft.Button(
                content=ft.Text("삭제", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.RED_400,
                on_click=create_delete_handler(i),
            )

            record_list.controls.append(
                ft.Row(
                    controls=[info_text, delete_btn],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                )
            )

        page.update()

    def handle_calculate(e):
        # 1. 입력값 가져오기
        start_val = entry_input.value
        end_val = exit_input.value

        # 2. 계산 로직 호출
        record, error = calc.calculate_fee(start_val, end_val)

        if error:
            # 실패 시: 에러 메시지 표시 및 입력창 초기화
            error_text.value = error
            entry_input.value = ""
            exit_input.value = ""
        else:
            # 성공 시: 기록 추가 및 에러 메시지 제거
            error_text.value = ""
            entry_input.value = ""
            exit_input.value = ""
            calc.add_record(record)
            refresh_record_list()

        # [Requirement 1] 계산 버튼을 누르면 성공·실패와 관계없이 날짜와 합계 갱신
        update_summary()
        page.update()

    def on_connect_handler(e):
        """새로고침 또는 재연결 시 호출되어 데이터를 초기화함"""
        # 데이터(기록) 초기화
        calc.records.clear()

        # UI 상태 초기화
        error_text.value = ""
        entry_input.value = ""
        exit_input.value = ""

        # UI 갱신 (목록, 합계, 날짜)
        refresh_record_list()
        update_summary()
        page.update()

    # Register event handler for reconnection/refresh
    page.on_connect = on_connect_handler

    # Initial Setup
    header_text.value = f"기준 날짜: {today_str}"
    update_summary()

    # Layout Construction (Simplified to match template's additive style)
    page.add(
        ft.Column(
            [
                ft.Row(
                    [header_text, total_fee_text],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Divider(),
                ft.Row(
                    [entry_input, exit_input], alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Row(
                    [
                        ft.Button(
                            content=ft.Text("계산"),
                            on_click=handle_calculate,
                            expand=True,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                error_text,
                ft.Text(
                    "※ 자정을 넘기는 주차는 지원하지 않습니다. 새로고침이나 재연결 시 기록이 초기화됩니다.",
                    size=10,
                    color=ft.Colors.GREY_500,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        ft.Divider(),
        ft.Text("계산 기록", size=18, weight=ft.FontWeight.BOLD),
        record_list,
    )

    # Initial list load
    refresh_record_list()


if __name__ == "__main__":
    ft.run(main)

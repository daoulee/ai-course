import sys
from datetime import datetime
from calculator import ParkingCalculator

def test_parking_calculator():
    calc = ParkingCalculator()
    passed = 0
    failed = 0
    errors = []

    def run_test(test_id, name, func):
        nonlocal passed, failed
        try:
            func()
            passed += 1
        except AssertionError as e:
            failed += 1
            errors.append(f"[{test_id}] {name}: {str(e)}")
        except Exception as e:
            failed += 1
            errors.append(f"[{test_id}] {name}: Unexpected Error ({type(e).__name__}: {str(e)})")

    # --- Case 1: 요금 계산 경계값 ---
    def t1():
        res = calc.calculate_fee("09:00", "09:29")
        record, error = res
        assert record is not None
        assert error is None
        assert record[2] == 29
        assert record[3] == 0
    run_test("T1", "무료 구간 (29분)", t1)

    def t2():
        res = calc.calculate_fee("09:00", "09:30")
        record, error = res
        assert record is not None
        assert error is None
        assert record[2] == 30
        assert record[3] == 0
    run_test("T2", "무료 구간 경계 (30분)", t2)

    def t3():
        res = calc.calculate_fee("09:00", "09:31")
        record, error = res
        assert record is not None
        assert error is None
        assert record[2] == 31
        assert record[3] == 500
    run_test("T3", "유료 구간 시작 (31분)", t3)

    def t4():
        res = calc.calculate_fee("09:00", "09:41")
        record, error = res
        assert record is not None
        assert error is None
        assert record[2] == 41
        assert record[3] == 1000
    run_test("T4", "10분 미만 올림 적용 (41분)", t4)

    def t5():
        res = calc.calculate_fee("09:00", "13:00")
        record, error = res
        assert record is not None
        assert error is None
        assert record[2] == 240
        assert record[3] == 10500
    run_test("T5", "정상 유료 계산 (4시간)", t5)

    def t6():
        res = calc.calculate_fee("09:00", "16:00")
        record, error = res
        assert record is not None
        assert error is None
        assert record[2] == 420
        assert record[3] == 19500
    run_test("T6", "정상 유료 계산 (7시간)", t6)

    def t7():
        res = calc.calculate_fee("09:00", "16:01")
        record, error = res
        assert record is not None
        assert error is None
        assert record[2] == 421
        assert record[3] == 20000
    run_test("T7", "상한 적용 (7시간 1분)", t7)

    def t8():
        res = calc.calculate_fee("09:00", "16:11")
        record, error = res
        assert record is not None
        assert error is None
        assert record[2] == 431
        assert record[3] == 20000
    run_test("T8", "상한 도달 후 유지 (7시간 11분)", t8)

    # --- Case 2: 입력 유효성 검증 ---
    def t9():
        res = calc.calculate_fee("", "10:00")
        record, error = res
        assert record is None
        assert error is not None
    run_test("T9", "빈 입력 (Entry)", t9)

    def t10():
        res = calc.calculate_fee("09:00", " ")
        record, error = res
        assert record is None
        assert error is not None
    run_test("T10", "공백 입력 (Exit)", t10)

    def t11():
        res = calc.calculate_fee("09:65", "10:00")
        record, error = res
        assert record is None
        assert error is not None
    run_test("T11", "잘못된 분 단위 (09:65)", t11)

    def t12():
        res = calc.calculate_fee("24:00", "25:00")
        record, error = res
        assert record is None
        assert error is not None
    run_test("T12", "범위를 벗어난 시각 (24:00)", t12)

    def t13():
        res = calc.calculate_fee("abc", "10:00")
        record, error = res
        assert record is None
        assert error is not None
    run_test("T13", "임의 문자열", t13)

    def t14():
        res = calc.calculate_fee("9:5", "10:0")
        record, error = res
        assert record is None
        assert error is not None
    run_test("T14", "두 자리 형식 미준수 (9:5)", t14)

    def t15():
        res = calc.calculate_fee("10:00", "10:00")
        record, error = res
        assert record is None
        assert error is not None
    run_test("T15", "입차와 출차 시각 동일", t15)

    def t16():
        res = calc.calculate_fee("10:00", "09:00")
        record, error = res
        assert record is None
        assert error is not None
    run_test("T16", "출차가 입차보다 빠름", t16)

    def t17():
        res = calc.calculate_fee(" 09:00 ", " 09:31 ")
        record, error = res
        assert record is not None
        assert error is None
        assert record[2] == 31
        assert record[3] == 500
    run_test("T17", "앞뒤 공백 제거 후 정상 처리", t17)

    def t18():
        res = calc.calculate_fee("09:00", "09:65")
        record, error = res
        assert record is None
        assert error is not None
    run_test("T18", "공백 제거 후에도 잘못된 형식", t18)

    # --- Case 3: 목록 및 합계 관리 ---
    def t19():
        c = ParkingCalculator()
        c.add_record(("09:00", "09:31", 31, 500, "2026-10-20"))
        c.add_record(("10:00", "10:41", 41, 1000, "2026-10-20"))
        c.add_record(("11:00", "12:10", 70, 2000, "2026-10-21"))
        assert c.get_today_total("2026-10-20") == 1500
    run_test("T19", "여러 날짜 기록 존재 (D1 합계)", t19)

    def t20():
        c = ParkingCalculator()
        r1 = ("09:00", "09:31", 31, 500, "2026-10-20")
        r2 = ("10:00", "10:41", 41, 1000, "2026-10-20")
        r3 = ("11:00", "12:10", 70, 2000, "2026-10-20")
        c.add_record(r1)
        c.add_record(r2)
        c.add_record(r3)
        c.delete_record(1)
        assert len(c.records) == 2
        assert c.records == [r1, r3]
        assert c.get_today_total("2026-10-20") == 2500
    run_test("T20", "중간 기록 삭제", t20)

    def t21():
        c = ParkingCalculator()
        c.add_record(("09:00", "09:31", 31, 500, "2026-10-20"))
        c.delete_record(0)
        assert len(c.records) == 0
        assert c.get_today_total("2026-10-20") == 0
    run_test("T21", "모든 기록 삭제", t21)

    def t22():
        c = ParkingCalculator()
        c.add_record(("09:00", "09:31", 31, 500, "2026-10-20"))
        before_records = c.records.copy()
        assert c.get_today_total("2026-10-21") == 0
        assert c.get_all_records() == before_records
    run_test("T22", "날짜 변경 시뮬레이션", t22)

    print(f"통과: {passed}, 실패: {failed}")
    if failed > 0:
        for err in errors:
            print(err)
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    test_parking_calculator()

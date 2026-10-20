from datetime import datetime, timedelta


class ParkingCalculator:
    def __init__(self):
        self.records = []

    def validate_time_format(self, time_str):
        """HH:MM 형식을 검사하고 (strip 후) 정규화된 문자열 또는 None을 반환"""
        if not time_str:
            return None

        t = time_str.strip()
        # 반드시 두 자리:두 자리 형식을 엄격히 검사 (HH:MM)
        if len(t) != 5 or t[2] != ":":
            return None

        try:
            hour_part = t[:2]
            minute_part = t[3:]

            if not (hour_part.isdigit() and minute_part.isdigit()):
                return None

            if len(hour_part) != 2 or len(minute_part) != 2:
                return None

            hour = int(hour_part)
            minute = int(minute_part)

            if 0 <= hour <= 23 and 0 <= minute <= 59:
                return t
            else:
                return None
        except ValueError:
            return None

    def calculate_fee(self, start_time_str, end_time_str):
        """
        입력값을 검증하고 요금을 계산함.
        성공 시 (record, None) 반환.
        실패 시 (None, error_message) 튜플 반환.
        """
        # 1. 빈 값 검사
        if (
            not start_time_str
            or not start_time_str.strip()
            or not end_time_str
            or not end_time_str.strip()
        ):
            return None, "입력값이 비어 있습니다."

        start_t = self.validate_time_format(start_time_str)
        end_t = self.validate_time_format(end_time_str)

        # 2. 형식 검사
        if start_t is None or end_t is None:
            return None, "잘못된 시각 형식입니다. (HH:MM)"

        # 3. 논리 검사 (입차 < 출차)
        fmt = "%H:%M"
        try:
            dt_start = datetime.strptime(start_t, fmt)
            dt_end = datetime.strptime(end_t, fmt)

            if dt_start >= dt_end:
                return None, "출차 시각은 입차 시각보다 늦어야 합니다."

            # 주차 시간 계산 (분 단위)
            duration = (dt_end - dt_start).total_seconds() / 60

            # 4. 요금 계산
            if duration <= 30:
                fee = 0
            else:
                # 30분 초과 시, 10분 단위 올림 계산
                # 31분 -> (31-30)=1분 -> 10분으로 간주 -> 500원
                extra_mins = duration - 30
                # math.ceil(extra_mins / 10) 과 동일한 정수 연산
                units = (int(extra_mins + 9) // 10) if extra_mins > 0 else 0
                # 위 식은 정교하게 하기 위해 다시 정의:
                # 1분이라도 있으면 1단위(10분)로 침.
                import math

                units = math.ceil(extra_mins / 10)
                fee = units * 500

            # 하루 최대 요금 20,000원
            if fee > 20000:
                fee = 20000

            return (
                start_t,
                end_t,
                int(duration),
                fee,
                datetime.now().strftime("%Y-%m-%d"),
            ), None

        except ValueError:
            return None, "유효하지 않은 시각 범위입니다."

    def add_record(self, record):
        """record: (entry, exit, duration, fee, date_str)"""
        self.records.append(record)

    def delete_record(self, index):
        """인덱스로 기록 삭제"""
        if 0 <= index < len(self.records):
            del self.records[index]
            return True
        return False

    def get_today_total(self, target_date_str):
        """지정된 날짜(YYYY-MM-DD)에 해당하는 요금 합계 계산"""
        total = 0
        for rec in self.records:
            # rec[4] 는 계산 날짜 (date_str)
            if rec[4] == target_date_str:
                total += rec[3]
        return total

    def get_all_records(self):
        return self.records

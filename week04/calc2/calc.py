from decimal import Decimal, getcontext, ROUND_HALF_UP, InvalidOperation

class Calculator:
    def __init__(self):
        getcontext().prec = 60
        self._reset_state()
        self._is_error = False

    def _reset_state(self):
        self._current_num_str = "0"
        self._stored_num = None
        self._operator = None
        self._is_result_shown = False
        self._has_decimal = False
        self.display = "0"

    def _format_result(self, val: Decimal) -> str:
        rounded = val.quantize(Decimal("1.0000000000"), rounding=ROUND_HALF_UP)
        s = format(rounded, 'f')
        if '.' in s:
            s = s.rstrip('0').rstrip('.')
        return s if s != "" else "0"

    def press(self, key: str) -> str:
        if self._is_error:
            if key == "C":
                self._reset_state()
                self._is_error = False
                self.display = "0"
            return self.display
        if key == "C":
            self._reset_state()
            self.display = "0"
            return self.display
        if key == "BS":
            if self._is_result_shown: return self.display
            if self._current_num_str == "0": return self.display
            if self._current_num_str == "-":
                self._current_num_str = "0"
            elif self._current_num_str.endswith("."):
                self._current_num_str = self._current_num_str[:-1]
                self._has_decimal = False
            elif len(self._current_num_str) == 1:
                self._current_num_str = "0"
            else:
                self._current_num_str = self._current_num_str[:-1]
                if self._current_num_str.endswith("."): self._has_decimal = False
            self.display = self._current_num_str
            return self.display
        if key == "+/-":
            if self._current_num_str != "0":
                if self._current_num_str.startswith("-"): self._current_num_str = self._current_num_str[1:]
                else: self._current_num_str = "-" + self._current_num_str
                self.display = self._current_num_str
            return self.display
        if key == "%":
            try:
                val = Decimal(self._current_num_str) / Decimal("100")
                self._current_num_str = self._format_result(val)
                self._has_decimal = "." in self._current_num_str
                self.display = self._current_num_str
            except: pass
            return self.display
        if key in "0123456789.":
            if self._is_result_shown:
                self._current_num_str, self._is_result_shown, self._stored_num, self._operator, self._has_decimal = "", False, None, None, False
            clean_digits = self._current_num_str.replace("-", "").replace(".", "")
            if len(clean_digits) >= 12 and key != ".":
                return self.display
            if key == ".":
                if not self._has_decimal:
                    if self._current_num_str == "0":
                        self._current_num_str = "0."
                    elif self._current_num_str == "-":
                        self._current_num_str = "-0."
                    else:
                        self._current_num_str += "."
                    self._has_decimal = True
                    self.display = self._current_num_str
                return self.display
            else:
                if self._current_num_str == "0" and key != "-":
                    self._current_num_str = key
                elif self._current_num_str == "-":
                    self._current_num_str += key
                else:
                    self._current_num_str += key
                self.display = self._current_num_str
            return self.display
        if key in "+-*/=":
            try: val_now = Decimal(self._current_num_str)
            except: val_now = Decimal("0")
            if key == "=":
                if self._operator is None: self.display = self._format_result(val_now)
                else:
                    try:
                        res = self._perform_op(self._stored_num, val_now, self._operator)
                        self.display = self._format_result(res)
                        self._stored_num = res
                    except ZeroDivisionError:
                        self._is_error = True
                        self.display = "0으로 나눌 수 없습니다"
                        return self.display
                self._current_num_str, self._is_result_shown, self._operator, self._has_decimal = self.display, True, None, "." in self.display
            else:
                if self._operator is None: self._stored_num = val_now
                else:
                    try:
                        res = self._perform_op(self._stored_num, val_now, self._operator)
                        self._stored_num = res
                        self.display = self._format_result(res)
                    except ZeroDivisionError:
                        self._is_error = True
                        self.display = "0으로 나눌 수 없습니다"
                        return self.display
                self._operator, self._is_result_shown, self._current_num_str, self._has_decimal = key, False, "0", False
                self.display = self._format_result(self._stored_num)
            return self.display
        return self.display

    def _perform_op(self, n1, n2, op):
        if op == "+": return n1 + n2
        if op == "-": return n1 - n2
        if op == "*": return n1 * n2
        if op == "/":
            if n2 == 0: raise ZeroDivisionError()
            return n1 / n2
        return n2

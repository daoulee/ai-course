from calc import Calculator

def test():
    # (inputs, expected_display)
    test_cases = [
        ([], "0"),
        (["1", "2", "+", "3", "="], "15"),
        (["2", "+", "3", "*", "4", "="], "20"),
        (["5", "+", "-", "3", "="], "2"),
        (["0", ".", "1", "+", "0", ".", "2", "="], "0.3"),
        (["6", "/", "3", "="], "2"),
        (["7", "/", "2", "="], "3.5"),
        (["5", "/", "0", "="], "0으로 나눌 수 없습니다"),
        (["5", "/", "0", "=", "7"], "0으로 나눌 수 없습니다"),
        (["5", "/", "0", "=", "C"], "0"),
        (["1", ".", ".", "5"], "1.5"),
        (["."], "0."),
        (["0", "0", "7"], "7"),
        (["1", "2", "3", "BS"], "12"),
        (["5", "BS"], "0"),
        (["9", "+/-"], "-9"),
        (["5", "0", "%"], "0.5"),
        (["2", "+", "3", "=", "4"], "4"),
        (["2", "+", "3", "=", "+", "4", "="], "9"),
        (["2", "+", "3", "=", "=", "5"], "5"),
    ]

    for i, (inputs, expected) in enumerate(test_cases):
        calc = Calculator()

        # Initial case handling for empty input
        if not inputs:
            actual = calc.display
        else:
            for key in inputs:
                calc.press(key)
            actual = calc.display

        if actual != expected:
            print(f"Fail at case {i+1}: input={' '.join(inputs) if inputs else '(empty)'}, expected='{expected}', actual='{actual}'")
            exit(1)

    print(f"모든 테스트 통과 ({len(test_cases)}개)")
    exit(0)

if __name__ == "__main__":
    test()

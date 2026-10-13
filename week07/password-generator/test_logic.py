import sys
from logic import generate_password

def test_password_generator():
    passed = 0
    failed = 0

    def assert_test(condition, message):
        nonlocal passed, failed
        if condition:
            passed += 1
        else:
            print(f"FAIL: {message}")
            failed += 1

    # 1. 길이 12, 모든 종류 선택 (소문자, 대문자, 숫자, 특수문자)
    pw, err = generate_password("12", True, True, True, False)
    assert_test(err == "", "Length 12, all types: Error should be empty")
    assert_test(len(pw) == 12, "Length 12, all types: Length mismatch")
    assert_test(all(c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*" for c in pw), "Length 12, all types: Invalid characters")
    # Check at least one of each
    has_lower = any(c in "abcdefghijklmnopqrstuvwxyz" for c in pw)
    has_upper = any(c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" for c in pw)
    has_digit = any(c in "0123456789" for c in pw)
    has_special = any(c in "!@#$%^&*" for c in pw)
    assert_test(has_lower and has_upper and has_digit and has_special, "Length 12, all types: Missing required character type")

    # 2. 길이 4, 선택 옵션 없음 (소문자만)
    pw, err = generate_password("4", False, False, False, False)
    assert_test(err == "", "Length 4, none selected: Error should be empty")
    assert_test(len(pw) == 4, "Length 4, none selected: Length mismatch")
    assert_test(all(c in "abcdefghijklmnopqrstuvwxyz" for c in pw), "Length 4, none selected: Contains unauthorized characters")

    # 3. 길이 32, 대문자·숫자 선택 (소문자 포함)
    pw, err = generate_password("32", True, True, False, False)
    assert_test(err == "", "Length 32, upper/digit: Error should be empty")
    assert_test(len(pw) == 32, "Length 32, upper/digit: Length mismatch")
    # Must have lower, upper, digits. Must NOT have special.
    has_lower = any(c in "abcdefghijklmnopqrstuvwxyz" for c in pw)
    has_upper = any(c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" for c in pw)
    has_digit = any(c in "0123456789" for c in pw)
    has_special = any(c in "!@#$%^&*" for c in pw)
    assert_test(has_lower and has_upper and has_digit, "Length 32, upper/digit: Missing required type")
    assert_test(not has_special, "Length 32, upper/digit: Should not contain special characters")

    # 4. 잘못된 길이 입력 (빈 값, abc, 4.5, 3, 33)
    for invalid_len in ["", "abc", "4.5", "3", "33"]:
        pw, err = generate_password(invalid_len, True, True, True, False)
        assert_test(pw == "" and err != "", f"Invalid length '{invalid_len}': Should return empty password and error message")

    # 5. 오타 방지 모드 (헷갈리는 문자 제외)
    pw, err = generate_password("12", True, True, True, True)
    assert_test(err == "", "Avoid ambiguous: Error should be empty")
    confusing = set("IOlo01")
    assert_test(all(c not in confusing for c in pw), "Avoid ambiguous: Contains confusing characters")
    # Verify categories still met
    has_lower = any(c in "abcdefghijklmnopqrstuvwxyz" for c in pw)
    has_upper = any(c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" for c in pw)
    has_digit = any(c in "0123456789" for c in pw)
    has_special = any(c in "!@#$%^&*" for c in pw)
    assert_test(has_lower and has_upper and has_digit and has_special, "Avoid ambiguous: Missing required character type")

    # 6. 같은 설정으로 두 번 호출
    pw1, err1 = generate_password("15", True, True, False, False)
    pw2, err2 = generate_password("15", True, True, False, False)

    # Verify both are valid
    assert_test(err1 == "" and len(pw1) == 15, "Second call 1: First call should be valid")
    assert_test(err2 == "" and len(pw2) == 15, "Second call 1: Second call should be valid")

    # Verify both follow same character constraints
    for p in [pw1, pw2]:
        has_lower = any(c in "abcdefghijklmnopqrstuvwxyz" for c in p)
        has_upper = any(c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" for c in p)
        has_digit = any(c in "0123456789" for c in p)
        has_special = any(c in "!@#$%^&*" for c in p)
        assert_test(has_lower and has_upper and has_digit and not has_special, f"Second call 1: Password {p} violates constraints")

    print(f"PASSED: {passed}, FAILED: {failed}")
    if failed > 0:
        sys.exit(1)

if __name__ == "__main__":
    test_password_generator()

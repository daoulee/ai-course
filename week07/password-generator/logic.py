import secrets
import string

def generate_password(length_text: str, include_upper: bool, include_digits: bool, include_special: bool, avoid_ambiguous: bool = False) -> tuple[str, str]:
    """
    Generates a password based on the given criteria.

    Returns:
        tuple[str, str]: (password, error_message)
    """
    # 1. Validate length input
    try:
        length = int(length_text)
        if not (4 <= length <= 32):
            return "", "길이는 4~32 사이여야 합니다."
    except (ValueError, TypeError):
        return "", "올바른 숫자를 입력해주세요."

    # 2. Define base character sets
    lower_set = string.ascii_lowercase
    upper_set = string.ascii_uppercase
    digits_set = string.digits
    special_set = "!@#$%^&*"

    confusing = set("IOlo01")

    # 3. Determine active categories and filter characters
    # Always include lowercase
    active_categories = []

    # Process Lowercase (Always)
    lower_chars = [c for c in lower_set if not (avoid_ambiguous and c in confusing)]
    active_categories.append(lower_chars)

    # Process Upper
    if include_upper:
        upper_chars = [c for c in upper_set if not (avoid_ambiguous and c in confusing)]
        if upper_chars:
            active_categories.append(upper_chars)

    # Process Digits
    if include_digits:
        digit_chars = [c for c in digits_set if not (avoid_ambiguous and c in confusing)]
        if digit_chars:
            active_categories.append(digit_chars)

    # Process Special
    if include_special:
        special_chars = [c for c in special_set if not (avoid_ambiguous and c in confusing)]
        if special_chars:
            active_categories.append(special_chars)

    # 4. Handle case where no categories are available (shouldn't happen since lower is always there)
    if not active_categories:
        return "", "선택된 문자 종류가 없습니다."

    # 5. Generate password
    password_list = []

    # Rule: Each selected type must have at least one character
    for chars in active_categories:
        password_list.append(secrets.choice(chars))

    # If selected categories exceed length, truncate (per spec min length 4, max categories 4, so unlikely)
    if len(password_list) > length:
        secrets.SystemRandom().shuffle(password_list)
        return "".join(password_list[:length]), ""

    # 6. Fill the rest of the length
    all_allowed_pool = []
    for chars in active_categories:
        all_allowed_pool.extend(chars)

    remaining_count = length - len(password_list)
    for _ in range(remaining_count):
        password_list.append(secrets.choice(all_allowed_pool))

    # 7. Shuffle the final result
    secrets.SystemRandom().shuffle(password_list)

    return "".join(password_list), ""

# -*- coding: utf-8 -*-
"""
⚾ 파이썬 숫자 야구 게임 (Number Baseball Game)
학번: 202230136
"""

import random

def generate_secret_numbers(digit_count=3):
    """중복되지 않는 0~9 사이의 무작위 숫자를 생성합니다."""
    numbers = list(range(10))
    return random.sample(numbers, digit_count)

def calculate_score(secret, guess):
    """스트라이크(Strike)와 볼(Ball)의 개수를 계산합니다."""
    strikes = 0
    balls = 0
    for i in range(len(guess)):
        if guess[i] == secret[i]:
            strikes += 1
        elif guess[i] in secret:
            balls += 1
    return strikes, balls

def play_game():
    print("=" * 55)
    print("       ⚾ 파이썬 숫자 야구 게임 (Number Baseball) ⚾")
    print("=" * 55)
    print("규칙: 서로 다른 3자리 숫자를 맞춰보세요! (총 9회의 기회)")
    print("- Strike (S): 숫자와 위치가 모두 일치")
    print("- Ball   (B): 숫자는 맞지만 위치가 다름")
    print("- Out    (O): 일치하는 숫자가 전혀 없음\n")

    secret = generate_secret_numbers(3)
    secret_str = "".join(map(str, secret))
    max_attempts = 9
    attempts = 1

    while attempts <= max_attempts:
        print(f"━━━━━━━━━━━━━━━ [ 제 {attempts} / {max_attempts} 이닝 ] ━━━━━━━━━━━━━━━")
        user_input = input("3자리 숫자를 입력하세요 (예: 123, 종료: q): ").strip()

        if user_input.lower() == 'q':
            print("\n게임을 종료합니다.")
            return

        # 입력 유효성 검사 (3자리 숫자, 중복 없음)
        if len(user_input) != 3 or not user_input.isdigit() or len(set(user_input)) != 3:
            print("⚠️ 서로 다른 3자리 숫자를 정확히 입력해주세요!\n")
            continue

        guess = [int(ch) for ch in user_input]
        strikes, balls = calculate_score(secret, guess)

        # 판정 결과 출력
        if strikes == 3:
            print(f"\n🎉🎉🎉 축하합니다! HOMERUN!! 정답입니다! [{secret_str}] 🎉🎉🎉")
            print(f"👉 {attempts}회 만에 승리하셨습니다!\n")
            return
        elif strikes == 0 and balls == 0:
            print("👉 결과: 🛑 OUT (아웃!)\n")
        else:
            print(f"👉 결과: 🟢 {strikes} Strike, 🟡 {balls} Ball\n")

        attempts += 1

    print(f"😢 9회말 종료! 아쉽게도 모든 기회를 사용하셨습니다.")
    print(f"정답은 [{secret_str}] 이었습니다. 다음 게임에 도전해보세요!\n")

if __name__ == "__main__":
    play_game()

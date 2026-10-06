def average(scores):
    if not scores:
        return 0
    return sum(scores) / len(scores)


def top_n(scores, n):
    return sorted(scores, reverse=True)[:n]


def grade(score):
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    return "F"


def pass_rate(scores, cut=60):
    if not scores:
        return 0
    passed = [s for s in scores if s >= cut]
    return len(passed) / len(scores) * 100

def _answer(text):
    balance = 0
    minimum = 0
    for char in text:
        balance += 1 if char == "(" else -1
        minimum = min(minimum, balance)
    return balance - 2 * minimum


def _family(text):
    balance = 0
    minimum = 0
    for char in text:
        balance += 1 if char == "(" else -1
        minimum = min(minimum, balance)
    answer = balance - 2 * minimum
    if answer == 1:
        return 0 if balance == -1 else 1
    if answer == 3:
        return 2 if balance < 0 else 3
    if answer == 5:
        return 4
    if answer == 7:
        return 5
    raise ValueError("outside domain")


def solve(text):
    answer = _answer(text)
    if text == text[::-1]:
        return answer + 1
    return answer

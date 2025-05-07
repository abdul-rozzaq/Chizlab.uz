import random


def generate_otp(digits: int = 6) -> int:
    return random.randint(10 ** (digits - 1), 10 ** digits - 1)

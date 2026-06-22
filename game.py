import random
import math


def generate_secret_number(min_number=1, max_number=100):
    if min_number >= max_number:
        raise ValueError("min_number must be less than max_number")
    return random.randint(min_number, max_number)


def check_guess(guess, secret):
    if not isinstance(guess, int) or isinstance(guess, bool):
        raise TypeError("guess must be an integer")
    if not isinstance(secret, int) or isinstance(secret, bool):
        raise TypeError("secret must be an integer")
    if guess < secret:
        return "higher"
    elif guess > secret:
        return "lower"
    else:
        return "correct"


def validate_guess(guess_str, min_number=1, max_number=100):
    try:
        guess = int(guess_str)
    except (ValueError, TypeError):
        raise ValueError(f"Ввод должен быть целым числом, получено: {guess_str!r}")
    if guess < min_number or guess > max_number:
        raise ValueError(f"Число должно быть от {min_number} до {max_number}")
    return guess


def calculate_optimal_attempts(min_number, max_number):
    if min_number >= max_number:
        raise ValueError("min_number must be less than max_number")
    return math.ceil(math.log2(max_number - min_number + 1))


def get_hint(guess, secret, min_number, max_number):
    range_size = max_number - min_number
    distance = abs(guess - secret)
    if distance == 0:
        return "Точное попадание!"
    elif distance <= range_size * 0.1:
        return "Очень горячо!"
    elif distance <= range_size * 0.25:
        return "Тепло!"
    elif distance <= range_size * 0.5:
        return "Прохладно"
    else:
        return "Холодно!"


def play_round(secret, min_number=1, max_number=100, input_func=input, print_func=print):
    attempts = 0
    while True:
        raw = input_func(f"Введите число от {min_number} до {max_number}: ")
        try:
            guess = validate_guess(raw, min_number, max_number)
        except ValueError as e:
            print_func(f"Ошибка: {e}")
            continue
        attempts += 1
        result = check_guess(guess, secret)
        hint = get_hint(guess, secret, min_number, max_number)
        if result == "correct":
            print_func(f"Правильно! Вы угадали за {attempts} попыток. {hint}")
            return attempts
        elif result == "higher":
            print_func(f"Загаданное число больше. {hint}")
        else:
            print_func(f"Загаданное число меньше. {hint}")

import pytest
from game import (
    generate_secret_number,
    check_guess,
    validate_guess,
    calculate_optimal_attempts,
    get_hint,
    play_round,
)


# ---------- generate_secret_number ----------

def test_generate_secret_number_in_range():
    for _ in range(200):
        n = generate_secret_number(1, 100)
        assert 1 <= n <= 100


def test_generate_secret_number_narrow_range():
    results = {generate_secret_number(1, 2) for _ in range(50)}
    assert results.issubset({1, 2})


def test_generate_secret_number_custom_range():
    for _ in range(50):
        n = generate_secret_number(50, 200)
        assert 50 <= n <= 200


def test_generate_secret_number_invalid_range_reversed():
    with pytest.raises(ValueError):
        generate_secret_number(100, 1)


def test_generate_secret_number_invalid_range_equal():
    with pytest.raises(ValueError):
        generate_secret_number(5, 5)


# ---------- check_guess ----------

def test_check_guess_correct():
    assert check_guess(42, 42) == "correct"


def test_check_guess_too_low_returns_higher():
    assert check_guess(10, 50) == "higher"


def test_check_guess_too_high_returns_lower():
    assert check_guess(90, 50) == "lower"


def test_check_guess_boundary_min():
    assert check_guess(1, 1) == "correct"


def test_check_guess_boundary_max():
    assert check_guess(100, 100) == "correct"


def test_check_guess_type_error_string_guess():
    with pytest.raises(TypeError):
        check_guess("10", 50)


def test_check_guess_type_error_string_secret():
    with pytest.raises(TypeError):
        check_guess(10, "50")


def test_check_guess_type_error_bool_guess():
    with pytest.raises(TypeError):
        check_guess(True, 1)


def test_check_guess_type_error_none():
    with pytest.raises(TypeError):
        check_guess(None, 50)


# ---------- validate_guess ----------

def test_validate_guess_valid_middle():
    assert validate_guess("50", 1, 100) == 50


def test_validate_guess_boundary_min():
    assert validate_guess("1", 1, 100) == 1


def test_validate_guess_boundary_max():
    assert validate_guess("100", 1, 100) == 100


def test_validate_guess_not_a_number():
    with pytest.raises(ValueError):
        validate_guess("abc", 1, 100)


def test_validate_guess_empty_string():
    with pytest.raises(ValueError):
        validate_guess("", 1, 100)


def test_validate_guess_below_min():
    with pytest.raises(ValueError):
        validate_guess("0", 1, 100)


def test_validate_guess_above_max():
    with pytest.raises(ValueError):
        validate_guess("101", 1, 100)


def test_validate_guess_float_string():
    with pytest.raises(ValueError):
        validate_guess("3.14", 1, 100)


def test_validate_guess_none():
    with pytest.raises(ValueError):
        validate_guess(None, 1, 100)


def test_validate_guess_whitespace():
    with pytest.raises(ValueError):
        validate_guess("   ", 1, 100)


# ---------- calculate_optimal_attempts ----------

def test_calculate_optimal_attempts_100():
    assert calculate_optimal_attempts(1, 100) == 7


def test_calculate_optimal_attempts_50():
    assert calculate_optimal_attempts(1, 50) == 6


def test_calculate_optimal_attempts_invalid():
    with pytest.raises(ValueError):
        calculate_optimal_attempts(100, 1)


def test_calculate_optimal_attempts_equal():
    with pytest.raises(ValueError):
        calculate_optimal_attempts(5, 5)


# ---------- get_hint ----------

def test_get_hint_exact():
    hint = get_hint(50, 50, 1, 100)
    assert "Точное" in hint


def test_get_hint_very_hot():
    hint = get_hint(48, 50, 1, 100)
    assert "горячо" in hint.lower()


def test_get_hint_warm():
    hint = get_hint(30, 50, 1, 100)
    assert "Тепло" in hint


def test_get_hint_cool():
    hint = get_hint(20, 50, 1, 100)
    assert "Прохладно" in hint


def test_get_hint_cold():
    hint = get_hint(1, 100, 1, 100)
    assert "Холодно" in hint


# ---------- play_round ----------

def test_play_round_correct_first_try():
    inputs = iter(["50"])
    outputs = []
    attempts = play_round(50, 1, 100, input_func=lambda _: next(inputs), print_func=outputs.append)
    assert attempts == 1
    assert any("Правильно" in s for s in outputs)


def test_play_round_correct_after_multiple_tries():
    inputs = iter(["20", "70", "50"])
    outputs = []
    attempts = play_round(50, 1, 100, input_func=lambda _: next(inputs), print_func=outputs.append)
    assert attempts == 3


def test_play_round_invalid_input_not_counted():
    inputs = iter(["abc", "200", "50"])
    outputs = []
    attempts = play_round(50, 1, 100, input_func=lambda _: next(inputs), print_func=outputs.append)
    assert attempts == 1


def test_play_round_hint_direction_higher():
    inputs = iter(["10", "50"])
    outputs = []
    play_round(50, 1, 100, input_func=lambda _: next(inputs), print_func=outputs.append)
    assert any("больше" in s for s in outputs)


def test_play_round_hint_direction_lower():
    inputs = iter(["90", "50"])
    outputs = []
    play_round(50, 1, 100, input_func=lambda _: next(inputs), print_func=outputs.append)
    assert any("меньше" in s for s in outputs)


def test_play_round_error_message_on_invalid():
    inputs = iter(["xyz", "50"])
    outputs = []
    play_round(50, 1, 100, input_func=lambda _: next(inputs), print_func=outputs.append)
    assert any("Ошибка" in s for s in outputs)

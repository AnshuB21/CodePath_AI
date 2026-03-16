from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from logic_utils import check_guess, parse_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == ("Win", "Correct!")

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == ("Too High", "Too high. Go LOWER!")

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == ("Too Low", "Too low. Go HIGHER.")

def test_invalid_guess_input():
    # Non-numeric guess should return a stable invalid response tuple.
    result = check_guess("abc", 50)
    assert result == ("Invalid", "Invalid guess input.")


def test_parse_guess_accepts_negative_numbers():
    result = parse_guess("-5")
    assert result == (True, -5, None)


def test_check_guess_handles_negative_numbers_gracefully():
    result = check_guess(-5, 50)
    assert result == ("Too Low", "Too low. Go HIGHER.")


def test_parse_guess_truncates_decimal_input():
    result = parse_guess("10.7")
    assert result == (True, 10, None)


def test_check_guess_handles_decimal_input_after_parsing():
    ok, guess, err = parse_guess("10.7")
    assert (ok, err) == (True, None)
    assert check_guess(guess, 9) == ("Too High", "Too high. Go LOWER!")


def test_parse_guess_accepts_extremely_large_numbers():
    huge_number = "999999999999999999999999999999"
    result = parse_guess(huge_number)
    assert result == (True, int(huge_number), None)


def test_check_guess_handles_extremely_large_numbers_gracefully():
    huge_number = 999999999999999999999999999999
    result = check_guess(huge_number, 50)
    assert result == ("Too High", "Too high. Go LOWER!")

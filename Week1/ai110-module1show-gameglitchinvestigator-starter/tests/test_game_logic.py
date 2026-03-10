from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from logic_utils import check_guess

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

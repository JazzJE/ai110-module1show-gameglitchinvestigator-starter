from logic_utils import check_guess, parse_guess, update_score

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


def test_parse_guess_rejects_fractional_decimal():
    ok, value, err = parse_guess("12.5")
    assert ok is False
    assert value is None
    assert err == "Use a whole number."


def test_parse_guess_accepts_whole_decimal():
    ok, value, err = parse_guess("12.0")
    assert ok is True
    assert value == 12
    assert err is None


def test_update_score_win_first_attempt():
    score = update_score(current_score=0, outcome="Win", attempt_number=1)
    assert score == 100


def test_update_score_miss_penalty():
    score = update_score(current_score=20, outcome="Too High", attempt_number=3)
    assert score == 15

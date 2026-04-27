from ai_advisor import analyze_game_state, retrieve_context


def test_advisor_recommends_midpoint_on_fresh_state():
    analysis = analyze_game_state(rounds=[], low=1, high=100, attempts_left=8)
    assert analysis["status"] == "ready"
    assert analysis["recommended_guess"] == 50
    assert 0.0 < analysis["confidence"] <= 1.0


def test_advisor_respects_narrowed_bounds():
    rounds = [
        {"guess": 50, "outcome": "Too High"},
        {"guess": 25, "outcome": "Too Low"},
    ]
    analysis = analyze_game_state(rounds=rounds, low=1, high=100, attempts_left=6)

    assert analysis["status"] == "ready"
    assert analysis["bounds"] == (26, 49)
    assert analysis["recommended_guess"] == 37


def test_advisor_guardrail_on_conflicting_history():
    rounds = [
        {"guess": 30, "outcome": "Too Low"},
        {"guess": 25, "outcome": "Too High"},
    ]
    analysis = analyze_game_state(rounds=rounds, low=1, high=40, attempts_left=4)

    assert analysis["status"] == "guardrail"
    assert analysis["recommended_guess"] is None
    assert analysis["confidence"] == 0.0


def test_retrieve_context_returns_ranked_items():
    results = retrieve_context("midpoint bounds attempts", top_k=2)
    assert len(results) >= 1
    assert results[0]["score"] >= 1

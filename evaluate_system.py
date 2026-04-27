from ai_advisor import analyze_game_state


def run_advisor_evaluation():
    scenarios = [
        {
            "name": "fresh_game",
            "rounds": [],
            "low": 1,
            "high": 100,
            "attempts_left": 8,
            "expected_status": "ready",
            "expected_guess": 50,
        },
        {
            "name": "narrowed_bounds",
            "rounds": [
                {"guess": 50, "outcome": "Too High"},
                {"guess": 25, "outcome": "Too Low"},
            ],
            "low": 1,
            "high": 100,
            "attempts_left": 6,
            "expected_status": "ready",
            "expected_guess": 37,
        },
        {
            "name": "guardrail_conflict",
            "rounds": [
                {"guess": 30, "outcome": "Too Low"},
                {"guess": 25, "outcome": "Too High"},
            ],
            "low": 1,
            "high": 40,
            "attempts_left": 4,
            "expected_status": "guardrail",
            "expected_guess": None,
        },
    ]

    passed = 0
    confidences = []

    print("=== AI Advisor Reliability Evaluation ===")

    for scenario in scenarios:
        analysis = analyze_game_state(
            rounds=scenario["rounds"],
            low=scenario["low"],
            high=scenario["high"],
            attempts_left=scenario["attempts_left"],
        )

        status_ok = analysis["status"] == scenario["expected_status"]
        guess_ok = analysis["recommended_guess"] == scenario["expected_guess"]
        scenario_passed = status_ok and guess_ok

        if analysis["status"] == "ready":
            confidences.append(analysis["confidence"])

        if scenario_passed:
            passed += 1

        print(f"- {scenario['name']}: {'PASS' if scenario_passed else 'FAIL'}")
        print(
            f"  status={analysis['status']} guess={analysis['recommended_guess']} "
            f"confidence={analysis.get('confidence', 0.0)}"
        )

    total = len(scenarios)
    avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0

    print("\n=== Summary ===")
    print(f"Passed: {passed}/{total}")
    print(f"Average confidence (ready scenarios): {avg_confidence:.2f}")


if __name__ == "__main__":
    run_advisor_evaluation()

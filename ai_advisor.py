import re
from typing import Dict, List, Tuple

KNOWLEDGE_BASE = [
    {
        "id": "bounds-first",
        "text": "Track a lower and upper bound from past hints. Ignore guesses outside those bounds.",
        "tags": ["bounds", "hints", "range", "consistency"],
    },
    {
        "id": "binary-midpoint",
        "text": "Use the midpoint of the current candidate range to minimize worst-case attempts.",
        "tags": ["strategy", "midpoint", "binary", "attempts"],
    },
    {
        "id": "late-game",
        "text": "When attempts are low, prioritize information gain. Midpoint guesses are safer than random picks.",
        "tags": ["attempts", "confidence", "risk", "late"],
    },
    {
        "id": "guardrails",
        "text": "If historical hints conflict, stop and reset the game state instead of giving a risky recommendation.",
        "tags": ["guardrails", "safety", "reset", "conflict"],
    },
]


def _tokenize(text: str) -> List[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def _compute_bounds(rounds: List[Dict], low: int, high: int) -> Tuple[int, int, bool]:
    lower = low
    upper = high

    for entry in rounds:
        guess = int(entry["guess"])
        outcome = entry["outcome"]

        if outcome == "Too Low":
            lower = max(lower, guess + 1)
        elif outcome == "Too High":
            upper = min(upper, guess - 1)
        elif outcome == "Win":
            lower = guess
            upper = guess

    return lower, upper, lower <= upper


def retrieve_context(query: str, top_k: int = 3) -> List[Dict]:
    query_tokens = set(_tokenize(query))
    scored = []

    for item in KNOWLEDGE_BASE:
        text_tokens = set(_tokenize(item["text"] + " " + " ".join(item["tags"])))
        overlap = len(query_tokens.intersection(text_tokens))
        if overlap > 0:
            scored.append(
                {
                    "id": item["id"],
                    "text": item["text"],
                    "score": overlap,
                }
            )

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]


def analyze_game_state(rounds: List[Dict], low: int, high: int, attempts_left: int) -> Dict:
    lower, upper, consistent = _compute_bounds(rounds, low, high)

    if not consistent:
        return {
            "status": "guardrail",
            "recommended_guess": None,
            "confidence": 0.0,
            "bounds": (lower, upper),
            "retrieved_context": retrieve_context("guardrails conflict reset state"),
            "reasoning_steps": [
                "Detected conflicting history from prior hints.",
                "Recommendation blocked by safety guardrail.",
                "Reset game to restore consistent state.",
            ],
        }

    if rounds and rounds[-1]["outcome"] == "Win":
        winning_guess = int(rounds[-1]["guess"])
        return {
            "status": "won",
            "recommended_guess": winning_guess,
            "confidence": 1.0,
            "bounds": (winning_guess, winning_guess),
            "retrieved_context": retrieve_context("win finished no next step"),
            "reasoning_steps": [
                "Game already solved.",
                "No further guess required.",
            ],
        }

    recommended = (lower + upper) // 2
    initial_range = max(1, high - low + 1)
    candidate_range = max(1, upper - lower + 1)

    range_reduction = 1.0 - (candidate_range / initial_range)
    confidence = 0.45 + (0.45 * range_reduction)
    if attempts_left <= 2:
        confidence += 0.05
    confidence = max(0.05, min(0.99, round(confidence, 2)))

    stage = "early" if len(rounds) <= 2 else "late"
    query = f"{stage} game bounds midpoint attempts {attempts_left}"

    return {
        "status": "ready",
        "recommended_guess": recommended,
        "confidence": confidence,
        "bounds": (lower, upper),
        "retrieved_context": retrieve_context(query),
        "reasoning_steps": [
            f"Computed candidate bounds as [{lower}, {upper}] from hint history.",
            "Selected midpoint strategy to reduce worst-case search depth.",
            f"Estimated confidence from remaining search space and attempts_left={attempts_left}.",
        ],
    }


def summarize_analysis(analysis: Dict) -> str:
    status = analysis.get("status")

    if status == "guardrail":
        return "AI advisor blocked a guess due to inconsistent history. Start a new game to recover."

    if status == "won":
        guess = analysis.get("recommended_guess")
        return f"AI advisor confirms the game is already solved at guess {guess}."

    guess = analysis.get("recommended_guess")
    confidence = analysis.get("confidence", 0.0)
    lower, upper = analysis.get("bounds", (None, None))

    return (
        f"AI advisor suggests {guess} within bounds [{lower}, {upper}] "
        f"with confidence {confidence:.2f}."
    )

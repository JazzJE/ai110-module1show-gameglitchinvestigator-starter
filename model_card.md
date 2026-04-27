# Model Card: AI Advisor for Game Glitch Investigator

## System Purpose
The AI component recommends the next guess in a number-guessing game and explains why it chose that guess. It uses retrieval from a small strategy knowledge base, computes bounds from prior outcomes, and returns a confidence score. The goal is to improve consistency and transparency over manual guesswork.

## Base Project and Evolution
Original project: Game Glitch Investigator (Module 1 debugging assignment). The original project focused on fixing game-state bugs and hint logic in a Streamlit guessing game. This final system extends that project with a retrieval-augmented AI advisor, confidence scoring, guardrails, and a reliability evaluation script.

## Inputs and Outputs
Inputs:
- Difficulty range and attempts remaining
- Historical guess/outcome records

Outputs:
- Recommended next guess
- Confidence score
- Retrieved context snippets
- Reasoning trace and guardrail state

## Limitations and Biases
- The knowledge base is small and hand-written, so recommendations reflect only those encoded strategies.
- Confidence is heuristic rather than statistically calibrated, so it may overstate certainty in edge cases.
- The advisor assumes truthful outcomes from the game logic; corrupted state can still reduce utility.

## Misuse Risks and Mitigations
Potential misuse:
- Treating confidence as guaranteed correctness.
- Reusing this advisor unchanged in unrelated decision domains.

Mitigations:
- Explicit guardrails block recommendations on contradictory history.
- The UI shows confidence as an estimate, not a guarantee.
- Reasoning steps and retrieved snippets are exposed for human verification.

## Reliability and Evaluation
Reliability methods:
- Unit tests for parsing, guessing, scoring, and advisor behavior.
- Scripted evaluation with predefined scenarios in `evaluate_system.py`.

Observed results (latest local run):
- All pytest tests pass.
- Evaluation scenarios pass with consistent status and recommendation behavior.

## Reflection on AI Collaboration
Helpful AI suggestion:
- AI suggested separating UI concerns from reusable logic functions, which improved testability and maintainability.

Flawed AI suggestion:
- Early AI-generated patterns mixed incompatible state assumptions, which caused inconsistent behavior. This was corrected by adding deterministic bounds logic and guardrail checks.

## Ethical Considerations
This system is low-risk because it operates in a game context, but it still demonstrates responsible AI patterns: transparency, confidence reporting, and fail-safe behavior when data is inconsistent. The same design principles are important for higher-stakes applications.

# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] Describe the game's purpose.
- [x] Detail which bugs you found.
- [x] Explain what fixes you applied.

### Game Purpose
This project is a number guessing game built with Streamlit where the player selects a difficulty, guesses a secret number, and receives feedback until they win or run out of attempts. The game tracks attempts, guess history, and score. The assignment focus is debugging AI-generated code, improving code structure, and validating repairs with automated tests.

### Bugs Found
1. Hint direction bug: when a guess was too high, the app told the user to go higher (and vice versa), which made gameplay misleading.
2. Secret type/state bug: the app sometimes converted the secret number to a string before comparison, causing inconsistent guess logic.
3. New game reset bug: pressing "New Game" did not reliably reset the full session state and could leave the app in a broken interaction state.
4. Attempts/flow bug: attempts handling could feel inconsistent, and invalid guesses could still interfere with expected game progression.

### Fixes Applied
1. Refactored core game logic into `logic_utils.py` by implementing `get_range_for_difficulty`, `parse_guess`, `check_guess`, and `update_score`.
2. Updated `app.py` to import and use logic helpers instead of keeping buggy duplicate logic in the UI layer.
3. Fixed hint logic so outcomes and guidance match correctly (`Too High -> Try lower`, `Too Low -> Try higher`).
4. Stabilized state management by resetting secret/attempts/score/status/history correctly on "New Game" and when difficulty changes.
5. Added safer input handling (empty input, non-number input, and fractional decimal rejection) and range checks.
6. Repaired and expanded tests to validate outcomes, parsing behavior, and scoring updates.

## 📸 Demo

- [ ] Insert screenshot: fixed winning game view (`streamlit run app.py`)
- [ ] Insert screenshot: `pytest` passing output (optional challenge evidence)

### Test Status
`pytest` result: **7 passed**

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]

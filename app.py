import random
import logging
import streamlit as st
from ai_advisor import analyze_game_state, summarize_analysis
from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)


logging.basicConfig(level=logging.INFO)


def reset_game_state(low: int, high: int, difficulty: str):
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.rounds = []
    st.session_state.ai_last = None
    st.session_state.difficulty = difficulty

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]
enable_ai_advisor = st.sidebar.checkbox("Enable AI advisor", value=True)
show_ai_trace = st.sidebar.checkbox("Show AI reasoning trace", value=False)

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

if "rounds" not in st.session_state:
    st.session_state.rounds = []

if "ai_last" not in st.session_state:
    st.session_state.ai_last = None

if "difficulty" not in st.session_state:
    st.session_state.difficulty = difficulty

if st.session_state.difficulty != difficulty:
    # Reset game state when difficulty changes to keep range/secret consistent.
    reset_game_state(low=low, high=high, difficulty=difficulty)

st.subheader("Make a guess")

st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)
    st.write("Rounds:", st.session_state.rounds)
    st.write("AI last analysis:", st.session_state.ai_last)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    ai_take_turn = st.button("AI Take Turn 🤖")

show_hint = st.checkbox("Show hint", value=True)


def show_ai_details(analysis: dict):
    st.info(summarize_analysis(analysis))
    if show_ai_trace:
        with st.expander("AI Reasoning Trace"):
            st.write("Reasoning steps:")
            for step in analysis.get("reasoning_steps", []):
                st.write(f"- {step}")
            st.write("Retrieved context:")
            for item in analysis.get("retrieved_context", []):
                st.write(f"- {item['id']}: {item['text']} (score={item['score']})")


def process_guess(guess_int: int, source: str):
    if guess_int < low or guess_int > high:
        st.session_state.history.append(guess_int)
        st.error(f"Guess must be between {low} and {high}.")
        return

    st.session_state.attempts += 1
    st.session_state.history.append(guess_int)

    outcome, message = check_guess(guess_int, st.session_state.secret)

    if show_hint:
        st.warning(message)

    st.session_state.score = update_score(
        current_score=st.session_state.score,
        outcome=outcome,
        attempt_number=st.session_state.attempts,
    )

    st.session_state.rounds.append(
        {
            "attempt": st.session_state.attempts,
            "guess": guess_int,
            "outcome": outcome,
            "source": source,
        }
    )

    attempts_left = max(0, attempt_limit - st.session_state.attempts)

    if enable_ai_advisor:
        analysis = analyze_game_state(
            rounds=st.session_state.rounds,
            low=low,
            high=high,
            attempts_left=attempts_left,
        )
        st.session_state.ai_last = analysis
        show_ai_details(analysis)

    logging.info(
        "round_end difficulty=%s source=%s guess=%s outcome=%s attempts=%s score=%s",
        difficulty,
        source,
        guess_int,
        outcome,
        st.session_state.attempts,
        st.session_state.score,
    )

    if outcome == "Win":
        st.balloons()
        st.session_state.status = "won"
        st.success(
            f"You won! The secret was {st.session_state.secret}. "
            f"Final score: {st.session_state.score}"
        )
    elif st.session_state.attempts >= attempt_limit:
        st.session_state.status = "lost"
        st.error(
            f"Out of attempts! "
            f"The secret was {st.session_state.secret}. "
            f"Score: {st.session_state.score}"
        )

if new_game:
    reset_game_state(low=low, high=high, difficulty=difficulty)
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        process_guess(guess_int=guess_int, source="human")

if ai_take_turn:
    if not enable_ai_advisor:
        st.warning("Enable AI advisor in the sidebar before using AI turn.")
    else:
        analysis = analyze_game_state(
            rounds=st.session_state.rounds,
            low=low,
            high=high,
            attempts_left=max(0, attempt_limit - st.session_state.attempts),
        )
        st.session_state.ai_last = analysis
        show_ai_details(analysis)

        ai_guess = analysis.get("recommended_guess")
        if ai_guess is None:
            st.error("AI advisor could not make a safe recommendation. Start a new game.")
        else:
            st.write(f"AI plays guess: {ai_guess}")
            process_guess(guess_int=int(ai_guess), source="ai")

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")

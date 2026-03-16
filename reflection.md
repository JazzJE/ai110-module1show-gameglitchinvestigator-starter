# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

The game looked polished at first because the UI rendered correctly and accepted guesses. After a few rounds, the behavior became inconsistent: hints felt wrong, resets were unreliable, and game state did not always behave as expected. The app gave the impression that it worked while hiding logic and state bugs underneath. This made it a good example of why "it runs" is not the same as "it is correct."

- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

  - The hints were backwards: when the guess was too high, the app said to go higher, and when too low, it said to go lower.
  - The code sometimes compared an integer guess against a string version of the secret number, which could cause misleading outcomes.
  - The "New Game" flow did not fully reset all state fields (attempts, history, score, status) in a stable way.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

I used GitHub Copilot in VS Code as my main pair-programming assistant. I used chat prompts for multi-file refactor suggestions and targeted inline questions when I wanted line-by-line clarification. I treated AI as a collaborator, not an autopilot, by validating every suggestion with tests and manual gameplay.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

One correct AI suggestion was to move core game logic (`parse_guess`, `check_guess`, `update_score`) into `logic_utils.py` and keep `app.py` focused on Streamlit UI/state. I verified this by running `pytest` after refactoring and confirming behavior in the app manually with multiple guess sequences. One misleading pattern from AI-generated starter code was converting the secret to a string on some attempts, which introduced inconsistent comparisons. I verified that this was wrong by tracing the branch logic and then removing mixed-type comparisons so `check_guess` always receives integers.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

I treated a bug as fixed only after two checks passed: automated tests and real gameplay behavior in Streamlit. For logic bugs, I confirmed expected outcomes directly in pytest assertions. For state bugs, I clicked through difficulty changes and "New Game" to ensure state reset was consistent. If either test or manual behavior failed, I considered the fix incomplete.

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I ran a test that checks a high guess (`60`) against secret `50` and confirms the outcome is `Too High`, plus a low guess case for `Too Low`. I also added parsing tests for decimal input (`12.5` rejected, `12.0` accepted) and score update tests for win and miss scenarios. These tests showed that the repaired logic was deterministic and no longer dependent on mixed types or UI state quirks. AI helped by proposing initial test structures, and I refined them to match the final function signatures and expected behavior.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

The secret issue came from state logic and inconsistent update patterns, not just random number generation itself. In Streamlit, every interaction reruns the script from top to bottom, so values must be stored in `st.session_state` if they should persist between clicks. I would explain reruns as "the app redraws on every interaction, but session_state is your memory." The final stability came from initializing `secret` once per game, resetting it only on explicit events (`New Game` or difficulty change), and keeping comparisons strictly int-to-int.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

One habit I want to keep is writing or updating tests immediately after each logic fix instead of waiting until the end. I also want to keep using focused prompts per bug (one glitch per chat thread) because it produces cleaner, more debuggable suggestions. Next time, I would ask AI for smaller patch-sized changes first and validate each patch before requesting the next one. This project changed my view of AI-generated code: it can accelerate implementation, but reliability still depends on human review, test coverage, and deliberate state reasoning.

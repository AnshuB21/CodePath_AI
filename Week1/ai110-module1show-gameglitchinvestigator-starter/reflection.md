# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

### Answer

a. The Show hint button is useless because it does nothing.
b. The new game button doesn't start a new game.
c. After hitting submit the checkbox doesn't get empty automatically and the guess in only retrived after another button is rendered.
d. When you give a wrong answer there is not information that pops up to say , the guess is wrong.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  ## Answer : Used chatgpt codex
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

## Answer : Ai suggested about the type error on the "Too high. Go higher" and "Too low, go lower"

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

## Answer: The local model on VS code intially suggested that the mistake wasn't in the check_guess function, but the how the submit button was handled when there was no pop ups for a wrong answer.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

## Answer: Crossed check in the webiste with different inputs, created the pytest with help of AI

## Answer:

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
  There were two pop up coming simulatneously initially when I manually tested. I worked fine after the update.

- Did AI help you design or understand any tests? How?
  Yes, it helped create the test cases and ran them.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.

## Answer: Because everything was re rendered initially with each click on any button. Because the secret was normal variable with "randint" which gives different random with each refresh.

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

## Answer: ---------Streamlit works by rerunning your whole app script every time the user does something, like clicking a button or typing in a box. That means regular variables get recreated each time, so anything you want to keep has to be stored somewhere more permanent. st.session_state is that place. It lets the app remember values between reruns, like a score, a secret number, or whether the game is over.

- What change did you make that finally gave the game a stable secret number?

## Answer: ---the secret is only created once with if "secret" not in st.session_state: and then stored in st.session_state.secret. That makes it persistent across reruns, so button clicks no longer replace

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or project?

## Answer: Create a new chat for each bug, create unit tests with the help of AI itself. Add comment when the problem exists for better fix and debug.

- This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?

## Answer: Will make a better folder structure and documentation.

- In one or two sentences, describe how this project changed the way you think about AI generated code.

## Answer: AI code and capability is changing faster than we can grasp.

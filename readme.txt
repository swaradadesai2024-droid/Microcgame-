RULES SUMMARY
- 9 blocks arranged 3×3 (Block 1 = bottom-left, Block 9 = top-right).
- There are 18 randomized multiple-choice questions (A/B/C).
- Correct answer -> move forward 1 block.
- Incorrect answer -> stay on block.
- Two wrong answers in a row:
  - If on Block 1 -> immediate game over (lose).
  - Otherwise -> move 1 block backward.
- Win by reaching Block 9.
- Lose if you run out of the 18 questions before reaching Block 9.

FILES
- main.py      → main Pygame program. Handles rendering + game logic.
- questions.py → contains the list of 18 questions and correct answers.
- readme.txt   → this file (setup + instructions).

REQUIREMENTS
- Python 3.8 or newer
- pygame (install via pip)

INSTALLATION
1. (optional) Create and activate a virtual environment:
   - python -m venv venv
   - Windows: venv\Scripts\activate
   - macOS/Linux: source venv/bin/activate
2. Install pygame:
   - pip install pygame

RUNNING THE GAME
Run from a terminal/command prompt (not VS Code’s debug console):
    python main.py


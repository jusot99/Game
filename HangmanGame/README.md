# Hangman Game with Pygame

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)

[![Pygame](https://img.shields.io/badge/Pygame-Library-green.svg)](https://www.pygame.org/)

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

This is a Hangman game implemented in Python using the Pygame library. The game includes features such as guessing letters, a hangman figure, win/lose conditions, and animation effects.

## Getting Started

### Prerequisites

- Python 3.x
- [Pygame library](https://www.pygame.org/)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/jusot99/Game/HangmanGame.git
   cd HangmanGame
   ```

2. **Install the required dependencies:**

   ```bash
   pip install pygame
   ```

### Running the Game

Run the following command to start the Hangman game:

```bash
python main.py
```

## Game Overview

- **Objective:** Guess the word correctly by inputting letters while avoiding exceeding the maximum attempts allowed.
- **Controls:**
  - Type a letter to guess.
  - Press 'r' to restart the game.
  - Press 'q' to quit the game.
  - Press 'a' to start an animation (feature-dependent).

## Code Structure

The code is organized as follows:

- **Initialization:**
  - Pygame and game variables are set up.
  - Word lists, fonts, and animation variables are defined.

- **Main Game Loop:**
  - Handles user input for guessing letters, restart, quit, and animation triggers.
  - Manages window resizing events.

- **Drawing the Hangman:**
  - Draws the hangman figure based on the number of incorrect attempts.

- **Drawing the Word:**
  - Displays the word with blanks and guessed letters.
  - Checks for win or lose conditions.

- **User Interaction:**
  - Displays information about guessed letters, attempts left, and the word database.

- **Word Database:**
  - Custom words can be added to the database for the game.

- **Animation:**
  - An optional animation can be triggered during specific events.

## Features

- Guess letters to uncover the word.
- Hangman figure drawn based on incorrect attempts.
- Win and lose conditions with appropriate messages.
- Restart and quit options.
- Animation effects during specific events.

## Customization

Feel free to customize the game by adjusting parameters such as window size, colors, or adding new features.

## License

This Hangman game is released under the [MIT License](LICENSE).

## Acknowledgments

- The Pygame community for providing a versatile library for game development.

Enjoy playing the Hangman game!

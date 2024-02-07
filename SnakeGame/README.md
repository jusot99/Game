# Snake Game with Pygame

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)

[![Pygame](https://img.shields.io/badge/Pygame-Library-green.svg)](https://www.pygame.org/)

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

This is a simple Snake game implemented in Python using the Pygame library. The game includes features such as snake movement, apple generation, collision detection, score tracking, and sound effects.

## Getting Started

### Prerequisites

- Python 3.x
- [Pygame library](https://www.pygame.org/)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/jusot99/Game/SnakeGame.git
   cd SnakeGame
   ```

2. **Install the required dependencies:**

   ```bash
   pip install pygame
   ```

### Running the Game

Run the following command to start the Snake game:

```bash
python main.py
```

## Game Overview

- **Objective:** Guide the snake to eat apples and grow longer while avoiding collisions with the borders and itself.
- **Controls:**
  - Arrow keys: Change the snake's direction
  - Space bar: Pause/Resume the game or restart after Game Over

## Code Structure

The code is organized as follows:

- **Initialization:**
  - Pygame and sound effects are initialized.
  - Sound effects are loaded.
  - Game parameters such as cell size, colors, and window dimensions are set.

- **Game Loop:**
  - The main game loop handles user input, snake movement, collisions, and drawing game elements on the screen.

- **Functions:**
  - `display_snake`: Draws the snake on the screen.
  - `display_game_over`: Displays the Game Over screen.

- **Event Handling:**
  - Handles key presses, window resizing, and quitting events.

- **Game Logic:**
  - Manages snake movement, collisions, apple generation, scoring, and level progression.

## Features

- Snake movement in four directions.
- Apple generation and collision detection.
- Score tracking, level progression, and timer display.
- Pause functionality.
- Game Over screen with score and restart option.
- Sound effects for snake movement, eating, and Game Over.

## Customization

Feel free to customize the game by adjusting parameters such as window size, colors, or adding new features.

## License

This Snake game is released under the [MIT License](LICENSE).

## Acknowledgments

- The Pygame community for providing a versatile library for game development.

Enjoy playing the Snake game!
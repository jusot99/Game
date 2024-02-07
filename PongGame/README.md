# Pong Game with Pygame

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)

[![Pygame](https://img.shields.io/badge/Pygame-Library-green.svg)](https://www.pygame.org/)

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

This is a classic Pong game implemented in Python using the Pygame library. The game includes features such as player controls, computer opponent, ball movement, collisions, scores, and multiplayer support.

## Getting Started

### Prerequisites

- Python 3.x
- [Pygame library](https://www.pygame.org/)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/jusot99/Game/PongGame.git
   cd PongGame
   ```

2. **Install the required dependencies:**

   ```bash
   pip install pygame
   ```

### Running the Game

Run the following command to start the Pong game:

```bash
python main.py
```

To run the server for multiplayer mode:

```bash
python server.py
```

## Game Overview

- **Objective:** Score more points than the opponent by hitting the ball past their paddle.
- **Controls:**
  - Player 1: Use the UP and DOWN arrow keys to move the paddle.
  - Player 2 (in multiplayer mode): Connect to the server and control the second paddle.
  - Computer Opponent (in single-player mode): Automatically moves to track the ball.

## Code Structure

The project consists of two main files:

- **server.py:** Manages the Pong game server, communication with clients, and game state updates.
- **main.py:** Implements the Pong game logic, including player controls, ball movement, collisions, and rendering.

## Features

- Player controls for paddle movement.
- Computer opponent in single-player mode.
- Multiplayer mode with a server handling communication.
- Ball movement, collisions, and scoring.
- Sound effects for paddle hits and goals.

## Customization

Feel free to customize the game by adjusting parameters such as window size, colors, or adding new features.

## License

This Pong game is released under the [MIT License](LICENSE).

## Acknowledgments

- The Pygame community for providing a versatile library for game development.

Enjoy playing the Pong game!

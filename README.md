
# Snake Game with Power-Ups

This project is a classic Snake game built using Python and the Tkinter library. It includes additional features such as power-ups and level progression, adding a modern twist to the traditional gameplay. The code is organized into separate classes to enhance readability and maintainability.

## Features

- **Classic Snake Mechanics**: The player controls the snake, which grows in length by consuming food.
- **Score and Level Tracking**: Players earn points by consuming food, with levels that increase difficulty.
- **Power-Ups**: Collecting power-ups grants temporary invincibility, allowing the snake to pass through itself and walls without dying.
- **Pause Functionality**: Pause and resume the game at any time by pressing `P`.
- **Game Over Screen**: When the snake collides with itself or the boundary, a game-over screen appears with options to restart or quit.
- **Dynamic Difficulty**: Game speed increases as levels advance, making it progressively challenging.

---

## Code Structure

The code is divided into classes for modularity and clarity, with specific sections for game constants, state management, and utility functions.

### Constants
The following constants are defined to control the game window and appearance:
- `GAME_WIDTH`, `GAME_HEIGHT`: Dimensions of the game canvas.
- `INITIAL_SPEED`: Starting speed of the snake.
- `SPACE_SIZE`: Size of each unit (square) on the game grid.
- `SNAKE_COLOR`, `FOOD_COLOR`, `POWERUP_COLOR`, etc.: Color settings for game elements.

### Game State Variables
Global variables track the state of the game:
- `score`, `level`: Track the player's score and current level.
- `direction`: Stores the current direction of the snake's movement.
- `game_paused`, `game_over_flag`: Boolean flags to manage pause and game-over states.
- `invincibility`: Tracks whether the snake is temporarily invincible.

### Classes

#### `Snake`
Handles the snake's movement, color, and collision detection. Key methods include:
- `move()`: Updates the position of the snake based on the current direction.
- `get_color()`: Returns the snake's color based on invincibility status.
- `check_collision()`: Checks if the snake has collided with itself or the boundary.

#### `Food`
Manages the food on the canvas, including generation at random positions. It includes:
- `generate_food()`: Spawns a food item at a random location on the grid.

#### `PowerUp`
Controls power-up behavior, including visibility and flickering effects. Key methods:
- `spawn()`: Generates a power-up at a random location.
- `flicker()`: Toggles the visibility of the power-up periodically.

### Core Functions

- **`food_eaten()`**: Checks if the snake's head has reached the food. Increases the score, updates levels, and initiates power-up spawning every 5 points.
- **`increase_difficulty()`**: Reduces the game speed with each level, increasing difficulty.
- **`check_powerup_collision()`**: Determines if the snake has collected a power-up, enabling invincibility.
- **`next_turn()`**: Controls the main game loop, moving the snake and checking for collisions.
- **`show_pause_screen()` and `show_game_over()`**: Display messages for paused or game-over states.
- **`restart_game()`**: Resets the game state and restarts gameplay.

### Controls
- **Arrow Keys**: Control the direction of the snake.
- **`P` Key**: Toggles pause/resume.

---

## How to Run

1. **Ensure Python is installed** on your system.
2. **Install Tkinter** if not already installed (included by default in most Python distributions).
3. **Run the game**:
   ```bash
   python snake_game_with_powerups.py
   ```

## Gameplay Mechanics

- **Score and Levels**: Each food item increases the score by 1. Every 5 points, the level increases, making the game faster.
- **Power-Ups**: Power-ups appear occasionally, flickering to grab attention. When collected, they grant temporary invincibility, allowing the snake to move through itself and walls without triggering a game over.
- **Game Over**: The game ends if the snake collides with itself or the boundary (when not invincible).


Enjoy the game!

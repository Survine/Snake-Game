from tkinter import *
import random

# Constants
GAME_WIDTH = 700
GAME_HEIGHT = 700
INITIAL_SPEED = 100
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "green"
FOOD_COLOR = "red"
POWERUP_COLOR = "blue"  # Blue color for power-up food
BACKGROUND_COLOR = "black"

# Initialize global variables for game state
score = 0
direction = 'down'
game_paused = False
invincibility = False
level = 1

# Snake class
class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        # Initialize snake at the starting position
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        # Draw each part of the snake on the canvas
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

# Food class
class Food:
    def __init__(self):
        self.x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        self.y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [self.x, self.y]
        canvas.create_oval(self.x, self.y, self.x + SPACE_SIZE, self.y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

# Power-Up class for special blue food that grants invincibility
class PowerUp:
    def __init__(self):
        self.x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        self.y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [self.x, self.y]
        canvas.create_oval(self.x, self.y, self.x + SPACE_SIZE, self.y + SPACE_SIZE, fill=POWERUP_COLOR, tag="powerup")

def next_turn(snake, food, powerup):
    global score, invincibility, INITIAL_SPEED, level

    if game_paused:
        return  # Skip turn if the game is paused

    # Get snake's current head position
    x, y = snake.coordinates[0]

    # Move the snake in the current direction
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    # Update snake coordinates
    snake.coordinates.insert(0, [x, y])
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    # Check for collision with regular food
    if x == food.coordinates[0] and y == food.coordinates[1]:
        score += 1
        label.config(text="Score: {}".format(score))
        canvas.delete("food")
        food = Food()

    # Check for collision with power-up
    elif powerup and x == powerup.coordinates[0] and y == powerup.coordinates[1]:
        invincibility = True
        canvas.delete("powerup")
        # Power-up effect lasts for 5 seconds
        window.after(5000, end_invincibility)  # End invincibility after 5 seconds
        powerup = None

    else:
        # Remove last part of the snake's tail if no food or power-up was eaten
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    # Check collision with walls or itself, unless invincible
    if not invincibility and check_collision(snake):
        game_over()
    else:
        # Level progression logic (increase difficulty every 5 points)
        if score > 0 and score % 5 == 0:
            level = (score // 5) + 1
            INITIAL_SPEED = max(50, INITIAL_SPEED - 10 * level)  # Increase speed
            spawn_powerup()  # Spawn a new power-up periodically

        # Continue the game loop
        window.after(INITIAL_SPEED, next_turn, snake, food, powerup)

def change_direction(new_direction):
    global direction

    # Prevent reversing direction
    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction

def check_collision(snake):
    x, y = snake.coordinates[0]

    # Check for collision with walls
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True

    # Check for collision with itself
    for part in snake.coordinates[1:]:
        if x == part[0] and y == part[1]:
            return True
    return False

def game_over():
    canvas.delete(ALL)
    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2, text="Game Over", font=("consolas", 50), fill="red")

def toggle_pause():
    global game_paused
    game_paused = not game_paused
    if not game_paused:
        next_turn(snake, food, powerup)  # Resume game if unpaused

def spawn_powerup():
    global powerup
    # Remove old powerup if it exists and spawn a new one
    canvas.delete("powerup")
    powerup = PowerUp()

def end_invincibility():
    global invincibility
    invincibility = False

# Set up the game window
window = Tk()
window.title("Snake Game with Power-Ups")
window.resizable(False, False)

# Initialize score label
label = Label(window, text="Score: {}".format(score), font=("consolas", 40))
label.pack()

# Create game canvas
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

# Center the game window on the screen
window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Bind arrow keys for movement and P key for pause/resume
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))
window.bind('<p>', lambda event: toggle_pause())

# Initialize game objects
snake = Snake()
food = Food()
powerup = None

# Start the game loop
next_turn(snake, food, powerup)

# Run the main event loop
window.mainloop()

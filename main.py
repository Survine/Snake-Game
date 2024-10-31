from tkinter import *
import random

# Constants
GAME_WIDTH = 700
GAME_HEIGHT = 700
INITIAL_SPEED = 100
SPACE_SIZE = 25
SNAKE_INITIAL_LENGTH = 3
SNAKE_COLOR = "green"
INVINCIBLE_SNAKE_COLOR = "yellow"
FOOD_COLOR = "red"
POWERUP_COLOR = "blue"
BACKGROUND_COLOR = "black"

# Game state variables
score = 0
direction = 'down'
game_paused = False
game_over_flag = False
invincibility = False
level = 1
powerup_timer = None
powerup_flicker_timer = None
powerup_visible = True

# Snake class
class Snake:
    def __init__(self):
        self.body = [[0, 0] for _ in range(SNAKE_INITIAL_LENGTH)]
        self.squares = []
        for x, y in self.body:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

    def move(self):
        global direction
        x, y = self.body[0]

        if direction == 'up':
            y -= SPACE_SIZE
        elif direction == 'down':
            y += SPACE_SIZE
        elif direction == 'left':
            x -= SPACE_SIZE
        elif direction == 'right':
            x += SPACE_SIZE

        self.body.insert(0, [x, y])
        new_square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=self.get_color())
        self.squares.insert(0, new_square)

        if not food_eaten():
            self.body.pop()
            canvas.delete(self.squares[-1])
            self.squares.pop()

    def get_color(self):
        return INVINCIBLE_SNAKE_COLOR if invincibility else SNAKE_COLOR

    def update_color(self):
        for square in self.squares:
            canvas.itemconfig(square, fill=self.get_color())

    def check_collision(self):
        head_x, head_y = self.body[0]
        if head_x < 0 or head_x >= GAME_WIDTH or head_y < 0 or head_y >= GAME_HEIGHT:
            return True
        for segment in self.body[1:]:
            if head_x == segment[0] and head_y == segment[1]:
                return True
        return False

# Food class
class Food:
    def __init__(self):
        self.generate_food()

    def generate_food(self):
        self.x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        self.y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        canvas.create_oval(self.x, self.y, self.x + SPACE_SIZE, self.y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

# Power-Up class with flicker effect
class PowerUp:
    def __init__(self):
        self.coordinates = self.spawn()
        self.powerup_id = canvas.create_oval(self.coordinates[0], self.coordinates[1],
                                             self.coordinates[0] + SPACE_SIZE, self.coordinates[1] + SPACE_SIZE,
                                             fill=POWERUP_COLOR, tag="powerup")
        self.flicker()

    def spawn(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        return [x, y]

    def flicker(self):
        global powerup_flicker_timer, powerup_visible
        if powerup_visible:
            canvas.itemconfig(self.powerup_id, state='hidden')
        else:
            canvas.itemconfig(self.powerup_id, state='normal')
        powerup_visible = not powerup_visible
        powerup_flicker_timer = window.after(500, self.flicker)

def food_eaten():
    global score, level
    if snake.body[0] == [food.x, food.y]:
        score += 1
        level = score // 5 + 1
        label.config(text=f"Score: {score}")
        canvas.delete("food")
        food.generate_food()
        if score % 5 == 0:
            increase_difficulty()
            if powerup_timer is None:
                spawn_powerup()
        return True
    return False

def increase_difficulty():
    global INITIAL_SPEED
    INITIAL_SPEED = max(50, INITIAL_SPEED - 5 * level)

def spawn_powerup():
    global powerup, powerup_timer
    powerup = PowerUp()
    powerup_timer = window.after(5000, remove_powerup)

def remove_powerup():
    global powerup, powerup_timer, powerup_flicker_timer
    if powerup_flicker_timer:
        window.after_cancel(powerup_flicker_timer)
    canvas.delete("powerup")
    powerup = None
    powerup_timer = None

def check_powerup_collision():
    global invincibility
    if powerup and snake.body[0] == powerup.coordinates:
        invincibility = True
        remove_powerup()
        snake.update_color()
        window.after(5000, end_invincibility)

def end_invincibility():
    global invincibility
    invincibility = False
    snake.update_color()

def next_turn():
    if game_paused or game_over_flag:
        return
    snake.move()
    if snake.check_collision() and not invincibility:
        show_game_over()
        return
    check_powerup_collision()
    window.after(INITIAL_SPEED, next_turn)

def change_direction(new_direction):
    global direction
    if (new_direction == 'left' and direction != 'right') or \
       (new_direction == 'right' and direction != 'left') or \
       (new_direction == 'up' and direction != 'down') or \
       (new_direction == 'down' and direction != 'up'):
        direction = new_direction

def toggle_pause():
    global game_paused
    game_paused = not game_paused
    if game_paused:
        show_pause_screen()
    else:
        hide_pause_screen()
        next_turn()

def show_pause_screen():
    global pause_text
    pause_text = canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2, text="Game Paused", font=("consolas", 40), fill="white")

def hide_pause_screen():
    global pause_text
    if pause_text:
        canvas.delete(pause_text)

def show_game_over():
    global game_over_flag, game_over_text, restart_button, quit_button
    game_over_flag = True
    game_over_text = canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 3, text="Game Over", font=("consolas", 50), fill="red")
    restart_button = Button(window, text="Restart", font=("consolas", 20), command=restart_game)
    restart_button.place(x=GAME_WIDTH / 2 - 50, y=GAME_HEIGHT / 2)
    quit_button = Button(window, text="Quit", font=("consolas", 20), command=window.quit)
    quit_button.place(x=GAME_WIDTH / 2 - 50, y=GAME_HEIGHT / 2 + 60)

def hide_game_over_screen():
    global game_over_flag, game_over_text, restart_button, quit_button
    game_over_flag = False
    canvas.delete(game_over_text)
    restart_button.destroy()
    quit_button.destroy()

def restart_game():
    global score, direction, invincibility, level
    hide_game_over_screen()
    score = 0
    direction = 'down'
    invincibility = False
    level = 1
    label.config(text="Score: {}".format(score))
    canvas.delete("snake")
    canvas.delete("food")
    canvas.delete("powerup")
    snake.__init__()
    food.generate_food()
    next_turn()

def game_over():
    canvas.delete(ALL)
    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2, text="Game Over", font=("consolas", 50), fill="red")

# Setup game window
window = Tk()
window.title("Snake Game with Power-Ups")
window.resizable(False, False)

label = Label(window, text="Score: {}".format(score), font=("consolas", 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

# Center the window
window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Bind controls
window.bind('<Left>', lambda _: change_direction('left'))
window.bind('<Right>', lambda _: change_direction('right'))
window.bind('<Up>', lambda _: change_direction('up'))
window.bind('<Down>', lambda _: change_direction('down'))
window.bind('<p>', lambda _: toggle_pause())

# Game objects
snake = Snake()
food = Food()
powerup = None

# Start game loop
next_turn()
window.mainloop()

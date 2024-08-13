from tkinter import *
import random
import time

GAME_WIDTH = 1000
GAME_HEIGHT = 600
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#FFFFFF"
FOOD_COLOR = "#FF0000"
OBSTACLE_COLOR = "#000000"
BACKGROUND_COLOR = "#00FF00"
INITIAL_SPEED = 150
LEVEL_UP_SPEED = 10


class Snake:

    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)


class Food:

    def __init__(self):
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")


class Obstacle:

    def __init__(self):
        self.coordinates = []
        for _ in range(5):
            x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
            y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
            self.coordinates.append([x, y])
            canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=OBSTACLE_COLOR, tag="obstacle")


def next_turn(snake, food, obstacles):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food = Food()
        check_level_up()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake, obstacles):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food, obstacles)


def change_direction(new_direction):
    global direction
    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction


def check_collisions(snake, obstacles):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    for obstacle in obstacles.coordinates:
        if x == obstacle[0] and y == obstacle[1]:
            return True

    return False


def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2,
                       font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")
    global high_score
    if score > high_score:
        high_score = score
        canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2 + 50,
                           font=('consolas', 40), text="New High Score: {}".format(high_score), fill="yellow", tag="highscore")
    restart_button.config(state=NORMAL)


def restart_game():
    global snake, food, obstacles, score, direction, SPEED
    canvas.delete(ALL)
    snake = Snake()
    food = Food()
    obstacles = Obstacle()
    score = 0
    direction = 'down'
    SPEED = INITIAL_SPEED
    label.config(text="Score: {}".format(score))
    next_turn(snake, food, obstacles)
    restart_button.config(state=DISABLED)


def check_level_up():
    global SPEED
    if score % 5 == 0:
        SPEED -= LEVEL_UP_SPEED


def pause_game(event):
    global is_paused
    is_paused = not is_paused
    if is_paused:
        canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2,
                           font=('consolas', 50), text="PAUSED", fill="white", tag="paused")
    else:
        canvas.delete("paused")
        next_turn(snake, food, obstacles)


window = Tk()
window.title("Advanced Snake Game")
window.resizable(False, False)

score = 0
high_score = 0
direction = 'down'
is_paused = False
SPEED = INITIAL_SPEED

label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

restart_button = Button(window, text="Restart", font=('consolas', 20), command=restart_game, state=DISABLED)
restart_button.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))
window.bind('<p>', pause_game)

snake = Snake()
food = Food()
obstacles = Obstacle()

next_turn(snake, food, obstacles)

window.mainloop()

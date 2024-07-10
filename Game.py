import turtle
import random2
import pygame
import time

pygame.mixer.init()

# Load sound effects
eat_sound = pygame.mixer.Sound("eat.wav")
collision_sound = pygame.mixer.Sound("collision.wav")
pause_sound = pygame.mixer.Sound("pause.wav")

w = 500
h = 500
food_size = 10
initial_delay = 100
paused = False
 
offsets = {
    "up": (0, 20),
    "down": (0, -20),
    "left": (-20, 0),
    "right": (20, 0)
}
 
def reset():
    global snake, snake_dir, food_position, pen, score, delay
    snake = [[0, 0], [0, 20], [0, 40], [0, 60], [0, 80]]
    snake_dir = "up"
    food_position = get_random_food_position()
    food.goto(food_position)
    score =0
    delay = initial_delay
    
    update_score()
    move_snake()
    
def update_score():
    pen.clear()
    pen.goto(0, h / 2 - 40)
    pen.write(f"Score: {score}", align="center", font=("Arial", 24, "normal"))
def move_snake():
    global snake_dir, delay, paused
    
    if paused:
        return
    
    new_head = snake[-1].copy()
    new_head[0] = snake[-1][0] + offsets[snake_dir][0]
    new_head[1] = snake[-1][1] + offsets[snake_dir][1]
 
     
    if new_head in snake[:-1]:
        pygame.mixer.Sound.play(collision_sound)
        time.sleep(1)
        reset()
    else:
        snake.append(new_head)
 
     
        if not food_collision():
            snake.pop(0)
 
 
        if snake[-1][0] > w / 2:
            snake[-1][0] -= w
        elif snake[-1][0] < - w / 2:
            snake[-1][0] += w
        elif snake[-1][1] > h / 2:
            snake[-1][1] -= h
        elif snake[-1][1] < -h / 2:
            snake[-1][1] += h
 
 
        pen.clearstamps()
 
         
        for segment in snake:
            pen.goto(segment[0], segment[1])
            pen.stamp()
        screen.update()
 
        turtle.ontimer(move_snake, delay)
 
def food_collision():
    global food_position, score, delay
    if get_distance(snake[-1], food_position) < 20:
        pygame.mixer.Sound.play(eat_sound)
        food_position = get_random_food_position()
        food.goto(food_position)
        score += 1
        delay = max(50, initial_delay - (score * 2))  # Increase speed as score increases
        update_score()
        return True
    return False
 
def get_random_food_position():
    x = random2.randint(- w / 2 + food_size, w / 2 - food_size)
    y = random2.randint(- h / 2 + food_size, h / 2 - food_size)
    return (x, y)
 
def get_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    distance = ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5
    return distance
def go_up():
    global snake_dir
    if snake_dir != "down":
        snake_dir = "up"
 
def go_right():
    global snake_dir
    if snake_dir != "left":
        snake_dir = "right"
 
def go_down():
    global snake_dir
    if snake_dir!= "up":
        snake_dir = "down"
 
def go_left():
    global snake_dir
    if snake_dir != "right":
        snake_dir = "left"
def toggle_pause():
    global paused
    paused = not paused
    if paused:
        pygame.mixer.Sound.play(pause_sound)
        pen.goto(0, 0)
        pen.write("Paused", align="center", font=("Arial", 36, "normal"))
    else:
        pen.clear()
        update_score()
        move_snake()

 
screen = turtle.Screen()
screen.setup(w, h)
screen.title("Snake")
screen.bgcolor("white")
screen.setup(500, 500)
screen.tracer(0)
 
 
pen = turtle.Turtle("square")
pen.penup()
 
 
food = turtle.Turtle()
food.shape("square")
food.color("red")
food.shapesize(food_size / 20)
food.penup()
 
 
screen.listen()
screen.onkey(go_up, "Up")
screen.onkey(go_right, "Right")
screen.onkey(go_down, "Down")
screen.onkey(go_left, "Left")
screen.onkey(toggle_pause, "space")
 
 
reset()
turtle.done()
from Fluffy import *
import random

window = init_pygame("test", 820, 620)
direction = "up"
SNK_SPEED = 12

total_score = 0

grid = []
for i in range(10, 600, 20):
    child = []
    for j in range(10, 800, 20):
        child.append(init_rect(j, i, 19, 19))

    grid.append(child)

location_of_y = int(len(grid) / 2)
location_of_x = int(len(grid[location_of_y]) / 2)
rect = grid[location_of_y][location_of_x]
snk = init_rect(rect.x, rect.y, 19, 19)

food_rect = random.choice(random.choice(grid))
food = init_rect(food_rect.x, food_rect.y, 19, 19)

count = 0
def snk_move():
    global _len, location_of_x, location_of_y, count, direction, food_rect, total_score

    if (is_key_pressed_input("up", DEFAULT_KEYS)): direction = "up"
    elif (is_key_pressed_input("down", DEFAULT_KEYS)): direction = "down"
    elif (is_key_pressed_input("left", DEFAULT_KEYS)): direction = "left"
    elif (is_key_pressed_input("right", DEFAULT_KEYS)): direction = "right"

    if (count == SNK_SPEED):
        if (direction == "up"):
            location_of_y = len(grid) - 1 if (location_of_y == 0) else location_of_y - 1

        elif (direction == "down"):
            location_of_y = 0 if (location_of_y == len(grid) - 1) else location_of_y + 1

        elif (direction == "left"):
            location_of_x = len(grid[location_of_y]) - 1 if (location_of_x == 0) else location_of_x - 1

        elif (direction == "right"):
            location_of_x = 0 if (location_of_x == len(grid[location_of_y]) - 1) else location_of_x + 1

        rect = grid[location_of_y][location_of_x]
        snk.y = rect.y
        snk.x = rect.x
        count = 0

    count += 1

    if (food_rect == snk):
        food_rect = random.choice(random.choice(grid))
        food.x = food_rect.x
        food.y = food_rect.y
        total_score += 1

while is_program_alive():
    clear_screen_pygame(window, (255, 255, 255))

    for i in range(len(grid)):
        for j in range(len(grid[i])): draw_rect(window, (0, 0, 0), grid[i][j])

    draw_rect(window, (255, 255, 255), snk)
    draw_rect(window, (255, 0, 0), food)
    snk_move()

    update_pygame()


print("##########################")
print("#          Score         #")
print(f"#            {total_score}\t\t #")
print("##########################")

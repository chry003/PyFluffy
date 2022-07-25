import pygame
import sys
from pygame.locals import *

#############################################
#               Constants                   #
#############################################
true = True
false = False
nil = None

fluffy_alive = true

DEFAULT_KEYS = {
            "right": {
                    "keystrokes": [K_RIGHT, K_d],
                    "keystrength": 1
                },
            "left": {
                    "keystrokes": [K_LEFT, K_a],
                    "keystrength": 1
                },
            "down": {
                    "keystrokes": [K_DOWN, K_s],
                    "keystrength": 1
                },
            "up": {
                    "keystrokes": [K_UP, K_w],
                    "keystrength": 1
                }
        }

#############################################
#               Basic setup                 #
#############################################

#####################
#       Error       #
#####################
def handle_err(message):
    print(f"[Error]: {message}")
    sys.exit(1);

#####################
#      Window       #
#####################
def init_pygame(title, width, height):
    # title: string
    # width: int
    # height: int

    # init pygame
    pygame.init()

    # create window
    window = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    pygame.display.set_caption(title)

    # return window
    return window

#####################
#      Update       #
#####################
def clear_screen_pygame(window, color):
    # window: pygame.surface
    # color: tuple[int]

    # it clears the screen of previous frame
    return window.fill(color)

def update_pygame():
    global fluffy_alive

    # check if user wants to quit the application
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fluffy_alive = false

    update = pygame.display.update()
    return update

def is_program_alive():
    return fluffy_alive

#############################################
#               Basic Input                 #
#############################################
def is_key_pressed_input(key, inputs):
    # key: string
    # inputs: dict

    get_pressed_keys = pygame.key.get_pressed()

    for keystroke in inputs[key]["keystrokes"]:
        if get_pressed_keys[keystroke]: return true

    return false

def get_action_strength_input(key, inputs):
    get_pressed_keys = pygame.key.get_pressed()
    actionStrength = 0

    for keystroke in inputs[key]["keystrokes"]:
        if get_pressed_keys[keystroke]: actionStrength = inputs[key]["keystrength"]

    return actionStrength

#############################################
#            Rects and Rendering            #
#############################################

#####################
#     Init Rect     #
#####################
def init_rect(position_x, position_y, width, height):
    # position_x: int
    # position_y: int
    # width: int
    # height: int

    rect = pygame.Rect(position_x, position_y, width, height)
    return rect

#####################
#     Draw Rect     #
#####################
def draw_rect(window, color, rect):
    # window: pygame.surface
    # color: tuple[int]
    # rect: pygame.Rect

    return pygame.draw.rect(window, color, rect)

#####################
#     Move Rect     #
#####################
def move_rect(inputs, rect, speed):

    flag = false
    for i in DEFAULT_KEYS.keys():
        if (i not in inputs.keys()): flag = true; break

    if (not flag):
        rect.x += (get_action_strength_input("right", inputs) - get_action_strength_input("left", inputs))
        rect.y += (get_action_strength_input("down", inputs) - get_action_strength_input("up", inputs))

    else: handle_err("cannot use <user_defined> inputs, not implemented yet.")

# run
if (__name__ == "__main__"):
    # Window
    window = init_pygame("Test", 800, 600)

    # Player Setup
    player = init_rect(100, 100, 100, 100)
    ball = init_rect(200, 200, 10, 10)

    grid = []
    for i in range(10, 500, 10):
        for j in range(10, 500, 10):
            grid.append(init_rect(j, i, 8, 8))

    while is_program_alive():
        clear_screen_pygame(window, (255, 255, 255))

        draw_rect(window, (0, 0, 0), player)
        move_rect(DEFAULT_KEYS, player, 100)

        for i in grid: draw_rect(window, (0, 0, 0), i)

        update_pygame()

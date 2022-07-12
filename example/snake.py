from Fluffy import *

window = init_pygame("test", 800, 600)
direction = "up"

grid = []
for i in range(10, 600, 20):
    child = []
    for j in range(10, 800, 20):
        child.append(init_rect(j, i, 19, 19))

    grid.append(child)

_len = len(grid) / 2
_x = grid[int( _len )]
_y = grid[grid.index(_x)][int( len( grid[grid.index(_x)] ) / 2 )]

snk = init_rect(_y.x, _y.y, 19, 19)

def snk_move():
    global _len, _x, _y

while true:
    clear_screen_pygame(window, (255, 255, 255))

    for i in range(len(grid)):
        for j in range(len(grid[i])): draw_rect(window, (0, 0, 0), grid[i][j])

    draw_rect(window, (255, 255, 255), snk)

    update_pygame()
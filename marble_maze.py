from sense_hat import SenseHat
from time import sleep

sh = SenseHat()
sh.clear()

# Variables--------------------

# Game status
game_over = False

# Colors
r = (255, 0, 0)
g = (0, 255, 0)
b = (0, 0, 0)
w = (255, 255, 255)

blank = (0, 0, 0)

# Marble position
x = 1
y = 1

# Maze walls
maze = [[r,r,r,r,r,r,r,r],
        [r,b,b,b,b,b,b,r],
        [r,r,r,b,r,b,b,r],
        [r,b,r,b,r,r,r,r],
        [r,b,b,b,b,b,b,r],
        [r,b,r,r,r,r,b,r],
        [r,b,b,r,g,b,b,r],
        [r,r,r,r,r,r,r,r]]

# Functions--------------------

def get_pi_orientation():
    o = sh.get_orientation()
    pitch = o["pitch"]
    roll = o["roll"]

    # Returning a tuple seems like the most idiomatic solution
    return (pitch, roll)

def move_marble(pitch, roll, x, y):
    new_x = x
    new_y = y

    # Transform x
    if 1 < pitch < 179 and x > 0:
        new_x -= 1
    elif 181 < pitch < 359 and x < 7:
        new_x += 1

    # Transform y
    if 1 < roll < 179 and y < 7:
        new_y += 1
    elif 181 < roll < 359 and y > 0:
        new_y -= 1
    
    # Using in-out here doesn't seem ideal 
    new_x, new_y = check_wall(x,y,new_x,new_y)

    return new_x, new_y

def check_wall(x, y, new_x, new_y):
    if maze[new_y][new_x] != r:
        return new_x, new_y
    elif maze[new_y][x] != r:
        return x, new_y
    elif maze[y][new_x] != r:
        return new_x, y
    else:
        return x, y

# Main-------------------------

while game_over == False:
    o = get_pi_orientation()
    x,y = move_marble(o[0], o[1], x, y)

    if maze[y][x] == g:
        game_over = True
        sh.set_rotation(180)
        sh.show_message("You Win!!!")

    maze[y][x] = w # Sets marble
    sh.set_pixels(sum(maze,[])) # Displays pixels

    sleep(0.1)
    maze[y][x] = blank # Clears previous marble position

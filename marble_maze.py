from sense_hat import SenseHat
from time import sleep
from recordclass import recordclass # For mutable named-tuple-like objects
import random

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

# Named tuples are immutable and structs aren't available in Python, so using recordclass,
# an external dependency installed with `$ pip install recordclass`
CoordinateObject = recordclass('CoordinateObject', 'x y')

# Marble position
marble = CoordinateObject(0, 0)

# Maze walls
maze = [[r,r,r,r,r,r,r,r],
        [r,b,b,b,b,b,b,r],
        [r,r,r,b,r,b,b,r],
        [r,b,r,b,r,r,r,r],
        [r,b,b,b,b,b,b,r],
        [r,b,r,r,r,r,b,r],
        [r,b,b,r,b,b,b,r],
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

# Sets marble at random location (could to use part of below func)
def set_marble():
    # The 'global' keyword is not needed here because what's changed is the _value_, 
    # not the underlying reference. Somewhat confusing...
    while maze[marble.y][marble.x] != b:
        marble.y = random.randint(1, 6)
        marble.x = random.randint(1, 6)
    
# Set goals at random location
def set_goals(number_of_goals):
    
    # The range is non-inclusive for the upper end,
    # so starting at 0 is a way to get the right number
    for i in range(0, number_of_goals):
        
        x = 0; y = 0
        while maze[y][x] != b:
            # The walls are at 0 and 7, so no need to even
            # bother generating a number with them 
            # randint is range-inclusive
            y = random.randint(1, 6) 
            x = random.randint(1, 6)

        # Pixel set after safe coordinate is found
        maze[y][x] = g

# Main-------------------------

# Initial setup
set_marble()
set_goals(3)

# Execution
while game_over == False:
    o = get_pi_orientation()
    marble.x, marble.y = move_marble(o[0], o[1], marble.x, marble.y)

    maze[marble.y][marble.x] = w # Sets marble
    sh.set_pixels(sum(maze,[])) # Displays pixels
    
    # This checks each list in the 2d maze list,
    # seeing if a green object appears
    if not any(g in inner_list for inner_list in maze):
        game_over = True
        sh.set_rotation(180)
        sh.show_message("You Win!!!")

    sleep(0.1)
    maze[marble.y][marble.x] = blank # Clears previous marble position


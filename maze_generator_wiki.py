import numpy
from numpy.random import random_integers as rand
import matplotlib.pyplot as pyplot
import matplotlib.animation as animation

class MazeCoords:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def maze(width=81, height=51, complexity=.75, density=.75):
    # Only odd shapes
    shape = ((height // 2) * 2 + 1, (width // 2) * 2 + 1)
    # Adjust complexity and density relative to maze size
    complexity = int(complexity * (5 * (shape[0] + shape[1]))) # number of components
    density    = int(density * ((shape[0] // 2) * (shape[1] // 2))) # size of components
    # Build actual maze
    Z = numpy.zeros(shape, dtype=numpy.float)
    # Fill borders
    Z[0, :] = Z[-1, :] = 1
    Z[:, 0] = Z[:, -1] = 1
    # Make aisles
    for i in range(density):
        x, y = rand(0, shape[1] // 2) * 2, rand(0, shape[0] // 2) * 2 # pick a random position
        Z[y, x] = 1
        for j in range(complexity):
            neighbours = []
            if x > 1:             neighbours.append((y, x - 2))
            if x < shape[1] - 2:  neighbours.append((y, x + 2))
            if y > 1:             neighbours.append((y - 2, x))
            if y < shape[0] - 2:  neighbours.append((y + 2, x))
            if len(neighbours):
                y_,x_ = neighbours[rand(0, len(neighbours) - 1)]
                if Z[y_, x_] == 0:
                    Z[y_, x_] = 1
                    Z[y_ + (y - y_) // 2, x_ + (x - x_) // 2] = 1
                    x, y = x_, y_    
    return Z

fig = pyplot.figure(figsize=(10, 5))
tmp = maze(80, 40)
original = tmp
im = pyplot.imshow(tmp, cmap=pyplot.cm.gist_yarg) # , cmap=pyplot.cm.gist_yarg, interpolation='nearest'
pyplot.colorbar()

def updatefig (frame):
    print(frame)
    if frame > 0 and frame < 80:
        tmp[frame,1] = 5.5
    im.set_array(tmp)
    return im,

def dfs (frame):
    global original
    global stack

    if not stack:
        print("list is empty")
        return im,
    
    value = 0.6

    last_val = stack.pop()
    g_x = last_val.x
    g_y = last_val.y
    
    print(len(stack), g_x, g_y, original[g_x, g_y], tmp[g_x, g_y])
    
    # up
    up_x_f = lambda: g_x - 1 if g_x > 0 else -1 
    up_x = up_x_f()
    up_y = g_y
    if (up_x >= 0) and (original[up_x, up_y] == 0) and (tmp[up_x, up_y] != value):
        tmp[up_x, up_y] = value
        #g_x = up_x
        #im.set_array(tmp)
        print("up")
        stack.append(MazeCoords(up_x, up_y))
        #return im,
    
    # down
    down_x_f = lambda: g_x + 1 if g_x < 80 else -1
    down_x = down_x_f()
    down_y = g_y
    if (down_x >= 0) and (original[down_x, down_y] == 0) and (tmp[down_x, down_y] != value):
        tmp[down_x, down_y] = value
        #g_x = down_x
        #im.set_array(tmp)
        print("down")
        stack.append(MazeCoords(down_x, down_y))
        #return im,
    
    # left
    left_x = g_x
    left_y_f = lambda: g_y - 1 if g_y > 0 else -1
    left_y = left_y_f()
    if (left_y >= 0) and (original[left_x, left_y] == 0) and (tmp[left_x, left_y] != value):
        tmp[left_x, left_y] = value
        #g_y = left_y
        #im.set_array(tmp)
        print("left")
        stack.append(MazeCoords(left_x, left_y))
        #return im,
    
    # right
    right_x = g_x
    right_y_f = lambda: g_y - 1 if g_y > 0 else -1
    right_y = right_y_f()
    if (right_y >= 0) and (original[right_x, right_y] == 0) and (tmp[right_x, right_y] != value):
        tmp[right_x, right_y] = value
        #g_y = right_y
        #im.set_array(tmp)
        print("right")
        stack.append(MazeCoords(right_x, right_y))
        #return im,

    #tmp[g_x, g_y] = value
    im.set_array(tmp)
    print("none", len(stack), up_x, up_y, down_x, down_y, left_x, left_y, right_x, right_y)
    return im,
    
g_x = 5
g_y = 5
stack = [MazeCoords(5,5)]

ani = animation.FuncAnimation(fig, dfs, interval=50, blit=True)

#pyplot.xticks([]), pyplot.yticks([])
pyplot.show()

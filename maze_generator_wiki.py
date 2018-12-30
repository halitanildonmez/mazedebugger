import numpy
from numpy.random import random_integers as rand
import matplotlib.pyplot as pyplot
import matplotlib.animation as animation

def maze(width=81, height=51, complexity=.75, density=.75):
    # Only odd shapes
    shape = ((height // 2) * 2 + 1, (width // 2) * 2 + 1)
    # Adjust complexity and density relative to maze size
    complexity = int(complexity * (5 * (shape[0] + shape[1]))) # number of components
    density    = int(density * ((shape[0] // 2) * (shape[1] // 2))) # size of components
    # Build actual maze
    Z = numpy.zeros(shape, dtype=numpy.int8)
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

    Z[5,5] = 5.5
    
    return Z

fig = pyplot.figure(figsize=(10, 5))
tmp = maze(80, 40)
im = pyplot.imshow(tmp, cmap=pyplot.cm.gist_yarg, interpolation='nearest')

def updatefig (frame):
    print(frame)
    if frame > 0 and frame < 80:
        tmp[frame,1] = 5.5
    im.set_array(tmp)
    return im,


def dfs (frame):
    global g_x
    global g_y
    # up
    if g_x > 0:
        g_x -= 1
    elif g_x < 40:
        g_x += 1
    
    if g_y > 0:
        g_y = g_y - 1
    elif g_y < 80:
        g_y = g_y + 1    
    
    print(g_x, g_y, tmp[g_x, g_y])
    
    if tmp[g_x, g_y] == 0:
        tmp[g_x, g_y] = 5.5
    
    im.set_array(tmp)
    return im,
    
g_x = 5
g_y = 5

ani = animation.FuncAnimation(fig, dfs, interval=50, blit=True)

#pyplot.xticks([]), pyplot.yticks([])
pyplot.show()

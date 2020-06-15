# Python code to implement Conway's Game Of Life 
import argparse 
import numpy as np 
import matplotlib.pyplot as plt  
import matplotlib.animation as animation 
  
# setting up the values for the grid 
sheep = 255
wolf = 120
dead = 0
vals = [sheep, wolf, dead]
current_time = 0
num = [[],[],[]]
  
def addRandom(N, grid):

    """returns a grid of NxN random values"""
    rand = np.random.choice(vals, int(N/4)*int(N/4), p=[0.08, 0.02, 0.9]).reshape(int(N/4), int(N/4))
    grid[int(3*N/8): int(3*N/8)+int(N/4), int(3*N/8): int(3*N/8)+int(N/4)] = rand

def addBar(i, j, grid):
    """adds a glider with top left cell at (i, j)"""
    bar = np.array([255, 255, 255])
    grid[i, j:j + 3] = bar

def add3Square(i, j, grid):
    """adds a glider with top left cell at (i, j)"""
    bar = np.array([[255, 255, 255], [255, 120, 255], [255, 120, 255]])
    grid[i:i+3, j:j+3] = bar

def addTriangle(i, j, grid):
    """adds a glider with top left cell at (i, j)"""
    triangle = np.array([[0, 255, 0], [0, 120, 255], [0, 255, 0]])
    grid[i:i+3, j:j+3] = triangle

def addAngle(i, j, grid):
    """adds a glider with top left cell at (i, j)"""
    angle = np.array([[0, 255, 0], [0, 255, 255], [0, 0, 0]])
    grid[i:i+3, j:j+3] = angle

def addGlider(i, j, grid):
    """adds a glider with top left cell at (i, j)"""
    glider = np.array([[0, 0, 255, 0],
                       [255, 120, 255, 0],
                       [255, 0, 0, 255],
                       [0, 255, 255, 120]])
    grid[i:i + 4, j:j + 4] = glider

def addGun(i, j, grid):
    """adds a glider with top left cell at (i, j)"""
    gun = np.array([[0, 0, 255, 0],
                    [0, 255, 255, 0],
                    [0, 0, 120, 255],
                    [0, 255, 255, 0],
                    [0, 0, 255, 0]])
    grid[i:i + 5, j:j + 4] = gun


def update(frameNum, img, grid, N, time):
    newGrid = grid.copy()
    global current_time
    total_sheep = 0
    total_wolf = 0
    for i in range(N):
        for j in range(N):
            # compute 8-neghbor sum
            Nsheep = 0
            Nwolf = 0
            for u in range(3):
                for v in range(3):
                    if 0 <= i - 1 + u <= N-1 and 0 <= j - 1 + v <= N - 1:
                        if grid[i - 1 + u, j - 1 + v] == sheep:
                            Nsheep += 1
                        elif grid[i - 1 + u, j - 1 + v] == wolf:
                            Nwolf += 1
            # apply Conway's rules
            if i == N-1 or j == N-1 or i == 0 or j == 0:
                if (i == 0 and j == 0) or (i == 0 and j == N-1) or(i == N-1 and j == 0) or (i == N-1 and j == N-1):
                    if grid[i, j] == sheep:
                        if Nsheep > 3 or Nsheep == 1 or current_time - time[i,j] >= 5:
                            newGrid[i, j] = dead
                        total_sheep += 1
                    elif grid[i, j] == wolf:
                        if Nsheep / Nwolf < 1 or current_time - time[i, j] >= 5:
                            newGrid[i, j] = dead
                        total_wolf += 1
                    else:
                        if Nsheep == 2:
                            newGrid[i,j] = sheep
                            time[i, j] = current_time
                        elif Nsheep >= 3:
                            newGrid[i, j] = wolf
                            time[i, j] = current_time
                else:
                    if grid[i, j] == sheep:
                        if Nsheep > 4 or Nsheep == 1 or current_time - time[i,j] >= 5:
                            newGrid[i, j] = dead
                        total_sheep += 1
                    elif grid[i, j] == wolf:
                        if Nsheep / Nwolf < 2 or current_time - time[i, j] >= 5:
                            newGrid[i, j] = dead
                        total_wolf += 1
                    else:
                        if Nsheep == 3:
                            newGrid[i,j] = sheep
                            time[i, j] = current_time
                        elif Nsheep >= 4:
                            newGrid[i, j] = wolf
                            time[i, j] = current_time
            else:
                if grid[i, j] == sheep:
                    if Nsheep > 5 or (Nwolf > 0 and Nsheep / Nwolf < 2) or Nsheep == 1 or current_time - time[i, j] >= 5:
                        newGrid[i, j] = dead
                    total_sheep += 1
                elif grid[i, j] == wolf:
                    if Nsheep / Nwolf < 3 or current_time - time[i, j] >= 5:
                        newGrid[i, j] = dead
                    total_wolf += 1
                else:
                    if Nsheep == 3:
                        newGrid[i, j] = sheep
                        time[i, j] = current_time
                    elif Nsheep >= 4:
                        newGrid[i, j] = wolf
                        time[i, j] = current_time
    num[0].append(total_sheep)
    num[1].append(total_wolf)
    num[2].append(total_wolf+total_sheep)
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    # print(grid)
    current_time += 1
    return img,


# main() function 
def main(N = 32, updateInterval = 1000, pattern=None):
  
    # check if "glider" demo flag is specified 
    if pattern == 'bar':
        grid = np.zeros(N*N).reshape(N, N) 
        addBar(int(N/2), int(N/2), grid)
    elif pattern == '3square':
        grid = np.zeros(N*N).reshape(N, N)
        add3Square(int(N/2), int(N/2), grid)
    elif pattern == 'triangle':
        grid = np.zeros(N*N).reshape(N, N)
        addTriangle(int(N/2), int(N/2), grid)
    elif pattern == 'glider':
        grid = np.zeros(N*N).reshape(N, N)
        addGlider(int(N/2), int(N/2), grid)
    elif pattern == 'gun':
        grid = np.zeros(N*N).reshape(N, N)
        addGun(int(N/2), int(N/2), grid)
    elif pattern == 'angle':
        grid = np.zeros(N*N).reshape(N, N)
        addAngle(int(N/2), int(N/2), grid)
    else:   # populate grid with random on/off -
            # more off than on
        grid = np.zeros(N * N).reshape(N, N)
        addRandom(N, grid)

    def init():
        return grid,

    time = np.zeros(N*N).reshape(N, N)
    # set up animation 
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')

    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, time,),
                                  frames=1, init_func=init,
                                  interval=updateInterval, 
                                  save_count=50, blit=False)
    plt.show()
    # ani.save('1.gif', fps=30, extra_args=['-vcodec', 'libx264'])
    plt.plot(num[0], label='sheep')
    plt.plot(num[1], label='wolf')
    plt.plot(num[2], label='total')
    plt.legend()
    plt.show()


# call main 
if __name__ == '__main__':
    main(N=64,updateInterval=300)
# 世界的模样
WORLD_H = 80
WORLD_W = 80
N = 1000
# 世界的规则
DEAD_CON = [0, 1, 4, 5, 6, 7, 8];  # 活着的部落，周围少于2个部落，或者周围多于3个部落，这个部落会死；
REVIVE_CON = [3, 4, 5, 6, 7, 8];  # 死了的部落，周围多于3个部落，这个部落会复活
KEEP_CON = [2, 3];  # 活着的部落，如果周围部落数为2或者3，这个部落会继续活着
NBH = [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1)];  # 近邻规则

import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
a = np.zeros((WORLD_H, WORLD_W))
a[40, 40] = 1
a[40, 41] = 1
a[40, 42] = 1
# a[40, 43] = 1
# a[40, 42] = 1

plt.ion()
for n in range(N):
    b = np.zeros((WORLD_H, WORLD_W))
    live = 0
    for i in range(WORLD_H):
        for j in range(WORLD_W):
            neighbors_alive = 0
            for neighbor in NBH:
                if 0 <= i + neighbor[0] < WORLD_H and 0 <= j + neighbor[1] < WORLD_W:
                    neighbors_alive += a[i + neighbor[0], j + neighbor[1]]
            if a[i, j] == 1 and neighbors_alive in DEAD_CON:
                b[i, j] = 0
            elif a[i, j] == 0 and neighbors_alive in REVIVE_CON:
                b[i, j] = 1
            else:
                b[i, j] = a[i, j]
    a = b
    print("Iter %d Live: %d" % (n, int(a.sum())) )
    ax.imshow(a)
    plt.pause(0.05)
    if n == N - 1:
        plt.close()
plt.ioff()
plt.show()

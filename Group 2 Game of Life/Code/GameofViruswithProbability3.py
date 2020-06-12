# 世界的模样
WORLD_H = 80
WORLD_W = 80
N = 50

# 人的模样
# Condition 0 健康 128 感染 255 死亡
# days 感染天数，感染天数大于14天，死亡，失去传染性
# probability
DIM = 3

# 世界的规则
NBH = [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1)];  # 近邻规则
PROB = 0.8

import numpy as np
import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
a = np.zeros((WORLD_H, WORLD_W, DIM))
a[40, 40, 0] = 128
a[:, :, 2] = np.random.random((WORLD_H, WORLD_W))
virus_alpha = 0
# ax.imshow(a[:, :, 0])
# plt.show()
plt.ion()
for n in range(N):
    a[:, :, 2] = np.random.random((WORLD_H, WORLD_W))
    b = np.zeros((WORLD_H, WORLD_W, DIM));
    for i in range(WORLD_H):
        for j in range(WORLD_W):
            if a[i, j, 0] == 0 and a[i, j, 2] > PROB:
                for neighbor in NBH:
                    if 0 <= i + neighbor[0] < WORLD_H and 0 <= j + neighbor[1] < WORLD_W:
                        if a[i + neighbor[0], j + neighbor[1], 0] == 128:
                            b[i, j, 0] = 128
                            b[i, j, 1] = 1
                            break
            elif a[i, j, 0] == 128:
                b[i, j, 1] = a[i, j, 1] + 1
                if b[i, j, 1] == 14:
                    b[i, j, 0] = 255
                else:
                    b[i, j, 0] = 128
            else:
                b[i, j, 0] = a[i, j, 0]
    a = b
    print("Day: %d PROB: %f Infected: %d Dead: %d Survivor: %d" % (
        n, PROB, sum(sum(a[:, :, 0] == 128)), sum(sum(a[:, :, 0] == 255)), sum(sum(a[:, :, 0] == 0))))
    ax.imshow(a[:, :, 0])
    plt.pause(0.01)
    if sum(sum(a[:, :, 0] == 128)) == WORLD_H * WORLD_W:
        print("Doomsday")
        plt.close()
        break
    #if n == N - 1:
    #    plt.close()
plt.ioff()
plt.show()

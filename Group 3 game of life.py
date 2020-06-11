# -*- coding: utf-8 -*-
import numpy as np
import matplotlib
from matplotlib import pyplot as plt


class Args:
    # 整个Game的参数
    n_rows, n_cols = (150, 150)
    epoch = 200

    # 关于病毒的参数
    theta = 25
    init_w = (30, 60)
    init_h = (75, 88)
    init_pnt = 0.005

    # 关于营养的参数
    delta = 0.5
    grow_consuming = 5
    sustenance_consuming = 3
    max_nutrient = 100

    # 关于绘图
    fig_size = (10, 4)
    pause = 0.2
    pass


class Virus:
    def __init__(self, n_rows: int, n_cols: int, theta: int = 3, convolve: callable = None):
        self.virus = self.init_virus(n_rows, n_cols)
        self.kernel = np.array([[0.125, 0.125, 0.125], [0.125, 0, 0.125], [0.125, 0.125, 0.125]])
        self.theta = theta
        self.convolve = convolve
        pass

    @staticmethod
    def init_virus(n_rows, n_cols):
        w, h = Args.init_w[1] - Args.init_w[0], Args.init_h[1] - Args.init_h[0]
        one = np.random.random(w * h).reshape((w, h))
        one[np.where(one > 1 - Args.init_pnt)] = 1
        one[np.where(one <= 1 - Args.init_pnt)] = 0
        virus = np.zeros((n_rows, n_cols))
        virus[Args.init_w[0]:Args.init_w[1], Args.init_h[0]:Args.init_h[1]] = one
        virus = virus.astype(np.int)
        return virus

    @property
    def crowing(self):
        avg = self.convolve(self.virus, self.kernel)
        c = np.sin(np.pi * avg)
        return c  # 0到1之间

    def next(self, now_nutrient: np.ndarray) -> np.ndarray:
        nxt = self.crowing * now_nutrient  # 0到10之间
        nxt = nxt > self.theta
        nxt = nxt + 0
        self.virus = nxt
        return nxt


class Nutrient:
    def __init__(self, n_rows: int, n_cols: int, delta: float = 0.5, growth: int = 3, sustenance: int = 1,
                 convolve: callable = None):
        self.nutrient = np.random.random(n_rows * n_cols).reshape((n_rows, n_cols)) * Args.max_nutrient
        self.delta = delta
        self.kernel = np.array([[1 / 20, 1 / 5, 1 / 20], [1 / 5, 0, 1 / 5], [1 / 20, 1 / 5, 1 / 20]])
        self.growth = growth
        self.sustenance = sustenance
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.convolve = convolve
        pass

    def next(self, now_virus: np.ndarray, next_virus: np.ndarray) -> np.ndarray:
        """
        n(t+1) = (1-delta) * n(t) + delta * average - eaten
        """
        term1 = (1 - self.delta) * self.nutrient

        average = self.convolve(self.nutrient, self.kernel)
        term2 = self.delta * average

        eaten = np.zeros((self.n_rows, self.n_cols))
        eaten[np.where((now_virus == 0) & (next_virus == 1))] = self.growth
        eaten[np.where((now_virus == 1) & (next_virus == 1))] = self.sustenance

        nxt = term1 + term2 - eaten
        nxt[np.where(nxt < 0)] = 0.0

        self.nutrient = nxt
        return nxt


class Game:
    def __init__(self):
        self.n_rows = Args.n_rows
        self.n_cols = Args.n_cols
        self.Virus = Virus(self.n_rows, self.n_cols, theta=Args.theta, convolve=self.convolve2d)
        self.Nutrient = Nutrient(self.n_rows, self.n_cols, delta=Args.delta, growth=Args.grow_consuming,
                                 sustenance=Args.sustenance_consuming, convolve=self.convolve2d)
        self.plotter = Plotter(fig_size=Args.fig_size, pause=Args.pause)
        pass

    @staticmethod
    def convolve2d(matrix: np.ndarray, kernel: np.ndarray) -> np.ndarray:
        rn, cn = matrix.shape
        nrn, ncn = rn + 2, cn + 2
        krn, kcn = kernel.shape
        new_matrix = np.zeros((nrn, ncn))
        new_matrix[1:-1, 1:-1] = matrix
        rstl = []
        for r in range(nrn - krn + 1):
            rst_row = []
            for c in range(ncn - kcn + 1):
                left = new_matrix[r: r + krn, c: c + kcn]
                rst = left * kernel
                rst = np.sum(rst)
                rst_row.append(rst)
            rstl.append(rst_row)
        return np.array(rstl)

    def run(self, steps: int = Args.epoch, show_img: bool = True):
        if show_img:
            # print('初始的营养矩阵：')
            # pprint(self.Nutrient.nt.round().astype(np.int).tolist())
            # print('初始的病毒：')
            # pprint(self.Virus.virus.tolist())

            self.plotter.plot(self.Nutrient.nutrient, self.Virus.virus, 0)

        # input('开始 [是/否]: ')
        for i in range(steps):
            # print('#' * 20, f'回合 {i + 1}', '#' * 20)
            now_virus = self.Virus.virus
            now_nutrient = self.Nutrient.nutrient

            new_virus = self.Virus.next(now_nutrient)
            new_nutrient = self.Nutrient.next(now_virus, new_virus)

            if show_img:
                # print('营养矩阵：')
                # pprint(new_nutrient.round().astype(np.int).tolist())
                # print('\n病毒矩阵：')
                # pprint(new_virus.tolist())

                self.plotter.plot(new_nutrient, new_virus, i + 1)

            if np.all(new_virus == 0):
                print('所有病毒都死亡了')
                # input()
                break
            # input('继续 [是/否]: ')
            # print()
        pass


class Plotter:
    def __init__(self, fig_size: tuple = (20, 10), pause: float = 0.1):
        matplotlib.use('Qt5Agg')
        plt.ion()
        self.fig = plt.figure(figsize=fig_size)
        self.subplot1 = self.fig.add_subplot(1, 2, 1)
        self.subplot2 = self.fig.add_subplot(1, 2, 2)

        self.pause = pause
        pass

    def show(self):
        plt.show()
        plt.pause(self.pause)
        pass

    def plot(self, nutrient: np.ndarray, virus: np.ndarray, round: int):
        self.subplot2.cla()
        plt.axis('off')

        axes = np.where(virus.T == 1)
        x, y = axes[0].tolist(), axes[1].tolist()
        if round:
            self.subplot1.scatter([round], [np.sum(virus)], marker='o', s=10)

        nt = nutrient.copy()
        nt = Args.max_nutrient - nt
        nt[-1, -1] = Args.max_nutrient
        self.subplot2.imshow(nt)
        self.subplot2.scatter(x, y, s=50 / Args.n_rows, c='w', marker=',')
        self.show()
        pass


if __name__ == '__main__':
    game = Game()
    game.run(show_img=True)

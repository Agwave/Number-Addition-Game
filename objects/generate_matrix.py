import copy
import numpy as np
import random

class Matrix(object):

    def __init__(self, n):
        self.n = n
        self.matrix = -np.ones((self.n, self.n))
        self.load = None
        self.generate()

    def generate(self):
        self.load = self._generate_road()
        self._generate_matrix()

    def _generate_road(self):
        n = copy.deepcopy(self.n)
        load_x = [0]
        load_y = [0]
        load_matrix = np.zeros((n, n))
        load_matrix[0, 0] = 1
        cur = [0, 0]

        while cur[0] != n-1 or cur[1] != n-1:
            next_direction = self._random_choice(load_matrix, cur)
            if next_direction is None:
                load_x.pop()
                load_y.pop()
                load_matrix[cur[0], cur[1]] = -1
                cur = [load_x[-1], load_y[-1]]
            else:
                cur = next_direction[:]
                load_x.append(cur[0])
                load_y.append(cur[1])
                load_matrix[cur[0], cur[1]] = 1

        load = []
        for i in range(len(load_x)):
            load.append([load_x[i], load_y[i]])

        return load

    def _random_choice(self, load_matrix, cur):
        n = copy.deepcopy(self.n)
        choice = []
        row, col = cur
        if row > 0 and load_matrix[row-1, col] == 0:
            choice.append([-1, 0])
        if row < n-1 and load_matrix[row+1, col] == 0:
            choice.append([1, 0])
        if col > 0 and load_matrix[row, col-1] == 0:
            choice.append([0, -1])
        if col < n-1 and load_matrix[row, col+1] == 0:
            choice.append([0, 1])

        if len(choice) > 0:
            c = random.choice(choice)
            cur[0] += c[0]
            cur[1] += c[1]
            return cur
        return None

    def _generate_matrix(self):
        first, second = random.randint(0, 9), random.randint(0, 9)
        last_last_num, last_num = first, second
        for i, (row, col) in enumerate(self.load):
            if i == 0:
                self.matrix[row, col] = last_last_num
            elif i == 1:
                self.matrix[row, col] = last_num
            else:
                cur_num = (last_last_num + last_num) % 10
                self.matrix[row, col] = cur_num
                last_last_num = last_num
                last_num = cur_num

        n = copy.deepcopy(self.n)
        for i in range(n):
            for j in range(n):
                if self.matrix[i, j] == -1:
                    self.matrix[i, j] = int(random.randint(0, 9))


if __name__ == '__main__':
    m = Matrix(10)
    print(m.matrix)
    print(m.load)

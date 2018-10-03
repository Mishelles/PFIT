import numpy as np
from scipy import special
from scipy import constants
from matplotlib import pyplot

FIRST_COLOR = 'green'
SECOND_COLOR = 'orange'


class Application:

    def __init__(self, input_data):
        try:
            self.eps = float(input_data['eps'])
            self.radius = float(input_data['radius'])
            self.power = int(input_data['power'])
            self.precision = 10 ** int(input_data['precision'])
            self.initial_frequency = float(input_data['initial_frequency']) * constants.pi
            self.max_root = int(input_data['max_root'])
        except KeyError:
            print("Неправильный формат входных данных!")
            exit(1)
        self.say_hello()

    def to_string(self):
        _str = 'EPS: {}\n'.format(self.eps)
        _str += 'РАДИУС: {}\n'.format(self.radius)
        _str += 'ТОЧНОСТЬ: {}\n'.format(self.precision)
        _str += 'КОЛИЧЕСТВО КРИВЫХ: {}\n'.format(self.max_root)
        _str += 'НАЧАЛЬНАЯ ЧАСТОТА: {} * {}\n'.format(self.initial_frequency, self.power)
        return _str

    def say_hello(self):
        print('***************')
        print('Приложение инициализировано следующими данными:')
        print(self.to_string())
        print('***************')

    def calculate_velocity(self, bessel, freq):
        x = self.radius ** 2 * freq ** 2
        y = bessel ** 2 * constants.c ** 2
        return np.sqrt(np.fabs(x / (self.eps * x - y)))

    def find_root(self, edges):
        x0 = edges[0] if (special.jv(0, edges[0]) * special.jvp(0, edges[0], 2) > 0) else edges[1]
        xn = x0 - special.jv(0, x0) / special.jvp(0, x0)

        while np.fabs(xn - x0) > self.precision:
            x0 = xn
            xn = x0 - special.jv(0, x0) / special.jvp(0, x0)

        return xn

    def sort_velocity(self, total):
        velocity = []
        for x in range(self.max_root):
            velocity.append([[], []])

        for item in total:
            for x in range(len(item[1])):
                velocity[x][0].append(item[0])
                velocity[x][1].append(item[1][x])
        return velocity

    def calculate(self):
        frequency = self.initial_frequency * self.power
        total = []
        votn = np.linspace(1 / np.sqrt(self.eps), 4 + 1 / self.eps, 1000)
        argument = None

        while True:
            try:
                argument = frequency / constants.c * np.sqrt(np.fabs(self.eps - 1 / votn ** 2)) * self.radius
            except Exception as e:
                pass

            y = special.jv(0, argument)
            edges = []
            root = 0
            for x in range(1, len(y)):
                if (y[x] * y[x - 1]) < 0:
                    root += 1
                    if argument[x - 1] < self.precision:
                        argument[x - 1] = 2
                    edges.append([argument[x - 1], argument[x]])
            if (root > 0) and (root <= self.max_root):
                answer = []
                for edge in edges:
                    answer.append(self.calculate_velocity(self.find_root(edge), frequency))
                total.append([frequency, answer])
            if root > self.max_root:
                break
            frequency += 0.1 * self.power

        points = self.sort_velocity(total)
        group = []
        for i in range(len(points)):
            group.append([[], []])
            for k in range(len(points[i][0]) - 1):
                group[i][1].append((points[i][0][k + 1] - points[i][0][k]) /
                                   (points[i][0][k + 1] / points[i][1][k + 1] - points[i][0][k] / points[i][1][k]))
                group[i][0].append(points[i][0][k])

        return points, group

    def draw_plot(self, points, group):
        figure = pyplot.gcf()
        figure.set_size_inches(1000, 800)
        figure.canvas.set_window_title('ИДЗ №1 - Фазовые кривые')
        figure.patch.set_facecolor('xkcd:mint green')

        pyplot.figtext(0, 0, self.to_string(), wrap=True, horizontalalignment='left', fontsize=9)

        # Первый график
        for x in range(self.max_root):
            pyplot.subplot(1, 3, 1)
            pyplot.plot(points[x][0], points[x][1], FIRST_COLOR)

        pyplot.xlabel('Частота')
        pyplot.ylabel('Относительная фазовая скорость')

        # Второй график
        for x in range(self.max_root):
            pyplot.subplot(1, 3, 2)
            pyplot.plot(points[x][0], points[x][1], FIRST_COLOR)

        for x in range(self.max_root):
            pyplot.subplot(1, 3, 2)
            pyplot.plot(group[x][0], group[x][1], SECOND_COLOR)

        pyplot.yscale('logit')
        pyplot.xlabel('Частота')
        pyplot.ylabel('Относительные фазовая и групповая скорости')

        # Третий график
        for x in range(self.max_root):
            pyplot.subplot(1, 3, 3)
            pyplot.plot(group[x][0], group[x][1], SECOND_COLOR)

        pyplot.xlabel('Частота')
        pyplot.ylabel('Относительная групповая скорость')

        pyplot.show()

    def start(self):
        print("Производятся вычисления...")
        points, group = self.calculate()
        self.draw_plot(points, group)

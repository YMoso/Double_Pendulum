import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

class Visualisation:
    def __init__(self, config, solution):
        self.length_1 = config['length_1']
        self.length_2 = config['length_2']
        self.interval = config['interval']
        self.solution = solution
        if config['plot']:
            self.plot_angles()
        if config['animate']:
            self.animate_pendulum()

    def plot_angles(self):
        t = self.solution.t
        theta1, theta2 = self.solution.y[0], self.solution.y[1]

        plt.plot(t, theta1, label='θ₁(t)')
        plt.plot(t, theta2, label='θ₂(t)')
        plt.xlabel("Time [s]")
        plt.ylabel("Angle [rad]")
        plt.title("Double Pendulum Angles")
        plt.grid()
        plt.legend()
        plt.show()

    def animate_pendulum(self):
        theta1 = self.solution.y[0]
        theta2 = self.solution.y[1]
        l1 = self.length_1
        l2 = self.length_2

        x1 = l1 * np.sin(theta1)
        y1 = -l1 * np.cos(theta1)
        x2 = x1 + l2 * np.sin(theta2)
        y2 = y1 - l2 * np.cos(theta2)

        fig, ax = plt.subplots()
        ax.set_xlim(-l1 - l2 - 0.5, l1 + l2 + 0.5)
        ax.set_ylim(-l1 - l2 - 0.5, l1 + l2 + 0.5)
        ax.set_aspect('equal')
        ax.grid()

        line, = ax.plot([], [], 'o-', lw=2)

        def update(i):
            line.set_data([0, x1[i], x2[i]], [0, y1[i], y2[i]])
            return line,

        ani = animation.FuncAnimation(fig, update, frames=len(theta1),
                                      interval=self.interval, blit=True)
        plt.title("Double Pendulum Animation")
        plt.show()



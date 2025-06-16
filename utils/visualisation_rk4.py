import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

class RK4Visualisation:
    def __init__(self, pendulum):
        self.pendulum = pendulum
        self.t = pendulum.solution_t
        self.y = pendulum.solution_y
        self.theta_1 = self.y[0]
        self.theta_2 = self.y[1]
        self.l1 = pendulum.length_1
        self.l2 = pendulum.length_2
        self.real_time_ratio = 1.0

    def plot_angles(self):
        plt.figure(figsize=(10, 5))
        plt.plot(self.t, np.degrees(self.theta_1), label='θ1 [deg]')
        plt.plot(self.t, np.degrees(self.theta_2), label='θ2 [deg]')
        plt.xlabel("Time [s]")
        plt.ylabel("Angle [degrees]")
        plt.title("Double Pendulum Angles (RK4)")
        plt.legend()
        plt.grid()
        plt.tight_layout()
        plt.show()

    def plot_energy(self):
        E = self.pendulum.compute_energy(self.t, self.y)
        plt.figure(figsize=(10, 5))
        plt.plot(self.t, E, label="Total Energy")
        plt.xlabel("Time [s]")
        plt.ylabel("Energy [J]")
        plt.title("Total Mechanical Energy (RK4)")
        plt.legend()
        plt.grid()
        plt.tight_layout()
        plt.show()

    def animate_motion(self):
        x1 = self.l1 * np.sin(self.theta_1)
        y1 = -self.l1 * np.cos(self.theta_1)
        x2 = x1 + self.l2 * np.sin(self.theta_2)
        y2 = y1 - self.l2 * np.cos(self.theta_2)

        fig, ax = plt.subplots()
        ax.set_xlim(-self.l1 - self.l2, self.l1 + self.l2)
        ax.set_ylim(-self.l1 - self.l2, self.l1 + self.l2)
        ax.set_aspect('equal')
        ax.grid()
        line, = ax.plot([], [], 'o-', lw=2)

        def update(i):
            line.set_data([0, x1[i], x2[i]], [0, y1[i], y2[i]])
            return line,

        dt = self.t[1] - self.t[0]
        interval = 1000 * dt / self.real_time_ratio
        ani = animation.FuncAnimation(fig, update, frames=len(self.t), interval=interval, blit=True)
        plt.title("Double Pendulum Animation (RK4)")
        plt.show()


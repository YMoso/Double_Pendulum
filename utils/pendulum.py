import numpy as np
from scipy.integrate import solve_ivp

class Pendulum:
    def __init__(self, config):
        self.mass_1 = config['mass_1']
        self.mass_2 = config['mass_2']
        self.length_1 = config['length_1']
        self.length_2 = config['length_2']
        self.theta_1 = np.radians(config["theta_1"])
        self.theta_2 = np.radians(config["theta_2"])
        self.theta_1_dot = np.radians(config['theta_1_dot'])
        self.theta_2_dot = np.radians(config['theta_2_dot'])
        self.t_span = config['t_span']
        self.steps = config['steps']
        self.method = config.get('method', 'solve_ivp')
        self.g = 9.81
        if self.method == 'solve_ivp':
            self.solution = self.simulate()
        else:
            self.solution_t, self.solution_y = self.rk4_solver()

    def compute_energy(self, *args):
        if len(args) == 1:
            sol = args[0]
            theta_1, theta_2 = sol.y[0], sol.y[1]
            theta_1_dot, theta_2_dot = sol.y[2], sol.y[3]
        else:
            t, y = args
            theta_1, theta_2 = y[0], y[1]
            theta_1_dot, theta_2_dot = y[2], y[3]

        delta = theta_1 - theta_2

        M = self.mass_1 + self.mass_2

        kinetic_energy = (
                0.5 * M * (self.length_1 ** 2) * (theta_1_dot ** 2)
                + 0.5 * self.mass_2 * (self.length_2 ** 2) * theta_2_dot ** 2
                + self.mass_2 * self.length_1 * self.length_2 * theta_1_dot * theta_2_dot * np.cos(delta)
        )

        potential_energy = (
                -M * self.g * self.length_1 * np.cos(theta_1)
                - self.mass_2 * self.g * self.length_2 * np.cos(theta_2)
        )

        return kinetic_energy + potential_energy

    def double_pendulum(self):
        M = self.mass_1 + self.mass_2
        delta = self.theta_1 - self.theta_2
        alpha = self.mass_1 + self.mass_2 * np.sin(delta)**2

        theta_1_ddot = (-np.sin(delta) *
                        (self.mass_2 * self.length_1 * self.theta_1_dot**2 * np.cos(delta)
                         + self.mass_2 * self.length_2 * self.theta_2_dot**2)
                        - self.g * (M * np.sin(self.theta_1)
                                    - self.mass_2 * np.sin(self.theta_2) * np.cos(delta))) / (self.length_1 * alpha)

        theta_2_ddot = (np.sin(delta) *
                        (M * self.length_1 * self.theta_1_dot**2
                         + self.mass_2 * self.length_2 * self.theta_2_dot**2 * np.cos(delta))
                        + self.g * (M * np.sin(self.theta_1) * np.cos(delta)
                                    - M * np.sin(self.theta_2))) / (self.length_2 * alpha)

        return theta_1_ddot, theta_2_ddot

    def derivatives(self, t, y):
        theta_1, theta_2, theta_1_dot, theta_2_dot = y
        self.theta_1 = theta_1
        self.theta_2 = theta_2
        self.theta_1_dot = theta_1_dot
        self.theta_2_dot = theta_2_dot
        theta_1_ddot, theta_2_ddot = self.double_pendulum()
        return [theta_1_dot, theta_2_dot, theta_1_ddot, theta_2_ddot]

    def simulate(self):
        y0 = [self.theta_1, self.theta_2, self.theta_1_dot, self.theta_2_dot]
        t_eval = np.linspace(self.t_span[0], self.t_span[1], self.steps)
        return solve_ivp(
            self.derivatives,
            self.t_span,
            y0,
            t_eval=t_eval,
            method='DOP853',
            rtol=1e-10,
            atol=1e-10
        )

    def rk4_solver(self):
        t0, tf = self.t_span
        h = (tf - t0) / self.steps
        t_vals = np.linspace(t0, tf, self.steps)
        y_vals = np.zeros((self.steps, 4))
        y_vals[0] = [self.theta_1, self.theta_2, self.theta_1_dot, self.theta_2_dot]

        for i in range(self.steps - 1):
            t = t_vals[i]
            y = y_vals[i]
            k1 = np.array(self.derivatives(t, y))
            k2 = np.array(self.derivatives(t + h / 2, y + h / 2 * k1))
            k3 = np.array(self.derivatives(t + h / 2, y + h / 2 * k2))
            k4 = np.array(self.derivatives(t + h, y + h * k3))
            y_vals[i + 1] = y + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)

        return t_vals, y_vals.T
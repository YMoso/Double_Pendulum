import numpy as np
from scipy.integrate import solve_ivp

class Pendulum:
    def __init__(self, config):
        self.mass_1 = config['mass_1']
        self.mass_2 = config['mass_2']
        self.length_1 = config['length_1']
        self.length_2 = config['length_2']
        self.theta_1 = config['theta_1']
        self.theta_2 = config['theta_2']
        self.theta_1_dot = config['theta_1_dot']
        self.theta_2_dot = config['theta_2_dot']
        self.t_span = config['t_span']
        self.steps = config['steps']
        self.g = 9.81
        self.solution = self.simulate()

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
        sol = solve_ivp(self.derivatives, self.t_span, y0, t_eval=t_eval)
        return sol

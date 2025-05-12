import numpy as np
from scipy.integrate import solve_ivp
from utils import Visualisation


"""

Przydatny link: https://physics.umd.edu/hep/drew/pendulum2.html

"""


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
        sol = self.simulate()
        Visualisation(config, sol)


    def coordinates(self):
        self.x_1 = self.length_1 * np.sin(self.theta_1)
        self.y_1 = -self.length_1 * np.cos(self.theta_1)
        self.x_2 = self.length_1 * np.sin(self.theta_1) + self.length_2 * np.sin(self.theta_2)
        self.y_2 = -self.length_1 * np.cos(self.theta_1) - self.length_2 * np.cos(self.theta_2)
        print(self.x_1, self.y_1, self.x_2, self.y_2)

    def kinetic_energy(self):
        delta = self.theta_1 - self.theta_2
        v1_dot = 0.5 * self.mass_1 * (self.length_1**2) * (self.theta_1_dot**2)
        v2_dot = 0.5 * self.mass_2 * (self.length_1**2 * self.theta_1_dot**2
                                      + self.length_2**2 * self.theta_2_dot**2
                                      + 2 * self.length_1 * self.length_2 * self.theta_1_dot
                                      * self.theta_2_dot * np.cos(delta))
        return v1_dot + v2_dot

    def potential_energy(self):
        return (-(self.mass_1 + self.mass_2) * self.g * self.length_1 * np.cos(self.theta_1)
                - self.mass_2 * self.g * self.length_2 * np.cos(self.theta_2))

    def lagrange(self):
        return self.kinetic_energy() - self.potential_energy()

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

    def derivatives(self,t, y):
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
        self.solution = sol
        return sol




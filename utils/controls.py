import copy
import matplotlib.pyplot as plt
from utils.pendulum import Pendulum
from utils.visualisation import Visualisation
from utils.visualisation_rk4 import RK4Visualisation


class Controls:
    def __init__(self, config):
        self.config = config

    def run(self):
        if self.config["multi_pendulum"]:
            self.run_multi()
        elif self.config["method"] == "rk4":
            self.run_rk4()
        else:
            self.run_single()

    def run_multi(self):
        pendulums = []
        for i in range(self.config["num_of_pendulums"]):
            cfg = copy.deepcopy(self.config)
            cfg["theta_1"] += i * 0.0001
            cfg["animate"] = True
            cfg["plot"] = False
            p = Pendulum(cfg)
            pendulums.append((cfg, p.solution))

        if self.config["animate"]:
            Visualisation.animate_multiple(pendulums)
        if self.config["plot"]:
            Visualisation.plot_phase_space(pendulums)
        if self.config["energy_plot"]:
            self.plot_energy(pendulums)

    def run_single(self):
        p = Pendulum(self.config)
        if self.config["animate"]:
            Visualisation(self.config, p.solution).animate_pendulum()
        if self.config["energy_plot"]:
            self.plot_energy([(self.config, p.solution)])
        if self.config["plot"]:
            Visualisation(self.config, p.solution).plot_angles()

    def run_rk4(self):
        pendulum = Pendulum(self.config)
        vis = RK4Visualisation(pendulum)

        vis.plot_angles()
        vis.plot_energy()
        vis.animate_motion()

    def plot_energy(self, pendulums):
        plt.figure(figsize=(8, 5))
        for idx, (cfg, sol) in enumerate(pendulums):
            p = Pendulum(cfg)
            E = p.compute_energy(sol)
            label = f"Pendulum {idx + 1}" if len(pendulums) > 1 else "Total Energy"
            plt.plot(sol.t, E, label=label)

        plt.xlabel("Time [s]")
        plt.ylabel("Total Energy [J]")
        plt.title("Total Energy Over Time")
        plt.grid(True)
        if len(pendulums) > 1:
            plt.legend()
        plt.tight_layout()
        plt.show()
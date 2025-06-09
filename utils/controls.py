import copy
import matplotlib.pyplot as plt
from utils.pendulum import Pendulum
from utils.visualisation import Visualisation

class Controls:
    def __init__(self, config):
        self.config = config

    def run(self):
        if self.config["multi_pendulum"]:
            self.run_multi()
        else:
            self.run_single()

    def run_multi(self):
        pendulums = []
        for i in range(self.config["num_of_pendulums"]):
            cfg = copy.deepcopy(self.config)
            cfg["theta_1"] += i * 0.01
            cfg["animate"] = False
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


    def plot_energy(self, pendulums):
        plt.figure(figsize=(8, 5))
        for idx, (cfg, sol) in enumerate(pendulums):
            p = Pendulum(cfg)
            E = p.compute_energy(sol)
            delta_E = E - E[0]
            label = f"Pendulum {idx+1}" if len(pendulums) > 1 else "Energy Drift"
            plt.plot(sol.t, delta_E, label=label)

        plt.xlabel("Time [s]")
        plt.ylabel("Δ Energy [J]")
        plt.title("Energy Over Time")
        plt.grid(True)
        if len(pendulums) > 1:
            plt.legend()
        plt.tight_layout()
        plt.show()
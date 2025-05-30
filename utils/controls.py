from utils.visualisation import Visualisation
from utils.pendulum import Pendulum
import copy

class MultiPendulumController:
    def __init__(self, base_config):
        self.config = base_config
        self.pendulums = self.create_multiple_pendulums()
        self.run()

    def create_multiple_pendulums(self):
        pendulums = []
        for i in range(self.config["num_of_pendulums"]):
            cfg = copy.deepcopy(self.config)
            cfg["theta_1"] += i * 0.01
            cfg["animate"] = False
            cfg["plot"] = False
            p = Pendulum(cfg)
            pendulums.append((cfg, p.solution))

        return pendulums

    def run(self):
        if self.config["plot"]:
            Visualisation.plot_phase_space(self.pendulums)
        Visualisation.animate_multiple(self.pendulums)
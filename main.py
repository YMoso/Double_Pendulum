from config import config
from utils.visualisation import Visualisation
from utils.pendulum import Pendulum
from utils.controls import MultiPendulumController


def main():
    if config["multi_pendulum"]:
        MultiPendulumController(config)
    else:
        p = Pendulum(config)
        vis = Visualisation(config, p.solution)
        vis.plot_angles()
        vis.animate_pendulum()

if __name__ == "__main__":
    main()
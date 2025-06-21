config = {
    "mass_1": 2,
    "mass_2": 10,
    "length_1": 1,
    "length_2": 1,
    "theta_1": 20, # degree for first bob
    "theta_2": 0, # degree for the second bob
    "theta_1_dot": 1,
    "theta_2_dot": 1,
    "t_span": (0, 30),
    "steps": 2000,
    "animate": True,
    "interval": 40,
    "plot": True,
    "multi_pendulum": True,
    "num_of_pendulums": 4,
    "energy_plot": True,
    "method": "solve_ivp" #solve_ivp or rk4
}

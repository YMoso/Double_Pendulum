# Double Pendulum Simulation

This project simulates the chaotic motion of a double pendulum using Python. It supports both Euler and RK4 (Runge–Kutta 4th order) numerical integration methods, provides detailed visualizations of the pendulum's behavior, and supports multi-pendulum comparisons.

---

## Features

- Physics-based simulation using `scipy.integrate.solve_ivp`
- RK4 and Euler integration methods available
- Modular architecture separating configuration, simulation, controls, and visualization
- Visualizations include:
  - Angle vs time plots
  - Energy conservation plots
  - Phase space and configuration space plots
  - Trajectory plots for each pendulum mass
- Real-time animation of the pendulum(s)
- Multi-pendulum mode: simulate many pendulums with slightly different starting conditions

---
1. **Installation:**
   - Make sure you have Python installed on your system.
   - Clone the repository to your local machine:
     ```bash
     git clone https://github.com/252514/Double_Pendulum.git
     cd Double_Pendulum
     ```

2. **Create and Activate a Virtual Environment:**
   - Create a virtual environment:
     ```bash
     python -m venv venv
     ```
   - Activate the virtual environment:
     - On Windows:
       
       ```bash
       .\venv\Scripts\activate
       ```
     - On macOS/Linux:
       
       ```bash
       source venv/bin/activate
       ```

3. **Dependencies:**
   - Install the required dependencies using pip:
     ```bash
     pip install -r requirements.txt
     ```

4. **Run the script:**
   - Execute the main script to start the game:
     ```bash
     python main.py
     ```

## Configuration (`config.py`)

The simulation is fully configurable via the `config.py` file. You can adjust any of the parameters below to customize the behavior of the double pendulum:

| Key             | Description                                      |
|------------------|--------------------------------------------------|
| `mass_1`         | Mass of the first pendulum                      |
| `mass_2`         | Mass of the second pendulum                     |
| `length_1`       | Length of the first pendulum arm                |
| `length_2`       | Length of the second pendulum arm               |
| `theta_1`        | Initial angle of the first pendulum (in radians)|
| `theta_2`        | Initial angle of the second pendulum (in radians)|
| `theta_1_dot`    | Initial angular velocity of pendulum 1          |
| `theta_2_dot`    | Initial angular velocity of pendulum 2          |
| `t_span`         | Time interval for simulation, e.g. `(0, 20)`    |
| `steps`          | Number of time steps in the simulation          |
| `plot`           | `True` to show the angle-over-time plot         |
| `animate`        | `True` to show the animated pendulum motion     |
| `multi_pendulum` | `True` Simulate multiple pendulums with slightly different angles     |
| `num_of_pendulums`| Number of pendulums to simulate if multi_pendulum is `True`|
| `interval`       | Frame update interval in the animation (in milliseconds)|
| `method`       | Set to "rk4" for Runge-Kutta method, else uses Euler|

### Example:

```python
config = {
    "mass_1": 2,
    "mass_2": 10,
    "length_1": 1,
    "length_2": 1,
    "theta_1": 20,
    "theta_2": 0,
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
    "method": "solve_ivp"
}


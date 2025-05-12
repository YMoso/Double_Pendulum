# 🎢 Double Pendulum Simulation

A physics-based simulation of a double pendulum using Python. Simulates chaotic motion, visualizes the angles, and animates the motion using `matplotlib`.

---

## 📦 Features

- Simulates double pendulum dynamics using `scipy.integrate.solve_ivp`
- Configurable through a Python `config.py` file
- Clean architecture with separation of simulation logic, configuration, and visualization
- Plots angle vs time
- Animates pendulum motion with `matplotlib.animation`

---


1. **Installation:**
   - Make sure you have Python installed on your system.
   - Clone the repository to your local machine:
     ```bash
     git clone https://github.com/252514/Double_Pendulum.git
     cd conways-game-of-life
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

## ⚙️ Configuration (`config.py`)

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

### 📌 Example:

```python
config = {
    "mass_1": 1,
    "mass_2": 10,
    "length_1": 1,
    "length_2": 10,
    "theta_1": 1,
    "theta_2": 1,
    "theta_1_dot": 1,
    "theta_2_dot": 1,
    "t_span": (0, 20),
    "steps": 1000,
    "plot": True,
    "animate": True
}

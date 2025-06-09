import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from collections import deque


class Visualisation:
    def __init__(self, config, solution):
        self.length_1 = config['length_1']
        self.length_2 = config['length_2']
        self.mass_1 = config['mass_1']
        self.mass_2 = config['mass_2']
        self.interval = config['interval']
        self.num_of_pendulums = config['num_of_pendulums']
        self.solution = solution




    def plot_angles(self):
        t = self.solution.t
        theta1, theta2 = self.solution.y[0], self.solution.y[1]

        plt.plot(t, theta1, label='θ₁(t)')
        plt.plot(t, theta2, label='θ₂(t)')
        plt.xlabel("Time [s]")
        plt.ylabel("Angle [rad]")
        plt.title("Double Pendulum Angles")
        plt.grid()
        plt.legend()
        plt.show()

    def animate_pendulum(self):
        Visualisation.animate_multiple([(self.__dict__, self.solution)])

    @staticmethod
    def plot_trajectories(pendulums):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57']

        for idx, (config, sol) in enumerate(pendulums):
            l1 = config['length_1']
            l2 = config['length_2']
            color = colors[idx % len(colors)]

            theta1 = sol.y[0]
            theta2 = sol.y[1]

            x1 = l1 * np.sin(theta1)
            y1 = -l1 * np.cos(theta1)
            x2 = x1 + l2 * np.sin(theta2)
            y2 = y1 - l2 * np.cos(theta2)

            ax1.plot(x1, y1, color=color, alpha=0.7, linewidth=1,
                     label=f'Pendulum {idx + 1} (Mass 1)')
            ax1.scatter(x1[0], y1[0], color=color, s=50, marker='o',
                        edgecolors='black', zorder=5)
            ax1.scatter(x1[-1], y1[-1], color=color, s=50, marker='s',
                        edgecolors='black', zorder=5)

            # Plot second mass trajectory
            ax2.plot(x2, y2, color=color, alpha=0.7, linewidth=1,
                     label=f'Pendulum {idx + 1} (Mass 2)')
            ax2.scatter(x2[0], y2[0], color=color, s=50, marker='o',
                        edgecolors='black', zorder=5)
            ax2.scatter(x2[-1], y2[-1], color=color, s=50, marker='s',
                        edgecolors='black', zorder=5)

        ax1.set_aspect('equal')
        ax1.grid(True, alpha=0.3)
        ax1.set_xlabel('X Position (m)')
        ax1.set_ylabel('Y Position (m)')
        ax1.set_title('First Mass Trajectories\n(Circle = Start, Square = End)')
        ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

        ax2.set_aspect('equal')
        ax2.grid(True, alpha=0.3)
        ax2.set_xlabel('X Position (m)')
        ax2.set_ylabel('Y Position (m)')
        ax2.set_title('Second Mass Trajectories\n(Circle = Start, Square = End)')
        ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

        plt.tight_layout()
        plt.show()

        return fig

    @staticmethod
    def plot_phase_space(pendulums):
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))

        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57']

        for idx, (config, sol) in enumerate(pendulums):
            color = colors[idx % len(colors)]

            theta1 = sol.y[0]
            theta2 = sol.y[1]
            theta1_dot = sol.y[2]
            theta2_dot = sol.y[3]

            ax1.plot(theta1, theta1_dot, color=color, alpha=0.7, linewidth=1,
                     label=f'Pendulum {idx + 1}')
            ax1.scatter(theta1[0], theta1_dot[0], color=color, s=30, marker='o',
                        edgecolors='black', zorder=5)

            ax2.plot(theta2, theta2_dot, color=color, alpha=0.7, linewidth=1,
                     label=f'Pendulum {idx + 1}')
            ax2.scatter(theta2[0], theta2_dot[0], color=color, s=30, marker='o',
                        edgecolors='black', zorder=5)

            ax3.plot(theta1, theta2, color=color, alpha=0.7, linewidth=1,
                     label=f'Pendulum {idx + 1}')
            ax3.scatter(theta1[0], theta2[0], color=color, s=30, marker='o',
                        edgecolors='black', zorder=5)

            ax4.plot(sol.t, color=color, alpha=0.7, linewidth=1,
                     label=f'Pendulum {idx + 1}')

        ax1.set_xlabel('θ₁ (rad)')
        ax1.set_ylabel('θ₁\' (rad/s)')
        ax1.set_title('Phase Space: First Pendulum')
        ax1.grid(True, alpha=0.3)
        ax1.legend()

        ax2.set_xlabel('θ₂ (rad)')
        ax2.set_ylabel('θ₂\' (rad/s)')
        ax2.set_title('Phase Space: Second Pendulum')
        ax2.grid(True, alpha=0.3)
        ax2.legend()

        ax3.set_xlabel('θ₁ (rad)')
        ax3.set_ylabel('θ₂ (rad)')
        ax3.set_title('Configuration Space')
        ax3.grid(True, alpha=0.3)
        ax3.legend()

        ax4.set_xlabel('Time (s)')
        ax4.set_ylabel('Value')
        ax4.set_title('Time Evolution')
        ax4.grid(True, alpha=0.3)
        ax4.legend()

        plt.tight_layout()
        plt.show()

        return fig

    @staticmethod
    def animate_multiple(pendulums):
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.set_xlim(-3, 3)
        ax.set_ylim(-3, 3)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_facecolor('black')

        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57']

        lines = []
        balls1 = []
        balls2 = []
        trajectories = []
        trajectory_lines = []

        dt = pendulums[0][1].t[1] - pendulums[0][1].t[0]
        trajectory_length = int(5.0 / dt)

        for idx, (config, sol) in enumerate(pendulums):
            l1 = config['length_1']
            l2 = config['length_2']
            m1 = config['mass_1']
            m2 = config['mass_2']
            color = colors[idx % len(colors)]

            theta1 = sol.y[0]
            theta2 = sol.y[1]

            x1 = l1 * np.sin(theta1)
            y1 = -l1 * np.cos(theta1)
            x2 = x1 + l2 * np.sin(theta2)
            y2 = y1 - l2 * np.cos(theta2)

            line, = ax.plot([], [], '-', lw=2, color=color, alpha=0.8)

            ball1 = plt.Circle((0, 0), 0.05 * m1 ** (1 / 3), fc=color, ec='white', linewidth=1)
            ball2 = plt.Circle((0, 0), 0.08 * m2 ** (1 / 3), fc=color, ec='white', linewidth=1)
            ax.add_patch(ball1)
            ax.add_patch(ball2)

            trajectory = deque(maxlen=trajectory_length)
            trajectory_line, = ax.plot([], [], '-', color=color, alpha=0.6, linewidth=1)

            lines.append((line, x1, y1, x2, y2))
            balls1.append(ball1)
            balls2.append(ball2)
            trajectories.append(trajectory)
            trajectory_lines.append(trajectory_line)

        pivot = plt.Circle((0, 0), 0.05, fc='white', ec='gray', linewidth=2)
        ax.add_patch(pivot)

        def update(i):
            for idx, (line, x1, y1, x2, y2) in enumerate(lines):
                line.set_data([0, x1[i], x2[i]], [0, y1[i], y2[i]])

                balls1[idx].center = (x1[i], y1[i])
                balls2[idx].center = (x2[i], y2[i])
                trajectories[idx].append((x2[i], y2[i]))
                if len(trajectories[idx]) > 1:
                    traj_x, traj_y = zip(*trajectories[idx])
                    trajectory_lines[idx].set_data(traj_x, traj_y)

            return [l[0] for l in lines] + balls1 + balls2 + trajectory_lines

        frame_count = min(len(sol.t) for _, sol in pendulums)
        ani = animation.FuncAnimation(fig, update, frames=frame_count,
                                      interval=pendulums[0][0]['interval'], blit=True, repeat=True)

        plt.title("Multiple Double Pendulums with Trajectory Traces", color='white', fontsize=14)
        plt.tight_layout()
        plt.show()

        return ani

class MultiPendulumVisualizer:
    def __init__(self, configs_and_solutions):
        self.pendulums = configs_and_solutions
        Visualisation.plot_trajectories(self.pendulums)
        Visualisation.plot_phase_space(self.pendulums)
        Visualisation.animate_multiple(self.pendulums)


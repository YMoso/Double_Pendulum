import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from collections import deque


class RK4Visualisation:
    def __init__(self, pendulum):
        self.pendulum = pendulum
        self.t = pendulum.solution_t
        self.y = pendulum.solution_y
        self.theta_1 = self.y[0]
        self.theta_2 = self.y[1]
        self.l1 = pendulum.length_1
        self.l2 = pendulum.length_2
        self.m1 = pendulum.mass_1
        self.m2 = pendulum.mass_2
        self.real_time_ratio = 1.0

    def plot_angles(self):
        plt.figure(figsize=(10, 5))
        plt.plot(self.t, np.degrees(self.theta_1), label='θ1 [deg]', color='#FF6B6B', linewidth=2)
        plt.plot(self.t, np.degrees(self.theta_2), label='θ2 [deg]', color='#4ECDC4', linewidth=2)
        plt.xlabel("Time [s]")
        plt.ylabel("Angle [degrees]")
        plt.title("Double Pendulum Angles (RK4)")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

    def plot_energy(self):
        E = self.pendulum.compute_energy(self.t, self.y)
        plt.figure(figsize=(10, 5))
        plt.plot(self.t, E, label="Total Energy", color='#45B7D1', linewidth=2)
        plt.xlabel("Time [s]")
        plt.ylabel("Energy [J]")
        plt.title("Total Mechanical Energy (RK4)")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

    def plot_trajectories(self):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

        x1 = self.l1 * np.sin(self.theta_1)
        y1 = -self.l1 * np.cos(self.theta_1)
        x2 = x1 + self.l2 * np.sin(self.theta_2)
        y2 = y1 - self.l2 * np.cos(self.theta_2)

        ax1.plot(x1, y1, color='#FF6B6B', alpha=0.7, linewidth=2, label='Mass 1 Trajectory')
        ax1.scatter(x1[0], y1[0], color='#FF6B6B', s=100, marker='o',
                    edgecolors='black', zorder=5, label='Start')
        ax1.scatter(x1[-1], y1[-1], color='#FF6B6B', s=100, marker='s',
                    edgecolors='black', zorder=5, label='End')

        ax1.set_aspect('equal')
        ax1.grid(True, alpha=0.3)
        ax1.set_xlabel('X Position (m)')
        ax1.set_ylabel('Y Position (m)')
        ax1.set_title('First Mass Trajectory (RK4)\n(Circle = Start, Square = End)')
        ax1.legend()

        ax2.plot(x2, y2, color='#4ECDC4', alpha=0.7, linewidth=2, label='Mass 2 Trajectory')
        ax2.scatter(x2[0], y2[0], color='#4ECDC4', s=100, marker='o',
                    edgecolors='black', zorder=5, label='Start')
        ax2.scatter(x2[-1], y2[-1], color='#4ECDC4', s=100, marker='s',
                    edgecolors='black', zorder=5, label='End')

        ax2.set_aspect('equal')
        ax2.grid(True, alpha=0.3)
        ax2.set_xlabel('X Position (m)')
        ax2.set_ylabel('Y Position (m)')
        ax2.set_title('Second Mass Trajectory (RK4)\n(Circle = Start, Square = End)')
        ax2.legend()

        plt.tight_layout()
        plt.show()
        return fig

    def plot_phase_space(self):
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))

        theta1_dot = self.y[2]
        theta2_dot = self.y[3]

        ax1.plot(self.theta_1, theta1_dot, color='#FF6B6B', alpha=0.7, linewidth=2)
        ax1.scatter(self.theta_1[0], theta1_dot[0], color='#FF6B6B', s=50,
                    marker='o', edgecolors='black', zorder=5)
        ax1.set_xlabel('θ_1 (rad)')
        ax1.set_ylabel('θ_1\' (rad/s)')
        ax1.set_title('Phase Space: First Pendulum (RK4)')
        ax1.grid(True, alpha=0.3)

        ax2.plot(self.theta_2, theta2_dot, color='#4ECDC4', alpha=0.7, linewidth=2)
        ax2.scatter(self.theta_2[0], theta2_dot[0], color='#4ECDC4', s=50,
                    marker='o', edgecolors='black', zorder=5)
        ax2.set_xlabel('θ_2 (rad)')
        ax2.set_ylabel('θ_2\' (rad/s)')
        ax2.set_title('Phase Space: Second Pendulum (RK4)')
        ax2.grid(True, alpha=0.3)

        ax3.plot(self.theta_1, self.theta_2, color='#45B7D1', alpha=0.7, linewidth=2)
        ax3.scatter(self.theta_1[0], self.theta_2[0], color='#45B7D1', s=50,
                    marker='o', edgecolors='black', zorder=5)
        ax3.set_xlabel('θ₁ (rad)')
        ax3.set_ylabel('θ₂ (rad)')
        ax3.set_title('Configuration Space (RK4)')
        ax3.grid(True, alpha=0.3)

        ax4.plot(self.t, np.degrees(self.theta_1), color='#FF6B6B',
                 label='θ₁', linewidth=2)
        ax4.plot(self.t, np.degrees(self.theta_2), color='#4ECDC4',
                 label='θ₂', linewidth=2)
        ax4.set_xlabel('Time (s)')
        ax4.set_ylabel('Angle (degrees)')
        ax4.set_title('Time Evolution (RK4)')
        ax4.grid(True, alpha=0.3)
        ax4.legend()

        plt.tight_layout()
        plt.show()
        return fig

    def animate_motion(self):
        x1 = self.l1 * np.sin(self.theta_1)
        y1 = -self.l1 * np.cos(self.theta_1)
        x2 = x1 + self.l2 * np.sin(self.theta_2)
        y2 = y1 - self.l2 * np.cos(self.theta_2)

        fig, ax = plt.subplots(figsize=(10, 8))
        ax.set_xlim(-self.l1 - self.l2 - 0.5, self.l1 + self.l2 + 0.5)
        ax.set_ylim(-self.l1 - self.l2 - 0.5, self.l1 + self.l2 + 0.5)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_facecolor('black')

        line, = ax.plot([], [], '-', lw=3, color='#FFFFFF', alpha=0.8)

        ball1 = plt.Circle((0, 0), 0.05 * self.m1 ** (1 / 3), fc='#FF6B6B',
                           ec='white', linewidth=2)
        ball2 = plt.Circle((0, 0), 0.08 * self.m2 ** (1 / 3), fc='#4ECDC4',
                           ec='white', linewidth=2)
        ax.add_patch(ball1)
        ax.add_patch(ball2)

        pivot = plt.Circle((0, 0), 0.05, fc='white', ec='gray', linewidth=2)
        ax.add_patch(pivot)

        dt = self.t[1] - self.t[0] if len(self.t) > 1 else 0.01
        trajectory_length = int(3.0 / dt)
        trajectory = deque(maxlen=trajectory_length)
        trajectory_line, = ax.plot([], [], '-', color='#4ECDC4', alpha=0.6, linewidth=1)

        def update(i):
            if i < len(x1):
                line.set_data([0, x1[i], x2[i]], [0, y1[i], y2[i]])

                ball1.center = (x1[i], y1[i])
                ball2.center = (x2[i], y2[i])

                trajectory.append((x2[i], y2[i]))
                if len(trajectory) > 1:
                    traj_x, traj_y = zip(*trajectory)
                    trajectory_line.set_data(traj_x, traj_y)

            return line, ball1, ball2, trajectory_line

        dt = self.t[1] - self.t[0] if len(self.t) > 1 else 0.01
        interval = 1000 * dt / self.real_time_ratio

        ani = animation.FuncAnimation(fig, update, frames=len(self.t),
                                      interval=interval, blit=True, repeat=True)

        plt.title("Double Pendulum Animation (RK4)", color='white', fontsize=14)
        plt.tight_layout()
        plt.show()
        return ani

    def create_complete_analysis(self):
        print("Creating complete RK4 analysis...")
        self.plot_angles()
        self.plot_energy()
        self.plot_trajectories()
        self.plot_phase_space()
        return self.animate_motion()


class MultiRK4Visualizer:
    def __init__(self, pendulums):
        self.pendulums = pendulums
        self.colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57']

    def plot_trajectories(self):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

        for idx, pendulum in enumerate(self.pendulums):
            color = self.colors[idx % len(self.colors)]

            theta1 = pendulum.solution_y[0]
            theta2 = pendulum.solution_y[1]

            x1 = pendulum.length_1 * np.sin(theta1)
            y1 = -pendulum.length_1 * np.cos(theta1)
            x2 = x1 + pendulum.length_2 * np.sin(theta2)
            y2 = y1 - pendulum.length_2 * np.cos(theta2)

            ax1.plot(x1, y1, color=color, alpha=0.7, linewidth=2,
                     label=f'Pendulum {idx + 1} (Mass 1)')
            ax1.scatter(x1[0], y1[0], color=color, s=50, marker='o',
                        edgecolors='black', zorder=5)
            ax1.scatter(x1[-1], y1[-1], color=color, s=50, marker='s',
                        edgecolors='black', zorder=5)

            ax2.plot(x2, y2, color=color, alpha=0.7, linewidth=2,
                     label=f'Pendulum {idx + 1} (Mass 2)')
            ax2.scatter(x2[0], y2[0], color=color, s=50, marker='o',
                        edgecolors='black', zorder=5)
            ax2.scatter(x2[-1], y2[-1], color=color, s=50, marker='s',
                        edgecolors='black', zorder=5)

        ax1.set_aspect('equal')
        ax1.grid(True, alpha=0.3)
        ax1.set_xlabel('X Position (m)')
        ax1.set_ylabel('Y Position (m)')
        ax1.set_title('First Mass Trajectories (RK4)\n(Circle = Start, Square = End)')
        ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

        ax2.set_aspect('equal')
        ax2.grid(True, alpha=0.3)
        ax2.set_xlabel('X Position (m)')
        ax2.set_ylabel('Y Position (m)')
        ax2.set_title('Second Mass Trajectories (RK4)\n(Circle = Start, Square = End)')
        ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

        plt.tight_layout()
        plt.show()
        return fig

    def plot_phase_space(self):
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5))

        for idx, pendulum in enumerate(self.pendulums):
            color = self.colors[idx % len(self.colors)]

            theta1 = pendulum.solution_y[0]
            theta2 = pendulum.solution_y[1]
            theta1_dot = pendulum.solution_y[2]
            theta2_dot = pendulum.solution_y[3]

            ax1.plot(theta1, theta1_dot, color=color, alpha=0.7, linewidth=2,
                     label=f'Pendulum {idx + 1}')
            ax1.scatter(theta1[0], theta1_dot[0], color=color, s=30, marker='o',
                        edgecolors='black', zorder=5)

            ax2.plot(theta2, theta2_dot, color=color, alpha=0.7, linewidth=2,
                     label=f'Pendulum {idx + 1}')
            ax2.scatter(theta2[0], theta2_dot[0], color=color, s=30, marker='o',
                        edgecolors='black', zorder=5)

            ax3.plot(theta1, theta2, color=color, alpha=0.7, linewidth=2,
                     label=f'Pendulum {idx + 1}')
            ax3.scatter(theta1[0], theta2[0], color=color, s=30, marker='o',
                        edgecolors='black', zorder=5)

            ax4.plot(pendulum.solution_t, np.degrees(theta1), color=color,
                     alpha=0.7, linewidth=2, label=f'Pendulum {idx + 1}')

        ax1.set_xlabel('θ_1 (rad)')
        ax1.set_ylabel('θ_1\' (rad/s)')
        ax1.set_title('Phase Space: First Pendulum (RK4)')
        ax1.grid(True, alpha=0.3)
        ax1.legend()

        ax2.set_xlabel('θ_2 (rad)')
        ax2.set_ylabel('θ_2\' (rad/s)')
        ax2.set_title('Phase Space: Second Pendulum (RK4)')
        ax2.grid(True, alpha=0.3)
        ax2.legend()

        ax3.set_xlabel('θ₁ (rad)')
        ax3.set_ylabel('θ₂ (rad)')
        ax3.set_title('Configuration Space (RK4)')
        ax3.grid(True, alpha=0.3)
        ax3.legend()

        plt.tight_layout()
        plt.show()
        return fig

    def animate_multiple(self):
        fig, ax = plt.subplots(figsize=(12, 10))
        ax.set_xlim(-3, 3)
        ax.set_ylim(-3, 3)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_facecolor('black')

        lines = []
        balls1 = []
        balls2 = []
        trajectories = []
        trajectory_lines = []

        dt = self.pendulums[0].solution_t[1] - self.pendulums[0].solution_t[0]
        trajectory_length = int(5.0 / dt)

        for idx, pendulum in enumerate(self.pendulums):
            color = self.colors[idx % len(self.colors)]

            theta1 = pendulum.solution_y[0]
            theta2 = pendulum.solution_y[1]

            x1 = pendulum.length_1 * np.sin(theta1)
            y1 = -pendulum.length_1 * np.cos(theta1)
            x2 = x1 + pendulum.length_2 * np.sin(theta2)
            y2 = y1 - pendulum.length_2 * np.cos(theta2)

            line, = ax.plot([], [], '-', lw=2, color=color, alpha=0.8)

            ball1 = plt.Circle((0, 0), 0.05 * pendulum.mass_1 ** (1 / 3),
                               fc=color, ec='white', linewidth=1)
            ball2 = plt.Circle((0, 0), 0.08 * pendulum.mass_2 ** (1 / 3),
                               fc=color, ec='white', linewidth=1)
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
                if i < len(x1):
                    line.set_data([0, x1[i], x2[i]], [0, y1[i], y2[i]])

                    balls1[idx].center = (x1[i], y1[i])
                    balls2[idx].center = (x2[i], y2[i])

                    trajectories[idx].append((x2[i], y2[i]))
                    if len(trajectories[idx]) > 1:
                        traj_x, traj_y = zip(*trajectories[idx])
                        trajectory_lines[idx].set_data(traj_x, traj_y)

            return [l[0] for l in lines] + balls1 + balls2 + trajectory_lines

        frame_count = min(len(p.solution_t) for p in self.pendulums)
        interval = 1000 * dt / 1.0

        ani = animation.FuncAnimation(fig, update, frames=frame_count,
                                      interval=interval, blit=True, repeat=True)

        plt.title("Multiple Double Pendulums (RK4)", color='white', fontsize=14)
        plt.tight_layout()
        plt.show()
        return ani

    def create_complete_analysis(self):
        print("Creating complete multi-pendulum RK4 analysis...")
        self.plot_trajectories()
        self.plot_phase_space()
        return self.animate_multiple()


def analyze_single_rk4_pendulum(pendulum):
    viz = RK4Visualisation(pendulum)
    return viz.create_complete_analysis()


def analyze_multiple_rk4_pendulums(pendulums):
    viz = MultiRK4Visualizer(pendulums)
    return viz.create_complete_analysis()

"""Lagrange acceleration """

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# Parameters
R = 1
sigma = 5
v_s0 = 0.9          # v_s(t_0)
A0 = 1.5            # Acceleration A(t_0)
x_s0 = 0.0          # Initial position x_s(t_0)
t_0 = 0.0           # Initial time

# Grid
x = np.linspace(-1.5, 1.5, 200)
y = np.linspace(-1.5, 1.5, 200)
X, Y = np.meshgrid(x, y)

# Define functions for v_s(t) and x_s(t)
def v_s(t):
    return v_s0 + A0 * (t - t_0)

def x_s(t):
    return x_s0 + v_s0 * (t - t_0) + 0.5 * A0 * (t - t_0)**2

# Compute fields at time t
def compute_fields(X, Y, t):
    xs = x_s(t)
    vs = v_s(t)
    r_s = np.sqrt((X - xs)**2 + Y**2)
    W_rs = (np.tanh(sigma * (r_s + R)) - np.tanh(sigma * (r_s - R))) / (2 * np.tanh(sigma * R))
    V_x = vs * W_rs
    dVx_dX = np.gradient(V_x, x, axis=1)
    dVx_dY = np.gradient(V_x, y, axis=0)
    theta = dVx_dX
    return theta, V_x, dVx_dY

# Vorticity
def compute_Omega2(theta0, dVx_dY, t):
    Omega2 = ((-0.5 * dVx_dY)**2) / (4 * (1 + theta0 * (t - t_0))**2)
    return Omega2

# Shear
def compute_Sigma2(theta_t, Omega2):
    return (1/3) * theta_t**2 + Omega2

# Initialize figure
fig = plt.figure(figsize=(18, 5))
ax_theta = fig.add_subplot(131, projection='3d')
ax_omega = fig.add_subplot(132, projection='3d')
ax_sigma = fig.add_subplot(133, projection='3d')

for ax, title, zlabel in zip([ax_theta, ax_omega, ax_sigma],
                             ["Expansion Θ(t,X)", "Vorticity Ω²(t,X)", "Shear Scalar Σ²(t,X)"],
                             ["Θ", "Ω²", "Σ²"]):
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel(zlabel)
    ax.set_title(title)

# Track surfaces
surfaces = [None, None, None]

# Animation function
def animate(t):
    global surfaces
    for surf in surfaces:
        if surf: surf.remove()

    theta0, Vx, dVx_dY = compute_fields(X, Y, t_0)
    theta_t, _, _ = compute_fields(X, Y, t)
    
    Omega2 = compute_Omega2(theta0, dVx_dY, t)
    Sigma2 = compute_Sigma2(theta_t, Omega2)

    surfaces[0] = ax_theta.plot_surface(X, Y, theta_t, cmap='coolwarm', edgecolor='none')
    surfaces[1] = ax_omega.plot_surface(X, Y, Omega2, cmap='plasma', edgecolor='none')
    surfaces[2] = ax_sigma.plot_surface(X, Y, Sigma2, cmap='viridis', edgecolor='none')

    ax_theta.set_zlim(-5, 5)
    ax_omega.set_zlim(0, np.max(Omega2) * 1.1)
    ax_sigma.set_zlim(0, np.max(Sigma2) * 1.1)

    fig.suptitle(f"Kinematic Fields at t = {t:.2f} | x_s(t) = {x_s(t):.2f} | v_s(t) = {v_s(t):.2f}", fontsize=15)

# Run animation
anim = FuncAnimation(fig, animate, frames=np.linspace(0.0, 0.45, 60), interval=100)
plt.tight_layout()
plt.show()

# Entry point
def main():
    print("Inertial Alcubierre bubble with accelerated motion A(t_0) = {:.2f}".format(A0))

if __name__ == "__main__":
    main()
















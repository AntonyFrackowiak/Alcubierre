"""Lagrange_constant_velocity"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# Parameters
R = 1
sigma = 5
v_s = 0.9
t_0 = 0.0

# Grid
x = np.linspace(-1.5, 1.5, 200)
y = np.linspace(-1.5, 1.5, 200)
X, Y = np.meshgrid(x, y)

# Compute initial fields
def update_fields(X, Y, t):
    r_s = np.sqrt(X**2 + Y**2)
    W_rs = (np.tanh(sigma * (r_s + R)) - np.tanh(sigma * (r_s - R))) / (2 * np.tanh(sigma * R))
    V_x = v_s * W_rs
    dV_x_dX = np.gradient(V_x, x, axis=1)
    dV_x_dY = np.gradient(V_x, y, axis=0)
    theta = dV_x_dX
    return theta, V_x, dV_x_dY

def compute_Omega2(theta0, dVx_dY, t):
    VS_Y = dVx_dY
    Omega_squared = ((-0.5 * VS_Y)**2) / (4 * (1 + theta0 * (t - t_0))**2)
    return Omega_squared

def compute_Sigma2(theta_t, Omega2):
    return (1/3) * theta_t**2 + Omega2

# Initial fields at t0
theta0, V_x0, dVx_dY0 = update_fields(X, Y, t_0)

# Setup figure with 3D subplots
fig = plt.figure(figsize=(18, 5))
ax_theta = fig.add_subplot(131, projection='3d')
ax_omega = fig.add_subplot(132, projection='3d')
ax_sigma = fig.add_subplot(133, projection='3d')

# Labels
for ax, title, zlabel in zip([ax_theta, ax_omega, ax_sigma],
                             ["Expansion Θ(t,X)", "Vorticity Ω²(t,X)", "Shear Scalar Σ²(t,X)"],
                             ["Θ", "Ω²", "Σ²"]):
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel(zlabel)
    ax.set_title(title)

# Storage for surfaces
surfaces = [None, None, None]

# Animation function
def animate(t):
    global surfaces
    # Clear previous surfaces
    for surf in surfaces:
        if surf:
            surf.remove()

    # Recompute fields at time t
    theta_t = theta0 / (1 + theta0 * (t - t_0))
    Omega2 = compute_Omega2(theta0, dVx_dY0, t)
    Sigma2 = compute_Sigma2(theta_t, Omega2)

    # Plot all three
    surfaces[0] = ax_theta.plot_surface(X, Y, theta_t, cmap='coolwarm', edgecolor='none')
    surfaces[1] = ax_omega.plot_surface(X, Y, Omega2, cmap='plasma', edgecolor='none')
    surfaces[2] = ax_sigma.plot_surface(X, Y, Sigma2, cmap='viridis', edgecolor='none')

    # Set z-axis limits for consistency
    ax_theta.set_zlim(-5, 5)
    ax_omega.set_zlim(0, np.max(Omega2)*1.1)
    ax_sigma.set_zlim(0, np.max(Sigma2)*1.1)

    fig.suptitle(f"Kinematic Fields at t = {t:.2f}", fontsize=16)

# Animate over time
anim = FuncAnimation(fig, animate, frames=np.linspace(-0.44, 0.44, 60), interval=100)
plt.tight_layout()
plt.show()

# Entry point
def main():
    print("Run complete kinematic field visualization of Alcubierre bubble.")

if __name__ == "__main__":
    main()


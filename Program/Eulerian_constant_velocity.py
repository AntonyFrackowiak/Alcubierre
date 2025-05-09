"""Eulerian_constant_velocity"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# Parameters
R = 1.0
sigma = 5.0
v_s = 0.9
t_0 = 1.0

# Grid
X = np.linspace(-1, 1, 400)
Y = np.linspace(-1.5, 1.5, 400)
X_grid, Y_grid = np.meshgrid(X, Y)

# Warp field W(r_s)
def warp_field(x_prime, y, t):
    r_s = np.sqrt((x_prime - v_s * t)**2 + y**2)
    return (np.tanh(sigma * (r_s + R)) - np.tanh(sigma * (r_s - R))) / (2 * np.tanh(sigma * R))

# Velocity profile at transported coordinate
def V_profile(X, Y, t):
    W_t0 = warp_field(X, Y, t_0)
    x_prime = X + v_s * W_t0 * (t - t_0)
    W = warp_field(x_prime, Y, t)
    Vx = v_s * W
    return Vx

# Main compute function
def compute_fields(t):
    Vx = V_profile(X_grid, Y_grid, t)
    dVx_dx = np.gradient(Vx, X, axis=1)
    dVx_dy = np.gradient(Vx, Y, axis=0)

    theta = dVx_dx
    sigma2 = dVx_dx**2 / 3 + dVx_dy**2 / 2
    omega2 = dVx_dy**2 / 2

    return theta, sigma2, omega2, Vx

# Initial plot
theta, sigma2, omega2, Vx = compute_fields(t_0)

fig = plt.figure(figsize=(16, 11))
ax1 = fig.add_subplot(221, projection='3d')
ax1.set_title("Rate of expansion θ")
ax1.set_xlabel('x'); ax1.set_ylabel('ρ'); ax1.set_zlabel('θ')
theta_surf = ax1.plot_surface(X_grid, Y_grid, theta, cmap='RdYlBu')

ax2 = fig.add_subplot(222, projection='3d')
ax2.set_title("Shear σ²")
ax2.set_xlabel('x'); ax2.set_ylabel('ρ'); ax2.set_zlabel('σ²')
sigma2_surf = ax2.plot_surface(X_grid, Y_grid, sigma2, cmap='RdYlBu')

ax3 = fig.add_subplot(224, projection='3d')
ax3.set_title("Vorticity ω²")
ax3.set_xlabel('x'); ax3.set_ylabel('ρ'); ax3.set_zlabel('ω²')
omega2_surf = ax3.plot_surface(X_grid, Y_grid, omega2, cmap='RdYlBu')

ax4 = fig.add_subplot(223, projection='3d')
ax4.set_title("Velocity Vₓ")
ax4.set_xlabel('x'); ax4.set_ylabel('ρ'); ax4.set_zlabel('Vₓ')
Vx_surf = ax4.plot_surface(X_grid, Y_grid, Vx, cmap='RdYlBu')

# Time annotation
time_text = fig.text(0.5, 0.92, '', ha='center', fontsize=14)

# Animation function
def animate(frame):
    t = t_0 + frame * 0.1  # evolve time
    theta, sigma2, omega2, Vx = compute_fields(t)
    
    # Clear old plots
    for ax in [ax1, ax2, ax3, ax4]:
        while len(ax.collections) > 0:
            ax.collections.pop()
    # Update surfaces
    ax1.plot_surface(X_grid, Y_grid, theta, cmap='RdYlBu')
    ax2.plot_surface(X_grid, Y_grid, sigma2, cmap='RdYlBu')
    ax3.plot_surface(X_grid, Y_grid, omega2, cmap='RdYlBu')
    ax4.plot_surface(X_grid, Y_grid, Vx, cmap='RdYlBu')

    time_text.set_text(f"Time t = {t:.2f}")
    return []

# Create animation
anim = FuncAnimation(fig, animate, frames=60, interval=150, blit=False)

plt.tight_layout()
plt.show()



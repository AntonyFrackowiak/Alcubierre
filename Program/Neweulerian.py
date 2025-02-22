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
x = np.linspace(-1.5, 1.5, 100)
y = np.linspace(-1.5, 1.5, 100)
X, Y = np.meshgrid(x, y)

# Function to update W(r_s) and velocities
def update_fields(X, Y, t):
    r_s = np.sqrt(X**2 + Y**2)  # Radial distance in Eulerian coordinates
    W_rs = (np.tanh(sigma * (r_s + R)) - np.tanh(sigma * (r_s - R))) / (2 * np.tanh(sigma * R))

    # Speed component
    V_x = v_s * W_rs

    # Partial derivatives
    dV_x_dX = np.gradient(V_x, x, axis=1)

    # Rate of expansion θ
    theta = dV_x_dX

    return theta, V_x, W_rs

# Create figure
fig = plt.figure(figsize=(12, 6))

# Eulerian plot
ax1 = fig.add_subplot(121, projection='3d')
ax1.set_title("Eulerian Rate of Expansion Θ")
ax1.set_xlabel('X')
ax1.set_ylabel('Y')
ax1.set_zlabel('Θ')

# Lagrangian plot
ax2 = fig.add_subplot(122, projection='3d')
ax2.set_title("Lagrangian Rate of Expansion Θ")
ax2.set_xlabel('X (Lagrangian)')
ax2.set_ylabel('Y (Lagrangian)')
ax2.set_zlabel('Θ')

# Animation function
def animate(t):
    ax1.cla()
    ax2.cla()

    ax1.set_title("Eulerian Rate of Expansion Θ")
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Θ')

    ax2.set_title("Lagrangian Rate of Expansion Θ")
    ax2.set_xlabel('X (Lagrangian)')
    ax2.set_ylabel('Y (Lagrangian)')
    ax2.set_zlabel('Θ')

    # Eulerian fields
    theta, V_x, _ = update_fields(X, Y, t)
    ax1.plot_surface(X, Y, theta, cmap='RdYlBu', edgecolor='none')

    # Lagrangian transformation
    X_lagrangian = X + V_x * t
    Y_lagrangian = Y + V_x * t
    theta_lagrangian, _, _ = update_fields(X_lagrangian, Y_lagrangian, t)
    ax2.plot_surface(X_lagrangian, Y_lagrangian, theta_lagrangian, cmap='RdYlBu', edgecolor='none')

    ax1.set_zlim(-0.5, 0.5)
    ax2.set_zlim(-0.5, 0.5)

# Animation
anim = FuncAnimation(fig, animate, frames=np.linspace(0, 1, 100), interval=100)
plt.tight_layout()
plt.show()








def main():
    print("Run of Neweulerian inertial warp bubble")

if __name__ == "__main__":
    main()


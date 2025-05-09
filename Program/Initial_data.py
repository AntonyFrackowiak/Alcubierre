"""Initial_data"""


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# Parameters
R = 1.0
sigma = 5.0
v_s = 0.9
x = 1 
l = 0 # Warp bubble position at t=1 

# Grid
x = np.linspace(-1, 1, 1000)
y = np.linspace(-1.5, 1.5, 1000)
X, Y = np.meshgrid(x, y)

# Function to update W(r_s) and velocities
def update_fields(t):
    r_s = np.sqrt((x-v_s*t)**2 + Y**2)
    W_rs = (np.tanh(sigma * (r_s + R)) - np.tanh(sigma * (r_s - R))) / (2 * np.tanh(sigma * R))
    
    # Speed component 
    V_x = v_s * W_rs
    V_y = v_s * W_rs
    
    # Partial derivatives 
    dV_x_dx = np.gradient(V_x, x, axis=1)
    dV_x_dy = np.gradient(V_x, y, axis=0)
    
    # Rate of expansion θ
    theta = dV_x_dx
    
    # Shear σ²
    sigma2 = (dV_x_dx)**2 / 3 + (dV_x_dy)**2 / 2
    
    # Vorticity ω²
    omega2 = (dV_x_dy**2) / 2
    
    #test if 0
    
    #i = 2/3*theta**2 - (sigma2*2)+ (omega2*2) 
    #print("Test of we have 0 for i = ", i)
    
    
    return theta, sigma2, omega2, V_x, V_y



# Initial fields
t_init = 1
theta, sigma2, omega2, V_x, V_y = update_fields(t_init)

# Plot setup
fig = plt.figure(figsize=(16, 11))

ax1 = fig.add_subplot(221, projection='3d')
ax1.set_title("Rate of expansion θ")
ax1.set_xlabel('x')
ax1.set_ylabel('rho')
ax1.set_zlabel('θ')
theta_surf = ax1.plot_surface(X, Y, theta, cmap='RdYlBu')

ax2 = fig.add_subplot(222, projection='3d')
ax2.set_title("Shear σ²")
ax2.set_xlabel('x')
ax2.set_ylabel('rho')
ax2.set_zlabel('σ²')
sigma2_surf = ax2.plot_surface(X, Y, sigma2, cmap='RdYlBu')

ax3 = fig.add_subplot(224, projection='3d')
ax3.set_title("Vorticity ω²")
ax3.set_xlabel('x')
ax3.set_ylabel('rho')
ax3.set_zlabel('ω²')
omega2_surf = ax3.plot_surface(X, Y, omega2, cmap='RdYlBu')

ax4 = fig.add_subplot(223, projection='3d')
ax4.set_title("Velocity Profile")
ax4.set_xlabel('x')
ax4.set_ylabel('rho')
ax4.set_zlabel('V')
V_surf = ax4.plot_surface(X, Y, V_x, cmap='RdYlBu')

# Animation function
def animate(t):
    global theta_surf, sigma2_surf, omega2_surf, V_surf
    theta, sigma2, omega2, V_x, V_y = update_fields(t)
    
    # Remove old surfaces
    ax1.collections.clear()
    ax2.collections.clear()
    ax3.collections.clear()
    ax4.collections.clear()
    
    # Plot new surfaces
    theta_surf = ax1.plot_surface(X, Y, theta, cmap='RdYlBu')
    sigma2_surf = ax2.plot_surface(X, Y, sigma2, cmap='RdYlBu')
    omega2_surf = ax3.plot_surface(X, Y, omega2, cmap='RdYlBu')
    V_surf = ax4.plot_surface(X, Y, V_x, cmap='RdYlBu')
    
    return theta_surf, sigma2_surf, omega2_surf, V_surf

# Create animation
anim = FuncAnimation(fig, animate, frames=np.linspace(1, 10, 60), interval=1000, blit=False)

plt.tight_layout()
plt.show()



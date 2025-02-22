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
x = np.linspace(-1.5, 1.5, 500)
y = np.linspace(-1.5, 1.5, 500)
X, Y = np.meshgrid(x, y)

# Function to update W(r_s) and velocities
def update_fields(X,Y,t):
    r_s = np.sqrt(X**2 + Y**2)  # Update r_s based on t_0
    W_rs = (np.tanh(sigma * (r_s + R)) - np.tanh(sigma * (r_s - R))) / (2 * np.tanh(sigma * R))
    
    # Speed component 
    V_x = v_s * W_rs
    
    # Partial derivatives 
    dV_x_dX = np.gradient(V_x, x, axis=1)
    
    # Rate of expansion θ
    theta = dV_x_dX
    
    return theta, V_x, W_rs

# Initial fields
theta, V_x, W_rs = update_fields(X,Y,t_0)  # Use t_0 for initial condition


#print('theta zero',update_fields(R,y,t_0))

# Create figure and 3D axes
fig = plt.figure(figsize=(6, 6))

#Plot for initial theta
#ax2 = fig.add_subplot(122, projection='3d')
#ax2.set_title("Initial rate of Expansion Θ at t_0 = 0")
#ax2.set_xlabel('x')
#ax2.set_ylabel('ρ')
#ax2.set_zlabel('Θ')
#theta_surf = ax2.plot_surface(X, Y, theta, linewidth=0, antialiased=False, cmap='RdYlBu')

# Plot for time-dependent theta_time
ax1 = fig.add_subplot(111, projection='3d')
#ax1.set_title("Rate of Expansion Θ (time-dependent)")
ax1.set_xlabel('X',fontsize=15)
ax1.set_ylabel('ρ',fontsize=15)
ax1.set_zlabel('Θ (t,X)',fontsize=15)
theta_time_surf = ax1.plot_surface(X, Y, theta, linewidth=0, antialiased=False, cmap='RdYlBu')


# Add a text annotation for time
#time_text = ax1.text2D(0.05, 0.95, '', transform=ax1.transAxes)
#theta_zero_text = ax1.text2D(0.05, 0.90, '', transform=ax1.transAxes)

def animate(t):
    global theta_time_surf, time_text, theta_zero_text
    
    # Remove old surfaces
    ax1.collections.clear()
    
    # Calculate new theta for the given time t
    theta, _, _ = update_fields(X,Y,t)
    theta_time = theta / (1 + theta * (t - t_0))
    
    # Plot new surface
    theta_time_surf = ax1.plot_surface(X, Y, theta_time, linewidth=0, antialiased=False, cmap='RdYlBu')
    
    ax1.set_zlim(-5, 3)
    
    # Update time annotation
    #time_text.set_text(f't = {t:.2f}')
    
    
  
# Animation function
anim = FuncAnimation(fig, animate, frames=np.linspace(0.0, 0.45, 100), interval=100, blit=False)

plt.tight_layout()
plt.show()



def main():
    print("Run Newlagrange model of inertial warp bubble")

if __name__ == "__main__":
    main()



import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Initial parameters
R = 1
sigma = 5
v_s = 0.9
t_0 = 0.0
Y = 0.0

# Define a range for t
t = np.linspace(0.0, 0.6, 500)

# List of different X values
X_values = [-1.4, -1.2, -1.0, -0.8, -0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.7, 0.8, 0.99, 1, 1.01, 1.15, 1.2, 1.3, 1.4]

# Create figure and axis for the main plot
fig, ax_main = plt.subplots(figsize=(10, 6))

# Plot the trajectories on the main axis
for X in X_values:
    r_s = np.sqrt(X**2 + Y**2)
    W_rs = (np.tanh(sigma * (r_s + R)) - np.tanh(sigma * (r_s - R))) / (2 * np.tanh(sigma * R))
    x = X + v_s * W_rs * (t - t_0)
    ax_main.plot(x, t, linewidth=1, label=f'X = {X}')

ax_main.set_xlabel('Position (x)')
ax_main.set_ylabel('Time (t)')
ax_main.legend()

# Add dotted grid to the main plot
ax_main.grid(True, linestyle=':', alpha=0.5)

# Set limits for the zoomed-in region
zoom_xmin, zoom_xmax = 1.18, 1.22
zoom_ymin, zoom_ymax = 0.40, 0.50

# Create axis for the zoomed-in plot
ax_zoom = fig.add_axes([0.35, 0.45, 0.2, 0.3])  # [left, bottom, width, height]
ax_zoom.set_xlim(zoom_xmin, zoom_xmax)
ax_zoom.set_ylim(zoom_ymin, zoom_ymax)
ax_zoom.set_title('Position of the caustic')

# Plot the zoomed-in trajectories on the zoom axis
for X in X_values:
    r_s = np.sqrt(X**2 + Y**2)
    W_rs = (np.tanh(sigma * (r_s + R)) - np.tanh(sigma * (r_s - R))) / (2 * np.tanh(sigma * R))
    x = X + v_s * W_rs * (t - t_0)
    ax_zoom.plot(x, t, linewidth=0.8)
    plt.xticks(np.arange(zoom_xmin,zoom_xmax,0.01))

# Add grid to the zoomed-in plot
ax_zoom.grid(True, linestyle=':', alpha=0.5)

# Indicate the zoomed region in ax_main
ax_main.indicate_inset_zoom(ax_zoom, linewidth=1)

plt.show()



def main():
    print("Running the program representing caustics")

if __name__ == "__main__":
    main()





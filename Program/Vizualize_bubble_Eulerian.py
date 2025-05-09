"""Vizualize_bubble_Eulerian"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# === PARAMÈTRES ===
R = 1.5        # Rayon de la bulle warp
sigma = 5.0    # Échelle de transition de W
g = 9.81       # Accélération (inutile ici car v_s est constant)
l = 0          # Centre initial
t_0 = 0        # Temps initial
R0 = 1.0       # Rayon initial de la sphère

# === VITESSE DE LA BULLE WARP (constante ici) ===
def v_s(t):
    return 0.9

# === COORDONNÉES SPHÉRIQUES INITIALES ===
phi = np.linspace(0, np.pi, 100)
theta = np.linspace(0, 2 * np.pi, 100)
phi, theta = np.meshgrid(phi, theta)

# Coord sphériques standard
X0 = R0 * np.sin(phi) * np.cos(theta)
Y0 = R0 * np.sin(phi) * np.sin(theta)
Z0 = R0 * np.cos(phi)

# === FONCTION POUR CALCULER LA SPHÈRE DÉFORMÉE AVEC x_dynamic ===
def compute_deformed_sphere(t):
    center = l + v_s(t) * t

    # Estimation initiale de r_s
    r_s_base = np.sqrt((X0 - center)**2 + Y0**2 + Z0**2)
    W_rs_guess = (np.tanh(sigma * (r_s_base + R)) - np.tanh(sigma * (r_s_base - R))) / (2 * np.tanh(sigma * R))

    # Correction dynamique
    x_dynamic = X0 + v_s(t) * W_rs_guess * (t - t_0)

    # r_s corrigé et W final
    r_s = np.sqrt((x_dynamic - center)**2 + Y0**2 + Z0**2)
    W_rs = (np.tanh(sigma * (r_s + R)) - np.tanh(sigma * (r_s - R))) / (2 * np.tanh(sigma * R))

    # Appliquer la déformation radiale
    R_def = R0 * W_rs
    X_def = R_def * np.sin(phi) * np.cos(theta)
    Y_def = R_def * np.sin(phi) * np.sin(theta)
    Z_def = R_def * np.cos(phi)

    return X_def, Y_def, Z_def, W_rs

# === FIGURE INITIALE ===
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.set_box_aspect([1, 1, 1])

# === ANIMATION ===
def animate(t):
    ax.clear()
    X_def, Y_def, Z_def, W_rs = compute_deformed_sphere(t)

    ax.plot_surface(X_def, Y_def, Z_def,
                    facecolors=plt.cm.plasma(W_rs),
                    rstride=1, cstride=1, antialiased=True, shade=False)

    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_zlim([-1, 1])
    ax.set_title(f"Déformation de la sphère W(rₛ), t = {t:.2f}s")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")

    return []

frames = np.linspace(0, 1.5, 50)
ani = FuncAnimation(fig, animate, frames=frames, interval=80, blit=False)

plt.tight_layout()
plt.show()

# === POUR SAUVEGARDER EN GIF ===
# from matplotlib.animation import PillowWriter
# writer = PillowWriter(fps=10)
# ani.save("deformation_sphere_Wrs.gif", writer=writer)


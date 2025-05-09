
"""Initial data acceleration """

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation, PillowWriter

# Paramètres
R = 1.0
sigma = 5.0
g = 9.81
l = 0  # Position initiale de la bulle

# Vitesse du warp bubble
def v_s(t):
    return 0.9 + g * t

# Grille
x_vals = np.linspace(-2.5, 25.5, 300)  # Réduction de la résolution de la grille
y_vals = np.linspace(-2.5, 2.5, 300)   # Réduction de la résolution de la grille
X, Y = np.meshgrid(x_vals, y_vals)

# Fonction pour mettre à jour les champs à l'instant t
def update_fields(t):
    center = l + v_s(t) * t
    r_s = np.sqrt((X - center)**2 + Y**2)
    W_rs = (np.tanh(sigma * (r_s + R)) - np.tanh(sigma * (r_s - R))) / (2 * np.tanh(sigma * R))
    
    V_x = v_s(t) * W_rs
    V_y = v_s(t) * W_rs  # Symétrique pour l'instant ; ajuster si nécessaire
    
    dV_x_dx = np.gradient(V_x, x_vals, axis=1)
    dV_x_dy = np.gradient(V_x, y_vals, axis=0)
    
    theta = dV_x_dx
    sigma2 = (dV_x_dx)**2 / 3 + (dV_x_dy)**2 / 2
    omega2 = (dV_x_dy**2) / 2
    
    return theta, sigma2, omega2, V_x, V_y

# Initialisation de la figure
fig = plt.figure(figsize=(10, 8))
ax1 = fig.add_subplot(projection='3d')
ax1.set_title("Taux d'expansion Θ")
ax1.set_xlabel('x')
ax1.set_ylabel('⍴')
ax1.set_zlabel('Θ')

# Frame initiale
theta_init, _, _, _, _ = update_fields(0)
theta_surf = ax1.plot_surface(X, Y, theta_init, cmap='plasma', antialiased=True, linewidth=0, rstride=5, cstride=5)  # Augmenter les pas pour accélérer

# Fonction d'animation
def animate(t):
    ax1.clear()
    theta, _, _, _, _ = update_fields(t)
    ax1.set_title(f"Taux d'expansion Θ à t = {t:.2f}s")
    ax1.set_xlabel('x')
    ax1.set_ylabel('⍴')
    ax1.set_zlabel('Θ')
    
    surf = ax1.plot_surface(X, Y, theta, cmap='plasma', antialiased=True, linewidth=0, rstride=5, cstride=5)  # Augmenter les pas
    return surf,

# Création de l'animation
anim = FuncAnimation(fig, animate, frames=np.linspace(0, 4, 600), interval=30, blit=False)
"""
# Utilisation de PillowWriter avec les paramètres appropriés pour fps
#writer = PillowWriter(fps=30)  # Définir fps ici
#anim.save('warp_bubble_animation.gif', writer=writer)
"""
plt.show()
plt.close()  # Ferme la fenêtre d'animation



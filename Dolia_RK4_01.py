# Dolia_RK4_01.py DOLIA-AUSTRIACA 05-11-26
import numpy as np
import matplotlib.pyplot as plt
# 1. Parameter der Dolia Austriaca
x_start = -60.0  # Linker Boden bei -60 cm
x_end = 60.0     # Rechter Deckel bei +60 cm
Länge = 120.0    # Gesamtlänge h = 120 cm
# Radiales Parabol-Dauben-Profil (Radius in Abh. von x)
def r(x):
    return 40.0 - (10.0 / 3600.0) * (x**2)
# Differenzialgleichung: Volumen-Änderung dV/dx per x
def dV_dx(x):
    return np.pi * (r(x)**2)
# 2. Runge-Kutta-4 (RK4) Simulation
num_steps = 100
h_step = Länge / num_steps
# Arrays zur Speicherung der berechneten Werte
x_vals = np.linspace(x_start, x_end, num_steps + 1)
V_vals = np.zeros(num_steps + 1)
# RK4-Schleife (Integration)
for i in range(num_steps):
    x = x_vals[i]
    V = V_vals[i]
    k1 = dV_dx(x)
    k2 = dV_dx(x + h_step/2.0)
    k3 = dV_dx(x + h_step/2.0)
    k4 = dV_dx(x + h_step)    
    # RK4-Gewichtung bei Schritt nach vorne
    V_vals[i+1] = V + (h_step / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
# Umrechnung Volumen cm³ in Liter (1 Liter = 1000 cm³)
V_liter = V_vals / 1000.0
# 3. Schnittbild und Plot der Integrations-Schleife
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
# Oberes Diagramm: Fassprofil
ax1.plot(x_vals, r(x_vals), 'brown', lw=2.5, label='Fassdaube r(x)')
ax1.plot(x_vals, -r(x_vals), 'brown', lw=2.5) # Untere Symmetriehälfte
ax1.axvline(x=x_start, color='black', linestyle='--')
ax1.axvline(x=x_end, color='black', linestyle='--')
ax1.fill_between(x_vals, r(x_vals), -r(x_vals),
                     color='bisque', alpha=0.5, label='Weinvolumen')
ax1.set_ylabel('Fassradius / Abmessung (cm)', fontsize=11)
ax1.set_title('RK4-Approx. Volumen Dolia Austriaca mit Parabol-Dauben',
                     fontsize=12, fontweight='bold')
ax1.grid(True, linestyle=':', alpha=0.6)
ax1.legend(loc='upper right')
# Unteres Diagramm: Stand der Approximation (Volumenkurve)
ax2.plot(x_vals, V_liter, 'blue', lw=3, label='Vol.approx. V(x)')
# Markierungspunkte entlang der RK4-Schleife
ax2.scatter(x_vals[::10], V_liter[::10], color='red',
                          zorder=5, label='RK4-Stützstellen-Auswahl')
ax2.set_xlabel('Pos. entlang Längsachse x (cm)', fontsize=11)
ax2.set_ylabel('Volumen kumuliert (Liter)', fontsize=11)
ax2.grid(True, linestyle=':', alpha=0.6)
ax2.legend(loc='lower right')
# Endwert im Diagramm als Text einblenden
final_volume = V_liter[-1]
ax2.annotate(f'Endstand: {final_volume:.2f} Liter', 
    xy=(x_end, final_volume), xytext=(20, final_volume - 200),
    arrowprops=dict(facecolor='black', shrink=0.05,
                                        width=0.25, headwidth=6))
plt.tight_layout()
plt.show()

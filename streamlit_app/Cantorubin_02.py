# Cantorubin_02.py Kartoffel-Distanz _ die Zweite
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

np.random.seed(12)
n_kartoffeln = 150
p_stufen = np.linspace(0.001, 0.999, 1000)

# =========================================================================
# LIEFERUNG A: Die brave Ernte (Folgt fast perfekt dem Idealrauschen)
# =========================================================================
ernte_a = np.random.normal(loc=500, scale=50, size=n_kartoffeln) # ca. 500g im Schnitt

mu_a, sigma_a = np.mean(ernte_a), np.std(ernte_a)
x_ideal_a = stats.norm.ppf(p_stufen, loc=mu_a, scale=sigma_a)
x_real_a = np.percentile(ernte_a, p_stufen * 100)
Kartoffel_dist_a = np.mean(np.abs(x_real_a - x_ideal_a))

# =========================================================================
# LIEFERUNG B: Der Ausreißer-Schock (Gleicher Schnitt, aber extreme Enden)
# =========================================================================
# Wir nehmen gleichmäßige Kartoffeln, mischen aber extreme Riesen & Minis unter
ernte_b = np.random.normal(loc=500, scale=25, size=n_kartoffeln - 10)
ausreisser = [150, 160, 180, 190, 200, 800, 810, 820, 830, 850] # Extreme Knollen
ernte_b = np.concatenate([ernte_b, ausreisser])

mu_b, sigma_b = np.mean(ernte_b), np.std(ernte_b)
x_ideal_b = stats.norm.ppf(p_stufen, loc=mu_b, scale=sigma_b)
x_real_b = np.percentile(ernte_b, p_stufen * 100)
Kartoffel_dist_b = np.mean(np.abs(x_real_b - x_ideal_b))

# =========================================================================
# DIE GRAFIK: Beide Lagerhäuser im Vergleich
# =========================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6), sharey=True)

# Plot für Lieferung A
ax1.plot(x_ideal_a, p_stufen, label='Idealer Haufen', color='blue', lw=2)
ax1.plot(x_real_a, p_stufen, label='Echte Ernte A', color='orange', lw=2)
ax1.fill_betweenx(p_stufen, x_ideal_a, x_real_a, color='orange', alpha=0.3)
ax1.set_title(f'Lieferung A: Brave Ernte\nKartoffel-Distanz: {Kartoffel_dist_a:.2f}g', fontsize=12, fontweight='bold')
ax1.set_xlabel('Kartoffelgewicht in Gramm (X-Achse)')
ax1.set_ylabel('Kumulierter Bestand (Y-Achse)')
ax1.grid(True, linestyle='--', alpha=0.5)
ax1.legend()

# Plot für Lieferung B
ax2.plot(x_ideal_b, p_stufen, label='Idealer Haufen', color='blue', lw=2)
ax2.plot(x_real_b, p_stufen, label='Echte Ernte B (Ausreißer)', color='red', lw=2)
ax2.fill_betweenx(p_stufen, x_ideal_b, x_real_b, color='red', alpha=0.3)
ax2.set_title(f'Lieferung B: Ausreißer-Schock\nKartoffel-Distanz: {Kartoffel_dist_b:.2f}g', fontsize=12, fontweight='bold')
ax2.set_xlabel('Kartoffelgewicht in Gramm (X-Achse)')
ax2.grid(True, linestyle='--', alpha=0.5)
ax2.legend()

plt.suptitle('Der Kartoffel-Verlagerungs-Vergleich', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.show()

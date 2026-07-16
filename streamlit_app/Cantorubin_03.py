# Cantorubin_03.py Kartoffel-Distanz _ die Dritte
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

# 1. Setup & stabile Zufallswerte für die Ernten
np.random.seed(12)
n_kartoffeln = 150
p_stufen = np.linspace(0.001, 0.999, 1000)

# -------------------------------------------------------------------------
# ERNTE A: Die brave Ernte (ca. 500g im Schnitt)
# -------------------------------------------------------------------------
ernte_a = np.random.normal(loc=500, scale=50, size=n_kartoffeln)
mu_a, sigma_a = np.mean(ernte_a), np.std(ernte_a)
x_ideal_a = stats.norm.ppf(p_stufen, loc=mu_a, scale=sigma_a)
x_real_a = np.percentile(ernte_a, p_stufen * 100)

# -------------------------------------------------------------------------
# ERNTE B: Der Ausreißer-Schock (Gleicher Kern, aber extreme Enden)
# -------------------------------------------------------------------------
ernte_b = np.random.normal(loc=500, scale=25, size=n_kartoffeln - 10)
# Hier kommen die geschmuggelten Winzlinge und Riesen-Klopper:
ausreisser = np.array([200, 210, 220, 230, 240, 760, 770, 780, 790, 800])
ernte_b = np.concatenate([ernte_b, ausreisser])

mu_b, sigma_b = np.mean(ernte_b), np.std(ernte_b)
x_ideal_b = stats.norm.ppf(p_stufen, loc=mu_b, scale=sigma_b)
x_real_b = np.percentile(ernte_b, p_stufen * 100)

# -------------------------------------------------------------------------
# DER WIRTSCHAFTLICHE OMA-TRICK: Die Preiskurve
# Wir sagen: Jedes Gramm Abweichung kostet uns im Schnitt 0,02 Euro (2 Cent)
# -------------------------------------------------------------------------
preis_pro_gramm_abweichung = 0.02 

# Berechnung der finanziellen Schaufel-Verluste
geld_flaeche_a = np.abs(x_real_a - x_ideal_a) * preis_pro_gramm_abweichung
geld_flaeche_b = np.abs(x_real_b - x_ideal_b) * preis_pro_gramm_abweichung

monetaere_kartoffel_dist_a = np.mean(geld_flaeche_a)
monetaere_kartoffel_dist_b = np.mean(geld_flaeche_b)

# -------------------------------------------------------------------------
# DIE GRAFIK: Das finanzielle Kartoffel-Lagerhaus
# -------------------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6), sharey=True)

# Plot für Lieferung A (Brave Ernte)
ax1.plot(x_ideal_a, p_stufen, label='Idealer Haufen', color='blue', lw=2)
ax1.plot(x_real_a, p_stufen, label='Echte Ernte A', color='orange', lw=2)
ax1.fill_betweenx(p_stufen, x_ideal_a, x_real_a, color='orange', alpha=0.3)
ax1.set_title(f'Lieferung A: Brave Ernte\nSortierverlust: {monetaere_kartoffel_dist_a:.2f} € / Knolle', fontsize=12, fontweight='bold')
ax1.set_xlabel('Kartoffelgewicht in Gramm (X-Achse)')
ax1.set_ylabel('Milliardstel Kartoffelvermögen (Y-Achse)')
ax1.grid(True, linestyle='--', alpha=0.5)
ax1.legend()

# Plot für Lieferung B (Ausreißer-Ernte)
ax2.plot(x_ideal_b, p_stufen, label='Idealer Haufen', color='blue', lw=2)
ax2.plot(x_real_b, p_stufen, label='Echte Ernte B', color='red', lw=2)
ax2.fill_betweenx(p_stufen, x_ideal_b, x_real_b, color='red', alpha=0.3)
ax2.set_title(f'Lieferung B: Ausreißer-Schock\nSortierverlust: {monetaere_kartoffel_dist_b:.2f} € / Knolle', fontsize=12, fontweight='bold')
ax2.set_xlabel('Kartoffelgewicht in Gramm (X-Achse)')
ax2.grid(True, linestyle='--', alpha=0.5)
ax2.legend()
plt.suptitle('Monetäre Kartoffel-Distanz (Wasserstein in Euro)', fontsize=12, y=0.92)
plt.tight_layout()
plt.show()


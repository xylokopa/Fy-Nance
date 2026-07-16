# Cantorubin_01.py Kartoffel-Distanz _ die Erste 
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

# -------------------------------------------------------------------------
# 1. Beispiel-Daten erzeugen (Ersetze dies durch 'diff_data')
# Wir erzeugen absichtlich leicht schiefe Daten, um Abweichungen zu sehen
np.random.seed(42)
diff_data = np.random.normal(loc=10, scale=3, size=150) + np.random.exponential(scale=1.5, size=150)

# Parameter aus Daten schätzen
mu, sigma = np.mean(diff_data), np.std(diff_data)
# -------------------------------------------------------------------------

# 2. Netz aus Wahrscheinlichkeits-Stufen (Y-Achse von 0% bis 100%)
p_stufen = np.linspace(0.001, 0.999, 1000)

# 3. Sondierung über die Umkehrfunktion (PPF) -> Werte auf der X-Achse
# Wo müssten die Werte laut normalverteiltem Idealrauschen liegen?
x_ideal = stats.norm.ppf(p_stufen, loc=mu, scale=sigma)

# Wo liegen deine echten Werte auf dieser Prozentstufe tatsächlich?
x_real = np.percentile(diff_data, p_stufen * 100)

# 4. Trans-Port-Distanz berechnen (Mittlerer horizontaler Verschiebungsweg)
Kartoffel_dist = np.mean(np.abs(x_real - x_ideal))

# 5. Das Ganze bildlich darstellen
plt.figure(figsize=(10, 6))

# Die beiden Umkehrkurven zeichnen (Achtung: p_stufen ist hier auf der Y-Achse!)
plt.plot(x_ideal, p_stufen, label='Ideales Rauschen (Normalverteilung)', color='blue', lw=2)
plt.plot(x_real, p_stufen, label='EchtDaten(Empirisch)', color='orange', lw=2)

# Die horizontale Schaufelarbeit/Verschiebung farbig ausfüllen
plt.fill_betweenx(p_stufen, x_ideal, x_real, color='orange', alpha=0.3, 
    label=f'Kartoffel-Verlagerung als Fläche\n(Kartoffel-Distanz: {Kartoffel_dist:.3f})')

# Diagramm hübsch machen
plt.title('Kartoffel-Distanz: Horizontale Kartoffel-Verschiebung', fontsize=14, fontweight='bold')
plt.xlabel('Messgröße(zB Kartoffelmenge)/Universelle Kartoffeleinheit(X-Achse)', fontsize=12)
plt.ylabel('Wertanteil v. 1 Mrd.Kartoffelvermögen/Kumuliert bis 1 Mrd(Y-Achse)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(fontsize=11, loc='upper left')

# Anzeigen
plt.tight_layout()
plt.show()

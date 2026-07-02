# Fliesenleger-Mosaik.py Proj.BOszi_03 R.Wu 02-07-26
import matplotlib.pyplot as plt

# 1. Zeilenkollinear geschriebens Layout (Kachel-Matrix)
layout = [
    ['.', '3Win', '1Win', '1Win', '4Win'],
    ['.', '2Win', '1Win', '1Win', '5Win'],
    ['.', '.',    '.',    '.',    '.'   ]  # Die leere Fußzeile/Fuge
]

# Dimensionsneutrale Vergabe von Verhältnissen ( Normalisierung)
breitverh = [0.525] * 1 + [1.25] * 1 + [1] * 2 + [1.25] * 1  # Ergibt 5 Elemente
hoeheverh = [1] * 2 + [0.5] * 1                              # Ergibt 3 Elemente

# 2. Vererbung an das tatsächlich eingeräumte Fenster(Kundenspezifisch)
# durch den constrained-layout-manager 
fig, axd = plt.subplot_mosaic(
    layout, 
    figsize=(15, 8),
    gridspec_kw={'width_ratios': breitverh, 'height_ratios': hoeheverh},
    layout='constrained'
)

# Pixel-Berechnung dazu im Speicher (virtueller Fliesenleger)
fig.canvas.draw()

# 3. Ausgabe der echten Pixel-Adressen in der IDLE-Konsole
print("--- ABSOLUTE PIXEL-ADRESSEN IM OSZILLOGRAPHEN-COCKPIT ---")
print("--MIT LINKS und UNTEN freigehaltenem Platz für WIDGETS --")

for name, ax in sorted(axd.items()):
    bbox = ax.get_window_extent()
    print(f"Fenster '{name}':")
    print(f"  -> X-Achse (Breite): {bbox.x0:.1f} px bis {bbox.x1:.1f} px ({bbox.width:.1f} px breit)")
    print(f"  -> Y-Achse (Höhe):   {bbox.y0:.1f} px bis {bbox.y1:.1f} px ({bbox.height:.1f} px hoch)\n")

# Diagramm anzeigen
plt.show()

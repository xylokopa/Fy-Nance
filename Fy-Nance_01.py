# Fy-Nance_01.py 02-06-2026 Prototyp Ticker-Oszillograph
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from datetime import datetime

# 1. Apple CSV-Datei einlesen
df = pd.read_csv('02Apple_Offline.csv')

# Datum in echte Zeitobjekte umwandeln (behebt den Fehler)
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')

# Sicherstellen, dass die Daten nach Datum sortiert sind
df = df.sort_values('Date').reset_index(drop=True)

# 2. Matplotlib-Fenster aufbauen
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.25)  # Platz für Widgets unten freimachen

# Initialer Plot mit allen Daten
line, = ax.plot(df['Date'], df['Price'], label='preis', color='blue')
ax.set_ylabel('Preis in €')
ax.grid(True, linestyle='--')
ax.legend(loc='upper left')

# X-Achsen-Beschriftung sauber formatieren
fig.autofmt_xdate()

# 3. Widgets (Slider & Textboxen) exakt positionieren
ax_von = plt.axes([0.15, 0.05, 0.25, 0.03])   # Schieberegler 'von'
ax_bis = plt.axes([0.60, 0.05, 0.25, 0.03])   # Schieberegler 'bis'
ax_btn = plt.axes([0.45, 0.04, 0.10, 0.05])   # Vorschau-Button

# Slider initialisieren (Nutzt Zeilen-Indizes von 0 bis Tabellenende)
slider_von = Slider(ax_von, 'von', 0, len(df)-1, valinit=0, valfmt='%0.0f')
slider_bis = Slider(ax_bis, 'bis', 0, len(df)-1, valinit=len(df)-1, valfmt='%0.0f')
btn_vorschau = Button(ax_btn, 'VORSCHAU')

# Weiße Kontrollfenster (Labels) über den Slidern platzieren
text_anfang = fig.text(0.18, 0.12, '', bbox=dict(facecolor='white', alpha=1.0, edgecolor='black'))
text_mitte = fig.text(0.36, 0.12, '', bbox=dict(facecolor='white', alpha=1.0, edgecolor='black'))
text_ende = fig.text(0.72, 0.12, '', bbox=dict(facecolor='white', alpha=1.0, edgecolor='black'))

# 4. Interaktive Update-Logik
def update(val):
    idx_von = int(slider_von.val)
    idx_bis = int(slider_bis.val)
    
    # Verhindern, dass 'von' rechts von 'bis' liegt
    if idx_von > idx_bis:
        idx_von = idx_bis
        slider_von.set_val(idx_von)
        
    # Aktiven Datenbereich ausschneiden
    df_filtered = df.iloc[idx_von:idx_bis+1]
    
    if not df_filtered.empty:
        # Datums-Objekte extrahieren
        dt_start = df_filtered['Date'].iloc[0]
        dt_end = df_filtered['Date'].iloc[-1]
        
        # Strings für die Textfelder formatieren
        str_start = dt_start.strftime('%Y-%m-%d')
        str_end = dt_end.strftime('%Y-%m-%d')
        
        # Echte Kalendertage berechnen (Enddatum minus Startdatum)
        tage_differenz = (dt_end - dt_start).days
        
        # Zoom der Grafikachsen anpassen
        ax.set_xlim(dt_start, dt_end)
        ax.set_ylim(df_filtered['Price'].min() * 0.95, df_filtered['Price'].max() * 1.05)
        
        # Fenster-Titel aktualisieren
        ax.set_title(f"fig0 {str_start} + {tage_differenz} Tage = {str_end}")
        
        # Inhalt der drei Kontrollfenster aktualisieren
        text_anfang.set_text(f" {str_start} ")
        text_mitte.set_text(f" {str_start} + {tage_differenz} Tage = {str_end} ")
        text_ende.set_text(f" {str_end} ")
        
    fig.canvas.draw_idle()

# Funktionen an Slider-Bewegung koppeln
slider_von.on_changed(update)
slider_bis.on_changed(update)

# Beim ersten Start einmalig ausführen, um Layout zu befüllen
update(None)

plt.show()

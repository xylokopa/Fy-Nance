# Fy-Nance_02.py 02-06-2026 Projekt Ticker-Oszillograph
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.widgets import Slider, Button, TextBox
from datetime import datetime

# 1. Apple CSV-Datei einlesen
df = pd.read_csv('02Apple_Offline.csv')
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
df = df.sort_values('Date').reset_index(drop=True)

# 2. Matplotlib-Fenster aufbauen
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.25)  # Platz für Widgets unten freimachen

# Initialer Plot mit allen Daten
line, = ax.plot(df['Date'], df['Price'], label='preis', color='blue')
ax.set_ylabel('Preis in €')
ax.grid(True, linestyle='--')
ax.legend(loc='upper left')

# X-Achse: Nur Jahreszahlen anzeigen und waagerecht (rotation=0) ausrichten
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.setp(ax.get_xticklabels(), rotation=0, ha='center')

# Flag, um Endlos-Update-Schleifen zwischen Slider und TextBox zu verhindern
is_updating = False

# 3. Widgets (Slider, Eingabefelder & Textbox) positionieren
ax_von = plt.axes([0.15, 0.05, 0.25, 0.03])    # Slider 'von'
ax_bis = plt.axes([0.60, 0.05, 0.25, 0.03])    # Slider 'bis'
ax_btn = plt.axes([0.45, 0.04, 0.10, 0.05])    # Vorschau-Button

# Slider initialisieren
slider_von = Slider(ax_von, 'von', 0, len(df)-1, valinit=0, valfmt='%0.0f')
slider_bis = Slider(ax_bis, 'bis', 0, len(df)-1, valinit=len(df)-1, valfmt='%0.0f')
btn_vorschau = Button(ax_btn, 'VORSCHAU')

# INPUT-FELDER (TextBox) für Start und Ende links und rechts platrieren
ax_box_start = plt.axes([0.16, 0.12, 0.10, 0.04])
ax_box_end = plt.axes([0.73, 0.12, 0.10, 0.04])

text_box_start = TextBox(ax_box_start, '', initial='')
text_box_end = TextBox(ax_box_end, '', initial='')

# Mittleres reines Textfenster (Label) für die Tageszählung
text_mitte = fig.text(0.35, 0.12, '', bbox=dict(facecolor='white', alpha=1.0, edgecolor='black'))

# 4. Zentrale Update-Funktion für Grafik und Widgets
def update_plot(idx_von, idx_bis):
    global is_updating
    if is_updating:
        return
    is_updating = True

    # Grenzen absichern
    idx_von = max(0, min(idx_von, len(df)-1))
    idx_bis = max(0, min(idx_bis, len(df)-1))
    if idx_von > idx_bis:
        idx_von = idx_bis

    # Slider-Positionen synchronisieren
    slider_von.set_val(idx_von)
    slider_bis.set_val(idx_bis)

    # Daten filtern
    df_filtered = df.iloc[idx_von:idx_bis+1]
    
    if not df_filtered.empty:
        dt_start = df_filtered['Date'].iloc[0]
        dt_end = df_filtered['Date'].iloc[-1]
        
        str_start = dt_start.strftime('%Y-%m-%d')
        str_end = dt_end.strftime('%Y-%m-%d')
        tage_differenz = (dt_end - dt_start).days
        
        # Achsenskalierung anpassen
        ax.set_xlim(dt_start, dt_end)
        ax.set_ylim(df_filtered['Price'].min() * 0.95, df_filtered['Price'].max() * 1.05)
        
        # Titel & Mittelelement aktualisieren
        ax.set_title(f"fig0 {str_start} + {tage_differenz} Tage = {str_end}")
        text_mitte.set_text(f" {str_start} + {tage_differenz} Tage = {str_end} ")
        
        # Text in den Input-Boxen aktualisieren, falls sie nicht fokussiert sind
        if text_box_start.text_disp.get_text() != str_start:
            text_box_start.set_val(str_start)
        if text_box_end.text_disp.get_text() != str_end:
            text_box_end.set_val(str_end)
            
    fig.canvas.draw_idle()
    is_updating = False

# 5. Event-Handler für Slider-Bewegungen
def on_slider_change(val):
    update_plot(int(slider_von.val), int(slider_bis.val))

slider_von.on_changed(on_slider_change)
slider_bis.on_changed(on_slider_change)

# 6. Event-Handler für die TextInput-Felder (Bestätigung mit ENTER)
def on_submit_start(text_input):
    try:
        target_date = pd.to_datetime(text_input.strip(), format='%Y-%m-%d')
        # Finde den nächstgelegenen Index in der CSV für das eingegebene Datum
        idx = (df['Date'] - target_date).abs().idxmin()
        update_plot(idx, int(slider_bis.val))
    except ValueError:
        # Bei falschem Datumsformat Eingabe zurücksetzen
        update_plot(int(slider_von.val), int(slider_bis.val))

def on_submit_end(text_input):
    try:
        target_date = pd.to_datetime(text_input.strip(), format='%Y-%m-%d')
        idx = (df['Date'] - target_date).abs().idxmin()
        update_plot(int(slider_von.val), idx)
    except ValueError:
        update_plot(int(slider_von.val), int(slider_bis.val))

text_box_start.on_submit(on_submit_start)
text_box_end.on_submit(on_submit_end)

# Initialer Aufruf beim Start
update_plot(0, len(df)-1)

plt.show()

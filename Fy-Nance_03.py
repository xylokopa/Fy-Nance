# Fy-Nance_03.py 02-06-2026 Projekt Ticker-Oszillograph
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker  # Korrekter Import für den NullFormatter
from matplotlib.widgets import Slider, Button, TextBox

# 1. Apple CSV-Datei einlesen
df = pd.read_csv('02Apple_Offline.csv')
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
df = df.sort_values('Date').reset_index(drop=True)

# 2. Matplotlib-Fenster aufbauen
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.25)

# Initialer Plot
line, = ax.plot(df['Date'], df['Price'], label='preis', color='blue')
ax.set_ylabel('Preis in €')
ax.grid(True, linestyle='--')
ax.legend(loc='upper left')

# Flag gegen Endlosschleifen
is_updating = False

# 3. Widgets positionieren
ax_von = plt.axes([0.15, 0.05, 0.25, 0.03])
ax_bis = plt.axes([0.60, 0.05, 0.25, 0.03])
ax_btn = plt.axes([0.45, 0.04, 0.10, 0.05])

slider_von = Slider(ax_von, 'von', 0, len(df)-1, valinit=0, valfmt='%0.0f')
slider_bis = Slider(ax_bis, 'bis', 0, len(df)-1, valinit=len(df)-1, valfmt='%0.0f')
btn_vorschau = Button(ax_btn, 'VORSCHAU')

ax_box_start = plt.axes([0.16, 0.12, 0.10, 0.04])
ax_box_end = plt.axes([0.73, 0.12, 0.10, 0.04])

text_box_start = TextBox(ax_box_start, '', initial='')
text_box_end = TextBox(ax_box_end, '', initial='')

text_mitte = fig.text(0.35, 0.12, '', bbox=dict(facecolor='white', alpha=1.0, edgecolor='black'))

# 4. Dynamische Ticks für die X-Achse berechnen
def update_x_ticks(dt_start, dt_end):
    tage_fenster = (dt_end - dt_start).days
    
    # Hauptstriche (Major Ticks) sind immer die Jahre (waagerecht)
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    
    if tage_fenster < 730:  # Weniger als 2 Jahre angezeigter Bereich
        # Monatsstriche werden sichtbar und als Nummer (01-12) beschriftet
        ax.xaxis.set_minor_locator(mdates.MonthLocator())
        ax.xaxis.set_minor_formatter(mdates.DateFormatter('%m'))
        
        # Grid für Haupt- und Nebenstriche anpassen
        ax.grid(True, which='both', linestyle='--', alpha=0.5)
    else:
        # Bei >= 2 Jahren: Monate nur als kleine Striche OHNE Beschriftung
        ax.xaxis.set_minor_locator(mdates.MonthLocator())
        ax.xaxis.set_minor_formatter(mticker.NullFormatter())  # ABSOLUT KORREKT HIER
        ax.grid(True, which='major', linestyle='--')

    # Formatierung der Achsenbeschriftungen fixieren (waagerecht)
    plt.setp(ax.get_xticklabels(), rotation=0, ha='center')
    plt.setp(ax.get_xminorticklabels(), rotation=0, ha='center', fontsize=8, color='gray')

# 5. Zentrale Update-Funktion
def update_plot(idx_von, idx_bis):
    global is_updating
    if is_updating:
        return
    is_updating = True

    idx_von = max(0, min(idx_von, len(df)-1))
    idx_bis = max(0, min(idx_bis, len(df)-1))
    if idx_von > idx_bis:
        idx_von = idx_bis

    slider_von.set_val(idx_von)
    slider_bis.set_val(idx_bis)

    df_filtered = df.iloc[idx_von:idx_bis+1]
    
    if not df_filtered.empty:
        dt_start = df_filtered['Date'].iloc[0]
        dt_end = df_filtered['Date'].iloc[-1]
        
        str_start = dt_start.strftime('%Y-%m-%d')
        str_end = dt_end.strftime('%Y-%m-%d')
        tage_differenz = (dt_end - dt_start).days
        
        ax.set_xlim(dt_start, dt_end)
        ax.set_ylim(df_filtered['Price'].min() * 0.95, df_filtered['Price'].max() * 1.05)
        
        # Ticks basierend auf dem neuen Zoom anpassen
        update_x_ticks(dt_start, dt_end)
        
        ax.set_title(f"fig0 {str_start} + {tage_differenz} Tage = {str_end}")
        text_mitte.set_text(f" {str_start} + {tage_differenz} Tage = {str_end} ")
        
        if text_box_start.text_disp.get_text() != str_start:
            text_box_start.set_val(str_start)
        if text_box_end.text_disp.get_text() != str_end:
            text_box_end.set_val(str_end)
            
    fig.canvas.draw_idle()
    is_updating = False

# 6. Event-Handler koppeln
def on_slider_change(val):
    update_plot(int(slider_von.val), int(slider_bis.val))

slider_von.on_changed(on_slider_change)
slider_bis.on_changed(on_slider_change)

def on_submit_start(text_input):
    try:
        target_date = pd.to_datetime(text_input.strip(), format='%Y-%m-%d')
        idx = (df['Date'] - target_date).abs().idxmin()
        update_plot(idx, int(slider_bis.val))
    except ValueError:
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

# Startkonfiguration (Zeigt initial alle Daten)
update_plot(0, len(df)-1)

plt.show()

# Fy-Nance_04.py 02-06-2026 Projekt Ticker-Oszillograph
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from matplotlib.widgets import Slider, Button, TextBox

# 1. Apple CSV-Datei einlesen
df = pd.read_csv('02Apple_Offline.csv')
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
df = df.sort_values('Date').reset_index(drop=True)

# 2. Hauptfenster (Figur 1) aufbauen
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.25)

# Initialer Plot im Hauptfenster
line, = ax.plot(df['Date'], df['Price'], label='preis', color='blue')
ax.set_ylabel('Preis in €')
ax.grid(True, linestyle='--')
ax.legend(loc='upper left')

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

# Hilfsfunktion für die dynamische X-Achsen-Skalierung
def apply_axis_ticks(target_ax, dt_start, dt_end):
    tage_fenster = (dt_end - dt_start).days
    target_ax.xaxis.set_major_locator(mdates.YearLocator())
    target_ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    
    if tage_fenster < 730:
        target_ax.xaxis.set_minor_locator(mdates.MonthLocator())
        target_ax.xaxis.set_minor_formatter(mdates.DateFormatter('%m'))
        target_ax.grid(True, which='both', linestyle='--', alpha=0.5)
    else:
        target_ax.xaxis.set_minor_locator(mdates.MonthLocator())
        target_ax.xaxis.set_minor_formatter(mticker.NullFormatter())
        target_ax.grid(True, which='major', linestyle='--')

    plt.setp(target_ax.get_xticklabels(), rotation=0, ha='center')
    plt.setp(target_ax.get_xminorticklabels(), rotation=0, ha='center', fontsize=8, color='gray')

# 4. Funktion für das zweite Fenster (VOLATILITÄT) bei Klick auf VORSCHAU
def on_vorschau_clicked(event):
    idx_von = int(slider_von.val)
    idx_bis = int(slider_bis.val)
    
    # Daten für den gewählten Zeitraum ausschneiden
    df_filtered = df.iloc[idx_von:idx_bis+1].copy()
    if df_filtered.empty:
        return

    # Berechnungen für die Volatilität
    miwe_val = df_filtered['Price'].mean()
    df_filtered['miwe'] = miwe_val
    
    # Tägliche Differenz berechnen und um den Mittelwert verschieben (Zentrierung)
    df_filtered['diff_raw'] = df_filtered['Price'].diff().fillna(0)
    df_filtered['diffz'] = miwe_val + df_filtered['diff_raw']

    # Zweites Fenster erstellen
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    fig2.canvas.manager.set_window_title('Figur 2 - Volatilitätsuntersuchung')

    # Linien zeichnen entsprechend der Vorgabe im Bild
    ax2.plot(df_filtered['Date'], df_filtered['miwe'], label='miwe', color='black', linewidth=1)
    ax2.plot(df_filtered['Date'], df_filtered['diffz'], label='diffz', color='blue', linewidth=1.2)
    ax2.plot(df_filtered['Date'], df_filtered['Price'], label='preis', color='red', linewidth=2.5)

    # Styling und Beschriftungen
    str_start = df_filtered['Date'].iloc[0].strftime('%Y-%m-%d')
    str_end = df_filtered['Date'].iloc[-1].strftime('%Y-%m-%d')
    
    ax2.set_title(f"fig1 Preis-Entwicklung , Mittelwert und Differenz-Werte vom {str_start} bis {str_end}")
    ax2.set_ylabel('Preis in €')
    ax2.legend(loc='upper left')
    
    # Grenzen setzen
    ax2.set_xlim(df_filtered['Date'].iloc[0], df_filtered['Date'].iloc[-1])
    ax2.set_ylim(df_filtered['Price'].min() * 0.95, df_filtered['Price'].max() * 1.05)

    # Dynamische Ticks anwenden
    apply_axis_ticks(ax2, df_filtered['Date'].iloc[0], df_filtered['Date'].iloc[-1])
    
    fig2.canvas.draw()
    plt.show()

# Klick-Event an den Button binden
btn_vorschau.on_clicked(on_vorschau_clicked)

# 5. Zentrale Update-Funktion für Hauptfenster
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
        
        apply_axis_ticks(ax, dt_start, dt_end)
        
        ax.set_title(f"fig0 {str_start} + {tage_differenz} Tage = {str_end}")
        text_mitte.set_text(f" {str_start} + {tage_differenz} Tage = {str_end} ")
        
        if text_box_start.text_disp.get_text() != str_start:
            text_box_start.set_val(str_start)
        if text_box_end.text_disp.get_text() != str_end:
            text_box_end.set_val(str_end)
            
    fig.canvas.draw_idle()
    is_updating = False

# 6. Event-Handler für Slider und TextBoxen koppeln
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

# Startkonfiguration
update_plot(0, len(df)-1)

plt.show()

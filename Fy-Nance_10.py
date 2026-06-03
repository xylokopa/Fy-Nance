# Fy-Nance_10.py 03-06-2026 Projekt Ticker-Oszillograph
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from matplotlib.widgets import Slider, Button, TextBox
import os
# ==============================================================================
#  ZENTRALES REGISTER DER GLOBALEN VARIABLEN
# ==============================================================================
# Hier sitzen die 8 Haupt-Steuerleitungen gut sichtbar direkt unter den Imports.
# In den Funktionen darunter wird nur noch gelesen oder gezielt zugegriffen.
online_schalter_val = 1            # default 1 = Online live, 0 = Offline
clr_schalter_val    = 1            # Default 1 = FIX (Zoom behalten), 0 = CLR (Reset)
aktiver_index       = 2            # Default-Ticker (Standard: 2 = Apple)
yfNAME = "AAPL"                    # Default-Ticker für den Online-Start
offlinecsv = "02Apple_Offline.csv" # Default-Ticker für den Offline-Start
is_updating = False                # Verriegelung gegen Endlosschleifen
ANF_DATUM = "2015-01-02"           # Default-Fenster ANF
END_DATUM = "2026-06-02"           # Default-Fenster END
# ==============================================================================
df = pd.DataFrame()         # Das zentrale DataFrame
# ==============================================================================
# Ticker-Liste aus CSV-Struktur laden
# Falls Datei nicht existiert, sicherer Fallback
try:
    ticker_df = pd.read_csv('Ticker-Liste.csv')
except FileNotFoundError:
    # Automatische In-Script-Ticker-Liste falls Ticker-Liste.csv fehlt
    data_setup = """Num,Nam,Tik
00,Allianz,ALV.DE
01,Alstom,AOMD.DE
02,Apple,AAPL
03,Basf,BAS.DE
04,BlackRock1,BR
05,BlackRock2,BLK
06,Boeing,BA
07,BYD,002594.SZ
08,DaimlerTruck,DTG.DE
09,Deu Bank,DB
10,Deu Boerse,DBOEY
11,Deu Post,DHL.DE
12,GoldApr26,GC=F
13,Google,GOOG
14,HubGroup,HUBG
15,Lockheed,LOM.F
16,Lufthansa,LHA.DE
17,Oracle,SOC.SG
18,Rheinmetall,RHM.DE
19,Siemens,SIE.DE
20,Stellantis,STLAM.MI
21,Tesla,TSLA
22,ThyssenKrupp,TKA.DE
23,Toyota,TOYOF
24,Vanguard,VWRL.SW
25,Volkswagen,VOW.DE
26,Volvo AB,VOL1.SG"""
    with open('Ticker-Liste.csv', 'w') as f:
        f.write(data_setup)
    ticker_df = pd.read_csv('Ticker-Liste.csv')

# --- DATENLADE-FUNKTION (KERNEL) ---
def load_ticker_data(num_str, name, ticker_str):
    global df
    filename = f"{num_str}{name}_Offline.csv"
    
    if online_schalter_val > 0:
        try:
            print(f"Lade {ticker_str} live von Yahoo Finance...")
            df_live = yf.Ticker(ticker_str).history(start=ANF_DATUM, end=END_DATUM)[["Close"]]
            df_live.index = df_live.index.tz_localize(None)
            df_working = df_live.rename(columns={"Close": "Price"}).dropna().reset_index()
            df_working['Date'] = pd.to_datetime(df_working['Date'])
            df_working.to_csv(filename, index=False)
            print(f"-> Erfolgreich live geladen und gepuffert in {filename}")
            df = df_working.sort_values('Date').reset_index(drop=True)
            return
        except Exception as e:
            print(f"Online-Laden für {ticker_str} fehlgeschlagen ({e}). Nutze Offline-Fallback!")
            
    # Offline-Strang
    if os.path.exists(filename):
        print(f"Lese lokale Datei {filename} ein...")
        df_working = pd.read_csv(filename)
        df_working['Date'] = pd.to_datetime(df_working['Date'])
        df = df_working.sort_values('Date').reset_index(drop=True)
    else:
        print(f"WARNUNG: Keine Offline-Daten für {filename} gefunden! Leere Struktur als Ersatz.")
        df = pd.DataFrame(columns=['Date', 'Price'])

# Initialer Startlauf mit Default-Ticker Apple
row_init = ticker_df.iloc[aktiver_index]
load_ticker_data(f"{row_init['Num']:02d}", row_init['Nam'], row_init['Tik'])

# ==============================================================================
# 2. GEOMETRISCHER COCKPIT-BAU (DAS INTERFACE)
# ==============================================================================
fig, ax = plt.subplots(figsize=(14, 8))
fig.canvas.manager.set_window_title('Figur 0 - Ticker Oszillograph')

# Platzzuweisung: left=0.22 lässt genug Raum für die 27 Ticker links
plt.subplots_adjust(left=0.22, bottom=0.22, right=0.99)

line, = ax.plot(df['Date'], df['Price'], label='preis', color='blue')
ax.set_ylabel('Preis in €')
ax.grid(True, linestyle='--')
ax.legend(loc='upper left')

is_updating = False

# --- PLATZIERUNG DER STEUER-ACHSEN (plt.axes) ---
ax_von = plt.axes([0.22, 0.055, 0.22, 0.03])    # Linkes Datumsfenster
ax_online = plt.axes([0.47, 0.05, 0.06, 0.05])  # ONLINE-OFFLINE-Schalter
ax_clr = plt.axes([0.44, 0.0125, 0.12, 0.035])  # unter ax_online 
ax_bis = plt.axes([0.56, 0.055, 0.22, 0.03])    # Linkes Datumsfenster

ax_box_start = plt.axes([0.22, 0.14, 0.12, 0.04])
ax_box_end = plt.axes([0.66, 0.14, 0.12, 0.04])
text_mitte = fig.text(0.40, 0.155, '', bbox=dict(facecolor='white', alpha=1.0, edgecolor='black'))


ax_diag1 = plt.axes([0.22, 0.01, 0.10, 0.04])
ax_diag2 = plt.axes([0.33, 0.01, 0.10, 0.04])
ax_diag3 = plt.axes([0.57, 0.01, 0.10, 0.04])
ax_diag4 = plt.axes([0.68, 0.01, 0.10, 0.04])

# 27-TASTEN-KLAVIER AM LINKEN RAND
# Tastenhöhe so abgestimmt daß 27 Tasten ohne Überlappung passen
ticker_buttons = []
button_handles = []  # Hält die Schalter-Referenzen im Speicher aktiv

total_buttons = len(ticker_df)
for i in range(total_buttons):
    row = ticker_df.iloc[i]
    num_str = f"{row['Num']:02d}"
    btn_label = f"{num_str} {row['Nam']}"
    
    # Dynamische Schalterhöhen von oben nach unten (0.95 bis 0.02)
    y_pos = 0.95 - (i * 0.033)
    ax_tick = plt.axes([0.02, y_pos, 0.15, 0.026])
    
    # Aktiven Button farblich hervorheben
    btn_color = '#b0c4de' if i == aktiver_index else '#e1e1e1'
    btn = Button(ax_tick, btn_label, color=btn_color)
    btn.label.set_fontsize(8)  # typische Schriftgröße für gute Lesbarkeit
    ticker_buttons.append((btn, num_str, row['Nam'], row['Tik'], i))
    button_handles.append(btn) # Schutz gegen Pythons Garbage Collector

# --- INITIALISIERUNG ALLER WIDGETS ---
slider_von = Slider(ax_von, 'von', 0, len(df)-1, valinit=0, valfmt='%0.0f')
slider_bis = Slider(ax_bis, 'bis', 0, len(df)-1, valinit=len(df)-1, valfmt='%0.0f')
btn_online = Button(ax_online, 'ONLINE' if online_schalter_val else 'OFFLINE', color='green' if online_schalter_val else 'red')

text_box_start = TextBox(ax_box_start, '', initial='')
text_box_end   = TextBox(ax_box_end, '', initial='')

# --- PLATZIERUNG DER STEUER-ACHSEN (nachträglich pixelgenau spätere Knöpfen nachbessern) ---
# CLR-Schalter direkt unter dem Online-Schalter (nachträglich pixelgenau nachbesserbar)
# Variable für den CLR-Zustand (1 = FIX / Zoom behalten, 0 = RESET / Vollansicht)
clr_schalter_val = 1 
# Button-Objekt initialisieren
btn_clr = Button(ax_clr, 'Zeitfenster : FIX', color='green')
btn_clr.label.set_fontsize(8)
# --- PLATZIERUNG DER DIAGNOSE-BUTTONS  ---
btn_diag1 = Button(ax_diag1, 'DIAGNOSE 1', color='#d3d3d3')
btn_diag2 = Button(ax_diag2, 'DIAGNOSE 2 [X]', color='#e0e0e0')
btn_diag3 = Button(ax_diag3, 'DIAGNOSE 3 [X]', color='#e0e0e0')
btn_diag4 = Button(ax_diag4, 'DIAGNOSE 4 [X]', color='#e0e0e0')

# ==============================================================================
# 3. INTERAKTIVE MECHANIK & EVENT-HANDLER
# ==============================================================================
# --- 1. FUNKTION: DYNAMISCHE TICKS (möglichst typensicher) ---
def apply_axis_ticks(target_ax, dt_start, dt_end):
    # Erzwingt Umwandlung in echte Timestamps, unabh. vom Input
    dt_start = pd.Timestamp(dt_start)
    dt_end = pd.Timestamp(dt_end)
    
    tage_fenster = (dt_end - dt_start).days
    
    target_ax.xaxis.set_major_locator(mdates.YearLocator())
    target_ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    
    if tage_fenster < 730:  # wegen Monats-Markierungen
        target_ax.xaxis.set_minor_locator(mdates.MonthLocator())
        target_ax.xaxis.set_minor_formatter(mdates.DateFormatter('%m'))
        target_ax.grid(True, which='both', linestyle='--', alpha=0.5)
    else:
        target_ax.xaxis.set_minor_locator(mdates.MonthLocator())
        target_ax.xaxis.set_minor_formatter(mticker.NullFormatter())
        target_ax.grid(True, which='major', linestyle='--')
        
    plt.setp(target_ax.get_xticklabels(), rotation=0, ha='center')

def get_current_data():
    idx_von = int(slider_von.val)
    idx_bis = int(slider_bis.val)
    df_filtered = df.iloc[idx_von:idx_bis+1].copy()
    
    if df_filtered.empty:
        return None, "", ""
        
    # Nachbesserung für Zugriff über .values und Umwandlung in sichere Timestamps
    dt_start = pd.Timestamp(df_filtered['Date'].values[0])
    dt_end = pd.Timestamp(df_filtered['Date'].values[-1])
    
    str_start = dt_start.strftime('%Y-%m-%d')
    str_end = dt_end.strftime('%Y-%m-%d')
    
    return df_filtered, str_start, str_end

# --- EVENT-HANDLER FÜR DIE VERKABELUNG DER ANZEIGEN ---
# --- 2. FUNKTION: ZENTRALES UPDATE-GETRIEBE ---
# --- GEÄNDERTER ZUGRIFF IN update_plot (Mit fehlender [0] für den Start!) ---
def update_plot(idx_von, idx_bis):
    global is_updating
    if is_updating or df.empty: return
    is_updating = True

    idx_von = max(0, min(idx_von, len(df)-1))
    idx_bis = max(0, min(idx_bis, len(df)-1))
    if idx_von > idx_bis: idx_von = idx_bis

    slider_von.set_val(idx_von)
    slider_bis.set_val(idx_bis)

    df_filtered = df.iloc[idx_von:idx_bis+1]
    if not df_filtered.empty:
        # Jetzt mit [0] für das erste Element des Arrays!
        dt_start = pd.Timestamp(df_filtered['Date'].values[0])   # <--- [0] WIRD ERGÄNZT
        dt_end = pd.Timestamp(df_filtered['Date'].values[-1])
        
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
# --- UM-SCHALTE-MECHANISMUS FÜR DAS TICKER-KLAVIER AM LINKEN RAND ---
# --- VORSPANN: SICHERHEITS-CALLBACK BEI TICKERWECHSEL ---
def create_ticker_callback(num_str, name, ticker_str, button_index):
    def callback(event):
        global aktiver_index
        print(f"\n[KLAVIER] Taste gedrückt: {num_str} {name} ({ticker_str})")
        
        # 1. Tastenfarbe umschalten
        for btn_obj, _, _, _, idx in ticker_buttons:
            if idx == button_index:
                btn_obj.color = '#b0c4de'
                btn_obj.ax.set_facecolor('#b0c4de')
            else:
                btn_obj.color = '#e1e1e1'
                btn_obj.ax.set_facecolor('#e1e1e1')
        
        aktiver_index = button_index
        
        # 2. Alte Zoom-Grenzen sichern
        old_idx_von = int(slider_von.val)
        old_idx_bis = int(slider_bis.val)
        
        # 3. Neuen Ticker laden
        load_ticker_data(num_str, name, ticker_str)
        
        if not df.empty:
            # Maximale Grenzen des neuen Tickers ermitteln
            max_index_neu = len(df) - 1
            
            # Die neuen Slider-Maximalgrenzen im GUI anpassen
            slider_von.valmax = max_index_neu
            slider_bis.valmax = max_index_neu
            
            line.set_data(df['Date'], df['Price'])
            
            # --- FEHLER-FALLE WENN NEUER TICKER NICHT INS AKTUELLE ZEITINTERVALL PASST ---
            # Prüfen, ob der alte Zoom überhaupt in die neue Aktie hineinpasst!
            if clr_schalter_val == 1 and old_idx_bis <= max_index_neu:
                # Zeitfenster Von-Bis absichern: Zeitraum existiert bei der neuen Aktie
                safe_von = min(old_idx_von, max_index_neu)
                safe_bis = min(old_idx_bis, max_index_neu)
                
                slider_von.set_val(safe_von)
                slider_bis.set_val(safe_bis)
                
                dt_start_new = pd.Timestamp(df.iloc[safe_von]['Date'])
                dt_end_new = pd.Timestamp(df.iloc[safe_bis]['Date'])
                str_start_new = dt_start_new.strftime('%Y-%m-%d')
                str_end_new = dt_end_new.strftime('%Y-%m-%d')
                
                text_box_start.set_val(str_start_new)
                text_box_end.set_val(str_end_new)
                
                update_plot(safe_von, safe_bis)
                print(f"-> Zeitfenster beibehalten (FIX).")
            else:
                # Zeitfenster RESET (Fallback), wenn FIX gesetzt, aber Aktie nicht im Zeitrahmen
                if clr_schalter_val == 1:
                    print("-> HINWEIS: Ticker hat zu wenig Historie. Automatischer Datums-Reset durchgeführt!")
                
                slider_von.set_val(0)
                slider_bis.set_val(max_index_neu)
                
                str_start_full = pd.Timestamp(df['Date'].values[0]).strftime('%Y-%m-%d')
                str_end_full = pd.Timestamp(df['Date'].values[-1]).strftime('%Y-%m-%d')
                text_box_start.set_val(str_start_full)
                text_box_end.set_val(str_end_full)
                
                update_plot(0, max_index_neu)
                print("-> Zeitfenster auf Vollansicht gesetzt (CLR).")
                
    return callback
# --- DIE EIGENTLICHE KLAVIER-MECHANIK ---
# Schleife zur event-treuen Verdrahtung aller Klaviertasten
for btn_obj, n_str, nam, tik, b_idx in ticker_buttons:
    btn_obj.on_clicked(create_ticker_callback(n_str, nam, tik, b_idx))
# --- NACHTRAG ZUM VORSPANN FÜR DEN CLR-SCHALTER ---
def on_clr_clicked(event):
    global clr_schalter_val
    if clr_schalter_val > 0:
        clr_schalter_val = 0
        btn_clr.label.set_text("CLR")
        btn_clr.color = "red"
        btn_clr.ax.set_facecolor("red")
        print("[COCKPIT] Modus gewechselt: Zeitfenster bei Tickerwechsel zurückgesetzt (CLR).")
    else:
        clr_schalter_val = 1
        btn_clr.label.set_text("Zeitfenster : FIX")
        btn_clr.color = "green"
        btn_clr.ax.set_facecolor("green")
        print("[COCKPIT] Modus gewechselt: Zeitfenster bei Tickerwechsel arretiert (FIX).")
    fig.canvas.draw_idle()

btn_clr.on_clicked(on_clr_clicked)
button_handles.append(btn_clr)

#Nachtrag Button Clear

# --- ONLINE/OFFLINE-SCHALTER ---
def on_online_clicked(event):
    global online_schalter_val
    # Zustand umschalten
    if online_schalter_val > 0:
        online_schalter_val = 0
        btn_online.label.set_text("OFFLINE")
        btn_online.color = "red"
    else:
        online_schalter_val = 1
        btn_online.label.set_text("ONLINE")
        btn_online.color = "green"
    
    # Aktuelle Aktie mit neuem Modus nachladen
    row = ticker_df.iloc[aktiver_index]
    load_ticker_data(f"{row['Num']:02d}", row['Nam'], row['Tik'])
    if not df.empty:
        line.set_data(df['Date'], df['Price'])
        update_plot(int(slider_von.val), int(slider_bis.val))
    fig.canvas.draw_idle()

btn_online.on_clicked(on_online_clicked)

# --- RECHTER RAND , EINRICHTUNG DIAGNOSE-MONITORE ---
# --- EVENT-HANDLER FÜR DIE VIER DIAGNOSE-MONITORE ---

def on_diag1_clicked(event):
    df_filtered, str_start, str_end = get_current_data()
    if df_filtered is None or df_filtered.empty: return
    
    miwe_val = df_filtered['Price'].mean()
    df_filtered['miwe'] = miwe_val
    df_filtered['diffz'] = miwe_val + df_filtered['Price'].diff().fillna(0)

    fig1, ax1 = plt.subplots(figsize=(9, 5.5))
    fig1.canvas.manager.set_window_title('Figur 1 - Volatilitätsuntersuchung')
    
    ax1.plot(df_filtered['Date'], df_filtered['miwe'], color='black', label='miwe')
    ax1.plot(df_filtered['Date'], df_filtered['diffz'], color='blue', label='diffz')
    ax1.plot(df_filtered['Date'], df_filtered['Price'], color='red', linewidth=2, label='preis')
    
    ax1.set_title(f"fig1 Preis, Mittelwert und Differenz-Werte ({str_start} bis {str_end})")
    ax1.set_ylabel('Preis in €')
    ax1.legend(loc='upper left')
    
    # Nachtrag NumPy-Werte direkt aus dem gefilterten Satz
    dt_start_safe = pd.Timestamp(df_filtered['Date'].values[0])
    dt_end_safe = pd.Timestamp(df_filtered['Date'].values[-1])
    apply_axis_ticks(ax1, dt_start_safe, dt_end_safe)
    
    fig1.canvas.draw()
    plt.show()

def on_diag2_clicked(event):
    df_filtered, str_start, str_end = get_current_data()
    fig2, ax2 = plt.subplots(figsize=(9, 5.5))
    fig2.canvas.manager.set_window_title('Figur 2 - PLatzhalter 1')
    ax2.text(0.5, 0.5, 'für weitere Auswertungsverfahren:\n\n[ DIAGNOSE 2 BLIND ]\n\nkann nachgerüstet werden.', 
             ha='center', va='center', fontsize=12, color='red', weight='bold', bbox=dict(facecolor='yellow', alpha=0.3))
    ax2.set_title(f"fig2 zB. Intervall-Analyse: {str_start} bis {str_end}")
    fig2.canvas.draw()
    plt.show()

def on_diag3_clicked(event):
    df_filtered, str_start, str_end = get_current_data()
    fig3, ax3 = plt.subplots(figsize=(9, 5.5))
    fig3.canvas.manager.set_window_title('Figur 3 - Platzhalter 2')
    ax3.text(0.5, 0.5, 'für weitere Auswertungsverfahren:\n\n[ DIAGNOSE 3 BLIND ]\n\nkann nachgerüstet werden.', 
             ha='center', va='center', fontsize=12, color='gray', weight='bold')
    ax3.set_title(f"fig3 zB. Trend-Oszillator: {str_start} bis {str_end}")
    fig3.canvas.draw()
    plt.show()

def on_diag4_clicked(event):
    df_filtered, str_start, str_end = get_current_data()
    fig4, ax4 = plt.subplots(figsize=(9, 5.5))
    fig4.canvas.manager.set_window_title('Figur 4 - Platzhalter 3')
    ax4.text(0.5, 0.5, 'für weitere Auswertungsverfahren:\n\n[ DIAGNOSE 4 BLIND ]\n\nkann nachgerüstet werden.', 
             ha='center', va='center', fontsize=12, color='gray', style='italic')
    ax4.set_title(f"fig4 zB. Resilienz-Display: {str_start} bis {str_end}")
    fig4.canvas.draw()
    plt.show()

btn_diag1.on_clicked(on_diag1_clicked)
btn_diag2.on_clicked(on_diag2_clicked)
btn_diag3.on_clicked(on_diag3_clicked)
btn_diag4.on_clicked(on_diag4_clicked)

slider_von.on_changed(lambda v: update_plot(int(slider_von.val), int(slider_bis.val)))
slider_bis.on_changed(lambda v: update_plot(int(slider_von.val), int(slider_bis.val)))

# --- ON_CLICKED NACHTRAG FÜR DEN CLR-SCHALTER ---
def on_clr_clicked(event):
    global clr_schalter_val
    if clr_schalter_val > 0:
        clr_schalter_val = 0
        btn_clr.label.set_text("CLR")
        btn_clr.color = "red"
        btn_clr.ax.set_facecolor("red")
        print("[COCKPIT] Modus gewechselt: Zeitfenster bei Tickerwechsel zurückgesetzt (CLR).")
    else:
        clr_schalter_val = 1
        btn_clr.label.set_text("Zeitfenster : FIX")
        btn_clr.color = "green"
        btn_clr.ax.set_facecolor("green")
        print("[COCKPIT] Modus gewechselt: Zeitfenster bei Tickerwechsel arretiert (FIX).")
    fig.canvas.draw_idle()

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

# Cockpit initial synchronisieren und Hauptschalter umlegen
update_plot(0, len(df)-1)
plt.show()


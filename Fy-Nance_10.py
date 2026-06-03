# Fy-Nance_10.py 03-06-2026 Projekt Ticker-Oszillograph
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from matplotlib.widgets import Slider, Button, TextBox
import os
# ==============================================================================
#     01    ZENTRALES REGISTER DER GLOBALEN VARIABLEN
# ==============================================================================
# Hier sitzen die 8 Haupt-Steuerleitungen gut sichtbar direkt unter den Imports.
# In den Funktionen darunter wird nur noch gelesen oder gezielt zugegriffen.
online_schalter_val = 1            # default 1 = Online live, 0 = Offline
clr_schalter_val    = 1            # Default 1 = FEST(Zoom behalten), 0 = VAR (Reset)
akt_index       = 2                # Default-Ticker (Standard: 2 = Apple)
yfNAME = "AAPL"                    # Default-Ticker für den Online-Start
offlinecsv = "02Apple_Offline.csv" # Default-Ticker für den Offline-Start
trigger = False                    # start-stop Schaubild-zeichnen
ANF_DATUM = "2015-01-02"           # Default-Fenster ANF
END_DATUM = "2026-06-02"           # Default-Fenster END
# ==============================================================================
df = pd.DataFrame()         # Das zentrale DataFrame
# ------------------------------------------------------------------------------
#     02 Ticker-Liste aus CSV-Liste laden
# ------------------------------------------------------------------------------
# Falls Datei nicht existiert, Fallback ticker_liste
try:
    ticker_df = pd.read_csv('Ticker-Liste.csv')
except FileNotFoundError:
    # Default In-Script-Ticker-Liste falls Ticker-Liste.csv fehlt
    ticker_liste = """Num,Nam,Tik
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
        f.write(ticker_liste)
    ticker_df = pd.read_csv('Ticker-Liste.csv')
# ------------------------------------------------------------------------------
#     03   Ticker-Daten Download oder aus csv lesen
# ------------------------------------------------------------------------------
def lade_ticker_daten(num_str, name, ticker_str):
    global df   # 1.globale Variable 
    csv_name = f"{num_str}{name}_Offline.csv"
    # Online-Download yfinance df_live 1.Spalte datum von start bis end  2.Spalte Preise
    if online_schalter_val > 0:
        try:
            print(f"Lade {ticker_str} live von Yahoo Finance...")
            df_live = yf.Ticker(ticker_str).history(start=ANF_DATUM, end=END_DATUM)[["Close"]]
            df_live.index = df_live.index.tz_localize(None)
            df_csv = df_live.rename(columns={"Close": "Price"}).dropna().reset_index()
            df_csv['Date'] = pd.to_datetime(df_csv['Date'])
            df_csv.to_csv(csv_name, index=False)
            print(f"-> Erfolgreich live geladen und gepuffert in {csv_name}")
            df = df_csv.sort_values('Date').reset_index(drop=True)
            return
        except Exception as e:
            print(f"Online-Laden für {ticker_str} fehlgeschlagen ({e}). Nutze Offline-Fallback!")
    # Offline-csv df_csv 1.Spalte datum von start bis end  2.Spalte Preise
    if os.path.exists(csv_name):
        print(f"Lese lokale csv {csv_name} ein...")
        df_csv = pd.read_csv(csv_name)
        df_csv['Date'] = pd.to_datetime(df_csv['Date'])
        df = df_csv.sort_values('Date').reset_index(drop=True)
    else:
        print(f"WARNUNG: Keine Offline-csv {csv_name} gefunden! Leeres Frame als Ersatz.")
        df = pd.DataFrame(columns=['Date', 'Price'])
# ------------------------------------------------------------------------------
#     04  Default-Ticker Applefür erstes Schaubild 
# ------------------------------------------------------------------------------
akt_ticker = ticker_df.iloc[akt_index] # Zeilenwahl in Ticker-Liste = integer location 
lade_ticker_daten(f"{akt_ticker['Num']:02d}", akt_ticker['Nam'], akt_ticker['Tik'])

# ------------------------------------------------------------------------------
#     05    Matplotlib-Fenster fig für Ticker-Schaubild mit Überwachungs-Trigger
# ------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 8))
fig.canvas.manager.set_window_title('Figur 0 - Ticker Oszillograph')
# Plot-Bereich plt Links 19% frei für Liste darunter 22% für Widgets 
plt.subplots_adjust(left=0.19, bottom=0.24, right=0.92)
# Schaulinie x=df([date]) y=df['Price'] mit Beschriftungen
line, = ax.plot(df['Date'], df['Price'], label='preis', color='blue')
ax.set_ylabel('Preis in €')
ax.grid(True, linestyle='--')
ax.legend(loc='upper left')

trigger = False

# ------------------------------------------------------------------------------
#     06        Achsen und Anheftungspunkte für Widgets plazieren 
# ------------------------------------------------------------------------------
ax_von = plt.axes([0.21, 0.07, 0.22, 0.03])       # Anheftung von-Slider
ax_online = plt.axes([0.47, 0.062, 0.06, 0.05])   # Anheftung ONLINE-OFFLINE-Schalter
ax_clr = plt.axes([0.44, 0.0125, 0.12, 0.035])    # Anheftung Zeitfenster-Umschalter 
ax_bis = plt.axes([0.56, 0.07, 0.22, 0.03])       # Anheftung bis-Slider

ax_box_start = plt.axes([0.21, 0.14, 0.12, 0.04]) # Anheftung Linkes Datumsfenster
ax_box_end = plt.axes([0.66, 0.14, 0.12, 0.04])   # Anheftung Rechtes Datumsfenster
text_mitte = fig.text(0.38, 0.155, '', bbox=dict(facecolor='white', alpha=1.0, edgecolor='black'))

ax_diag1 = plt.axes([0.22, 0.01, 0.10, 0.04])     # Anheftung der Diagnose-Schalter
ax_diag2 = plt.axes([0.33, 0.01, 0.10, 0.04])
ax_diag3 = plt.axes([0.57, 0.01, 0.10, 0.04])
ax_diag4 = plt.axes([0.68, 0.01, 0.10, 0.04])

# ------------------------------------------------------------------------------
#     07           Vorbereitung Ticker-Klavier am linken Rand 
# ------------------------------------------------------------------------------
ticker_klavier = []
schalter_handles = []  # Hält die Schalter-Referenzen im Speicher aktiv
anzahl_ticker = len(ticker_df)

for i in range(anzahl_ticker):
    zeil = ticker_df.iloc[i]
    num_str = f"{zeil['Num']:02d}"
    btn_label = f"{num_str} {zeil['Nam']}"
    # Tasten-Anheftung iterativ von oben nach unten (0.95 bis 0.02) plaziert
    y_pos = 0.95 - (i * 0.033)
    ax_tick = plt.axes([0.02, y_pos, 0.12, 0.028])
    
    # Aktiven Button farblich hervorheben
    btn_color = '#b0c4de' if i == akt_index else '#e1e1e1'
    btn = Button(ax_tick, btn_label, color=btn_color)
    btn.label.set_fontsize(10)  # typische Schriftgröße für gute Lesbarkeit
    # ------------------------------------------------------------------------------
    ticker_klavier.append((btn, num_str, zeil['Nam'], zeil['Tik'], i))
    # ------------------------------------------------------------------------------
    schalter_handles.append(btn) # Schutz gegen Pythons Garbage Collector

# ------------------------------------------------------------------------------
#     08                     Widgets plazieren 
# ------------------------------------------------------------------------------

slider_von = Slider(ax_von, 'von', 0, len(df)-1, valinit=0, valfmt='%0.0f')
slider_bis = Slider(ax_bis, 'bis', 0, len(df)-1, valinit=len(df)-1, valfmt='%0.0f')
btn_online = Button(ax_online, 'ONLINE' if online_schalter_val else 'OFFLINE', color='aqua' if online_schalter_val else 'teal')

text_box_start = TextBox(ax_box_start, '', initial='')
text_box_end   = TextBox(ax_box_end, '', initial='')

# CLR-Schalter direkt unter Online-Schalter einstellen
# Variable für den CLR-Zustand (1 = FEST / Zoom behalten, 0 = RESET / Vollansicht)
clr_schalter_val = 1 
btn_clr = Button(ax_clr, 'Zeitfenster : FEST', color='lime')
btn_clr.label.set_fontsize(10)

# --- PLATZIERUNG DER DIAGNOSE-BUTTONS  ---
btn_diag1 = Button(ax_diag1, 'DIAGNOSE 1', color='#d3d3d3')
btn_diag2 = Button(ax_diag2, 'DIAGNOSE 2 [X]', color='#e0e0e0')
btn_diag3 = Button(ax_diag3, 'DIAGNOSE 3 [X]', color='#e0e0e0')
btn_diag4 = Button(ax_diag4, 'DIAGNOSE 4 [X]', color='#e0e0e0')

# ------------------------------------------------------------------------------
#     09                      Schaubild-Achsen skalieren
# ------------------------------------------------------------------------------
def axen_skalierung(target_ax, dt_start, dt_end):
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
# ------------------------------------------------------------------------------
#     10                       Zeitfenster auslesen
# ------------------------------------------------------------------------------
def von_bis_ablesen():
    idx_von = int(slider_von.val)
    idx_bis = int(slider_bis.val)
    df_zeitfenster = df.iloc[idx_von:idx_bis+1].copy()
    
    if df_zeitfenster.empty:
        return None, "", ""
        
    # Nachbesserung für Zugriff über .values und Umwandlung in sichere Timestamps
    dt_start = pd.Timestamp(df_zeitfenster['Date'].values[0])
    dt_end = pd.Timestamp(df_zeitfenster['Date'].values[-1])
    
    str_start = dt_start.strftime('%Y-%m-%d')
    str_end = dt_end.strftime('%Y-%m-%d')
    
    return df_zeitfenster, str_start, str_end
# ------------------------------------------------------------------------------
#     11                         Schaubild neu zeichnen
# ------------------------------------------------------------------------------
def neu_zeichnen(idx_von, idx_bis):
    global trigger
    if trigger or df.empty: return
    trigger = True

    idx_von = max(0, min(idx_von, len(df)-1))
    idx_bis = max(0, min(idx_bis, len(df)-1))
    if idx_von > idx_bis: idx_von = idx_bis

    slider_von.set_val(idx_von)
    slider_bis.set_val(idx_bis)

    df_zeitfenster = df.iloc[idx_von:idx_bis+1]
    if not df_zeitfenster.empty:
        # index [0] zeigt auf erste Element des Arrays!
        dt_start = pd.Timestamp(df_zeitfenster['Date'].values[0])
        # index [-1] zeigt auf letztes Element des Arrays!        
        dt_end = pd.Timestamp(df_zeitfenster['Date'].values[-1])
        
        str_start = dt_start.strftime('%Y-%m-%d')
        str_end = dt_end.strftime('%Y-%m-%d')
        tage_differenz = (dt_end - dt_start).days
        
        ax.set_xlim(dt_start, dt_end)
        ax.set_ylim(df_zeitfenster['Price'].min() * 0.95, df_zeitfenster['Price'].max() * 1.05)
        
        axen_skalierung(ax, dt_start, dt_end)
        
        ax.set_title(f"fig0 {str_start} + {tage_differenz} Tage = {str_end}")
        text_mitte.set_text(f" {str_start} + {tage_differenz} Tage = {str_end} ")
        
        if text_box_start.text_disp.get_text() != str_start: 
            text_box_start.set_val(str_start)
        if text_box_end.text_disp.get_text() != str_end: 
            text_box_end.set_val(str_end)
            
    fig.canvas.draw_idle()
    trigger = False

# ------------------------------------------------------------------------------
#      12   event-überwachung Ticker-Klavier am linken Rand 
# ------------------------------------------------------------------------------

def ticker_klavier_klick(num_str, name, ticker_str, button_index):
    def callback(event):
        global akt_index
        print(f"\n[KLAVIER] Taste gedrückt: {num_str} {name} ({ticker_str})")      
        # 1. Tastenfarbe umschalten
        for btn_obj, _, _, _, idx in ticker_klavier:
            if idx == button_index:
                btn_obj.color = '#b0c4de'
                btn_obj.ax.set_facecolor('#b0c4de')
            else:
                btn_obj.color = '#e1e1e1'
                btn_obj.ax.set_facecolor('#e1e1e1')        
        akt_index = button_index

        # 2. Alte Zoom-Grenzen sichern
        idx_von_alt = int(slider_von.val)
        idx_bis_alt = int(slider_bis.val)

        # 3. Neuen Ticker laden
        lade_ticker_daten(num_str, name, ticker_str)
        if not df.empty:
            # Maximale Grenzen des neuen Tickers ermitteln
            max_index_neu = len(df) - 1
            
            # Die neuen Slider-Maximalgrenzen im GUI anpassen
            slider_von.valmax = max_index_neu
            slider_bis.valmax = max_index_neu
            
            line.set_data(df['Date'], df['Price'])
            # -------------------------------------
            # Prüfen, ob der alte Zoom überhaupt in die neue Aktie hineinpasst!
            # -------------------------------------
            if clr_schalter_val == 1 and idx_bis_alt <= max_index_neu:
                # -------------------------------------
                # Zeitfenster Von-Bis absichern: Zeitraum existiert bei der neuen Aktie
                # -------------------------------------
                von_abgesichert = min(idx_von_alt, max_index_neu)
                bis_abgesichert = min(idx_bis_alt, max_index_neu)
                
                slider_von.set_val(von_abgesichert)
                slider_bis.set_val(bis_abgesichert)
                
                dt_start_neu = pd.Timestamp(df.iloc[von_abgesichert]['Date'])
                dt_end_neu = pd.Timestamp(df.iloc[bis_abgesichert]['Date'])
                str_start_neu = dt_start_neu.strftime('%Y-%m-%d')
                str_end_neu = dt_end_neu.strftime('%Y-%m-%d')
                
                text_box_start.set_val(str_start_neu)
                text_box_end.set_val(str_end_neu)
                
                neu_zeichnen(von_abgesichert, bis_abgesichert)
                print(f"-> Zeitfenster beibehalten (FEST).")
            else:
                # -------------------------------------
                # Zeitfenster RESET (Fallback), wenn FEST gesetzt, aber Aktie nicht im Zeitrahmen
                # -------------------------------------
                if clr_schalter_val == 1:
                    print("-> Ticker mit zu wenig Historie. Datums-Reset nötig")
                
                slider_von.set_val(0)
                slider_bis.set_val(max_index_neu)
                
                str_start_full = pd.Timestamp(df['Date'].values[0]).strftime('%Y-%m-%d')
                str_end_full = pd.Timestamp(df['Date'].values[-1]).strftime('%Y-%m-%d')
                text_box_start.set_val(str_start_full)
                text_box_end.set_val(str_end_full)
                
                neu_zeichnen(0, max_index_neu)
                print("-> Zeitfenster auf Vollansicht gesetzt (VAR).")
                
    return callback

# ------------------------------------------------------------------------------
#     13     Schleife zur event-überwachung aller Klaviertasten
# ------------------------------------------------------------------------------
for btn_obj, n_str, nam, tik, b_idx in ticker_klavier:
    btn_obj.on_clicked(ticker_klavier_klick(n_str, nam, tik, b_idx))

# ------------------------------------------------------------------------------
#     14               Funktionalität der CLR-Schalters
# ------------------------------------------------------------------------------
def on_clr_clicked(event):
    global clr_schalter_val
    if clr_schalter_val > 0:
        clr_schalter_val = 0
        btn_clr.label.set_text("Zeitfenster : VAR")
        btn_clr.color = "pink"
        btn_clr.ax.set_facecolor("pink")
        print("[COCKPIT] Modus gewechselt: Zeitfenster bei Tickerwechsel variabel (VAR).")
    else:
        clr_schalter_val = 1
        btn_clr.label.set_text("Zeitfenster : FEST")
        btn_clr.color = "lime"
        btn_clr.ax.set_facecolor("lime")
        print("[COCKPIT] Modus gewechselt: Zeitfenster bei Tickerwechsel konstant (FEST).")
    fig.canvas.draw_idle()

btn_clr.on_clicked(on_clr_clicked)   # clr-Schalter abrufen
schalter_handles.append(btn_clr)     # in aktive schalter einreihen

# ------------------------------------------------------------------------------
#     15              Funktionalität des ONLINE-Schalters
# ------------------------------------------------------------------------------
def on_online_clicked(event):
    global online_schalter_val
    # Modus umschalten
    if online_schalter_val > 0:
        online_schalter_val = 0
        btn_online.label.set_text("OFFLINE")
        btn_online.color = "teal"
    else:
        online_schalter_val = 1
        btn_online.label.set_text("ONLINE")
        btn_online.color = "aqua"
    
    # Aktuelle Aktie im neuen Modus nachladen
    zeil = ticker_df.iloc[akt_index]
    lade_ticker_daten(f"{zeil['Num']:02d}", zeil['Nam'], zeil['Tik'])
    if not df.empty:
        line.set_data(df['Date'], df['Price'])
        neu_zeichnen(int(slider_von.val), int(slider_bis.val))
    fig.canvas.draw_idle()

btn_online.on_clicked(on_online_clicked)  # online-Schalter abrufen

# ------------------------------------------------------------------------------
#    16                Aufruf 1 Diagnose-Schalter
# ------------------------------------------------------------------------------
def on_diag1_clicked(event):
    df_zeitfenster, str_start, str_end = von_bis_ablesen()
    if df_zeitfenster is None or df_zeitfenster.empty: return
    
    miwe_val = df_zeitfenster['Price'].mean()
    df_zeitfenster['miwe'] = miwe_val
    df_zeitfenster['diffz'] = miwe_val + df_zeitfenster['Price'].diff().fillna(0)

    fig1, ax1 = plt.subplots(figsize=(9, 5.5))
    fig1.canvas.manager.set_window_title('Figur 1 - Volatilitätsuntersuchung')
    
    ax1.plot(df_zeitfenster['Date'], df_zeitfenster['miwe'], color='black', label='miwe')
    ax1.plot(df_zeitfenster['Date'], df_zeitfenster['diffz'], color='blue', label='diffz')
    ax1.plot(df_zeitfenster['Date'], df_zeitfenster['Price'], color='red', linewidth=2, label='preis')
    
    ax1.set_title(f"fig1 Preis, Mittelwert und Differenz-Werte ({str_start} bis {str_end})")
    ax1.set_ylabel('Preis in €')
    ax1.legend(loc='upper left')
    
    # Timestamp-Werte direkt aus dem zeitfenster abholen
    dt_start_gesichert= pd.Timestamp(df_zeitfenster['Date'].values[0])
    dt_end_gesichert = pd.Timestamp(df_zeitfenster['Date'].values[-1])
    axen_skalierung(ax1, dt_start_gesichert, dt_end_gesichert)
    
    fig1.canvas.draw()          # Overlay-Fenster zu Diagnose 1 ausgeben
    plt.show()

# ------------------------------------------------------------------------------
#      17              Aufruf 2 Diagnose-Dummy
# ------------------------------------------------------------------------------
def on_diag2_clicked(event):
    df_zeitfenster, str_start, str_end = von_bis_ablesen()
    fig2, ax2 = plt.subplots(figsize=(9, 5.5))
    fig2.canvas.manager.set_window_title('Figur 2 - PLatzhalter 1')
    ax2.text(0.5, 0.5, 'für weitere Auswertungsverfahren:\n\n[ DIAGNOSE 2 BLIND ]\n\nkann nachgerüstet werden.', 
             ha='center', va='center', fontsize=12, color='red', weight='bold', bbox=dict(facecolor='yellow', alpha=0.3))
    ax2.set_title(f"fig2 zB. Intervall-Analyse: {str_start} bis {str_end}")
    fig2.canvas.draw()
    plt.show()
# ------------------------------------------------------------------------------
#      18              Aufruf 3 Diagnose-Dummy
# ------------------------------------------------------------------------------
def on_diag3_clicked(event):
    df_zeitfenster, str_start, str_end = von_bis_ablesen()
    fig3, ax3 = plt.subplots(figsize=(9, 5.5))
    fig3.canvas.manager.set_window_title('Figur 3 - Platzhalter 2')
    ax3.text(0.5, 0.5, 'für weitere Auswertungsverfahren:\n\n[ DIAGNOSE 3 BLIND ]\n\nkann nachgerüstet werden.', 
             ha='center', va='center', fontsize=12, color='gray', weight='bold')
    ax3.set_title(f"fig3 zB. Trend-Oszillator: {str_start} bis {str_end}")
    fig3.canvas.draw()
    plt.show()
# ------------------------------------------------------------------------------
#      19              Aufruf 4 Diagnose-Dummy
# ------------------------------------------------------------------------------
def on_diag4_clicked(event):
    df_zeitfenster, str_start, str_end = von_bis_ablesen()
    fig4, ax4 = plt.subplots(figsize=(9, 5.5))
    fig4.canvas.manager.set_window_title('Figur 4 - Platzhalter 3')
    ax4.text(0.5, 0.5, 'für weitere Auswertungsverfahren:\n\n[ DIAGNOSE 4 BLIND ]\n\nkann nachgerüstet werden.', 
             ha='center', va='center', fontsize=12, color='gray', style='italic')
    ax4.set_title(f"fig4 zB. Resilienz-Display: {str_start} bis {str_end}")
    fig4.canvas.draw()
    plt.show()

btn_diag1.on_clicked(on_diag1_clicked)  # Diagnose-Schalter abrufen
btn_diag2.on_clicked(on_diag2_clicked)
btn_diag3.on_clicked(on_diag3_clicked)
btn_diag4.on_clicked(on_diag4_clicked)
# ---------------------------------------------------------------------------------
#     20  Huckepack-Aufruf der beiden Slider um bei Bewegung plot neu zu zeichnen
# ---------------------------------------------------------------------------------
slider_von.on_changed(lambda v: neu_zeichnen(int(slider_von.val), int(slider_bis.val)))
slider_bis.on_changed(lambda v: neu_zeichnen(int(slider_von.val), int(slider_bis.val)))
# ----------------------------------------------------------------------------------
#     21  Textbox-ENTER-Submit-Funktionalität für das Zeitfenster per Datums-Eingabe
# ----------------------------------------------------------------------------------
def on_submit_start(text_input):
    try:
        target_date = pd.to_datetime(text_input.strip(), format='%Y-%m-%d')
        idx = (df['Date'] - target_date).abs().idxmin()
        neu_zeichnen(idx, int(slider_bis.val))
    except ValueError:
        neu_zeichnen(int(slider_von.val), int(slider_bis.val))

def on_submit_end(text_input):
    try:
        target_date = pd.to_datetime(text_input.strip(), format='%Y-%m-%d')
        idx = (df['Date'] - target_date).abs().idxmin()
        neu_zeichnen(int(slider_von.val), idx)
    except ValueError:
        neu_zeichnen(int(slider_von.val), int(slider_bis.val))

text_box_start.on_submit(on_submit_start)   # Start-Datum abrufen
text_box_end.on_submit(on_submit_end)       # Ende-Datum abrufen 

# ------------------------------------------------------------------------------
#     22       Ticker-Oszillograph starten und neu zeichnen
# ------------------------------------------------------------------------------
neu_zeichnen(0, len(df)-1)
plt.show()


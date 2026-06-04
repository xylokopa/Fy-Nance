# Fy-Nance_13.py 03-06-2026 Projekt Ticker-Oszillograph
import numpy as np
import pandas as pd
import yfinance as yf
import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from matplotlib.widgets import Slider, Button, TextBox
import os
# ==============================================================================
#     01a    GLOBALEN VARIABLEN
# ==============================================================================
# Hier sitzen die 8 Haupt-Steuerleitungen gut sichtbar direkt unter den Imports.
# In den Funktionen darunter wird nur noch gelesen oder gezielt zugegriffen.
online_schalter_val = 1            # default 1 = Online live, 0 = Offline
clr_schalter_val    = 1            # Default 1 = FEST(Zoom behalten), 0 = VAR (Reset)
akt_index       = 2                # Default-Ticker (Standard: 2 = Apple)
yfNAME = "AAPL"                    # Default-Ticker für den Online-Start
offlinecsv = "02Apple_Offline.csv" # Default-Ticker für den Offline-Start
trigger = False                    # start-stop zum Schaubild-zeichnen
ANF_DATUM = "2020-01-02"           # Default-Fenster ANF
END_DATUM = "2020-09-27"           # Default-Fenster END
# ==============================================================================
df = pd.DataFrame()                # globales DataFrame
# ==============================================================================
#     01b drei Fenster fig,ax und fig2,ax2 für canvas.draw_idle() bereitstellen
# ==============================================================================
# Frequenz-Rezept des im Tupel(Ticker,Zeitfenster) erfassten Börsen-Ereignisses
fig3, ax3 = plt.subplots(figsize=(10, 6))
fig3.canvas.manager.set_window_title('Fourier-Signatur des Börsen-Ereignisses')
# Das Statistik-Fenster als globalem Einzelgaenger bereitstellen
fig2, ax2 = plt.subplots(figsize=(10, 6))
fig2.canvas.manager.set_window_title('Statistische Verteilungs-Analyse')
# Das im Interpreter-Ablauf VORHER zu befüllende Oszillographen-Fenster danach ...
fig, ax = plt.subplots(figsize=(12, 8))
fig.canvas.manager.set_window_title('Figur 0 - Ticker Oszillograph')
plt.subplots_adjust(left=0.19, bottom=0.24, right=0.92)

# ------------------------------------------------------------------------------
#     02 Ticker-Liste aus CSV-Liste laden
# ------------------------------------------------------------------------------
try:
    ticker_df = pd.read_csv('Ticker-Liste.csv')
except FileNotFoundError:
    # Default Liste falls Ticker-Liste.csv fehlt
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
    # Download df_live mit 1.Spalte datum (von start bis end) und 2.Spalte Preis
    if online_schalter_val > 0:
        try:
            print(f"Lade {ticker_str} live von Yahoo Finance...")
            df_live = yf.Ticker(ticker_str).history(start=ANF_DATUM, end=END_DATUM)[["Close"]]
            df_live.index = df_live.index.tz_localize(None)
            df_csv = df_live.rename(columns={"Close": "Price"}).dropna().reset_index()
            df_csv['Date'] = pd.to_datetime(df_csv['Date'])
            df_csv.to_csv(csv_name, index=False)
            print(f"-> live geladen und in {csv_name} gepuffert")
            df = df_csv.sort_values('Date').reset_index(drop=True)
            return
        except Exception as e:
            print(f"{ticker_str} Download gescheitert ({e}) => Offline-csv")
    # Offline-csv df_csv mit 1.Spalte datum (von start bis end) und 2.Spalte Preis
    if os.path.exists(csv_name):
        print(f"lokale csv {csv_name} wird geladen...")
        df_csv = pd.read_csv(csv_name)
        df_csv['Date'] = pd.to_datetime(df_csv['Date'])
        df = df_csv.sort_values('Date').reset_index(drop=True)
    else:
        print(f"Offline-csv {csv_name} nicht gefunden! Leeres Frame als Ersatz.")
        df = pd.DataFrame(columns=['Date', 'Price'])
# ------------------------------------------------------------------------------
#     04  Default-Ticker Apple für erstes Schaubild 
# ------------------------------------------------------------------------------
akt_ticker = ticker_df.iloc[akt_index] # Zeilenwahl in Ticker-Liste = integer location 
lade_ticker_daten(f"{akt_ticker['Num']:02d}", akt_ticker['Nam'], akt_ticker['Tik'])
# ------------------------------------------------------------------------------
#     04b  MA(MeanAverage) redundant einbauen ... Siehe auch Def neu_zeichnen()
# ------------------------------------------------------------------------------
# Parameter für das Zeitfenster (z.B. 20 Tage)
window_size = 20 
# Gleitenden Durchschnitt berechnen
df['MA'] = df['Price'].rolling(window=window_size).mean()
# ------------------------------------------------------------------------------
#     05    Matplotlib-Fenster fig für Ticker-Schaubild mit Überwachungs-Trigger
# ------------------------------------------------------------------------------

trigger = False

# ------------------------------------------------------------------------------
#     06        Achsen und Anheftungspunkte für Widgets platzieren 
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
    # Tasten-Anheftung iterativ von oben nach unten (0.95 bis 0.02) platziert
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
#     08                     Widgets platzieren 
# ------------------------------------------------------------------------------

slider_von = Slider(ax_von, 'von', 0, len(df)-1, valinit=0, valfmt='%0.0f')
slider_bis = Slider(ax_bis, 'bis', 0, len(df)-1, valinit=len(df)-1, valfmt='%0.0f')
btn_online = Button(ax_online, 'ONLINE' if online_schalter_val else 'OFFLINE', color='aqua' if online_schalter_val else 'teal')

text_box_start = TextBox(ax_box_start, '', initial='')
text_box_end   = TextBox(ax_box_end, '', initial='')

# CLR-Schalter direkt unter Online-Schalter 
# Variable für CLR-Zustand (1 = FEST / Zoom behalten, 0 = RESET / Vollansicht)
clr_schalter_val = 1 
btn_clr = Button(ax_clr, 'Zeitfenster : FEST', color='lime')
btn_clr.label.set_fontsize(10)

# --- PLATZIERUNG DIAGNOSE-BUTTONS  ---
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
    
    if tage_fenster < 730:  # => Monats-Markierungen
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
        
    # Zugriff über .values und Umwandlung in sichere Timestamps
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
    # --- Database-Erweiterungen Refresh ------------
    window_size = 20 # Ihr gewähltes MA-Zeitfenster
    df['MA'] = df['Price'].rolling(window=window_size).mean()
    df['Diff'] = df['Price'] - df['MA']
    # -----------------------------------------------
    
    ax.clear()   ###
    
    fig.canvas.manager.set_window_title('Figur 0 - Ticker Oszillograph')
    plt.subplots_adjust(left=0.19, bottom=0.24, right=0.92)
    
    # 1. Hauptlinien zeichnen (Nutzt noch das ganze df, Matplotlib clippt das per xlim)
    line_preis, = ax.plot(df['Date'], df['Price'], label='preis', color='blue')
    line_MAmiw, = ax.plot(df['Date'], df['MA'], label='MA', color='green')
    
    ma_mittelwert = df['MA'].mean()
    y_mamiw = [ma_mittelwert] * len(df)
    line_mamiw, = ax.plot(df['Date'], y_mamiw, label='MA-Mittelwert', color='black', linestyle='--')
    
    df['Diff'] =  df['Price'] - df['MA']
    line_diff, = ax.plot(df['Date'], ma_mittelwert + df['Diff'], label='diffz', color='red')

    ax.set_xlabel('Abweichung vom MA (Euro)')
    ax.set_ylabel('Preis in €')
    ax.grid(True, linestyle='--')
    ax.legend(loc='upper left')

    # 2. Index-Validierung der Slider
    idx_von = max(0, min(idx_von, len(df)-1))
    idx_bis = max(0, min(idx_bis, len(df)-1))
    if idx_von > idx_bis: idx_von = idx_bis

    slider_von.set_val(idx_von)
    slider_bis.set_val(idx_bis)

    # 3. DAS DYNAMISCHE ZEITFENSTER ERSTELLEN
    df_zeitfenster = df.iloc[idx_von:idx_bis+1]
    
    if not df_zeitfenster.empty:
        dt_start = pd.Timestamp(df_zeitfenster['Date'].values[0])
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
            
        # ----------------------------------------------------------------------
        # neu_zeichnen holt die dynamischen Daten aus 'df_zeitfenster'
        # ----------------------------------------------------------------------
        diff_dropna = df_zeitfenster['Diff'].dropna() # <-- GEAENDERT auf df_zeitfenster
        diff_data = diff_dropna.values
        
        # Sicherheitspruefung: Genug Datenpunkte im Sliderfenster vorhanden?
        if len(diff_data) > 5:
            # Statistik auf Basis des neuen Slider-Fensters berechnen
            mu = np.mean(diff_data)
            sigma = np.std(diff_data)
            ks_stat, p_value = stats.kstest(diff_data, 'norm', args=(mu, sigma))
            
            # Konsole haemmert die aktuellen Werte raus:
            print(f"Fenster [{str_start} bis {str_end}] -> KS-Abweichung: {ks_stat:.4f}")
            
            # FFT ebenfalls auf Basis des neuen Slider-Fensters berechnen
            signal = diff_data
            N = len(signal) ##
            if N > 5:
                 fft_werte = np.fft.fft(signal)
                 frequenzen = np.fft.fftfreq(len(signal))
            
                 halbe = len(signal) // 2
                 freq = frequenzen[:halbe]
                 amp = np.abs(fft_werte[:halbe])

                 # 2. Die Top 3 "Resonanz-Zungen" (Formanten) des Boersen-Ereignisses finden
                 # Wir ignorieren die Frequenz 0 (Gleichanteil)
                 sortierte_idxs = np.argsort(amp[1:])[::-1] + 1
                 print("\n--- KLANGREZEPT DES TICKERS (FORMANTEN) ---")
                 for i in range(min(3, len(sortierte_idxs))):
                     idx = sortierte_idxs[i]
                     # Zyklusdauer in Tagen (Kehrwert der Frequenz)
                     zyklus_tage = 1.0 / freq[idx] if freq[idx] > 0 else float('inf')
                     # Relative Lautstaerke (Energieanteil)
                     lautstaerke_prozent = (amp[idx] / np.sum(amp)) * 100
        
                     print(f"Zunge {i+1} (Resonanz): {zyklus_tage:.1f} Tage Takt "
                           f"| Lautstaerke: {lautstaerke_prozent:.1f}%")
            
                 dominant_idx = np.argmax(amp[1:]) + 1
                 dominanter_zyklus = 1 / freq[dominant_idx]
                 print(f"Dominanter Zyklus im Fenster: {dominanter_zyklus:.1f} Tage")
            # ----------------------------------------------------------------------           
            # Zweites Fenster ax2 saubermachen und dynamisch neu befuellen
            # ----------------------------------------------------------------------
            ax2.clear()          
            
            count, bins, ignored = ax2.hist(diff_data, bins=30, density=True, 
                                       alpha=0.6, color='blue', label='Echte Oszillation')
            
            gauss = stats.norm.pdf(bins, mu, sigma)
            ax2.plot(bins, gauss, color='red', linewidth=2, 
                    label=f'Ideale Gauss-Kurve\n(KS-Abweichung: {ks_stat:.3f})')
            
            ax2.set_ylabel('Wahrscheinlichkeitsdichte (Gauss)', color='red')
            ax2.legend()
            ax2.grid(True, linestyle='--')
            # ----------------------------------------------------------------------           
            # Drittes Fenster ax3 ebenso
            # ----------------------------------------------------------------------
            ax3.clear()
            ax3.set_xscale('log')
            ax3.set_title('Logarithmisch skaliertes Spektrum', fontsize=12, fontweight='bold')
            # Das lila Amplituden-Spektrum logarithmisch aufzeichnen
            ax3.plot(freq, amp, color='purple', label='Klang-Spektrum') 
        
            # Die Top 3 Resonanz-Zungen als vertikale Linien einzeichnen
            farben = ['darkred', 'red', 'orange']
            for i in range(min(3, len(sortierte_idxs))):
                idx = sortierte_idxs[i]
                f_zunge = freq[idx]
                amp_zunge = amp[idx]
                zyklus_tage = 1.0 / f_zunge if f_zunge > 0 else 0
            
                ax3.vlines(f_zunge, 0, amp_zunge, colors=farben[i], linestyle='-', linewidth=2,
                       label=f'Zunge {i+1}: {zyklus_tage:.1f} Tage')
            
            ax3.set_xlabel('Frequenz (1/Tage)')
            ax3.set_ylabel('Lautstaerke (Amplitude)')
            ax3.legend(loc='upper right')
            ax3.grid(True, linestyle='--')
    # ----------------------------------------------------------------------
    # drei Leinwaende synchron neu rendern
    # ----------------------------------------------------------------------
    fig.canvas.draw_idle()
    fig2.canvas.draw_idle()
    fig3.canvas.draw_idle()  # <-- Das dritte Glied der Kette

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

        # 2. Alte Zeitfenster sichern
        idx_von_alt = int(slider_von.val)
        idx_bis_alt = int(slider_bis.val)

        # 3. Neuen Ticker laden
        lade_ticker_daten(num_str, name, ticker_str)
        if not df.empty:
            # Max. Grenzen des neuen Tickers ermitteln
            max_index_neu = len(df) - 1
            
            # neue Slider-Maximalgrenzen anpassen
            slider_von.valmax = max_index_neu
            slider_bis.valmax = max_index_neu

            neu_zeichnen(idx_von_alt, idx_bis_alt)

            # statt line.set_data(df['Date'], df['Price'])
            # -------------------------------------
            # Prüfen, ob das alte Zeitfenster zur neuen Aktie passt
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
                print("-> Zeitfenster auf Vollansicht (VAR).")
                
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
schalter_handles.append(btn_clr)     # in aktive handles-Liste eintragen

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
    
    # Timestamp-Wert direkt im Zeitfenster abholen
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
    ax2.text(0.5, 0.5, 'weiteres Auswertungsverfahren:\n\n[ DIAGNOSE 2 LEER ]\n\nkann nachgetragen werden.', 
             ha='center', va='center', fontsize=12, color='red', weight='bold', bbox=dict(facecolor='yellow', alpha=0.3))
    ax2.set_title(f"fig2 noch ohne Titel: {str_start} bis {str_end}")
    fig2.canvas.draw()
    plt.show()
# ------------------------------------------------------------------------------
#      18              Aufruf 3 Diagnose-Dummy
# ------------------------------------------------------------------------------
def on_diag3_clicked(event):
    df_zeitfenster, str_start, str_end = von_bis_ablesen()
    fig3, ax3 = plt.subplots(figsize=(9, 5.5))
    fig3.canvas.manager.set_window_title('Figur 3 - Platzhalter 2')
    ax3.text(0.5, 0.5, 'weiteres Auswertungsverfahren:\n\n[ DIAGNOSE 3 LEER ]\n\nkann nachgetragen werden.', 
             ha='center', va='center', fontsize=12, color='gray', weight='bold')
    ax3.set_title(f"fig3 noch ohne Titel: {str_start} bis {str_end}")
    fig3.canvas.draw()
    plt.show()
# ------------------------------------------------------------------------------
#      19              Aufruf 4 Diagnose-Dummy
# ------------------------------------------------------------------------------
def on_diag4_clicked(event):
    df_zeitfenster, str_start, str_end = von_bis_ablesen()
    fig4, ax4 = plt.subplots(figsize=(9, 5.5))
    fig4.canvas.manager.set_window_title('Figur 4 - Platzhalter 3')
    ax4.text(0.5, 0.5, 'weiteres Auswertungsverfahren:\n\n[ DIAGNOSE 4 LEER ]\n\nkann nachgetragen werden.', 
             ha='center', va='center', fontsize=12, color='gray', style='italic')
    ax4.set_title(f"fig4 noch ohne Titel: {str_start} bis {str_end}")
    fig4.canvas.draw()
    plt.show()

btn_diag1.on_clicked(on_diag1_clicked)  # Diagnose-Schalter abrufen
btn_diag2.on_clicked(on_diag2_clicked)
btn_diag3.on_clicked(on_diag3_clicked)
btn_diag4.on_clicked(on_diag4_clicked)
# ---------------------------------------------------------------------------------
#     20  Huckepack-Aufruf der beiden Slider um beim Schieben plot neu zu zeichnen
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
#     22 Ticker-Oszillograph starten/neu zeichnen und fig2,ax2 nachtragen
# ------------------------------------------------------------------------------
neu_zeichnen(0, len(df)-1)
plt.show()


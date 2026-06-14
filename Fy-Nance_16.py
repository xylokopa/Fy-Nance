# Fy-Nance_16_260614.py 14-06-2026 800Zeilen Ticker-Oszillograph R.Wu_GastH_Nr178854
# https://github.com/xylokopa/Fy-Nance
import math
import numpy as np
import pandas as pd
import yfinance as yf
import scipy.stats as stats
import statsmodels.api as sm  # pip install statsmodels (Lilliefors)
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from matplotlib.widgets import Slider, Button, TextBox
import os
plt.rcParams['toolbar'] = 'None'
# ==============================================================================
#     01    Projekt Variablen
# ==============================================================================
# Hier sitzen die 8 Haupt-Steuerleitungen gut sichtbar direkt unter den Imports.
# In den Funktionen darunter wird nur noch gelesen oder gezielt zugegriffen.
val_online = 0            # default 1 = Online live, 0 = Offline
val_clr    = 1            # Default 1 = FEST(Zoom behalten), 0 = VAR (Reset)
akt_index  = 2            # Default-Ticker (Standard: 2 = Apple)
yfNAME = "AAPL"                    # Default-Ticker für den Online-Start
offlinecsv = "02Apple_Offline.csv" # Default-Ticker für den Offline-Start
trigger = False                    # start-stop zum Schaubild-zeichnen
ANF_DATUM = "2015-01-05"           # MAX-Fenster ANF
END_DATUM = "2026-06-05"           # MAX-Fenster END
ANF_DATUM = "2020-01-05"           # CORONA-Fenster ANF
END_DATUM = "2020-11-05"           # CORONA-Fenster END
moving_size = 20                   # Moving-Average-Fenster
preis_linie = 1  # Preis-Linie ein
MAmiw_linie = 0  # MoveAverage aus
FEmiw_linie = 0  # Fenster-MiW aus
diffz_linie = 0  # PreisMA-Dif aus
FFT_Diagram = 0  # Fourier-Spektrum(Log) aus
df = pd.DataFrame()                # Projekt DataFrame
# ==============================================================================
#     02 drei Fenster fig1,ax1 bis fig3,ax3 für canvas.draw_idle() bereitstellen
# ==============================================================================
# Frequenz-Rezept des im Tupel(Ticker,Zeitfenster) erfassten Börsen-Ereignisses
fig3, ax3 = plt.subplots(figsize=(5.5, 4.20))
fig3.canvas.manager.set_window_title('3.Fenster - Fourier-Signatur des Börsen-Ereignisses')
# Positionieren: Breite=550, Höhe=412, X=0 (ganz links), Y=0 (ganz oben)
fig3.canvas.manager.window.geometry("550x420+0+0")
# Das Statistik-Fenster bereitstellen
fig2, ax2 = plt.subplots(figsize=(5.5, 4.20))
fig2.canvas.manager.set_window_title('2.Fenster - Abweichungsdichte vom Moving-Average')
# Positionieren: X=0 (ganz links), Y=450 (unter Fenster 3)
fig2.canvas.manager.window.geometry("550x420+0+440")
# Das im Interpreter-Ablauf VORHER zu befüllende Oszillographen-Fenster danach ...
fig1, ax1 = plt.subplots(figsize=(11, 8.60))
fig1.canvas.manager.set_window_title('1.Fenster  - Ticker Oszillograph')
plt.subplots_adjust(left=0.20, bottom=0.24, right=0.95)
# Positionieren: X=560 (rechts von Fenster 2/3), Y=0 (ganz oben)
fig1.canvas.manager.window.geometry("1100x860+550+0")

# ------------------------------------------------------------------------------
#     03 Ticker-Liste aus CSV-Liste laden
# ------------------------------------------------------------------------------
try:
    ticker_df = pd.read_csv('Ticker-Liste_alt.csv')
except FileNotFoundError:
    # Default Liste falls Ticker-Liste_alt.csv fehlt
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
    with open('Ticker-Liste_alt.csv', 'w') as f:
        f.write(ticker_liste)
    ticker_df = pd.read_csv('Ticker-Liste_alt.csv')
# ------------------------------------------------------------------------------
#     04  Ticker-Daten Download oder aus csv lesen
# ------------------------------------------------------------------------------
def lade_ticker_daten():# nur globale Argumente
    global df           # 1.Dataframe
    global ticker_df    # 2.Ticker-liste
    global akt_index    # 3.Ticker_index
    global moving_size  # 4.Moving_average-Fenster
    akt_ticker = ticker_df.iloc[akt_index] # Zeilenwahl in Ticker-Liste = integer location 
    akt_Num = akt_ticker['Num']
    akt_Nam = akt_ticker['Nam']
    akt_Tik = akt_ticker['Tik']
    csv_Nam = f"{akt_Num}{akt_Nam}_Offline.csv"
    csv_Bak = f"{akt_Num}{akt_Nam}_Offline.bak"
    # Download df_live mit 1.Spalte datum (von start bis end) und 2.Spalte Preis
    if val_online > 0:
        try:
            print(f"Lade {akt_Tik} live von Yahoo Finance...")
            df_live = yf.Ticker(akt_Tik).history(start=ANF_DATUM, end=END_DATUM)[["Close"]]
            df_live.index = df_live.index.tz_localize(None)
            df_csv = df_live.rename(columns={"Close": "Price"}).dropna().reset_index()
            df_csv['Date'] = pd.to_datetime(df_csv['Date'])
            df_csv.to_csv(csv_Bak, index=False)
            print(f"-> live geladen und in {csv_Bak} gepuffert")
            df = df_csv.sort_values('Date').reset_index(drop=True)
            return
        except Exception as e:
            print(f"{akt_Tik} Download gescheitert ({e}) => Offline-csv")
    # Offline-csv df_csv mit 1.Spalte datum (von start bis end) und 2.Spalte Preis
    if os.path.exists(csv_Nam):
        print(f"lokale csv {csv_Nam} wird geladen...")
        df_csv = pd.read_csv(csv_Nam)
        df_csv['Date'] = pd.to_datetime(df_csv['Date'])
        df = df_csv.sort_values('Date').reset_index(drop=True)
    else:
        print(f"Offline-csv {csv_Nam} nicht gefunden! Leeres Frame als Ersatz.")
        df = pd.DataFrame(columns=['Date', 'Price'])
# ------------------------------------------------------------------------------
#     05  Default-Ticker Apple laden und draw_idle()-Überwachungs-Trigger setzen 
# ------------------------------------------------------------------------------
lade_ticker_daten()
line_preis = None
trigger = False
# ------------------------------------------------------------------------------
#     06  Gleitenden Durchschnitt MA(MeanAverage) redundant einbauen ... 
# ------------------------------------------------------------------------------
df['MA'] = df['Price'].rolling(window=moving_size).mean()
# ------------------------------------------------------------------------------
#     07  Achsen und Anheftungspunkte für Widgets platzieren 
# ------------------------------------------------------------------------------
ax1_von = plt.axes([0.21, 0.07, 0.22, 0.03])       # Anheftung von-Slider
ax1_online = plt.axes([0.47, 0.062, 0.06, 0.05])   # Anheftung ONLINE-OFFLINE-Schalter
ax1_clr = plt.axes([0.44, 0.0125, 0.12, 0.035])    # Anheftung Zeitfenster-Umschalter 
ax1_bis = plt.axes([0.56, 0.07, 0.22, 0.03])       # Anheftung bis-Slider

ax1_box_start = plt.axes([0.21, 0.14, 0.12, 0.04]) # Anheftung Linkes Datumsfenster
ax1_box_end = plt.axes([0.66, 0.14, 0.12, 0.04])   # Anheftung Rechtes Datumsfenster
text_mitte = fig1.text(0.38, 0.155, '', bbox=dict(facecolor='white', alpha=1.0, edgecolor='black'))

ax1_diag1 = plt.axes([0.22, 0.01, 0.10, 0.04])     # Anheftung der Diagnose-Schalter
ax1_diag2 = plt.axes([0.33, 0.01, 0.10, 0.04])
ax1_diag3 = plt.axes([0.57, 0.01, 0.10, 0.04])
ax1_diag4 = plt.axes([0.68, 0.01, 0.10, 0.04])
# ------------------------------------------------------------------------------
#     08   Vorbereitung Ticker-Klavier am linken Rand 
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
#     09            Schalter-Widgets platzieren 
# ------------------------------------------------------------------------------

slider_von = Slider(ax1_von, 'von', 0, len(df)-1, valinit=0, valfmt='%0.0f')
slider_bis = Slider(ax1_bis, 'bis', 0, len(df)-1, valinit=len(df)-1, valfmt='%0.0f')
btn_online = Button(ax1_online, 'ONLINE' if val_online else 'OFFLINE', color='aqua' if val_online else 'pink')

text_box_start = TextBox(ax1_box_start, '', initial='')
text_box_end   = TextBox(ax1_box_end, '', initial='')

# CLR-Schalter direkt unter Online-Schalter 
# Variable für CLR-Zustand (1 = FEST / Zoom behalten, 0 = RESET / Vollansicht)
val_clr = 1 
btn_clr = Button(ax1_clr, 'Zeitfenster : FEST', color='lime')
btn_clr.label.set_fontsize(10)

# --- PLATZIERUNG DIAGNOSE-BUTTONS  ---
btn_diag1 = Button(ax1_diag1, 'VOLATILITAET', color='#d3d3d3')
btn_diag2 = Button(ax1_diag2, 'Movg-Average', color='#e0e0e0')
btn_diag3 = Button(ax1_diag3, 'Diffz-Dichte', color='#e0e0e0')
btn_diag4 = Button(ax1_diag4, 'FFT-Perioden', color='#e0e0e0')

# ------------------------------------------------------------------------------
#     10       Schaubild-Achsen skalieren
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
#     11                 Zeitfenster auslesen
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
    
    return df_zeitfenster, str_start, str_end, idx_von, idx_bis
# ------------------------------------------------------------------------------
#                      Bewertung statistische Tests
# ------------------------------------------------------------------------------
def Bewertung_popup(n,lf_stat,lf_p,lf_Hyp,sw_stat,sw_p,sw_Hyp):
    global fig5
    # Grenzziehung & Fallunterscheidung für den Text
    if n < 30:
        sample_class = "KLEINE STICHPROBE"
        grenzwert_text = "N/A"
        wuerdigung = ("WARNUNG: Geringe statistische Aussagekraft!\n"
                      "Verteilungstests bei n < 30 sehr ungenau.\n"
                      "Nutze primär visuelles Histogramm."
        )
    elif 30 <= n <= 250:
        sample_class = "MITTLERE STICHPROBE (Optimaler Bereich)"
        lilliefors_critical = 0.886 / np.sqrt(n)
        grenzwert_text = f"{lilliefors_critical:.4f}"
        wuerdigung = ("Stichprobe im opt.mathematik-Fenster.\n"
        "Testergebnissen mit hoher Verlässlichkeit\n"
        "und direkter Aussagekraft."
        )
    else: # n > 250 (Trifft bei Ihren n=283 zu)
        sample_class = "GROSSE STICHPROBE (Hohe Sensitivität)"
        lilliefors_critical = 0.886 / np.sqrt(n)
        grenzwert_text = f"{lilliefors_critical:.4f}"
        wuerdigung = (f"BEM: Bei n={n} greift das Schärfe-Paradoxon.\n"
        f"Der Test bestraft kleinste Abweichungen. Trotz Ablehnung\n"
        f"zeigt Shapiro-Wilk ({sw_stat*100:.1f}%), dass die dMA-Grundform\n"
        f"im Kernbereich stabil der Gauß-Kurve folgt."
        )
    # Entscheidungen textlich aufbereiten
    lf_Hyp = "Annahme (Normalverteilt)" if lf_p > 0.05 else "Ablehnung"
    sw_Hyp = "Annahme (Normalverteilt)" if sw_p > 0.05 else "ABGELEHNT"  
    # --- 2. String-Zusammensetzung im Monospace-Look ---
    report_text = (
        f"===  ({sample_class}) ===\n"
        f"Effekt. Handelstage: n = {n}\n"
        f"Lilliefors-Zufallstoleranz: {grenzwert_text}\n"
        f"--------------------------------------------------------\n"
        f"1.LILLIEFORS-TEST\n  (KS-Korrektur f.geschätztes Mu/Sigma)\n"
        f"- Teststatistik (D): {lf_stat:.4f}\n"
        f"- p-Wert:            {lf_p:.4f}\n"
        f"- H0-Entscheidung:   {lf_Hyp}\n\n"
        f"2.SHAPIRO-WILK-TEST (Symmetrie & Formprüfung)\n"
        f"- Teststatistik (W): {sw_stat:.4f} (Ähnlichkeit:{sw_stat*100:.1f}%)\n"
        f"- p-Wert:            {sw_p:.4f}\n"
        f"- H0-Entscheidung:   {sw_Hyp}\n"
        f"--------------------------------------------------------\n"
        f"FAZIT FÜR DIE FINANZANALYSE:\n{wuerdigung}"
    )
    # --- 3. Matplotlib Canvas Update ---
    bbox_props = dict(boxstyle="round,pad=1", facecolor="#f8f9fa", edgecolor="#b3b3b3", alpha=1.0)

    if 'fig5' in globals() and fig5 is not None and plt.fignum_exists(fig5.number):
        fig5.canvas.manager.window.lift()  # Holt bestehendes Fenster on top
        return

    fig5, ax5 = plt.subplots(figsize=(8,3.125))
    fig5.canvas.manager.set_window_title('5.Fenster - Stichproben-Bewertung')
    # Positionieren: Breite=550, Höhe=412, X=0 (ganz links), Y=0 (ganz oben)
    fig5.canvas.manager.window.geometry("550x412+0+45")
    ax5.axis('off')  
    ax5.text(0.00,1, report_text, 
          transform=ax5.transAxes, 
          fontsize=9, 
          verticalalignment='top', 
          fontfamily='monospace', # Wichtig für die Tabellen-Ausrichtung (feste Zeichenbreite)
          bbox=bbox_props)
    fig5.canvas.draw_idle()
# ------------------------------------------------------------------------------
def Bewertung_konsole(n):
    # 1. Berechnung des kritischen Grenzwerts (nur gültig ab n > 30)
    if n >= 30:
        lilliefors_critical = 0.886 / np.sqrt(n)
        grenzwert_text = f"{lilliefors_critical:.4f}"
    else:
        lilliefors_critical = None
        grenzwert_text = "N/A (Tabelle nutzen)"
    
    # 2. Fallunterscheidung und Text-Würdigung
    if n < 30:
        Proben_typ = "KLEINE STICHPROBE"
        Kommentar = ("WARNUNG: Geringe statistische Aussagekraft! Verteilungstests bei n < 30\n"
                     "sehr ungenau. Nutze primär visuelle Histogramm-Analyse."
        )
    elif 30 <= n <= 250:
        Proben_typ = "MITTLERE STICHPROBE (Optimaler Testbereich)"
        Kommentar = ("Stichprobe liegt im optimalen mathem. Fenster. Testergebnisse\n"
                     "mit hoher Verlässlichkeit und direkter Aussagekraft."
        )
    else:  # n > 250
        Proben_typ = "GROSSE STICHPROBE (Vorsicht: Hohe Sensitivität)"
        Kommentar = (f"HINWEIS: Bei n={n} Schärfe-Paradoxon. Test bestraft kleinste\n"
                     f"Abweichungen. Shapiro-Wilk ({sw_stat*100:.1f}%),\n"
                     f"dMA-Grundform folgt im Kernbereich stabil der Gauß-Kurve."
        )
    # --- Ausgabe-Template (Ausschnitt für Ihre Konsole) ---
    print("=" * 70)
    print(f"BEWERTUNG der Ticker-Linie bei {n}-Handelstagen :\n Proben-Typ: {Proben_typ}")
    print(f"Stichprobenumfang (n): {n} | Lilliefors-Zufallstoleranz: {grenzwert_text}")
    print("=" * 70)
    print(f"Kommentar:\n",Kommentar)
    print("=" * 70)
# ------------------------------------------------------------------------------
#     12   Ticker-Schaubild neu zeichen
# ------------------------------------------------------------------------------
def neu_zeichnen(idx_von, idx_bis):
    global line_preis
    global trigger
    global df           # 1.Dataframe
    global ticker_df    # 2.Ticker-liste
    global akt_index    # 3.Ticker_index
    global moving_size  # 4.Moving_average-Fenster
    global fig3
    akt_ticker = ticker_df.iloc[akt_index] # Zeilenwahl in Ticker-Liste = integer location 
    akt_Num = akt_ticker['Num']
    akt_Nam = akt_ticker['Nam']
    akt_Tik = akt_ticker['Tik']
    csv_Nam = f"{akt_Num}{akt_Nam}_Offline.csv"

    if trigger or df.empty: return
    trigger = True
    # --- Database-Erweiterungen Refresh ------------
    df['MA'] = df['Price'].rolling(window=moving_size).mean()
    df['Diff'] = df['Price'] - df['MA']
    # ----------------------------------------------------------------------           
    # Erstes Fenster ax1 Ticker-Linie mit Mov'Average MA und Abweichg. dMA
    # ----------------------------------------------------------------------  
    ax1.clear()   # MAIN-WINDOW
    ax1.set_title(f"[2]Ticker:{akt_Num}/{akt_Nam}/{akt_Tik} von {idx_von} bis {idx_bis}",fontsize=12, fontweight='bold')
    fig1.canvas.manager.set_window_title('1.Fenster - Ticker Oszillograph')
    plt.subplots_adjust(left=0.20, bottom=0.24, right=0.92)
    
    # 1. Hauptlinie zeichnen (Nutzt noch das ganze df, Matplotlib clippt das per xlim)
    if preis_linie:
       line_preis, = ax1.plot(df['Date'], df['Price'], label='preis', color='blue')
    # 2. Hauptlinie -------------------------   
    if MAmiw_linie:
       line_MAmiw, = ax1.plot(df['Date'], df['MA'], label='MA', color='green')    

    ma_mittelwert = df['MA'].mean()
    y_FEmiw = [ma_mittelwert] * len(df)
    # 3. Hauptlinie -------------------------
    if FEmiw_linie:
       line_FEmiw, = ax1.plot(df['Date'], y_FEmiw, label='Fenster-MW', color='black', linestyle='--')
    df['Diff'] =  df['Price'] - df['MA']
    # 4. Hauptlinie -------------------------
    if diffz_linie:
       line_diff, = ax1.plot(df['Date'], ma_mittelwert + df['Diff'], label='diffz', color='red')

    ax1.set_xlabel('Abweichung vom MA (Euro)')
    ax1.set_ylabel('Preis in €')
    ax1.grid(True, linestyle='--')
    ax1.legend(loc='upper right')

    # 2. Slider-Index-Validierung für Synchronisation
    idx_von = max(0, min(idx_von, len(df)-1))
    idx_bis = max(0, min(idx_bis, len(df)-1))
    if idx_von > idx_bis: idx_von = idx_bis

    slider_von.set_val(idx_von)
    slider_bis.set_val(idx_bis)

    # 3. Synchronisierung des Zeitfensters
    df_zeitfenster = df.iloc[idx_von:idx_bis+1]
    
    if not df_zeitfenster.empty:
        dt_start = pd.Timestamp(df_zeitfenster['Date'].values[0])
        dt_end = pd.Timestamp(df_zeitfenster['Date'].values[-1])
        
        str_start = dt_start.strftime('%Y-%m-%d')
        str_end = dt_end.strftime('%Y-%m-%d')
        tage_differenz = (dt_end - dt_start).days
        
        ax1.set_xlim(dt_start, dt_end)
        ax1.set_ylim(df_zeitfenster['Price'].min() * 0.95, df_zeitfenster['Price'].max() * 1.05)
        
        axen_skalierung(ax1, dt_start, dt_end)
        
        ax1.set_title(f"[1]Ticker:{akt_Num}/{akt_Nam}/{akt_Tik} {str_start} + {tage_differenz} Tage = {str_end}")
        plt.subplots_adjust(left=0.20, bottom=0.24, right=0.92)

        text_mitte.set_text(f" {str_start} + {tage_differenz} Tage = {str_end} ")
        
        if text_box_start.text_disp.get_text() != str_start: 
            text_box_start.set_val(str_start)
        if text_box_end.text_disp.get_text() != str_end: 
            text_box_end.set_val(str_end)
            
        # ----------------------------------------------------------------------
        # Refresh der dynamisch veränderten Daten im 'df_zeitfenster'
        # ----------------------------------------------------------------------
        diff_dropna = df_zeitfenster['Diff'].dropna() # <-- GEAENDERT auf df_zeitfenster
        diff_data = diff_dropna.values
        
        # Kontrolle ob genug Datenpunkte im Slider-Refresh-Fenster vorhanden
        if len(diff_data) > 5:
            # Statistik auf Basis des synchronisierten Slider-Fensters berechnen
            mu = np.mean(diff_data)
            sigma = np.std(diff_data) # verzerrter Schätzer
            sigmd = np.std(diff_data,ddof=1)
            alpha = 0.05
            n_stat = len(diff_data)
            sqrt1n = 1/math.sqrt(n_stat)
            # Bewertung_popup(n_stat,lf_stat,lf_p,lf_Hyp,sw_stat,sw_p,sw_Hyp)
            ks_stat, ks_p = stats.kstest(diff_data, 'norm', args=(mu, sigma))
            ks_Hyp = 1 if ks_p > alpha else 0
            lf_stat, lf_p = sm.stats.lilliefors(diff_data,dist='norm')
            lf_Hyp = 1 if lf_p > alpha else 0
            sw_stat, sw_p = stats.shapiro(diff_data)
            sw_Hyp = 1 if sw_p > alpha else 0
            # Konsole gibt aktuelle Fenster-Werte und Kolmogorov-Smirnov-Abweichung aus:
            print(f"Fenster [{str_start} bis {str_end}] -> KS-Abweichung: {ks_stat:.4f}")
            print(f"Nullhypothese KolmSmi={ks_Hyp},Lillifo={ks_Hyp},ShapWil={sw_Hyp}")
            if (diffz_linie):
               Bewertung_konsole(n_stat)
               Bewertung_popup(n_stat,lf_stat,lf_p,lf_Hyp,sw_stat,sw_p,sw_Hyp)
            # ----------------------------------------------------------------------           
            # Zweites Fenster ax2 dMA-Histogramm und Vergl.Gauss-Verteilung
            # ----------------------------------------------------------------------
            ax2.clear()
            if MAmiw_linie:
               count, bins, ignored = ax2.hist(diff_data, bins=30, density=True, 
                                   alpha=0.6, color='blue', label='dMA in €/Tag')          
            if diffz_linie:
               ax2.set_title(f"n:{n_stat} KolmogSmirnov:{ks_Hyp}  Lilliefors:{lf_Hyp}  ShapiroWilk:{sw_Hyp}")
                                                      #fontsize=10, fontweight='bold')           
               gauss = stats.norm.pdf(bins, mu, sigma)
               ax2.plot(bins, gauss, color='red', linewidth=2, 
                       label=f'Gauss.Abw\n(KS:{ks_stat:.3f}\n(LF:{lf_stat:.3f}\n(SW:{sw_stat:.3f})')
               ax2.set_ylabel('dMA-Dichte gegen Gauss-Dichte', color='red')
               ax2.legend()
               ax2.grid(True, linestyle='--')
            # ----------------------------------------------------------------------           
            # Drittes Fenster ax3 FFT-Analyse Abweichung dMA vom Gleit-Mittelwert MA
            # ----------------------------------------------------------------------
            signal = diff_data
            N = len(signal) ##
            if N > 5:
                 fft_werte = np.fft.fft(signal)
                 frequenzen = np.fft.fftfreq(len(signal))
            
                 halbe = len(signal) // 2
                 freq = frequenzen[:halbe]
                 amp = np.abs(fft_werte[:halbe])
                 # ----------------------------------------------------------------------           
                 # Konsolen-Ausgabe zur FFT-Analyse der dMA-Zyklen vs. Gleitmittelwert MA
                 # ----------------------------------------------------------------------
                 # 2. Top 3 "Resonanzen" (Formanten) des Boersen-Ereignisses 
                 # ignoriert die Abweichung 0 (Gleichanteil)
                 sortierte_idxs = np.argsort(amp[1:])[::-1] + 1
                 print("\n--- FREQUENZREZEPT DES TICKERS (FORMANTEN) ---")
                 for i in range(min(3, len(sortierte_idxs))):
                     idx = sortierte_idxs[i]
                     # Zyklusdauer in Tagen (Kehrwert der Frequenz)
                     zyklus_tage = 1.0 / freq[idx] if freq[idx] > 0 else float('inf')
                     # Relative Amplitude (der fft_werte)
                     amp_prozent = (amp[idx] / np.sum(amp)) * 100
        
                     print(f"Periode {i+1} (Resonanz): {zyklus_tage:.1f} Tage Takt "
                           f"| Amplitude: {amp_prozent:.1f}%")
            
                 dominant_amp = np.argmax(amp[1:]) + 1
                 dominant_frq = 1 / freq[dominant_amp]
                 print(f"Dominanter Zyklus im Zeitfenster: {dominant_frq:.1f} Tage")
            # ----------------------------------------------------------------------           
            #  FFT-Schaubild der dMA-Zyklen im Kurs-Diagramm vs. Gleitmittelwert MA
            # ----------------------------------------------------------------------
            if FFT_Diagram:
               ax3.clear()
               ax3.set_xscale('log')
               ax3.set_title('Log-Spektrum  FFT(dMA) der MA-Abweichungen ', fontsize=10, fontweight='bold')
               # Das lila Amplituden-Spektrum logarithmisch aufzeichnen
               ax3.plot(freq, amp, color='purple', label='dMA-FFT-Spektrum') 
        
               # Die Top 3 Resonanz-Frequenzen als vertikale Linien einzeichnen
               farben = ['darkred', 'red', 'orange']
               for i in range(min(3, len(sortierte_idxs))):
                   idx = sortierte_idxs[i]
                   f_frequz = freq[idx]
                   amp_frequz = amp[idx]
                   zyklus_tage = 1.0 / f_frequz if f_frequz > 0 else 0
                   ax3.vlines(f_frequz, 0, amp_frequz, colors=farben[i], linestyle='-', linewidth=2,
                   label=f'Periode {i+1}: {zyklus_tage:.1f} Tage')
               ax3.set_xlabel('Frequenz (1/Tage)')
               ax3.set_ylabel('Amplitude')
               ax3.legend(loc='upper right')
               ax3.grid(True, linestyle='--')
               fig3.tight_layout()
    # ----------------------------------------------------------------------
    # drei Leinwaende synchron neu rendern
    # ----------------------------------------------------------------------
    fig1.canvas.draw_idle()
    fig2.canvas.draw_idle()
    fig3.canvas.draw_idle()  # <-- Das dritte Glied der Fenster-Kette

    trigger = False
# ------------------------------------------------------------------------------
#     13  event-überwachung Ticker-Klavier am linken Rand 
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
        lade_ticker_daten()
        if not df.empty:
            # Max. Grenzen des neuen Tickers ermitteln
            max_index_neu = len(df) - 1
            
            # neue Slider-Maximalgrenzen anpassen
            slider_von.valmax = max_index_neu
            slider_bis.valmax = max_index_neu

            neu_zeichnen(idx_von_alt, idx_bis_alt)

            # statt line_preis.set_data(df['Date'], df['Price'])
            # -------------------------------------
            # Prüfen, ob das alte Zeitfenster zur neuen Aktie passt
            # -------------------------------------
            if val_clr == 1 and idx_bis_alt <= max_index_neu:
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
                if val_clr == 1:
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
#     14     Schleife zur event-überwachung aller Klaviertasten
# ------------------------------------------------------------------------------
for btn_obj, n_str, nam, tik, b_idx in ticker_klavier:
    btn_obj.on_clicked(ticker_klavier_klick(n_str, nam, tik, b_idx))

# ------------------------------------------------------------------------------
#     15             Funktionalität des CLR-Schalters
# ------------------------------------------------------------------------------
def on_clr_clicked(event):
    global val_clr
    if val_clr > 0:
        val_clr = 0
        btn_clr.label.set_text("Zeitfenster : VAR")
        btn_clr.color = "pink"
        btn_clr.ax1.set_facecolor("pink")
        print("[COCKPIT] Modus gewechselt: Zeitfenster bei Tickerwechsel variabel (VAR).")
    else:
        val_clr = 1
        btn_clr.label.set_text("Zeitfenster : FEST")
        btn_clr.color = "lime"
        btn_clr.ax1.set_facecolor("lime")
        print("[COCKPIT] Modus gewechselt: Zeitfenster bei Tickerwechsel konstant (FEST).")
    fig1.canvas.draw_idle()

btn_clr.on_clicked(on_clr_clicked)   # clr-Schalter abrufen
schalter_handles.append(btn_clr)     # in aktive handles-Liste eintragen
# ------------------------------------------------------------------------------
#     16           Funktionalität des ONLINE-Schalters
# ------------------------------------------------------------------------------
def on_online_clicked(event):
    global line_preis
    global val_online
    global df           # 1.Dataframe
    global ticker_df    # 2.Ticker-liste
    global akt_index    # 3.Ticker_index
    global moving_size  # 4.Moving_average-Fenster
    akt_ticker = ticker_df.iloc[akt_index] # Zeilenwahl in Ticker-Liste = integer location 
    akt_Num = akt_ticker['Num']
    akt_Nam = akt_ticker['Nam']
    akt_Tik = akt_ticker['Tik']
    csv_Nam = f"{akt_Num}{akt_Nam}_Offline.csv"  
    # Modus umschalten
    if val_online > 0:
        val_online = 0
        btn_online.label.set_text("OFFLINE")
        btn_online.color = "pink"
    else:
        val_online = 1
        btn_online.label.set_text("ONLINE")
        btn_online.color = "aqua"    
    # Aktuelle Aktie im neuen Modus nachladen
    lade_ticker_daten()
    if not df.empty:
        line_preis.set_data(df['Date'], df['Price'])
        neu_zeichnen(int(slider_von.val), int(slider_bis.val))
    fig1.canvas.draw_idle()

btn_online.on_clicked(on_online_clicked)  # online-Schalter abrufen
# ------------------------------------------------------------------------------
#     17                Fenster 4 Diagnose-Volatilität
# ------------------------------------------------------------------------------
def on_diag1_clicked(event):
    global fig4
    df_zeitfenster, str_start, str_end, idx_von, idx_bis = von_bis_ablesen()
    if df_zeitfenster is None or df_zeitfenster.empty: return
    
    miwe_val = df_zeitfenster['Price'].mean()
    df_zeitfenster['miwe'] = miwe_val
    df_zeitfenster['diffz'] = miwe_val + df_zeitfenster['Price'].diff().fillna(0)

    if 'fig4' in globals() and fig4 is not None and plt.fignum_exists(fig4.number):
        fig4.canvas.manager.window.lift()  # Holt bestehendes Fenster on top
        return

    fig4, ax4 = plt.subplots(figsize=(9, 5.5))
    fig4.canvas.manager.set_window_title('4.Fenster - Volatilitätsuntersuchung')
    
    ax4.plot(df_zeitfenster['Date'], df_zeitfenster['miwe'], color='black', label='miwe')
    ax4.plot(df_zeitfenster['Date'], df_zeitfenster['diffz'], color='blue', label='diffz')
    ax4.plot(df_zeitfenster['Date'], df_zeitfenster['Price'], color='red', linewidth=2, label='preis')
    
    ax4.set_title(f"fig1 Preis, Mittelwert und Differenz-Werte ({str_start} bis {str_end})")
    ax4.set_ylabel('Preis in €')
    ax4.legend(loc='upper left')
    
    # Timestamp-Wert direkt im Zeitfenster abholen
    dt_start_gesichert= pd.Timestamp(df_zeitfenster['Date'].values[0])
    dt_end_gesichert = pd.Timestamp(df_zeitfenster['Date'].values[-1])
    axen_skalierung(ax4, dt_start_gesichert, dt_end_gesichert)
    
    fig4.canvas.draw()          # Overlay-Fenster zu Diagnose 1 ausgeben
    plt.show()

# ------------------------------------------------------------------------------
#     18             Fenster 5 Diagnose-Dummy
# ------------------------------------------------------------------------------
def on_diag2_clicked(event):
    global preis_linie # Preis-Linie Semaphor
    global MAmiw_linie # MoveAverage Semaphor
    global FEmiw_linie # Fenster-MiW Semaphor
    global diffz_linie # PreisMA-Dif Semaphor
    global FFT_Diagram # FFT-Spektrum(Log)
    preis_linie = 1    # ein
    if MAmiw_linie == 1: MAmiw_linie = 0
    else: MAmiw_linie = 1
    if FEmiw_linie == 1: FEmiw_linie = 0
    else: FEmiw_linie = 1
    diffz_linie = 0    # aus
    FFT_Diagram = 0    # aus  
    df_zeitfenster, str_start, str_end, idx_von, idx_bis = von_bis_ablesen()
    neu_zeichnen(idx_von, idx_bis)
    plt.show()
# ------------------------------------------------------------------------------
#      19              Fenster 6 Diagnose-Dummy
# ------------------------------------------------------------------------------
def on_diag3_clicked(event):
    global preis_linie # Preis-Linie Semaphor
    global MAmiw_linie # MoveAverage Semaphor
    global FEmiw_linie # Fenster-MiW Semaphor
    global diffz_linie # PreisMA-Dif Semaphor
    global FFT_Diagram # FFT-Spektrum(Log)
    preis_linie = 1    # Preis-Linie ein
    if diffz_linie == 1: diffz_linie = 0
    else: diffz_linie = 1
    MAmiw_linie = 1    # ein
    FEmiw_linie = 1    # ein
    FFT_Diagram = 0    # aus
    df_zeitfenster, str_start, str_end, idx_von, idx_bis = von_bis_ablesen()
    neu_zeichnen(idx_von, idx_bis)
    plt.show()
# ------------------------------------------------------------------------------
#     20              Fenster 7 Diagnose-Dummy
# ------------------------------------------------------------------------------
def on_diag4_clicked(event):
    global preis_linie # Preis-Linie Semaphor
    global MAmiw_linie # MoveAverage Semaphor
    global FEmiw_linie # Fenster-MiW Semaphor
    global diffz_linie # PreisMA-Dif Semaphor
    global FFT_Diagram # FFT-Spektrum(Log)
    preis_linie = 1    # ein
    MAmiw_linie = 1    # ein
    FEmiw_linie = 1    # ein
    diffz_linie = 1    # ein
    if FFT_Diagram == 1: FFT_Diagram = 0
    else: FFT_Diagram = 1
    df_zeitfenster, str_start, str_end, idx_von, idx_bis = von_bis_ablesen()
    neu_zeichnen(idx_von, idx_bis)
    plt.show()
# ------------------------------------------------------------------------------
btn_diag1.on_clicked(on_diag1_clicked)  # Diagnose-Schalter abrufen
btn_diag2.on_clicked(on_diag2_clicked)
btn_diag3.on_clicked(on_diag3_clicked)
btn_diag4.on_clicked(on_diag4_clicked)
# ---------------------------------------------------------------------------------
#     21  Huckepack-Aufruf der beiden Slider um beim Schieben plot neu zu zeichnen
# ---------------------------------------------------------------------------------
slider_von.on_changed(lambda v: neu_zeichnen(int(slider_von.val), int(slider_bis.val)))
slider_bis.on_changed(lambda v: neu_zeichnen(int(slider_von.val), int(slider_bis.val)))
# ----------------------------------------------------------------------------------
#     22  Textbox-ENTER-Submit-Funktionalität für das Zeitfenster per Datums-Eingabe
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
#     23 Ticker-Oszillograph starten/neu zeichnen und fig123,ax123 refreshen
# ------------------------------------------------------------------------------
neu_zeichnen(0, len(df)-1)
plt.show()


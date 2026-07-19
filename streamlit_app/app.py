# fy-nance-app.streamlit.app.py 16-07-2026 514-Zeilen new-app_10Bootstrap_6.bak
# ==============================================================================
# TEIL 1: IMPORTE & PROJEKT-INITIALISIERUNG
# ==============================================================================
import math
import numpy as np
import pandas as pd
import yfinance as yf
from scipy import stats
import statsmodels.api as sm
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from datetime import datetime, date
import os
import locale
import streamlit as st
st.markdown("""<style>[data-testid="stSidebar"] {min-width:200px;max-width:200px;}
            [data-testid="stMainBlockContainer"] {
             padding-left: 1rem !important;padding-right: 1rem !important;
             padding-top: 3rem !important;max-width: 100% !important;}</style>""",
             unsafe_allow_html=True)
# Seite für breites Web-Layout 
st.set_page_config(layout="wide", page_title="Börsen-Oszillograph")
osz = 'Oszi_03n'
AKTUELLER_ORDNER = os.path.dirname(os.path.abspath(__file__))
csv_ordner = os.path.join(AKTUELLER_ORDNER, "CSV")
# Lokale Zeiteinstellung initialisieren
try:
    locale.setlocale(locale.LC_TIME, "de_DE.utf8")
except Exception:
    try:
        locale.setlocale(locale.LC_TIME, "de_DE")
    except Exception:
        pass  # Fallback, falls System-Locale fehlt
# Ticker-Liste laden (Automatisches Fallback, falls Datei fehlt)
if not os.path.exists('Ticker-Liste_alt.csv'):
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
    with open('ticker-liste_alt.csv', 'w', encoding='utf-8') as f:
        f.write(ticker_liste)
ticker_df = pd.read_csv('ticker-liste_alt.csv')
# ==============================================================================
# TEIL 2: STREAMLIT UI (INITIALISIERUNG & SIDEBAR WIDGETS)
# ==============================================================================
# 1. INIT ALL SESSION-STATE-VARS (Verhindert AttributeError)
if 'aktueller_ticker_index' not in st.session_state:
    st.session_state.aktueller_ticker_index = 2  # Standardwert Apple
if 'letzter_ticker' not in st.session_state:
    st.session_state.letzter_ticker = 2
if 'hist_bak' not in st.session_state:
    st.session_state.hist_bak = []
if 'hist_vor' not in st.session_state:
    st.session_state.hist_vor = []
if 'vergleichs_daten' not in st.session_state:
    st.session_state.vergleichs_daten = None
if 'vergleichs_ticker_name' not in st.session_state:
    st.session_state.vergleichs_ticker_name = ""
if 'freeze_aktiviert' not in st.session_state:
    st.session_state.freeze_aktiviert = False
# Ticker-Optionen für Selectbox vorbereiten
ticker_options = [f"{row['Num']:02d} - {row['Nam']} ({row['Tik']})" for _, row in ticker_df.iterrows()]
# Ticker-Auswahl (Greift auf initialisierte Variable)
ausgewaehlter_ticker_str = st.sidebar.selectbox(
    "test",
    ticker_options, 
    index=int(st.session_state.aktueller_ticker_index),
    label_visibility="collapsed")
# Aktuellen Index und Ticker auflösen
akt_index = ticker_options.index(ausgewaehlter_ticker_str)
akt_ticker = ticker_df.iloc[akt_index]
# Online / Offline Betriebsmodus
val_online = st.sidebar.radio("Betriebsmodus", ["Offline (Lokale CSV)", "Online (Yahoo Live)"],
                              label_visibility="collapsed")
# Kalendarische Zeitfenster
start_date = st.sidebar.date_input("Anfang (ANF_DAT)", date(2015, 1, 2))
end_date = st.sidebar.date_input("Ende (END_DAT)", date(2026, 7, 5))
# Dynamische Diagnose-Schalter
moving_size = st.sidebar.slider("Moving-Average Fenster", min_value=5, max_value=150, value=20)
preis_linie = st.sidebar.checkbox("Preis-Linie ein", value=True)
MAmiw_linie = st.sidebar.checkbox("Moving Average (MA)", value=True)
diffz_linie = st.sidebar.checkbox("Diffz-Dichte (Statistik)", value=True)
FEmiw_linie = True # Reiner Schalter ohne Callback (Verhindert Widget-Verschwinden)
FFT_Diagram = st.sidebar.checkbox("Fourier oder Wasserstein-Test", value=False)
# Wasserstein = st.sidebar.checkbox("Wasserstein-Test(W1)", value=False)
Wasserstein = True # Reiner Schalter ohne Callback 
Freez_linie = st.sidebar.checkbox("Freeze Linie in ax4", value=False)
# ==============================================================================
# TEIL 3: HISTORY-LOGBUCH (NAVIGATION MIT ABSOLUTER LOCK-STEUERUNG)
# ==============================================================================
# Den Sprung-Flag initialisieren, falls er beim ersten Start fehlt
if 'history_sprung' not in st.session_state:
    st.session_state.history_sprung = False
if 'letzter_ticker' not in st.session_state:
    st.session_state.letzter_ticker = akt_index
# ERKENNUNG DER TICKER-HERKUNFT (gesperrt gegen Überschreiben!)
if st.session_state.letzter_ticker != akt_index:
    if st.session_state.history_sprung:
        # logge nichts in 'hist_bak' und lösche NICHT 'hist_vor'!
        st.session_state.history_sprung = False  # Schalter für nächsten Klick zurück
    else:
        # Manueller Klick im Dropdown -> Rückwärts-History speichern, Vorwärts löschen
        st.session_state.hist_bak.append((st.session_state.letzter_ticker, start_date, end_date))
        st.session_state.hist_vor.clear()    
    # Aktualisiere Vergleicher auf aktuellen Stand
    st.session_state.letzter_ticker = akt_index
    st.session_state.aktueller_ticker_index = akt_index
# HTML/Streamlit-Sidebar Buttons rendern
st.sidebar.subheader("Navigation History")
col1, col2 = st.sidebar.columns(2)
with col1:
    ist_zurueck_disabled = len(st.session_state.hist_bak) == 0
    if st.button("<< Zurück <<", disabled=ist_zurueck_disabled):
        # Letzten Zustand aus dem Rückwärts-Speicher holen
        ziel_idx, ziel_start, ziel_end = st.session_state.hist_bak.pop()        
        # Aktuellen Zustand in den Vorwärts-Speicher schieben (für den >> Vor >> Button)
        st.session_state.hist_vor.append((akt_index, start_date, end_date))      
        # AKTIVIERUNG DES LOCKS: Verhindert, dass die Erkennung oben gleich zuschlägt
        st.session_state.history_sprung = True
        st.session_state.aktueller_ticker_index = ziel_idx  
        st.session_state.letzter_ticker = ziel_idx
        st.rerun()
with col2:
    ist_vor_disabled = len(st.session_state.hist_vor) == 0
    if st.button(">> Vor >>", disabled=ist_vor_disabled):
        # Nächsten Zustand aus dem Vorwärts-Speicher holen
        ziel_idx, ziel_start, ziel_end = st.session_state.hist_vor.pop()        
        # Aktuellen Zustand zurück in den Rückwärts-Speicher schieben
        st.session_state.hist_bak.append((akt_index, start_date, end_date))      
        # AKTIVIERUNG DES LOCKS: Verhindert, dass die Erkennung oben gleich zuschlägt
        st.session_state.history_sprung = True
        st.session_state.aktueller_ticker_index = ziel_idx  
        st.session_state.letzter_ticker = ziel_idx
        st.rerun()
# ==============================================================================
# TEIL 4: DATEN-LADEENGINE & FREEZE-KONTROLLE
# ==============================================================================
def lade_ticker_daten(num, nam, tik, modus, start, ende):
    if modus == "Online (Yahoo Live)":
        df = yf.download(tik, start=start, end=ende)
    else:
        num_formatted = f"{int(num):02d}"
        dateiname = f"{num_formatted}{nam}_Offline.csv"
        csv_pfad = os.path.join(csv_ordner, dateiname)
        if not os.path.exists(csv_pfad):
            raise FileNotFoundError(f"Datei fehlt: '{dateiname}' im Ordner '{csv_ordner}'")
        df = pd.read_csv(csv_pfad, parse_dates=True, index_col='Date')
        df = df.loc[start:ende]
    return df
# Feste Zeitgrenzen für den Vergleichsgraphen
VERGLEICH_START = "2015-01-01"
VERGLEICH_ENDE = "2026-07-14"
# Die Freeze-Ablaufsteuerung für ax4 im sequentiellen Code
if not Freez_linie:
    # Schalter ist AUS -> Daten folgen kontinuierlich dem aktuellen Ticker
    st.session_state.freeze_aktiviert = False
    try:
        df_vergleich = lade_ticker_daten(
            f"{akt_ticker['Num']}", 
            akt_ticker['Nam'], 
            akt_ticker['Tik'], 
            val_online, 
            VERGLEICH_START, 
            VERGLEICH_ENDE)
        st.session_state.vergleichs_daten = df_vergleich
        st.session_state.vergleichs_ticker_name = akt_ticker['Nam']
    except Exception as e:
        st.sidebar.error(f"Fehler beim Aktualisieren der Hintergrunddaten: {e}")
else:
    # Schalter ist AN -> Zustand einfrieren
    if not st.session_state.freeze_aktiviert:
        # Wird exakt einmal ausgeführt, wenn das Häkchen gesetzt wird.
        st.session_state.freeze_aktiviert = True
# HAUPTDATENSATZ LADEN (Für die Kacheln ax1, ax2, ax3)
try:
    df_raw = lade_ticker_daten(
        f"{akt_ticker['Num']}", 
        akt_ticker['Nam'], 
        akt_ticker['Tik'], 
        val_online, 
        start_date, 
        end_date)
except Exception as e:
    st.error(f"Fehler beim Laden Hauptdatensatz: {e}")
    df_raw = pd.DataFrame()
# ==============================================================================
# TEIL 5: HILFSFUNKTIONEN FÜR SKALIERUNG & ZEITFENSTER
# ==============================================================================
def zeitfenst(df_input):
    if df_input.empty:
        return df_input, 0, 0, pd.Timestamp.now(), pd.Timestamp.now(), "", ""
    df_zeitfenst = df_input.copy()
    dt_start = pd.Timestamp(df_zeitfenst['Date'].values[0])
    dt_end = pd.Timestamp(df_zeitfenst['Date'].values[-1])
    s_start = dt_start.strftime('%Y-%m-%d')
    s_end = dt_end.strftime('%Y-%m-%d')
    return df_zeitfenst, 0, len(df_input)-1, dt_start, dt_end, s_start, s_end
def axen_skalierung(target_ax, df_zeitfen, target_ax_name=""):
    if df_zeitfen.empty: return
    dt_start = pd.Timestamp(df_zeitfen['Date'].iloc[0])
    dt_end = pd.Timestamp(df_zeitfen['Date'].iloc[-1])
    target_ax.set_xlim(dt_start, dt_end)    
    if target_ax_name != '3Win':  # Keine Preis-Skala im FFT-Log
        target_ax.set_ylim(df_zeitfen['Price'].min() * 0.95, df_zeitfen['Price'].max() * 1.05)
    if target_ax_name == '4Win':
        dt_mitte = dt_start + (dt_end - dt_start) / 2
        target_ax.xaxis.set_major_locator(mticker.FixedLocator([mdates.date2num(dt_start), mdates.date2num(dt_mitte),
                                                                mdates.date2num(dt_end)]))
        def spar_formatierer(x, pos):
            def abst(x, y): return abs(x - mdates.date2num(y))
            if (abst(x, dt_mitte) < 1.0) or (abst(x, dt_start) < 1.0) or (abst(x, dt_end) < 1.0):
                return pd.to_datetime(mdates.num2date(x)).strftime('%Y-%m-%d')
            return ''
        target_ax.xaxis.set_major_formatter(mticker.FuncFormatter(spar_formatierer))
        target_ax.xaxis.set_minor_locator(mticker.NullLocator())
        target_ax.grid(True, which='major', linestyle='--', alpha=0.3)
    else:
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
# ==============================================================================
# TEIL 6: STATISTISCHE TESTS & REPORT-PLOTTING (KACHEL 5)
# ==============================================================================
def Bewertung_popup(target_ax, n, lf_stat, lf_p, lf_Hyp, sw_stat, sw_p, sw_Hyp, Nam):
    if n < 30:
        sample_class = "KLEINE STICHPROBE"
        grenzwert_text = "N/A"
        kommentar = "Geringe statistische Aussagekraft!\nVerteilungstests bei n < 30 sehr ungenau.\nPrimär visuelles Histogramm nutzen."
    elif 30 <= n <= 250:
        sample_class = "MITTLERE STICHPROBE (Optimaler Bereich)"
        grenzwert_text = f"{0.886 / np.sqrt(n):.4f}"
        kommentar = "Stichprobe im opt.mathem.Fenster.\nTestergebnissen mit hoher Verlässlichkeit\nund direkter Aussagekraft."
    else:
        sample_class = "GROSSE STICHPROBE (Hohe Sensitivität)"
        grenzwert_text = f"{0.886 / np.sqrt(n):.4f}"
        kommentar = (f"BEM:\n\nBei n={n} greift das Schärfe-Paradoxon.\n\nTest bestraft kleinste Abweichungen.\n\n"
                     f"Trotz Ablehnung zeigt Shapiro-Wilk ({sw_stat*100:.1f}%),\n\ndass die dMA-Grundform "
                     f"im Kernbereich\n\nstabil der Gauß-Kurve folgt.")
    lf_Hyp_text = "Annahme (Normalverteilt)" if lf_p > 0.05 else "Ablehnung"
    sw_Hyp_text = "Annahme (Normalverteilt)" if sw_p > 0.05 else "ABGELEHNT"  
    report_text = (
        f"{Nam} ({sample_class})\n"
        f"\nEffekt. Handelstage: n = {n}\n"
        f"\nLilliefors-Zufallstoleranz: {grenzwert_text}\n"
        f"-----------------------------------------------\n\n"
        f"1. LILLIEFORS-TEST\n  (KS-Korrektur f.geschätztes Mu/Sigma)\n\n"
        f"- Teststatistik (D): {lf_stat:.4f}\n"
        f"- p-Wert:            {lf_p:.4f}\n"
        f"- H0-Entscheidung:   {lf_Hyp_text}\n\n"
        f"2. SHAPIRO-WILK-TEST (Symmetrie & Formprüfung)\n\n"
        f"- Teststatistik (W): {sw_stat:.4f} (Ähnlichkeit:{sw_stat*100:.1f}%)\n"
        f"- p-Wert:            {sw_p:.4f}\n"
        f"- H0-Entscheidung:   {sw_Hyp_text}\n"
        f"-----------------------------------------------\n"
        f"FAZIT FINANZANALYSE:\n\n{kommentar}")
    target_ax.axis('off')  
    target_ax.text(0.00, 1.0, report_text, transform=target_ax.transAxes, fontsize=13, verticalalignment='top',
                              fontfamily='monospace')
# ==============================================================================
# TEIL 7: MAIN MOSAIC PLOTTER ENGINE (CHARTS & GRAPHICS)
# ==============================================================================
def generiere_mosaik(df_input, akt_ticker, config):
    global Wasserstein
    df_eff = df_input.copy()
    df_eff['MA'] = df_eff['Price'].rolling(window=config['moving_size']).mean()
    df_eff['Diff'] = df_eff['Price'] - df_eff['MA']
    df_zeitfenst, id_von, id_bis, dt_start, dt_end, s_start, s_end = zeitfenst(df_eff)
    if df_zeitfenst.empty: return None
    layout = [['4Win', '4Win', '2Win', '2Win', '3Win', '3Win'],
              ['1Win', '1Win', '1Win', '1Win', '5Win', '5Win'],
              ['1Win', '1Win', '1Win', '1Win', '5Win', '5Win'],
              ['1Win', '1Win', '1Win', '1Win', '5Win', '5Win']]
    fig, axd = plt.subplot_mosaic(layout, figsize=(15, 10.0),
               gridspec_kw={'width_ratios': [1.0, 1.0, 1.0, 1.0, 1.0, 1.5],
                           'height_ratios': [1.25, 1.0, 1.0, 1.0]}, layout='constrained')
    ax = axd['1Win']
    ax2 = axd['2Win']
    ax3 = axd['3Win']
    ax4 = axd['4Win']
    ax5 = axd['5Win']
    # --- FENSTER 1: CHARTS & LINE-GRAPHICS ---
    tage_diff = (dt_end - dt_start).days
    ax.set_title(f"{config['OSZ']} : {akt_ticker['Num']:02d}/{akt_ticker['Nam']}/{akt_ticker['Tik']}\n{s_start} + {tage_diff} Tage = {s_end}", fontsize=10, fontweight='bold')
    if config['preis_linie']: ax.plot(df_eff['Date'], df_eff['Price'], label='Preis', color='blue')
    if config['MAmiw_linie']: ax.plot(df_eff['Date'], df_eff['MA'], label='MA', color='green')   
    ma_mittelwert = df_zeitfenst['MA'].mean()
    if FEmiw_linie : ax.plot(df_eff['Date'], [ma_mittelwert]*len(df_eff), label='Fenster-MW', color='black', linestyle='--')
    if config['diffz_linie']: ax.plot(df_eff['Date'], ma_mittelwert + df_eff['Diff'], label='diffz zentriert', color='red')   
    ax.set_ylabel('Preis in €')
    ax.grid(True, linestyle='--')
    ax.legend(loc='upper left', fontsize=8)
    axen_skalierung(ax, df_zeitfenst, '1Win')
# ==============================================================================
# TEIL 8: STATISTISCHES POSTPROCESSING, FFT & MAIN RUNNER TRIGGER
# ==============================================================================
    diff_data = df_zeitfenst['Diff'].dropna().values
    if len(diff_data) > 5:
        mu, sigma = np.mean(diff_data), np.std(diff_data)
        alpha = 0.05
        n_stat = len(diff_data)
        # erstellt fertige Kurve und testet sie
        norm_verteilung = stats.norm(loc=mu, scale=sigma)
        ks_stat, ks_p = stats.kstest(diff_data, norm_verteilung.cdf)
        ks_Hyp = 1 if ks_p > alpha else 0 # Monte-Carlo-Rauschabstand mehr als 5% => KEIN K.S-Gauss
        lf_stat, lf_p = sm.stats.lilliefors(diff_data, dist='norm')
        lf_Hyp = 1 if lf_p > alpha else 0 # Monte-Carlo-Rauschabstand mehr als 5% => KEIN L.F-Gauss
        sw_stat, sw_p = stats.shapiro(diff_data)
        sw_Hyp = 1 if sw_p > alpha else 0 # Monte-Carlo-Rauschabstand mehr als 5% => KEIN S.W-Gauss
        if config['diffz_linie']:
            Bewertung_popup(ax5, n_stat, lf_stat, lf_p, lf_Hyp, sw_stat, sw_p, sw_Hyp, akt_ticker['Nam'])
        if config['MAmiw_linie']:
            count, bins, ignored = ax2.hist(diff_data, bins=30, density=True, alpha=0.6, color='blue', label=f"{akt_ticker['Tik']}/dMA")
            if config['diffz_linie']:
                ax2.set_title(f'n:{n_stat} p>5%.Soft-NoGauss-Test(1=ja/0=nein) KS:{ks_Hyp} / LF:{lf_Hyp} / SW:{sw_Hyp}', fontsize=8, fontweight='bold')
                gauss = stats.norm.pdf(bins, mu, sigma)
                ax2.plot(bins, gauss, color='red', linewidth=1.5, label=f'Gauss.Dichte\n(D ={ks_stat:.4f})')
                ax2.legend(fontsize=7)
                ax2.grid(True, linestyle='--')
        fft_werte = np.fft.fft(diff_data)   
        halbe = len(diff_data) // 2
        freq = np.fft.fftfreq(len(diff_data))[:halbe]
        amp = np.abs(fft_werte)[:halbe]
        if len(amp) > 1 and config['FFT_Diagram']:
            Wasserstein = False
            ax3.set_xscale('log')
            ax3.set_title("Log-skala dMA-Spektrum", fontsize=8, fontweight='bold')
            ax3.plot(freq, amp, color='purple', label='FFT')
            sortierte_idxs = np.argsort(amp[1:])[::-1] + 1
            farben = ['darkred', 'red', 'orange']
            for i in range(min(3, len(sortierte_idxs))):
                idx = sortierte_idxs[i]
                if freq[idx] > 0:
                    zyklus_tage = 1.0 / freq[idx]
                    ax3.vlines(freq[idx], 0, amp[idx], colors=farben[i], label=f'P{i+1}: {zyklus_tage:.1f}T')
            ax3.legend(fontsize=7, loc='upper right')
            ax3.grid(True, linestyle='--')
        # === HIER WIRD WASSERSTEIN-TEST EINGEBAUT ===
        else:
            if Wasserstein:
                Wasserstein = False  
                config.get('FFT_Diagram', False)
                ax3.clear()        # Vorherige Reste entfernen
                ax3.get_xaxis().set_visible(False) 
                ax3.get_yaxis().set_visible(False) 
                try:
                    # Nutzt darüber berechnete diff_data der FFT-Vorbereitung
                    aktuelle_diffs = diff_data.dropna().values if hasattr(diff_data, 'dropna') else diff_data               
                    if len(aktuelle_diffs) > 1:
                        mu = aktuelle_diffs.mean()
                        sigma = aktuelle_diffs.std()                        
                        # Ideale Normalverteilung als statistischer Zwilling
                        theoretische_norm = np.random.normal(mu, sigma if sigma > 0 else 1.0, len(aktuelle_diffs))                        
                        # 1D Wasserstein-Distanz via SciPy
                        w_distance = stats.wasserstein_distance(aktuelle_diffs, theoretische_norm)                        
                        # ==============================================================================
                        # PARAMETRISCHER BOOTSTRAP (MONTE-CARLO-EMULATION IM RAM)
                        # ==============================================================================
                        bootstrap_w1s = []
                        n_samples = len(aktuelle_diffs)
                        sig_calc = sigma if sigma > 0 else 1.0
                        # 1.000 Ideal-Markt simulieren und vergleichen
                        for _ in range(1000):
                            sim_real = np.random.normal(mu, sig_calc, n_samples)
                            sim_norm = np.random.normal(mu, sig_calc, n_samples)
                            sim_w1 = stats.wasserstein_distance(sim_real, sim_norm)
                            bootstrap_w1s.append(sim_w1)
                        # p-Wert empirisch (Wie oft reiner Zufall extremer?)
                        p_value = np.mean(np.array(bootstrap_w1s) >= w_distance)
                        # Urteil entspr. Alarmschwelle
                        if p_value < 0.05:
                            decision_text = (
                                f"  ► Bootstrap p-value: {p_value:.4f}\n"
                                f"  ► Decision: REJECT the null hypothesis.\n"
                                f"  The market's geometry shifted significantly.")
                        else:
                            decision_text = (
                                f"  ► Bootstrap p-value: {p_value:.4f}\n"
                                f"  ► Decision: ACCEPT the null hypothesis.\n"
                                f"  Barycenter change is within random sampling noise.")
                        # ==============================================================================                        
                        # statistische Form-Merkmale (Schiefe & Wölbung)
                        schiefe = stats.skew(aktuelle_diffs)
                        woelbung = stats.kurtosis(aktuelle_diffs)                       
                        # Text-Layout für ax3 (Inkl.Bootstrap-Urteil)
                        info_text = (
                            f"# KANTOROVITCH-RUBINSTEIN bzw WASSERSTEIN-DISTANZ #\n"
                            f"Ticker: {akt_ticker['Nam']}\n"
                            f"W1-Distanz: {w_distance:.4f}\n"
                            f"(Kantorovitch-Rubinstein Abstand zur Gauß-Kurve)\n"
                            f"Mittelwert (μ): {mu:.2f}\n"
                            f"Volatilität (σ): {sigma:.2f}\n"
                            f"Schiefe (Skew): {schiefe:.4f}\n"
                            f"Wölbung (Kurt): {woelbung:.4f}\n"
                            f"Realer Stichproben-Umfang (N): {len(aktuelle_diffs)}\n"
                            f"# Ergebnis Bootstrap-Simulation(1000 Durchläufe) #\n"
                            f"{decision_text}")
                        # Text knapp in Kachel setzen (Klammern & Einrückung korrigiert!)
                        ax3.text(0.05, 0.93, info_text, transform=ax3.transAxes,
                                 fontsize=10, fontfamily='monospace', fontweight='bold', va='top', ha='left',
                                 bbox=dict(boxstyle='round,pad=0.6', facecolor='wheat', alpha=0.25))             
                        ax3.set_title("Kachel 3: SCHAUFELBAGGER-DISTANZ (W1)", fontsize=10, fontweight='bold', color='darkred')
                    else:
                        ax3.text(0.5, 0.5, "N unzureichend", ha='center', va='center', fontsize=8)
                except Exception as e:
                    ax3.text(0.5, 0.5, f"Fehler W1:\n{str(e)}", ha='center', va='center', color='red', fontsize=7)            
            else:
                # Weder FFT noch Wasserstein aktiv -> Kachel komplett unsichtbar machen
                ax3.clear()
                ax3.axis('off')           
    #==============================================================================
    # ENDE MIT TEIL 9: WEICHENSTEUERUNG FÜR KACHEL 4 (ACTUAL TICKER FROZEN OR LIVE)
    # ==============================================================================
    # WEICHE 1: WENN FREEZE AUS -> LIVE BERECHNEN & IM SPEICHER MERKEN
    if not Freez_linie:
    # 1. originale mathematische Berechnungen durchführen
        miwe_val = df_zeitfenst['Price'].mean()
        df_plot_ax4 = df_zeitfenst.copy()
        df_plot_ax4['miwe'] = miwe_val
        df_plot_ax4['diffz'] = miwe_val + df_plot_ax4['Price'].diff().fillna(0)  
    # 2. ZUSAETZLICH IM SESSION-STATE SPEICHERN: falls gleich eingefroren wird
        st.session_state.vergleichs_daten = df_plot_ax4
        st.session_state.vergleichs_ticker_name = akt_ticker['Nam']
    # WEICHE 2: WENN FREEZE AN -> HOLE ALTE DATEN AUS DEM SPEICHER
    else:
    # Falls nichts im Speicher , aktuellen Daten als Fallback
        if st.session_state.vergleichs_daten is not None:
            df_plot_ax4 = st.session_state.vergleichs_daten
        else:
            miwe_val = df_zeitfenst['Price'].mean()
            df_plot_ax4 = df_zeitfenst.copy()
            df_plot_ax4['miwe'] = miwe_val
            df_plot_ax4['diffz'] = miwe_val + df_plot_ax4['Price'].diff().fillna(0)
    # ==============================================================================
    # ZEICHNEN mit df_plot_ax4
    # ==============================================================================
    ax4.clear()  # Säubert Achse vor dem Neuzeichnen
    # Titel anpassen, damit man sieht, wer eingefroren ist
    v_name = st.session_state.get('vergleichs_ticker_name', akt_ticker['Nam'])
    status_text = "Vergleichs-Ticker" if Freez_linie else "dMA-Überblick"
    # Die 3 Kennlinien plotten (Preis, MiWe, Diffz)
    ax4.plot(df_plot_ax4['Date'], df_plot_ax4['Price'], color='black', linewidth=1.5, label='Preis')
    ax4.plot(df_plot_ax4['Date'], df_plot_ax4['miwe'], color='red', linestyle=':', label='MiWe')
    ax4.plot(df_plot_ax4['Date'], df_plot_ax4['diffz'], color='gray', alpha=0.7, label='Diffz')
    # Titel, Legende und deine Skalierungsfunktion anwenden
    ax4.set_title(f"Kachel 4: {status_text} [ {v_name} ]", fontsize=8, fontweight='bold')
    ax4.legend(fontsize=7, loc='upper left')
    # Skalierungsfunktion muss ausgewähltes DataFrame nutzen
    axen_skalierung(ax4, df_plot_ax4, '4Win') 
    # ==============================================================================
    # Wenn BEIDE Schalter aus , Achsenstriche ax3 aus.
    # rufe NICHT ax3.clear() auf, da sonst Text gelöscht
    if not config['FFT_Diagram'] and not config.get('Wasserstein', False): 
        ax3.get_xaxis().set_visible(False)
        ax3.get_yaxis().set_visible(False)
        ax3.set_title("") # Macht den Titel leer, wenn beide aus sind
    if not config['MAmiw_linie']: ax2.axis('off')
    if not config['diffz_linie']: ax5.axis('off')
    return fig
# --- MAIN RUNNER TRIGGER ---
df_roh = lade_ticker_daten(f"{akt_ticker['Num']}", akt_ticker['Nam'], akt_ticker['Tik'], val_online, start_date, end_date)
if not df_roh.empty:
    # filter geladenes DataFrame live nach Eingabe aus Sidebar
    df = df_roh.reset_index()  
    if not df.empty:
        runtime_config = {
           'moving_size': moving_size,
           'preis_linie': preis_linie,
           'MAmiw_linie': MAmiw_linie,
           'FEmiw_linie': FEmiw_linie,
           'diffz_linie': diffz_linie,
           'FFT_Diagram': FFT_Diagram,
           'Freez_linie': Freez_linie,       # Schalter f. Einfrieren von ax4
           'Wasserstein': Wasserstein,       # Schalter f. W1-Test in ax3
           'OSZ': osz}                       # Softwarekürzel IDLE-Version
        fig_mosaik = generiere_mosaik(df, akt_ticker, runtime_config)
        if fig_mosaik:
            st.pyplot(fig_mosaik)
            with st.expander("🔍 Letzte 50 Handelstage als Rohdatentabelle einsehen"):
                st.dataframe(df.tail(50), use_container_width=True)
    else:
        st.error(f"Keine Daten im Zeitraum von {start_date} bis {end_date}.")
else:
    st.error(f"Keine historischen Daten in '{CSV_ORDNER}/' oder via Yahoo.")

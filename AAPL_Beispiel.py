# AAPL_Beispiel.py  Übungsbeispiel 50Zeilen Aktiensparen zwischen 2019 und 2021
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import os
# %matplotlib widget
csv_Nam ="02Apple_Offline.csv"  # geht von 2015 bis 2026
if os.path.exists(csv_Nam):
   print(f"lokale csv {csv_Nam} wird geladen...")
   df_csv = pd.read_csv(csv_Nam)
   # Apple-Ticker-Preise aus CSV-Datei in Pandas-DataFrame laden
   df_csv['Date'] = pd.to_datetime(df_csv['Date'])
   # Werte in Spalte Date in ein standardisiertes Datumsformat umwandeln.
   df = df_csv.sort_values('Date').reset_index(drop=True)
   # Daten chronologisch nach Datum sortieren, Zeilennummern neu durchnummerieren.
   df.set_index('Date', inplace=True)
   # Alle Elemente werden ohne Kopier-Zwischenschritt per Datum indentifiziert
df_aktiensparen = df.loc['2019-01-01':'2021-10-01'].copy()
# Erstellen einer Teil-Kopie direkt über den Datums-Index
df_monthly = df_aktiensparen.resample("MS").first()
# Nach monatlichem Zusammenfassen der erfassten Monats-Ersttage(Anfaenge)
df_monthly = df_monthly.dropna(subset=["Price"])
# NaN(NotANumber) Elemente mit Defekt in Spalte "Price" aus Datei streichen
investment_per_month = 20
raten_plan = []
raten_nr = 0
for date, row in df_monthly.iterrows():
    # Paare (row-Index,row-Inhalt), letzteres als pd.series  
    price = row["Price"]
    # Inhalt der Spalte "Price" in der pd.series row
    units = investment_per_month / price
    # im aktuellen Monat moegl. Anteile
    datum = date.strftime("%d.%m.%Y")
    # index als formatiertes Datum    
    rate  = round(units,6)
    raten_nr = raten_nr + 1
    print(raten_nr,datum,rate)
    raten_plan.append(rate)
    # Folge der monatsweise erworbenen Anteile
# Summe aller erworbenen Anteile
gesamte_anteile = sum(raten_plan)
letzter_preis = df_monthly["Price"].iloc[-1]
# letztes Element
depot_wert = gesamte_anteile * letzter_preis
# x-werte entspr. monatlich
x_zahlen = np.arange(len(df_monthly))
y = raten_plan
x_labels = [date.strftime("%m-%y") for date in df_monthly.index]
plt.figure(figsize=(8, 4))
plt.plot(x_zahlen, y, label='Invest. 20Eu‚/mtl' 
                    , color='red', linestyle='solid') 
# x-Achse enstspr Anzahl der Werte
plt.xlim(0, len(df_monthly) - 1)
# Anzeige jeder zweite Monat
plt.xticks(ticks=x_zahlen[::2], labels=x_labels[::2], rotation=0)
titel_text = (f"AAPL-Aktie(2019-2021)\n"
              f"Anteile: {gesamte_anteile:.4f} Stueck | "
              f"Depot  : {depot_wert:.2f} Eu (Kurs: {letzter_preis:.2f} Eu)")
plt.title(titel_text, fontsize=12, fontweight='bold')
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.show()

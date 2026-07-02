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
   df_csv['Date'] = pd.to_datetime(df_csv['Date'])
   df = df_csv.sort_values('Date').reset_index(drop=True)
   df.set_index('Date', inplace=True) 
df_aktiensparen = df.loc['2019-01-01':'2021-10-01'].copy()
df_monthly = df_aktiensparen.resample("MS").first()
df_monthly = df_monthly.dropna(subset=["Price"])
investment_per_month = 20
raten_plan = []
raten_nr = 0
for date, row in df_monthly.iterrows():
    price = row["Price"]
    units = investment_per_month / price
    datum = date.strftime("%d.%m.%Y")
    rate  = round(units,6)
    raten_nr = raten_nr + 1
    print(raten_nr,datum,rate)
    raten_plan.append(rate)
# depot-wert
gesamte_anteile = sum(raten_plan)
letzter_preis = df_monthly["Price"].iloc[-1]
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

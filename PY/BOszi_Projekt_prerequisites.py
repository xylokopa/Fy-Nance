# prerequisites.py - REINER PREREQUISITES-TEST
# Version 03 R.Wu_GastH_Nr178854
# für alle nötigen importe
print("Prüfe System-Voraussetzungen... Bitte warten...\n")
try:
    import math
    import numpy as np
    import pandas as pd
    import yfinance as yf
    from scipy import stats
    import statsmodels.api as sm
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    import matplotlib.ticker as mticker
    from matplotlib.widgets import Slider, Button, TextBox
    from datetime import datetime
    import os
    import csv
    import locale  
    # Test, ob deutsche Formatierung auf dem PC 
    locale.setlocale(locale.LC_TIME, "de_DE")
    print("==========================================================")
    print("ALLES OK ! Die nötigen Pakete sind installiert.")
    print("Das System ist bereit für den Börsen-Oszillographen.")
    print("==========================================================")
except ModuleNotFoundError as e:
    # Fehlerfalle, sobald IDLE läuft
    print("==========================================================")
    print(f"FEHLER: Dir fehlt ein wichtiges Paket!")
    print(f"   {e}")
    print("\n REPARATUR-BEFEHL FÜR DEINE CMD:")
    print("   pip install numpy pandas matplotlib scipy statsmodels yfinance")
    print("==========================================================")
except locale.Error:
    print("HINWEIS : deutsche Locale ('de_DE') nicht aktiv.")
    print("   Skript läuft,aber Datumsformate können abweichen.")
input("\n[ENTER zum Schließen des Prerequisites-Tests]")


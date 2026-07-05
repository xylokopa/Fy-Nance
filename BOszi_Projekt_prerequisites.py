# prerequisites.py - REINER PREREQUISITES-TEST
# Version 03 R.Wu_GastH_Nr178854
# für alle noetigen importe
print("Inspecting the Prerequisites of your installation... Please Wait...\n")
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
    print("YOUR SYSTEM IS OK ! The necessary imports are available.")
    print("Das System ist bereit fuer den Boersen-Oszillographen.")
    print("==========================================================")
except ModuleNotFoundError as e:
    # Fehlerfalle, sobald IDLE läuft
    print("==========================================================")
    print(f"ERROR: You have to download necessary packages!")
    print(f"   {e}")
    print("\nREPAIR-INSTRUCTION for your download via CMD:")
    print("   pip install numpy pandas matplotlib scipy statsmodels yfinance")
    print("==========================================================")
except locale.Error:
    print("HINWEIS : deutsche Locale ('de_DE') nicht aktiv.")
    print("   Skript laeuft,aber Datumsformate koennen abweichen.")
input("\n[ENTER zum Schliessen des Prerequisites-Tests]\n"+
       " [Press ENTER to exit the prerequisites-test]")


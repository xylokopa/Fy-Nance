# prerequisites.py - ERWEITERTER SYSTEM-TEST FÜR STREAMLIT
print("Prüfe System-Voraussetzungen für die Web-App... Bitte warten...\n")
try:
    import streamlit as st
    import math
    import numpy as np
    import pandas as pd
    import yfinance as yf
    from scipy import stats
    import statsmodels.api as sm
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    import matplotlib.ticker as mticker
    from datetime import datetime
    import os
    import csv
    import locale  
    
    # Test, ob deutsche Formatierung auf dem PC aktiv ist
    try:
        locale.setlocale(locale.LC_TIME, "de_DE.utf8")
    except locale.Error:
        locale.setlocale(locale.LC_TIME, "de_DE")
        
    print("==========================================================")
    print("ALLES OK! Alle Pakete inklusive Streamlit sind installiert.")
    print("Das System ist bereit für den Web-Börsen-Oszillographen.")
    print("==========================================================")
except ModuleNotFoundError as e:
    print("==========================================================")
    print(f"FEHLER: Dir fehlt ein wichtiges Paket!")
    print(f"   {e}")
    print("\n REPARATUR-BEFEHL FÜR DEINE CMD:")
    print("   pip install streamlit numpy pandas matplotlib scipy statsmodels yfinance")
    print("==========================================================")
except locale.Error:
    print("HINWEIS: Deutsche Locale nicht aktiv. Datumsformate weichen evtl. ab.")

input("\n[ENTER zum Schließen des Prerequisites-Tests]")

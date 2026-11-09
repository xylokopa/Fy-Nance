# Dolia_RK4_02.py DOLIA-AUSTRIACA 05-11-26
import numpy as np
def r(x): 
    return 40.0 - (10.0 / 3600.0) * (x**2)
def dV_dx(x): 
    return np.pi * (r(x)**2)
V_exakt = 515.221
print(f"Exakter Sollwert: {V_exakt:.3f} Liter\n")
print(f"{'Schritte':<10} | {'Schrittweite (cm)':<18} | {'RK4-Ergebnis (L)':<18} | {'Absoluter Fehler (L)':<20}")
print("-" * 75)
# Erzeugt Zahlen von 2 bis 120
schritt_liste = list(range(2, 121, 20)) 
for steps in schritt_liste:
    h_step = 120.0 / steps
    x = -60.0
    V = 0.0    
    for _ in range(steps):
        k1 = dV_dx(x)
        k2 = dV_dx(x + h_step/2.0)
        k3 = dV_dx(x + h_step/2.0)
        k4 = dV_dx(x + h_step)
        V += (h_step / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
        x += h_step      
    V_lit = V / 1000.0
    fehler = abs(V_lit - V_exakt)
    print(f"{steps:<10} | {h_step:<18.1f} | {V_lit:<18.3f} | {fehler:<20.3e}")

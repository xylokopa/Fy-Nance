# 📈 Xylokopa's Github 
Willkommen auf Xylokopa's Github-Website. Hier werden UNI-Projekte  
Revue passiert, anstatt auf meiner Festplatte zu verstauben.
---
## 🚀 Projekt 1: Fy-Nance (Juli 2026)
Dieses Projekt entstand als Kurs-Projekt im Sommersemester 2026. Es kombiniert 
Kurs-Diagramme mit Daten-Tests am Beispiel von Tickern wie z.B APPLE (`AAPL`).

### Kernkomponenten & Programme
* **[Hauptprogramm Börsen-Oszillograph](PY/BOszi_Projekt.py):** Der zentrale Python-Code zur Berechnung der Modelle.
* **[Interaktives Jupyter Notebook](IPYNB/Oszi_03n_290626.ipynb):** Die mathematische Herleitung und Schritt-für-Schritt-Analyse.
* **[Streamlit Web-App](fy_nance_app.streamlit.app.py):** Der Code für die interaktive Benutzeroberfläche.

### 🎮 Interaktive Live-App (Direkt ausprobieren)
Hier kannst du das Dashboard live bedienen. Nutze die Regler auf der linken Seite, um Zeiträume und das Moving-Average-Fenster anzupassen:

<iframe src="https://fy-nance-app.streamlit.app?embed=true" width="100%" height="700px" style="border: 1px solid #ccc; border-radius: 8px"></iframe>

### 🎮 Interaktiver Flugdaten-Auswertungstest zum Üben für das neue Projekt WS26 (Direkt ausprobieren)
Hier kannst du die Flugdaten in den Diagrammen mit der Maus abtasten. Ändere die Karten-Wahl auf der linken Seite, falls die Kartenwahl blockiert ist.

<iframe src="Auswertung.html" width="100%" height="700px" style="border: 1px solid #ccc; border-radius: 8px"></iframe>

### Dokumentation & Analysen
* 📄 [Vollständige Python-Script-Dokumentation (PDF)](PDF/BOszi_03.pdf)
* 📊 [PCA-Ressourcen & Theorie zur Hauptkomponentenanalyse (PDF)](PDF/PCA-Data-ressources.pdf)

### Visueller Eindruck
Hier ein Auszug der berechneten Statistiken aus dem Projekt:
![Statistische Auswertung](PNG/STATISTICS.PNG)
---
*Hier entsteht ab Dezember 2026 ein neues Projekt...*
---

## 🚏 Die Albatros-Flight-Map

"Flugplan"-skizze und als realistisch eingeschätzte Projektphasen

* **Zeitraum:** Nov/Dez 2026
### Phase 1: Flugdaten ausbauen
* **Status:** Vorbereitet (GPX-Rohdaten bevorzugt aus St-Auban/Hangwindsegeln Authon/Auribeau aus den Jahren 2012 und 2015).
* **Nächster Schritt:** XML-Struktur in eine schlanke, html-unempfindliche Tabelle mit Zeilenzähler.
* **Übergabeparameter:** `[Zeilennummer] -> [lon_x, lat_y, ele_z, time_t]`.

### Phase 2: Gelände einbeziehen
* **Status:** Mathematische Grundidee : Einbettung eines einfachen Geländemodells
* **Leitlinie:** Umrechnung Erdkrümmung und Längengrad-Stauchung in einen euklidischen XYZ-Koordinatenquader 
                 mittels dimensionsloser Abszissen-Anpassung: x.cos(lat)
* **Ziel:** Projektion der Flugspur in ein anschauliches, händisch skalierbares 3D-Schrägbilddiagramm ohne "Heavy Rendering".

### Phase 3: Wechselwirkung von Wind und Gelände zwischen null und abstandsabhängig
* **Paradigma:** "Melken" eines Hangwindes bzw. einer Wellenkamm-Linie unter 45°.
* **Mathematischer Ansatz:** Lineare Approximation (evtl. auch 2.ten Grades) des Gelände-Netzes ( à la Cavalieri geschichtet  ). 
* **Steuergrössen:** Bewegung in x- bzw. y-Richtung entspr. in der Realität entstandener Flugdaten 
* **Zustandsänderung:** Resultierendes Steigen in z-Richtung vor der Felswand (bzw. über der Wasseroberfläche) bei abstandsabhängig
                        gedämpftem Aufwind der sich bei Annäherung ans Geländenetz annulliert 
                     
### Phase 4: Gespeicherte reale Flugbahnen mit rechnerisch modellierten einander gegenüber stellen
* **Zeitraum:** Jan/Feb 2027.
* **Ziel:** Einsatz von Python,um bei vorgegebener xy-Flugspur mit im einfachsten Modell zumindest konstanter Gleitzahl von Ort zu Ort 
            die geschätzte nächste Flugposition mit der tatsächlich beobachteten zu vergleichen und abzugleichen.Modellverfeinerung mit
            übergang zu einer variablen Gleitzahl anhand geeignet zu definierender variabler Parameter und deren Implementierung...

---
*Fahrplanstand: Freitag, 30. Oktober 2026, 18:45 Uhr. Wintereinbruch hin oder her...*


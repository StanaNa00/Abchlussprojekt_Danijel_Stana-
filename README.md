# Abschlussprojekt_Danijel_Stana

## Autoren

- Danijel PALADIN (DanijelRS)
- Stana NARIC (StanaNa00)

## Programmieren 1 – Abschlussprojekt

Dieses Projekt simuliert den Energieverbrauch eines E-Bikes anhand von GPS-Fahrdaten. Dabei werden die Fahrphysik berechnet, zwei unterschiedliche Akkumodelle simuliert und die Ergebnisse grafisch dargestellt.

---

## Funktionen

Das Programm bietet folgende Funktionen:

- Einlesen einer GPS-Datei (CSV)
- Berechnung der Fahrphysik
- Berechnung der Geschwindigkeit
- Berechnung der Beschleunigung
- Berechnung der Steigung
- Berechnung des Motordrehmoments
- Berechnung der Motorleistung
- Simulation eines LiPo-Akkus
- Simulation eines NMC-Akkus
- Vergleich beider Akkutypen
- Berechnung des Ladezustands (SoC)
- Berechnung der Akkuspannung
- Berechnung der Hauptfahrtrichtung aus GPS-Daten
- Erstellung einer interaktiven Folium-Karte
- Farbige Darstellung der Geschwindigkeit entlang der Route
- Automatische Parameterstudie
- Erstellung verschiedener Diagramme
- Zusammenfassender Bericht im Terminal

---

## Ausgegeben werden

Nach jeder Simulation werden folgende Kennwerte ausgegeben:

- Gesamt gefahrene Strecke
- Strecke mit Motorunterstützung
- Durchschnittsgeschwindigkeit
- Fahrzeit
- Maximale Leistung
- Gesamter Anstieg
- Gesamter Abstieg
- Restlicher Ladezustand
- Restspannung

---

## Projektstruktur

```
Abschlussprojekt_Danijel_Stana-/

├── data/
│   └── final_project_input_data.csv
│
├── output/
│   ├── 1_höhenprofil.png
│   ├── 2_geschwindigkeit.png
│   ├── 3_leistung.png
│   ├── 4_soc.png
│   ├── 5_spannung.png
│   ├── 6_route_map.png.png
│   ├── 7_parameterstudie_masse.png
│   ├── 8_parameterstudie_reifen.png
│   └── parameterstudie.txt
│
├── src/
│   └── main.py
│
├── plots.png
├── battery_base.py
├── battery_models.py
├── battery_pack.py
├── data_parser.py
├── EBikeSimulator.py
├── lifepo4_battery.py
├── motor_base.py
├── physics_engine.py
├── plotting_utils.py
├── requirements.txt
├── README.md
└── route_map.html
```

---

## Installation

Repository klonen

```bash
git clone https://github.com/StanaNa00/Abchlussprojekt_Danijel_Stana-.git
```

Projektordner öffnen

```bash
cd Abschlussprojekt_Danijel_Stana-
```

Benötigte Pakete installieren

```bash
pip install -r requirements.txt
```

---

## Programm starten

```bash
python src/main.py
```

---

## Verwendete Bibliotheken

- pandas
- numpy
- matplotlib
- folium
- openpyxl

Weitere benötigte Pakete befinden sich in der Datei `requirements.txt`.

---

## Erweiterungen

Zusätzlich zu den Minimalanforderungen wurden folgende Erweiterungen umgesetzt:

- Simulation von zwei verschiedenen Akkutypen (LiPo und NMC)
- Vergleich der beiden Akkumodelle
- Grafische Darstellung aller Simulationsergebnisse
- Höhenprofil der Fahrt
- Vergleich des Ladezustands beider Akkus
- Vergleich der Akkuspannung
- Berechnung der Durchschnittsgeschwindigkeit
- Berechnung der maximalen Leistung
- Berechnung des gesamten Anstiegs und Abstiegs
- Zusammenfassender Bericht im Terminal
- Logging der wichtigsten Programmschritte während der Simulation



- python +
- daten lesen +
- geschwindigkeit +
- beschleunigung +
- leistung +
- steigung +
- drehmoment +
- motor strom +
- SoC +
- durchcchnittsgeschwindigkeit +
- zuruckgelegte strecke +
- benotigte zeit +
- hohenmeter +
- maximalleistung +
- 009 +
- LiPo +
- NMC +
- plots:
	  Geschwindigkeit +
	  leistung +
	  SoC +
	  hohenprofil +
- Logging +
- Aktivitatsdiagram
- requirements.txt +

- exstras:

- hilfreiche dinge +
- gute GitHub Commits +
- Ploten der strecke +
- Unit-test -
- auto parametriserung -
- luftdichte -
- rollwiderstand sim -
- akkutemp sim -
- bremswiderstand sim -
- ort/adresse -
- wetterdaten -
- orientirung +
- LaTeX -

---

### parameterstudie.txt

Enthält sämtliche Ergebnisse der Parameterstudie in Textform.

Ausgegeben werden:

- Einfluss der Fahrermasse
- Einfluss des Reifendurchmessers
- Motorunterstützte Strecke
- Maximale Leistung

### 7_parameterstudie_masse.png

Diagramm über den Einfluss der Fahrermasse auf die Strecke mit Motorunterstützung.

Es zeigt deutlich, dass mit steigender Fahrermasse die motorunterstützte Strecke abnimmt.

### 8_parameterstudie_reifen.png

Diagramm über den Einfluss des Reifendurchmessers auf die Strecke mit Motorunterstützung.

Dadurch können unterschiedliche Reifendurchmesser miteinander verglichen werden.

Alle Dateien werden bei jedem Programmstart automatisch neu erzeugt.
import sys
import os

# Projektordner bestimmen
hauptordner = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if hauptordner not in sys.path:
    sys.path.append(hauptordner)

from battery_models import LiPoAkku, NMCAkku
from data_parser import GPSDataParser
from physics_engine import EBikePhysics
from plotting_utils import plot_ergebnisse


def simuliere_akku_fahrt(datenframe, akku_objekt):
    """
    Simuliert die E-Bike-Fahrt Sekunde für Sekunde.
    Nutzt den berechneten Motorstrom (I_motor), um den SoC und die Spannung zu aktualisieren.
    """
    soc_liste = []
    spannung_liste = []
    warnung_ausgegeben = False
    
    for index, zeile in datenframe.iterrows():
        strom = zeile['I_motor']
        dauer = zeile['delta_t']
        
        # Strom auf das Akku-Objekt anwenden
        akku_objekt.apply_current(current=strom, duration=dauer)
        
        # Aktuellen Zustand speichern
        soc_liste.append(akku_objekt.soc)
        spannung_liste.append(akku_objekt.voltage(current=strom))
        
        # Warnung falls der Akku leer ist
        if akku_objekt.is_empty() and not warnung_ausgegeben:
            print(f"WARNUNG: Akku komplett entladen bei Zeitstempel {zeile['time']}!")
            warnung_ausgegeben = True
            
    # Ergebnisse in den DataFrame schreiben
    datenframe['akku_soc'] = soc_liste
    datenframe['akku_spannung'] = spannung_liste
    return datenframe

def main():
    # Eingabedatei wählen 
    dateipfad = os.path.join(hauptordner, "data", "final_project_input_data.csv")
    
    print("Lade GPS-Daten...")
    parser = GPSDataParser(dateipfad)
    gps_daten = parser.load_data()
    
    print("Berechne physikalische Größen...")
    physik = EBikePhysics(gps_daten)
    berechnete_daten = physik.calculate_physics()
    

    # Erste werte anzeigen 
    print("\nErste 10 Zeilen der berechneten Daten:")
    print(berechnete_daten[['time', 'v', 'a', 'F_ges', 'I_motor']].head(10))

    print("\nStarte E-Bike-Batteriesimulation mit LiPo-Akku (10Ah, 100% Start-SoC)...")
    lipo_batterie = LiPoAkku(capacity_nom_Ah=10.0, initial_soc=1.0)
    
    # Simulation ausführen
    simulations_daten = simuliere_akku_fahrt(berechnete_daten, lipo_batterie)
    
    print("\n--------------------------------------------------")
    print("Simulation beendet. Endzustand des Akkus:")
    print(lipo_batterie)
    print("--------------------------------------------------")
    
    # Anzeigen der neuen Akku-Werte in den ersten 10 Zeilen
    print("\nErste 10 Zeilen der Simulationsdaten mit Akku-Werten:")
    anzeige_spalten = ['time', 'v', 'I_motor', 'akku_soc', 'akku_spannung']
    print(simulations_daten[anzeige_spalten].head(10))

    # Bericht
    gesamt_km = simulations_daten["delta_s"].sum() / 1000
    motor_km = simulations_daten.loc[
    (simulations_daten["I_motor"] > 0) & (simulations_daten["akku_soc"] > 0),
    "delta_s"
    ].sum() / 1000

    durchschnitt_v = simulations_daten["v"].mean() * 3.6
    max_leistung = simulations_daten["P_mech"].max()
    fahrzeit = simulations_daten["delta_t"].sum()

    höhen_diff = simulations_daten["ele"].diff()
    anstieg = höhen_diff[höhen_diff > 0].sum()
    abstieg = -höhen_diff[höhen_diff < 0].sum()

    print("\n----- Bericht -----")
    print(f"Gesamt gefahrene Strecke: {gesamt_km:.2f} km")
    print(f"Strecke mit Motorunterstützung: {motor_km:.2f} km")
    print(f"Verwendete Batterie: LiPo (10 Ah)")
    print(f"Restlicher Ladezustand: {lipo_batterie.soc * 100:.1f} %")
    print(f"Restspannung: {lipo_batterie.voltage():.2f} V")
    print(f"Durchschnittsgeschwindigkeit: {durchschnitt_v:.2f} km/h")
    print(f"Fahrzeit: {fahrzeit / 60:.1f} min")
    print(f"Maximale Leistung: {max_leistung:.1f} W")
    print(f"Gesamter Anstieg: {anstieg:.1f} m")
    print(f"Gesamter Abstieg: {abstieg:.1f} m")


    plot_ergebnisse(simulations_daten)

if __name__ == "__main__":
    main()
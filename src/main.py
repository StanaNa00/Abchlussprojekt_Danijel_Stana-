import sys
import os

# Projektordner bestimmen
hauptordner = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if hauptordner not in sys.path:
    sys.path.append(hauptordner)

from data_parser import GPSDataParser
from physics_engine import EBikePhysics

def main():
    # Eingabedatei wählen 
    dateipfad = os.path.join(hauptordner, "final_project_input_data.csv")
    
    print("Lade GPS-Daten...")
    parser = GPSDataParser(dateipfad)
    gps_daten = parser.load_data()
    
    print("Berechne physikalische Größen...")
    physik = EBikePhysics(gps_daten)
    berechnete_daten = physik.calculate_physics()
    
    # Erste werte anzeigen 
    print("\nErste 10 Zeilen der berechneten Daten:")
    print(berechnete_daten[['time', 'v', 'a', 'F_ges', 'I_motor']].head(10))

if __name__ == "__main__":
    main()
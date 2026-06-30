import sys
import os

# Projektordner bestimmen
hauptordner = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if hauptordner not in sys.path:
    sys.path.append(hauptordner)

from battery_models import LiPoAkku, NMCAkku
from data_parser import GPSDataParser
from physics_engine import EBikePhysics
from plotting_utils import plot_simulations_ergebnisse


def simuliere_akku_fahrt(datenframe, akku_objekt):
    df_sim = datenframe.copy(deep=True)

    soc_liste = []
    spannung_liste = []
    strom_liste = []
    
    for index, zeile in df_sim.iterrows():
        if akku_objekt.is_empty():
            strom = 0.0
        else:
            strom = zeile['I_motor']
            
        dauer = zeile['delta_t']
        
        akku_objekt.apply_current(current=strom, duration=dauer)
        
        soc_liste.append(akku_objekt.soc)
        spannung_liste.append(akku_objekt.voltage(current=strom))
        strom_liste.append(strom)
        
    df_sim['akku_soc'] = soc_liste
    df_sim['akku_spannung'] = spannung_liste
    # echten strom speichern
    df_sim['I_motor'] = strom_liste
    
    return df_sim

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


    kapacitet_test = 30.0

    print("\nStarte E-Bike-Batteriesimulation mit LiPo-Akku ({kapacitet_test}Ah, 100% Start-SoC)...")
    lipo_batterie = LiPoAkku(capacity_nom_Ah=kapacitet_test, initial_soc=1.0)
    daten_lipo = simuliere_akku_fahrt(berechnete_daten, lipo_batterie)
    
    print("\nStarte E-Bike-Batteriesimulation mit NMC-Akku ({kapacitet_test}Ah, 100% Start-SoC)...")
    nmc_batterie = NMCAkku(capacity_nom_Ah=kapacitet_test, initial_soc=1.0)
    daten_nmc = simuliere_akku_fahrt(berechnete_daten, nmc_batterie)



# Bericht
    gesamt_strecke_km = berechnete_daten['delta_s'].sum() / 1000.0
    # Strecke, bei der der Motor Strom gezogen hat (I_motor > 0)
    strecke_motor_lipo = daten_lipo[daten_lipo['I_motor'] > 0]['delta_s'].sum() / 1000.0
    strecke_motor_nmc = daten_nmc[daten_nmc['I_motor'] > 0]['delta_s'].sum() / 1000.0

    print("\n----- Bericht -----")
    print(f"Gesamt gefahrene Strecke: {gesamt_strecke_km:.2f} km")
    print(f"Strecke mit Motorunterstuetzung (LiPo): {strecke_motor_lipo:.2f} km")
    print(f"Strecke mit Motorunterstuetzung (NMC): {strecke_motor_nmc:.2f} km")
    print(f"Verwendete Batterie: LiPo ({lipo_batterie.C_nom / 3600.0:.1f} Ah)")
    print(f"Verwendete Batterie: NMC ({nmc_batterie.C_nom / 3600.0:.1f} Ah)")
    print(f"Restlicher Ladezustand: LiPo {lipo_batterie.soc * 100:.1f} %")
    print(f"Restlicher Ladezustand: NMC {nmc_batterie.soc * 100:.1f} %")
    print(f"Restspannung: LiPo {daten_lipo['akku_spannung'].iloc[-1]:.2f} V")
    print(f"Restspannung: NMC {daten_nmc['akku_spannung'].iloc[-1]:.2f} V")

    print("\nGeneriere Simulationsgrafiken...")
    plot_simulations_ergebnisse(berechnete_daten, daten_lipo, daten_nmc, hauptordner)

if __name__ == "__main__":
    main()
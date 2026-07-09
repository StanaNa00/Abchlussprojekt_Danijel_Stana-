import sys
import os
import logging
import math 
import matplotlib.pyplot as plt

# Projektordner bestimmen
hauptordner = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if hauptordner not in sys.path:
    sys.path.append(hauptordner)


from battery_models import LiPoAkku, NMCAkku
from data_parser import GPSDataParser
from physics_engine import EBikePhysics
from plotting_utils import plot_simulations_ergebnisse
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

from plotting_utils import create_route_map

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


def berechne_himmelsrichtung(df):
    lat1 = math.radians(df["lat"].iloc[0])
    lon1 = math.radians(df["lon"].iloc[0])
    lat2 = math.radians(df["lat"].iloc[-1])
    lon2 = math.radians(df["lon"].iloc[-1])

    delta_lon = lon2 - lon1

    x = math.sin(delta_lon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(delta_lon)

    winkel = (math.degrees(math.atan2(x, y)) + 360) % 360

    richtungen = [
        "Nord", "Nordost", "Ost", "Südost",
        "Süd", "Südwest", "West", "Nordwest"
    ]

    index = round(winkel / 45) % 8
    return winkel, richtungen[index]



def parameterstudie_masse_reifen(gps_daten, hauptordner):
    fahrer_massen = [60, 70, 80, 90, 100]
    reifen_zoll = [26, 27, 27.5, 28, 29]

    ergebnisse_masse = []

    for masse in fahrer_massen:
        physik = EBikePhysics(gps_daten.copy(deep=True), m_fahrer=masse, m_fahrrad=10.0, raddurchmesser_zoll=27.0)
        daten = physik.calculate_physics()

        akku = LiPoAkku(capacity_nom_Ah=30.0, initial_soc=1.0)
        daten_akku = simuliere_akku_fahrt(daten, akku)

        strecke_motor = daten_akku[daten_akku["I_motor"] > 0]["delta_s"].sum() / 1000.0
        max_leistung = daten["P_mech"].max()

        ergebnisse_masse.append((masse, strecke_motor, max_leistung))

    ergebnisse_reifen = []

    for zoll in reifen_zoll:
        physik = EBikePhysics(gps_daten.copy(deep=True), m_fahrer=70.0, m_fahrrad=10.0, raddurchmesser_zoll=zoll)
        daten = physik.calculate_physics()

        akku = LiPoAkku(capacity_nom_Ah=30.0, initial_soc=1.0)
        daten_akku = simuliere_akku_fahrt(daten, akku)

        strecke_motor = daten_akku[daten_akku["I_motor"] > 0]["delta_s"].sum() / 1000.0

        ergebnisse_reifen.append((zoll, strecke_motor))

    output_ordner = os.path.join(hauptordner, "output")
    os.makedirs(output_ordner, exist_ok=True)

    txt_pfad = os.path.join(output_ordner, "parameterstudie.txt")

    with open(txt_pfad, "w", encoding="utf-8") as datei:
        datei.write("Parameterstudie\n")
        datei.write("================\n\n")

        datei.write("Einfluss der Fahrermasse:\n")
        for masse, strecke, leistung in ergebnisse_masse:
            datei.write(f"{masse} kg Fahrer: {strecke:.2f} km Motorunterstützung, max. Leistung {leistung:.1f} W\n")

        datei.write("\nEinfluss des Reifendurchmessers:\n")
        for zoll, strecke in ergebnisse_reifen:
            datei.write(f"{zoll} Zoll Reifen: {strecke:.2f} km Motorunterstützung\n")

    plt.figure(figsize=(8, 5))
    plt.plot(
        [x[0] for x in ergebnisse_masse],
        [x[1] for x in ergebnisse_masse],
        marker="o"
    )
    plt.title("Parameterstudie: Einfluss der Fahrermasse")
    plt.xlabel("Fahrermasse [kg]")
    plt.ylabel("Motorunterstützte Strecke [km]")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_ordner, "7_parameterstudie_masse.png"))
    plt.close()

    plt.figure(figsize=(8, 5))
    plt.plot(
        [x[0] for x in ergebnisse_reifen],
        [x[1] for x in ergebnisse_reifen],
        marker="o"
    )
    plt.title("Parameterstudie: Einfluss des Reifendurchmessers")
    plt.xlabel("Reifendurchmesser [Zoll]")
    plt.ylabel("Motorunterstützte Strecke [km]")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_ordner, "8_parameterstudie_reifen.png"))
    plt.close()


    print("Parameterstudie gespeichert.")


def main():
    # Eingabedatei wählen 
    dateipfad = os.path.join(hauptordner, "data", "final_project_input_data.csv")
    
    logging.info("Lade GPS-Daten")
    parser = GPSDataParser(dateipfad)
    gps_daten = parser.load_data()
    
    logging.info("Berechne physikalische Größen")
    physik = EBikePhysics(gps_daten)
    berechnete_daten = physik.calculate_physics()

    # steigung
    hoehen_diff = berechnete_daten['ele'].diff().fillna(0)
    berechnete_daten['steigung'] = (hoehen_diff / berechnete_daten['delta_s'].replace(0, 1)) * 100
    
    # drehmoment
    motorkonstante_nm_pro_a = 1.5 
    berechnete_daten['drehmoment'] = berechnete_daten['I_motor'] * motorkonstante_nm_pro_a

    # Erste werte anzeigen 
    print(f"Erste 10 Zeilen der berechneten Daten:")
    print(berechnete_daten[['time', 'v', 'a', 'F_ges', 'I_motor']].head(10))


    kapacitet_test = 40.0

    logging.info(f"Starte E-Bike-Batteriesimulation mit LiPo-Akku ({kapacitet_test}Ah, 100% Start-SoC)")
    lipo_batterie = LiPoAkku(capacity_nom_Ah=kapacitet_test, initial_soc=1.0)
    daten_lipo = simuliere_akku_fahrt(berechnete_daten, lipo_batterie)
    
    logging.info(f"Starte E-Bike-Batteriesimulation mit NMC-Akku ({kapacitet_test}Ah, 100% Start-SoC)")
    nmc_batterie = NMCAkku(capacity_nom_Ah=kapacitet_test, initial_soc=1.0)
    daten_nmc = simuliere_akku_fahrt(berechnete_daten, nmc_batterie)





# Bericht
    gesamt_strecke_km = berechnete_daten['delta_s'].sum() / 1000.0
    # Strecke, bei der der Motor Strom gezogen hat (I_motor > 0)
    strecke_motor_lipo = daten_lipo[daten_lipo['I_motor'] > 0]['delta_s'].sum() / 1000.0
    strecke_motor_nmc = daten_nmc[daten_nmc['I_motor'] > 0]['delta_s'].sum() / 1000.0
    durchschnitt_v = berechnete_daten["v"].mean() * 3.6
    fahrzeit = berechnete_daten["delta_t"].sum() / 60
    max_leistung = berechnete_daten["P_mech"].max()
    höhen_diff = berechnete_daten["ele"].diff()
    anstieg = höhen_diff[höhen_diff > 0].sum()
    abstieg = -höhen_diff[höhen_diff < 0].sum()
    max_steigung = berechnete_daten["steigung"].max()
    max_drehmoment = berechnete_daten["drehmoment"].max()
    winkel, richtung = berechne_himmelsrichtung(berechnete_daten)

    
    
    
    
    print("\n----- Bericht -----")
    print(f"Gesamt gefahrene Strecke: {gesamt_strecke_km:.2f} km")
    print(f"Strecke mit Motorunterstützung (LiPo): {strecke_motor_lipo:.2f} km")
    print(f"Strecke mit Motorunterstützung (NMC): {strecke_motor_nmc:.2f} km")
    print(f"Durchschnittsgeschwindigkeit: {durchschnitt_v:.2f} km/h")
    print(f"Fahrzeit: {fahrzeit:.1f} min")
    print(f"Maximale Leistung: {max_leistung:.1f} W")
    print(f"Maximale Steigung: {max_steigung:.1f} %")
    print(f"Maximales Drehmoment: {max_drehmoment:.1f} Nm")
    print(f"Gesamter Anstieg: {anstieg:.1f} m")
    print(f"Gesamter Abstieg: {abstieg:.1f} m")
    print(f"Hauptrichtung der Fahrt: {richtung} ({winkel:.1f}°)")
    print()
    print(f"Verwendete Batterie: LiPo ({lipo_batterie.C_nom / 3600.0:.1f} Ah)")
    print(f"Verwendete Batterie: NMC ({nmc_batterie.C_nom / 3600.0:.1f} Ah)")
    print(f"Restlicher Ladezustand: LiPo {lipo_batterie.soc * 100:.1f} %")
    print(f"Restlicher Ladezustand: NMC {nmc_batterie.soc * 100:.1f} %")
    print(f"Restspannung: LiPo {daten_lipo['akku_spannung'].iloc[-1]:.2f} V")
    print(f"Restspannung: NMC {daten_nmc['akku_spannung'].iloc[-1]:.2f} V")

    logging.info(f"Generiere Simulationsgrafiken")
    plot_simulations_ergebnisse(berechnete_daten, daten_lipo, daten_nmc, hauptordner)

    create_route_map(berechnete_daten)

    parameterstudie_masse_reifen(gps_daten, hauptordner)

if __name__ == "__main__":
    main()
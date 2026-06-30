import matplotlib.pyplot as plt


def plot_ergebnisse(daten):
    """
    Zeigt alle wichtigen Diagramme der E-Bike-Simulation an.
    """

    # Geschwindigkeit
    plt.figure(figsize=(10, 4))
    plt.plot(daten["time"], daten["v"])
    plt.title("Geschwindigkeit über die Zeit")
    plt.xlabel("Zeit")
    plt.ylabel("Geschwindigkeit [m/s]")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Mechanische Leistung
    plt.figure(figsize=(10, 4))
    plt.plot(daten["time"], daten["P_mech"])
    plt.title("Mechanische Leistung über die Zeit")
    plt.xlabel("Zeit")
    plt.ylabel("Leistung [W]")
    plt.grid(True)
    plt.tight_layout()
    plt.show()



    # Motorstrom
    plt.figure(figsize=(10, 4))
    plt.plot(daten["time"], daten["I_motor"])
    plt.title("Motorstrom über die Zeit")
    plt.xlabel("Zeit")
    plt.ylabel("Motorstrom [A]")
    plt.grid(True)
    plt.tight_layout()
    plt.show()



    # Ladezustand
    plt.figure(figsize=(10, 4))
    plt.plot(daten["time"], daten["akku_soc"] * 100)
    plt.title("Ladezustand des Akkus")
    plt.xlabel("Zeit")
    plt.ylabel("SoC [%]")
    plt.grid(True)
    plt.tight_layout()
    plt.show()



    # Akkuspannung
    plt.figure(figsize=(10, 4))
    plt.plot(daten["time"], daten["akku_spannung"])
    plt.title("Akkuspannung über die Zeit")
    plt.xlabel("Zeit")
    plt.ylabel("Spannung [V]")
    plt.grid(True)
    plt.tight_layout()
    plt.show()



    # Höhenprofil
    plt.figure(figsize=(10, 4))
    plt.plot(daten["time"], daten["ele"])
    plt.title("Höhenprofil")
    plt.xlabel("Zeit")
    plt.ylabel("Höhe [m]")
    plt.grid(True)
    plt.tight_layout()


    plt.show()
import numpy as np
from battery_pack import BatteryPack

class LiPoAkku(BatteryPack):
    def __init__(self, capacity_nom_Ah: float, initial_soc: float = 1.0):
        # Innenwiderstand (10 zellen)
        super().__init__(
            capacity_nom_Ah=capacity_nom_Ah,
            internal_resistance_mOhm=80.0,
            initial_soc=initial_soc,
            Vmin=32.0,
            Vmax=42.0
        )
        
        # SoC und OCV werte (Aufgabstelung)
        self.soc_values = [0.00, 0.04, 0.09, 0.13, 0.17, 0.21, 0.26, 0.30, 0.40, 0.52, 0.64, 0.76, 0.88, 1.00]
        self.ocv_values = [32.00, 35.87, 36.85, 37.56, 37.87, 38.28, 38.81, 39.05, 39.55, 40.27, 40.70, 41.16, 41.65, 42.00]

    def voltage(self, current: float = 0.0) -> float:
        """Berechnet die Spannung basierend auf der Lookup-Tabelle und dem Entladestrom."""
        # Leerlaufspannung aus dem SoC berechnen
        open_circuit_voltage = np.interp(self.soc, self.soc_values, self.ocv_values)
        
        # Klemmenspannung berechnen
        return open_circuit_voltage - (self.R_int * current)


class NMCAkku(BatteryPack):
    def __init__(self, capacity_nom_Ah: float, initial_soc: float = 1.0):
        # 10 zellen serie: R_int = 10 * 7 mOhm = 70 mOhm
        super().__init__(
            capacity_nom_Ah=capacity_nom_Ah,
            internal_resistance_mOhm=70.0,
            initial_soc=initial_soc,
            Vmin=32.0,
            Vmax=42.0
        )
        
        # SoC und OCV werte für NMC 
        self.soc_values = [0.00, 0.04, 0.09, 0.13, 0.17, 0.21, 0.26, 0.30, 0.40, 0.52, 0.64, 0.76, 0.88, 1.00]
        self.ocv_values = [32.00, 32.61, 33.17, 33.85, 34.24, 34.66, 35.39, 35.65, 36.65, 37.64, 38.91, 40.14, 41.08, 42.00]

    def voltage(self, current: float = 0.0) -> float:
        """Berechnet die Spannung basierend auf der Lookup-Tabelle und dem Entladestrom."""
        # Leerlaufspanung berechnen 
        open_circuit_voltage = np.interp(self.soc, self.soc_values, self.ocv_values)
        
        # Spannung unter Last berechnen
        return open_circuit_voltage - (self.R_int * current)